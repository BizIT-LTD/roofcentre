"""Zip the CONTENTS of website/ for upload to Hostinger's public_html.

    python tools/package.py   ->  dist/roofcentre-website.zip

The zip has no top-level folder, so extracting it inside public_html puts
index.html directly in public_html. Hidden files such as .htaccess are included.
"""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "website"
DEST = ROOT / "dist" / "roofcentre-website.zip"
BLOCKED = {".sql", ".gz", ".zip", ".tar", ".env", ".log"}
BLOCKED_NAMES = {"roofcentre-enquiry-config.php", "wp-config.php"}


def main():
    DEST.parent.mkdir(exist_ok=True)
    files = sorted(p for p in SRC.rglob("*") if p.is_file())
    bad = [p for p in files if p.suffix.lower() in BLOCKED or p.name in BLOCKED_NAMES]
    if bad:
        raise SystemExit("Refusing to package private or backup files:\n" + "\n".join(str(b) for b in bad))
    for required in (".htaccess", "index.html", "404.html", "sitemap.xml", "robots.txt", "api/enquiry.php"):
        if not (SRC / required).is_file():
            raise SystemExit(f"Missing {required}; run python tools/build.py first.")
    with zipfile.ZipFile(DEST, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(p, p.relative_to(SRC).as_posix())
    print(f"{DEST.relative_to(ROOT)}: {len(files)} files, {DEST.stat().st_size / 1e6:.1f} MB (includes .htaccess)")


if __name__ == "__main__":
    main()
