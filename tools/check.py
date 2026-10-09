"""Audit the built site: internal links, images, SEO tags and sitemap.

    python tools/serve.py   (in another terminal)
    python tools/check.py
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import re
import sys

ROOT = Path(__file__).resolve().parent.parent / "website"
BASE = "http://127.0.0.1:8080"
SITE = "https://www.roofcentre.com.au"


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.srcs, self.imgs_no_alt, self.h1, self.ids = [], [], 0, 0, set()
        self.title, self.desc, self.canon, self.noindex, self._t = "", None, None, False, False

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img":
            if a.get("src"):
                self.srcs.append(a["src"])
            for part in (a.get("srcset") or "").split(","):
                if part.strip():
                    self.srcs.append(part.strip().split()[0])
            if a.get("alt") is None or (a.get("alt") == "" and "data-lightbox-img" not in a):
                self.imgs_no_alt += 1
        if tag == "link" and a.get("rel") in ("stylesheet", "icon", "apple-touch-icon", "manifest") and a.get("href", "").startswith("/"):
            self.srcs.append(a["href"])
        if tag == "script" and a.get("src", "").startswith("/"):
            self.srcs.append(a["src"])
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self._t = True
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content")
        if tag == "meta" and a.get("name") == "robots" and "noindex" in a.get("content", ""):
            self.noindex = True
        if tag == "link" and a.get("rel") == "canonical":
            self.canon = a.get("href")

    def handle_endtag(self, tag):
        if tag == "title":
            self._t = False

    def handle_data(self, d):
        if self._t:
            self.title += d


def status(url):
    try:
        with urlopen(Request(url, method="HEAD")) as r:
            return r.status
    except HTTPError as e:
        return e.code


def main():
    problems, checked, titles = [], {}, {}
    pages = sorted(ROOT.rglob("*.html"))
    parsed = {}
    for f in pages:
        rel = "/" + f.relative_to(ROOT).as_posix()
        url_path = rel[:-len("index.html")] if rel.endswith("index.html") else rel
        p = P()
        p.feed(f.read_text(encoding="utf-8"))
        parsed[url_path] = p
    for url_path, p in parsed.items():
        indexable = not p.noindex
        if p.h1 != 1:
            problems.append(f"{url_path}: {p.h1} h1 elements")
        if p.imgs_no_alt:
            problems.append(f"{url_path}: {p.imgs_no_alt} images without alt")
        if indexable:
            if not (10 <= len(p.title) <= 65):
                problems.append(f"{url_path}: title length {len(p.title)}: {p.title}")
            if not p.desc or not (70 <= len(p.desc) <= 165):
                problems.append(f"{url_path}: description length {len(p.desc or '')}")
            if p.canon != SITE + url_path:
                problems.append(f"{url_path}: canonical {p.canon}")
            if p.title in titles:
                problems.append(f"{url_path}: duplicate title with {titles[p.title]}")
            titles[p.title] = url_path
        for href in p.links + p.srcs:
            if href.startswith(("tel:", "mailto:", "http://", "https://")):
                if href.startswith("tel:") and not re.fullmatch(r"tel:(\+61\d{9}|\d{6})", href):
                    problems.append(f"{url_path}: odd tel link {href}")
                continue
            full = urljoin(BASE + url_path, href)
            parts = urlsplit(full)
            target = parts.path
            if parts.fragment and target == url_path and parts.fragment not in p.ids:
                problems.append(f"{url_path}: missing anchor #{parts.fragment}")
            if parts.fragment and target != url_path and target in parsed and parts.fragment not in parsed[target].ids:
                problems.append(f"{url_path}: {href} anchor not found on target")
            if target not in checked:
                checked[target] = status(BASE + target)
            if checked[target] != 200:
                problems.append(f"{url_path}: {href} -> {checked[target]}")

    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    locs = re.findall(r"<loc>(.*?)</loc>", sm)
    for loc in locs:
        path = loc.replace(SITE, "")
        if path not in parsed:
            problems.append(f"sitemap: {loc} has no page")
    indexable = [u for u, p in parsed.items() if not p.noindex]
    for u in indexable:
        if SITE + u not in locs:
            problems.append(f"sitemap: missing {u}")

    # Original WordPress URLs that must still resolve
    original = ["/", "/about/", "/contact/", "/projects/", "/faq/", "/roof-repair/", "/roof-restoration/", "/roof-replacment/",
                "/colorbond-roofing/", "/gutter-8-downpipe-replacement/", "/gutter-protection/", "/emergency-roof-make-safe/",
                "/custom-valley-flashings/", "/roof-repair-botany/", "/roof-repair-near-me/", "/roof-repair-chipping-norton/"]
    for u in original:
        s = status(BASE + u)
        if s != 200:
            problems.append(f"original URL {u} -> {s}")

    print(f"Pages: {len(parsed)}  indexable: {len(indexable)}  unique URLs checked: {len(checked)}  sitemap URLs: {len(locs)}")
    print("\n".join(problems) if problems else "No problems found.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
