"""Local preview server for the Roof Centre static site.

    python tools/serve.py            # http://localhost:8080
    python tools/serve.py 9000       # custom port

Serves website/ like the live host: folder URLs, the custom 404 page and a
mock of /api/enquiry.php (PHP is not needed locally). Mock enquiries are
validated and printed to the console. Nothing is emailed.
"""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
import json
import sys

ROOT = Path(__file__).resolve().parent.parent / "website"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def send_error(self, code, message=None, explain=None):
        if code == 404 and (ROOT / "404.html").exists():
            body = (ROOT / "404.html").read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
            return
        super().send_error(code, message, explain)

    def do_GET(self):
        if urlsplit(self.path).path.startswith("/api/"):
            return self.send_error(404)
        return super().do_GET()

    def do_POST(self):
        if urlsplit(self.path).path != "/api/enquiry.php":
            return self.send_error(404)
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        ctype = self.headers.get("Content-Type", "")
        fields = {}
        if ctype.startswith("multipart/form-data"):
            from email.parser import BytesParser
            from email.policy import default
            msg = BytesParser(policy=default).parsebytes(b"Content-Type: " + ctype.encode() + b"\r\n\r\n" + raw)
            for part in msg.iter_parts():
                fields[part.get_param("name", header="content-disposition")] = part.get_content().strip()
        else:
            fields = {k: v[0].strip() for k, v in parse_qs(raw.decode()).items()}
        missing = [f for f in ("name", "phone", "email", "message") if not fields.get(f)]
        ok = not missing
        print("\n--- MOCK ENQUIRY (not emailed) ---")
        for k, v in fields.items():
            if k not in ("website", "started"):
                print(f"{k:>8}: {v}")
        print("result:", "ok" if ok else f"missing {missing}")
        payload = json.dumps({"ok": True} if ok else {"ok": False, "error": "Please check your " + ", ".join(missing) + "."}).encode()
        if "application/json" in self.headers.get("Accept", ""):
            self.send_response(200 if ok else 422)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        else:
            self.send_response(303)
            self.send_header("Location", "/thank-you/" if ok else "/contact/")
            self.end_headers()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print(f"Roof Centre preview: http://localhost:{port}/  (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
