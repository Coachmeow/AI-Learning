#!/usr/bin/env python3
"""Check that every site-internal link and image in the built site (dist/) points to a real file.

Usage: python3 scripts/check-links.py [dist-dir] [base]
"""
import html.parser
import pathlib
import sys
import urllib.parse

dist = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
base = sys.argv[2] if len(sys.argv) > 2 else "/"


class Refs(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value and ((tag == "a" and name == "href") or (tag in ("img", "script", "source") and name == "src") or (tag == "link" and name == "href")):
                self.refs.append(value)


def exists(url):
    path = urllib.parse.unquote(urllib.parse.urlsplit(url).path)
    if not path.startswith(base):
        return True
    rel = path[len(base):]
    target = dist / rel
    return target.is_file() or (target / "index.html").is_file()


broken = {}
pages = sorted(dist.rglob("*.html"))
for page in pages:
    parser = Refs()
    parser.feed(page.read_text(encoding="utf-8", errors="replace"))
    for ref in parser.refs:
        if ref.startswith(("http:", "https:", "mailto:", "#", "data:", "javascript:")):
            continue
        url = ref if ref.startswith("/") else urllib.parse.urljoin("/" + str(page.relative_to(dist).as_posix()), ref)
        if not exists(url):
            broken.setdefault(url, set()).add(str(page.relative_to(dist)))

for url, where in sorted(broken.items()):
    print(f"BROKEN {url}  (in {len(where)} page(s), e.g. {sorted(where)[0]})")
print(f"{len(pages)} pages checked, {len(broken)} broken target(s)")
sys.exit(1 if broken else 0)
