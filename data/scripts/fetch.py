#!/usr/bin/env python3
"""Fetch raw HTML of www.darbtech.net in French and English.

Usage (run from this scripts/ folder):
    python -I fetch.py            # fetch every page (sitemap + nav), both languages
    python -I fetch.py --no-blog-posts   # skip individual blog articles

Output: ../raw/<lang>/<slug>.html, ../raw/sitemap.xml, ../raw/pages.json
Odoo serves French (default language) without prefix and English under /en/.
The French version is forced with the cookie frontend_lang=fr_FR, because the
server otherwise redirects to /en/ depending on Accept-Language / cookies.
Standard library only.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar

BASE = "https://www.darbtech.net"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.normpath(os.path.join(HERE, "..", "raw"))
UA = "Mozilla/5.0 (DarbTech redesign content audit)"
LANGS = {"fr": ("fr_FR", "fr-FR,fr;q=0.9", ""), "en": ("en_US", "en-US,en;q=0.9", "/en")}

# Pages we never need (feeds, apply forms are fetched once, cart etc.)
SKIP = re.compile(r"/feed$|/shop/cart|/website/info$")


def opener(lang):
    code, accept, _ = LANGS[lang]
    jar = CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    op.addheaders = [("User-Agent", UA), ("Accept-Language", accept),
                     ("Cookie", "frontend_lang=" + code)]
    return op


def get(op, url, tries=3):
    for i in range(tries):
        try:
            url = urllib.parse.quote(url, safe=":/?=&%#")
            with op.open(url, timeout=40) as r:
                return r.status, r.geturl(), r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return e.code, url, e.read().decode("utf-8", "replace")
        except Exception as e:  # network hiccup
            if i == tries - 1:
                return 0, url, str(e)
            time.sleep(2)


def slug_of(path):
    path = path.strip("/")
    return re.sub(r"[^A-Za-z0-9._-]+", "_", path) or "home"


def discover(op):
    status, _, xml = get(op, BASE + "/sitemap.xml")
    os.makedirs(RAW, exist_ok=True)
    with open(os.path.join(RAW, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    paths = []
    for loc in re.findall(r"<loc>([^<]+)</loc>", xml):
        p = loc.replace(BASE, "") or "/"
        if not SKIP.search(p):
            paths.append(p)
    # Add nav/footer links found on the homepage that are not in the sitemap
    _, _, home = get(op, BASE + "/")
    for href in re.findall(r'href="(/[^"#?]*)"', home):
        if href.startswith(("/web/", "/en/web", "/website/")) or SKIP.search(href):
            continue
        if href.startswith("/en/") or href == "/en":
            href = href[3:] or "/"
        if href not in paths:
            paths.append(href)
    return paths


def main():
    no_posts = "--no-blog-posts" in sys.argv
    paths = discover(opener("fr"))
    if no_posts:
        paths = [p for p in paths if not re.match(r"/blog/[^/]+/[^/]+", p)]
    index = []
    for lang, (_, _, prefix) in LANGS.items():
        op = opener(lang)
        outdir = os.path.join(RAW, lang)
        os.makedirs(outdir, exist_ok=True)
        for p in paths:
            url = BASE + (prefix + p if p != "/" else (prefix or "/"))
            status, final, html = get(op, url)
            slug = slug_of(p)
            with open(os.path.join(outdir, slug + ".html"), "w", encoding="utf-8") as f:
                f.write(html)
            m = re.search(r'<html[^>]*lang="([^"]+)"', html)
            index.append({"lang": lang, "path": p, "url": url, "final_url": final,
                          "status": status, "html_lang": m.group(1) if m else None,
                          "file": f"raw/{lang}/{slug}.html"})
            print(lang, status, url, "->", final)
            time.sleep(0.3)
    with open(os.path.join(RAW, "pages.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
