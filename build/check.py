"""Validate the generated site: internal links/assets resolve, one H1 per page, unique titles and
descriptions, alt on every <img>, hreflang/canonical present, and CSS+JS weight. Standard library only.

    python build/check.py
"""
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.h1, self.imgs_no_alt, self.title, self.desc = [], set(), 0, [], None, None
        self.hreflang, self.canonical, self._in_title, self._in_tpl = 0, False, False, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "template":
            self._in_tpl += 1
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "h1" and not self._in_tpl:
            self.h1 += 1
        if tag == "img" and "alt" not in a:
            self.imgs_no_alt.append(a.get("src"))
        if tag == "title":
            self._in_title = True
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content")
        if tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"):
            self.hreflang += 1
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = True
        for k in ("href", "src"):
            if k in a and a[k]:
                if tag == "link" and a.get("rel") in ("canonical", "alternate", "preconnect"):
                    continue
                self.links.append(a[k])

    def handle_endtag(self, tag):
        if tag == "template":
            self._in_tpl -= 1
        if tag == "title":
            self._in_title = False

    def handle_data(self, d):
        if self._in_title:
            self.title = (self.title or "") + d


def main():
    errors, titles, descs, external = [], {}, {}, set()
    pages = []
    for dp, _, fs in os.walk(ROOT):
        for f in fs:
            if f.endswith(".html"):
                pages.append(os.path.join(dp, f))
    parsed = {}
    for path in pages:
        p = P()
        with open(path, encoding="utf-8") as fh:
            p.feed(fh.read())
        parsed[path] = p
    for path, p in parsed.items():
        rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        if p.h1 != 1:
            errors.append(f"{rel}: {p.h1} <h1>")
        if p.imgs_no_alt:
            errors.append(f"{rel}: img without alt {p.imgs_no_alt}")
        if p.hreflang != 3 or not p.canonical:
            errors.append(f"{rel}: hreflang/canonical missing")
        titles.setdefault(p.title, []).append(rel)
        descs.setdefault(p.desc, []).append(rel)
        for link in p.links:
            u = urlparse(link)
            if u.scheme in ("http", "https"):
                external.add(link)
                continue
            if u.scheme in ("mailto", "tel", "data") or link.startswith("javascript"):
                continue
            target = path if not u.path else os.path.normpath(os.path.join(os.path.dirname(path), unquote(u.path)))
            if not os.path.isfile(target):
                errors.append(f"{rel}: broken link {link}")
                continue
            if u.fragment and target.endswith(".html"):
                tp = parsed.get(target)
                if tp and u.fragment not in tp.ids:
                    errors.append(f"{rel}: missing anchor {link}")
    for t, l in titles.items():
        if len(l) > 1:
            errors.append(f"duplicate title {t!r}: {l}")
    for d, l in descs.items():
        if len(l) > 1:
            errors.append(f"duplicate description: {l}")
    size = sum(os.path.getsize(os.path.join(dp, f)) for sub in ("css", "js")
               for dp, _, fs in os.walk(os.path.join(ROOT, "assets", sub)) for f in fs)
    print(f"{len(pages)} pages checked, {len(external)} distinct external URLs, CSS+JS = {size / 1024:.1f} KB")
    for e in errors:
        print("ERROR", e)
    if "--external" in sys.argv:
        for e in sorted(external):
            print("EXT", e)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
