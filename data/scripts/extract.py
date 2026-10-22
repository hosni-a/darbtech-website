#!/usr/bin/env python3
"""Turn the raw HTML saved by fetch.py into a renderable data layer.

Usage (run from this scripts/ folder, after fetch.py):
    python -I extract.py              # extract + download assets (cached)
    python -I extract.py --no-assets  # extract only, no network

Writes (all in ../):
    content.fr.json, content.en.json   site, pages -> sections -> blocks, inventory
    blog.fr.json, blog.en.json         every blog article with full body blocks
    assets.json                        asset manifest
    assets/<category>/<file>           downloaded images
Standard library only. The raw HTML is parsed as data, never executed.
"""
import base64
import datetime
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from html.parser import HTMLParser

sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://www.darbtech.net"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, ".."))
RAW = os.path.join(DATA, "raw")
ASSETS = os.path.join(DATA, "assets")
MAX_ASSET_BYTES = 2_500_000

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}
BLOCK = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "blockquote", "td", "th", "dt", "dd",
         "figcaption", "label", "option", "div", "section", "ul", "ol", "table", "tr", "form",
         "header", "footer", "nav", "main", "article", "aside", "address", "pre", "button",
         "select", "textarea", "figure", "small"}
HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}


# ----------------------------------------------------------------- mini DOM
class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs=None, parent=None):
        self.tag, self.attrs, self.children, self.parent = tag, dict(attrs or {}), [], parent

    def cls(self):
        return (self.attrs.get("class") or "").split()

    def iter(self):
        yield self
        for c in self.children:
            if isinstance(c, Node):
                yield from c.iter()

    def find_all(self, pred):
        return [n for n in self.iter() if pred(n)]

    def find(self, pred):
        for n in self.iter():
            if pred(n):
                return n
        return None

    def text(self):
        out = []
        for c in self.children:
            if isinstance(c, str):
                out.append(c)
            elif c.tag not in ("script", "style"):
                if c.tag == "br":
                    out.append("\n")
                out.append(c.text())
        return "".join(out)

    def ancestors(self):
        p = self.parent
        while p is not None:
            yield p
            p = p.parent


class Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root")
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def parse(path):
    b = Builder()
    with open(path, encoding="utf-8") as f:
        b.feed(f.read())
    return b.root


# ----------------------------------------------------------------- helpers
def clean(s):
    if s is None:
        return ""
    s = s.replace("​", "").replace("﻿", "").replace("\xa0", " ")
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\s*\n\s*", "\n", s)
    return s.strip()


def one_line(s):
    return re.sub(r"\s+", " ", clean(s)).strip()


def absurl(u):
    if not u:
        return u
    if u.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
        return u
    return urllib.parse.urljoin(BASE + "/", u)


def site_path(href, lang):
    """Normalise an internal href to a language-neutral path ('/aboutus')."""
    if not href or href.startswith(("mailto:", "tel:", "#", "javascript:")):
        return None
    u = urllib.parse.urlparse(absurl(href))
    if u.netloc and u.netloc not in ("www.darbtech.net", "darbtech.net"):
        return None
    p = urllib.parse.unquote(u.path) or "/"
    if p == "/en" or p.startswith("/en/"):
        p = p[3:] or "/"
    return p


FR_WORDS = set("le la les des du de et est une un pour vous nous avec dans sur au aux votre vos notre "
               "nos qui que ce cette ces ses son sa par plus être sont pas ou chez leur leurs "
               "afin ainsi entre très tout tous toutes aussi mais dont où lors sans selon".split())
EN_WORDS = set("the and of to in is for with your our we you by are that this it as be from or an "
               "will can which their they has have at into more all its these those about".split())
FR_CHARS = set("éèêàâçùûôîœ")


def detect_lang(text):
    words = re.findall(r"[a-zàâçéèêëîïôûùüÿœ']+", text.lower())
    words = [w.split("'")[-1] for w in words]
    fr = sum(w in FR_WORDS for w in words)
    en = sum(w in EN_WORDS for w in words)
    fr += 0.5 * sum(1 for w in words if FR_CHARS & set(w))
    if fr >= 1 and fr > en * 1.2:
        return "fr"
    if en >= 1 and en > fr * 1.2:
        return "en"
    return None


# ----------------------------------------------------------------- block extraction
def is_hidden_or_noise(n):
    c = n.cls()
    return (n.tag in ("script", "style", "noscript", "template", "svg")
            or "d-none" in c and "d-lg-block" not in c and "d-md-block" not in c
            or "o_not_editable" in c and n.tag == "div" and n.find(lambda x: x.tag == "i") is not None and not clean(n.text())
            or "css_editable_mode_display" in c)


def bg_image(n):
    st = n.attrs.get("style") or ""
    m = re.search(r"background-image:\s*url\(['\"]?([^'\")]+)", st)
    return m.group(1) if m else None


class Walker:
    """Flatten a subtree into an ordered list of renderable blocks."""

    def __init__(self, lang, images):
        self.lang, self.images = lang, images
        self.blocks = []

    def img(self, src, alt, ctx, kind="image"):
        if not src:
            return
        url = absurl(src)
        b = {"type": kind, "src": url, "alt": clean(alt) or ""}
        why = next((r for rx, r in SKIP_ASSET if r and re.search(rx, url)), None)
        if why:
            b["decorative_or_placeholder"] = why
        self.blocks.append(b)
        self.images.append({"url": url, "alt": b["alt"], "block": b, **ctx})

    def walk(self, n, ctx):
        if isinstance(n, str) or is_hidden_or_noise(n):
            return
        bg = bg_image(n)
        if bg:
            self.img(bg, "", ctx, "background_image")
        t = n.tag
        if t == "img":
            self.img(n.attrs.get("src"), n.attrs.get("alt"), ctx)
            return
        if t in ("input", "textarea", "select"):
            return  # forms handled separately
        if t in ("ul", "ol"):
            items = []
            for li in [c for c in n.children if isinstance(c, Node) and c.tag == "li"]:
                txt = clean(self.own_text(li))
                links = self.links_in(li)
                sub = [x for x in li.iter() if x is not li and x.tag in ("ul", "ol")]
                if txt or links:
                    it = {"text": txt}
                    if links:
                        it["links"] = links
                    items.append(it)
                for x in li.iter():
                    if x.tag == "img":
                        self.img(x.attrs.get("src"), x.attrs.get("alt"), ctx)
                for s in sub:
                    if s.parent is li or s.parent.parent is li:
                        pass
            if items:
                self.blocks.append({"type": "list", "ordered": t == "ol", "items": items})
            return
        if t in HEADINGS or t in ("p", "blockquote", "pre", "address", "figcaption") or self.is_text_leaf(n):
            txt = clean(self.own_text(n))
            links = self.links_in(n)
            for x in n.iter():
                if x is not n and x.tag == "img":
                    self.img(x.attrs.get("src"), x.attrs.get("alt"), ctx)
            if txt:
                b = {"type": "heading", "level": int(t[1])} if t in HEADINGS else {"type": "text"}
                b["text"] = txt
                if links:
                    # a paragraph that is only a link is a CTA/link block
                    if len(links) == 1 and one_line(links[0]["text"]) == one_line(txt):
                        b = {"type": "link", **links[0]}
                        if t in HEADINGS:
                            b["heading_level"] = int(t[1])
                    else:
                        b["links"] = links
                self.blocks.append(b)
            else:
                for l in links:
                    if l.get("href") and l["href"] not in ("#",):
                        self.blocks.append({"type": "link", **l})
            return
        if t == "a" and not self.has_block_child(n):
            l = self.link(n)
            for x in n.iter():
                if x.tag == "img":
                    self.img(x.attrs.get("src"), x.attrs.get("alt"), {**ctx, "link": l.get("href")})
            if l["text"]:
                self.blocks.append({"type": "link", **l})
            elif l.get("href") and l["href"] != "#" and not n.find(lambda x: x.tag == "img"):
                self.blocks.append({"type": "link", **l})
            return
        for c in n.children:
            if isinstance(c, str):
                txt = clean(c)
                if txt and n.tag not in ("ul", "ol", "table", "tr", "select"):
                    self.blocks.append({"type": "text", "text": txt})
            else:
                self.walk(c, ctx)

    def has_block_child(self, n):
        return any(isinstance(c, Node) and c.tag in BLOCK | HEADINGS for c in n.iter() if c is not n)

    def is_text_leaf(self, n):
        """A div/span-like container whose content is only inline."""
        if n.tag not in ("div", "span", "font", "strong", "b", "em", "i", "u", "small", "td", "th",
                         "dt", "dd", "label", "button"):
            return False
        if self.has_block_child(n):
            return False
        return bool(clean(n.text()))

    def own_text(self, n):
        out = []
        for c in n.children:
            if isinstance(c, str):
                out.append(c)
            elif c.tag == "br":
                out.append("\n")
            elif c.tag in ("ul", "ol", "script", "style") or is_hidden_or_noise(c):
                continue
            else:
                out.append(self.own_text(c))
        return "".join(out)

    def link(self, a):
        href = a.attrs.get("href")
        c = a.cls()
        d = {"text": one_line(self.own_text(a)), "href": absurl(href) if href else None}
        if href and site_path(href, self.lang) is not None and not href.startswith("#"):
            d["path"] = site_path(href, self.lang)
        if any(x.startswith("btn") for x in c):
            d["button"] = True
        if a.attrs.get("target") == "_blank":
            d["new_tab"] = True
        if not d["text"]:
            d["text"] = clean(a.attrs.get("aria-label") or a.attrs.get("title") or "")
        return d

    def links_in(self, n):
        return [self.link(a) for a in n.iter() if a.tag == "a" and a is not n
                and (a.attrs.get("href") or clean(a.text()))]


def form_fields(form, lang):
    fields = []
    labels = {}
    for lab in form.iter():
        if lab.tag == "label" and lab.attrs.get("for"):
            labels[lab.attrs["for"]] = one_line(lab.text())
    for n in form.iter():
        if n.tag not in ("input", "textarea", "select"):
            continue
        typ = n.attrs.get("type", n.tag) if n.tag == "input" else n.tag
        if typ in ("hidden", "submit"):
            continue
        name = n.attrs.get("name")
        f = {"name": name, "type": typ}
        lab = labels.get(n.attrs.get("id"))
        if not lab:  # Odoo puts the label in the enclosing .s_website_form_field
            fld = next((a for a in n.ancestors() if "s_website_form_field" in a.cls()), None)
            if fld is not None:
                l = fld.find(lambda x: x.tag == "label" or "s_website_form_label" in x.cls())
                lab = one_line(l.text()) if l is not None else None
        if typ in ("radio", "checkbox"):
            opt = next((a for a in n.ancestors() if a.tag in ("div", "label")), None)
            optlab = labels.get(n.attrs.get("id"))
            existing = next((x for x in fields if x["name"] == name and x["type"] == typ), None)
            val = optlab or n.attrs.get("value")
            if existing:
                existing["options"].append(val)
                continue
            fld = next((a for a in n.ancestors() if "s_website_form_field" in a.cls()), None)
            l = fld.find(lambda x: "s_website_form_label" in x.cls()) if fld is not None else None
            f["label"] = one_line(l.text()) if l is not None else None
            f["options"] = [val]
        else:
            f["label"] = lab
        if n.tag == "select":
            f["options"] = [one_line(o.text()) for o in n.iter() if o.tag == "option" and one_line(o.text())]
        if n.attrs.get("placeholder"):
            f["placeholder"] = clean(n.attrs["placeholder"])
        if "required" in n.attrs:
            f["required"] = True
        else:
            fld = next((a for a in n.ancestors() if "s_website_form_field" in a.cls()), None)
            if fld is not None and ("s_website_form_required" in fld.cls() or "s_website_form_model_required" in fld.cls()):
                f["required"] = True
        if f.get("label"):
            f["label"] = f["label"].rstrip(" *").strip()
        fields.append(f)
    submit = form.find(lambda x: ("s_website_form_send" in x.cls() or x.attrs.get("type") == "submit"))
    action = form.attrs.get("action")
    return {"action": action, "model": form.attrs.get("data-model_name"), "fields": fields,
            "submit_label": one_line(submit.text()) if submit is not None else None}


def mark_missing(blocks, lang, stats):
    """Flag blocks whose text is in the other language (untranslated in Odoo)."""
    other = "en" if lang == "fr" else "fr"

    def chk(d):
        if not d.get("text") or len(d["text"]) < 4:
            return
        dl = detect_lang(d["text"])
        if dl == other:
            d["_missing"] = True
            d["_text_lang"] = other
            stats["missing"] += 1
        stats["total"] += 1

    for b in blocks:
        if b["type"] == "list":
            for it in b["items"]:
                chk(it)
        else:
            chk(b)


# ----------------------------------------------------------------- page extraction
def head_meta(root):
    def meta(attr, val):
        m = root.find(lambda n: n.tag == "meta" and n.attrs.get(attr) == val)
        return clean(m.attrs.get("content")) if m is not None else None

    t = root.find(lambda n: n.tag == "title")
    alts = {n.attrs.get("hreflang"): n.attrs.get("href") for n in root.iter()
            if n.tag == "link" and n.attrs.get("rel") == "alternate" and n.attrs.get("hreflang")}
    canon = root.find(lambda n: n.tag == "link" and n.attrs.get("rel") == "canonical")
    return {"title": clean(t.text()) if t is not None else None,
            "meta_description": meta("name", "description"),
            "meta_keywords": meta("name", "keywords"),
            "og_title": meta("property", "og:title"),
            "og_image": meta("property", "og:image"),
            "canonical": canon.attrs.get("href") if canon is not None else None,
            "alternates": alts or None,
            "published_time": meta("property", "article:published_time"),
            "modified_time": meta("property", "article:modified_time")}


def sections_of(container, lang, images, page_key):
    """Split a container into top-level <section>s; loose content becomes its own section."""
    sections = []
    loose = []

    def flush_loose():
        if loose:
            w = Walker(lang, images)
            ctx = {"page": page_key, "section": f"loose-{len(sections)}"}
            for n in loose:
                w.walk(n, ctx)
            if w.blocks:
                sections.append({"id": f"s{len(sections) + 1}", "snippet": None, "name": None,
                                 "blocks": w.blocks})
            loose.clear()

    def visit(n):
        for c in n.children:
            if isinstance(c, str):
                if clean(c):
                    loose.append(Node("span", {}, n))
                    loose[-1].children.append(c)
                continue
            if is_hidden_or_noise(c):
                continue
            if c.tag == "section":
                flush_loose()
                sid = f"s{len(sections) + 1}"
                w = Walker(lang, images)
                w.walk(c, {"page": page_key, "section": sid, "snippet": c.attrs.get("data-snippet")})
                sec = {"id": sid, "snippet": c.attrs.get("data-snippet"),
                       "name": c.attrs.get("data-name"), "blocks": w.blocks}
                forms = [form_fields(f, lang) for f in c.iter() if f.tag == "form"]
                if forms:
                    sec["forms"] = forms
                if w.blocks or forms:
                    sections.append(sec)
            elif c.find(lambda x: x.tag == "section") is not None:
                visit(c)
            else:
                loose.append(c)
        return

    visit(container)
    flush_loose()
    return sections


def extract_nav(root, lang):
    menu = root.find(lambda n: n.tag == "ul" and n.attrs.get("id") == "top_menu")
    items = []
    if menu is None:
        return items
    for li in [c for c in menu.children if isinstance(c, Node) and c.tag == "li"]:
        a = li.find(lambda n: n.tag == "a")
        it = {"label": one_line(a.text()), "href": absurl(a.attrs.get("href")),
              "path": site_path(a.attrs.get("href"), lang) if a.attrs.get("href") != "#" else None}
        sub = li.find(lambda n: n.tag == "ul")
        if sub is not None:
            it["children"] = [{"label": one_line(x.text()), "href": absurl(x.attrs.get("href")),
                               "path": site_path(x.attrs.get("href"), lang)}
                              for x in sub.iter() if x.tag == "a"]
        items.append(it)
    return items


def group_by_heading(blocks):
    """Group a flat block list into items that start at each heading."""
    groups, cur = [], None
    for b in blocks:
        if b["type"] == "heading":
            cur = {"heading": b["text"], "level": b["level"], "blocks": []}
            groups.append(cur)
        else:
            if cur is None:
                cur = {"heading": None, "blocks": []}
                groups.append(cur)
            cur["blocks"].append(b)
    return groups


def extract_site(root, lang, images):
    header = root.find(lambda n: n.tag == "header")
    footer = root.find(lambda n: n.tag == "footer")
    site = {"name": "DarbTech", "nav": extract_nav(root, lang)}
    logo = header.find(lambda n: n.tag == "img" and "logo" in (n.attrs.get("src") or ""))
    if logo is not None:
        site["logo"] = {"src": absurl(logo.attrs["src"]), "alt": logo.attrs.get("alt")}
        images.append({"url": site["logo"]["src"], "alt": logo.attrs.get("alt"), "page": "_site",
                       "section": "header", "block": site["logo"], "category": "brand", "name": "logo"})
    fav = root.find(lambda n: n.tag == "link" and "icon" in (n.attrs.get("rel") or ""))
    if fav is not None:
        site["favicon"] = {"src": absurl(fav.attrs["href"])}
        images.append({"url": site["favicon"]["src"], "alt": "", "page": "_site", "section": "head",
                       "block": site["favicon"], "category": "brand", "name": "favicon"})
    # header extras: phone + CTA (desktop navbar only)
    nav = header.find(lambda n: n.tag == "nav")
    hw = Walker(lang, [])
    for li in nav.iter():
        if li.tag == "li" and ("s_text_block" in " ".join(x.attrs.get("class", "") for x in li.iter())):
            hw.walk(li, {})
    txt = [b["text"] for b in hw.blocks if b["type"] == "text"]
    site["header_phone"] = txt[0] if txt else None
    cta = nav.find(lambda n: n.tag == "a" and "_cta" in n.cls())
    site["header_cta"] = ({"text": one_line(cta.text()), "href": absurl(cta.attrs.get("href")),
                           "path": site_path(cta.attrs.get("href"), lang)} if cta is not None else None)
    langs = []
    for a in header.iter():
        if a.tag == "a" and "js_change_lang" in a.cls():
            if not any(l["code"] == a.attrs.get("data-url_code") for l in langs):
                langs.append({"code": a.attrs.get("data-url_code"), "label": clean(a.attrs.get("title")),
                              "active": "active" in a.cls()})
    site["languages"] = langs
    # footer
    fw = Walker(lang, [])
    main_footer = footer.find(lambda n: n.attrs.get("id") == "footer") or footer
    fw.walk(main_footer, {})
    cols = []
    for g in group_by_heading(fw.blocks):
        if g["heading"] is None:
            continue
        col = {"heading": g["heading"], "links": [], "lines": []}
        for b in g["blocks"]:
            if b["type"] == "list":
                for it in b["items"]:
                    if it.get("links"):
                        for l in it["links"]:
                            l = dict(l)
                            l["text"] = one_line(it["text"]) or l["text"]
                            col["links"].append(l)
                    elif it["text"]:
                        col["lines"].append(it["text"])
            elif b["type"] == "link":
                col["links"].append({k: v for k, v in b.items() if k != "type"})
            elif b.get("text"):
                col["lines"].extend(b["text"].split("\n"))
        cols.append(col)
    copy = footer.find(lambda n: "o_footer_copyright" in n.cls())
    cw = Walker(lang, [])
    if copy is not None:
        cw.walk(copy, {})
    site["footer"] = {
        "columns": cols,
        "copyright": next((b["text"] for b in cw.blocks if b["type"] == "text" and "©" in b["text"]), None),
        "powered_by_lines": [b["text"] for b in cw.blocks if b.get("text") and "©" not in b["text"]
                             and b["text"] != "-"],
        "_note_powered_by": "Odoo default 'Powered by Odoo' badge (Odoo logo image + link to odoo.com)",
    }
    mark_missing(fw.blocks, lang, {"missing": 0, "total": 0})
    for col in cols:
        for l in col["links"]:
            if detect_lang(l["text"]) == ("en" if lang == "fr" else "fr"):
                l["_missing"] = True
    return site


def page_key_of(path):
    p = path.strip("/")
    return p.replace("/", "__") or "home"


def extract_page(path, lang, images):
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", path.strip("/")) or "home"
    root = parse(os.path.join(RAW, lang, slug + ".html"))
    main = root.find(lambda n: n.tag == "main")
    key = page_key_of(path)
    page = {"path": path, "url": BASE + (("/en" if lang == "en" else "") + path if path != "/" else ("/en" if lang == "en" else "/")),
            **head_meta(root)}
    page["sections"] = sections_of(main, lang, images, key) if main is not None else []
    stats = {"missing": 0, "total": 0}
    for s in page["sections"]:
        mark_missing(s["blocks"], lang, stats)
    page["translation"] = {"blocks_checked": stats["total"], "blocks_in_other_language": stats["missing"]}
    other = "en" if lang == "fr" else "fr"
    meta_missing = [k for k in ("title", "meta_description", "og_title")
                    if page.get(k) and detect_lang(page[k]) == other]
    if meta_missing:
        page["translation"]["meta_fields_in_other_language"] = meta_missing
    if stats["total"] and stats["missing"] / stats["total"] > 0.5:
        page["_missing"] = True
    return root, page


def blog_post(root, page, lang, images):
    t = root.find(lambda n: n.attrs.get("id") == "o_wblog_post_name")
    sub = root.find(lambda n: n.attrs.get("id") == "o_wblog_post_subtitle")
    content = root.find(lambda n: "o_wblog_post_content_field" in n.cls())
    cover = root.find(lambda n: "o_wblog_post_page_cover" in n.cls())
    cover_url = None
    if cover is not None:
        ci = cover.find(lambda n: "o_record_cover_image" in n.cls())
        cover_url = absurl(bg_image(ci)) if ci is not None and bg_image(ci) else None
    crumbs = root.find(lambda n: "breadcrumb" in n.cls())
    cat = None
    if crumbs is not None:
        links = [a for a in crumbs.iter() if a.tag == "a"]
        if len(links) >= 2:
            cat = {"name": one_line(links[1].text()), "path": site_path(links[1].attrs.get("href"), lang)}
    hdr = t.parent.parent if t is not None else None
    date = author = None
    if hdr is not None:
        sp = [one_line(s.text()) for s in hdr.iter() if s.tag == "span" and one_line(s.text())]
        date = next((s for s in sp if re.search(r"\d{4}", s)), None)
        author = sp[-1] if sp else None
    tags = sorted({one_line(a.text()) for a in root.iter() if a.tag == "a" and "/tag/" in (a.attrs.get("href") or "")
                   and one_line(a.text())})
    w = Walker(lang, images)
    if content is not None:
        w.walk(content, {"page": page_key_of(page["path"]), "section": "body", "category": "blog"})
    stats = {"missing": 0, "total": 0}
    mark_missing(w.blocks, lang, stats)
    post = {"path": page["path"], "url": page["canonical"] or page["url"],
            "title": one_line(t.text()) if t is not None else page["title"],
            "subtitle": one_line(sub.text()) if sub is not None and one_line(sub.text()) else None,
            "category": cat, "tags": tags, "date_display": date,
            "published_time": page["published_time"], "modified_time": page["modified_time"],
            "author": author, "cover_image": {"src": cover_url} if cover_url else None,
            "meta_description": page["meta_description"], "body": w.blocks,
            "translation": {"blocks_checked": stats["total"], "blocks_in_other_language": stats["missing"]}}
    for k in ("title", "subtitle"):
        if post[k] and detect_lang(post[k]) == ("en" if lang == "fr" else "fr"):
            post.setdefault("_missing_fields", []).append(k)
    if stats["total"] and stats["missing"] / stats["total"] > 0.5:
        post["_missing"] = True
    if cover_url:
        images.append({"url": cover_url, "alt": post["title"], "page": page_key_of(page["path"]),
                       "section": "cover", "block": post["cover_image"], "category": "blog"})
    first = next((b["text"] for b in w.blocks if b["type"] == "text" and len(b["text"]) > 60), None)
    post["excerpt"] = (first[:240].rsplit(" ", 1)[0] + "…") if first and len(first) > 240 else first
    return post


# ----------------------------------------------------------------- inventory
ODOO_APPS = {
    "CRM": r"\bCRM\b", "ERP": r"\bERP\b", "MRP / Fabrication": r"\bMRP\b|\bfabrication\b|\bmanufacturing\b",
    "Helpdesk": r"\bhelpdesk\b", "Planning": r"\bplanning\b", "Ventes / Sales": r"\bventes?\b|\bsales\b",
    "Achats / Purchase": r"\bachats?\b|\bpurchas\w*", "Inventaire / Stock": r"\bstocks?\b|\binventor\w+|\binventaire\b",
    "Comptabilité / Accounting": r"\bcomptab\w+|\baccounting\b", "Facturation / Invoicing": r"\bfactur\w+|\binvoic\w+",
    "RH / HR": r"\bRH\b|\bHR\b|ressources humaines|human resources", "Paie / Payroll": r"\bpaie\b|\bpayroll\b",
    "eCommerce": r"\be-?commerce\b", "Site web / Website": r"\bsite web\b|\bwebsite\b",
    "Projet / Project": r"\bgestion de projets?\b|\bproject management\b", "Marketing automation": r"marketing automation",
    "Recrutement / Recruitment": r"\brecrutement\b|\brecruitment\b", "CTI / Téléphonie": r"\bCTI\b",
    "Point de vente / PoS": r"\bpoint de vente\b|\bpoint of sale\b|\bPoS\b", "Field service": r"field service|intervention sur site",
    "Documents / GED": r"\bGED\b|\bsharepoint\b", "Studio": r"\bodoo studio\b",
}


# Client logos carry no alt text; these names were read off the logo images themselves
# (manual visual check, 2026-10-22) because the file names are not explicit.
LOGO_TEXT = {"1. Logo original": "L'AMBASSADE DES LANGUES PARIS", "CMT company": "CMT GROUP",
             "netiwan": "netiwan GROUPE", "Puthod": "PUTHOD PÉPINIÈRES", "ACSP": "ACSP Conseil",
             "Tionis": "tionis."}


def all_texts(blocks):
    for b in blocks:
        if b["type"] == "list":
            for it in b["items"]:
                yield it["text"]
        elif b.get("text"):
            yield b["text"]


def build_inventory(pages, posts, lang):
    inv = {}
    P = pages
    # services: services, devops, integrateurdelogiciel pages grouped by heading
    services = []
    for key in ("services", "devops", "integrateurdelogiciel"):
        pg = P.get(key)
        if not pg:
            continue
        for s in pg["sections"]:
            if s["snippet"] in ("s_references", "s_title", "s_images_wall", "s_masonry_block"):
                continue
            for g in group_by_heading(s["blocks"]):
                if not g["heading"]:
                    continue
                texts = [b["text"] for b in g["blocks"] if b["type"] == "text"]
                if (not texts and not any(b["type"] == "list" for b in g["blocks"])
                        and s["snippet"] != "s_text_block"):
                    continue
                services.append({"page": key, "section": s["id"], "snippet": s["snippet"], "title": g["heading"],
                                 "text": texts,
                                 "links": [{k: v for k, v in b.items() if k != "type"} for b in g["blocks"] if b["type"] == "link"],
                                 "images": [b["src"] for b in g["blocks"] if b["type"] in ("image", "background_image")]})
    # services page "text_block" bullet headings (ERP projects, full stack...)
    inv["services"] = services
    # Odoo modules mentioned (pages + blog titles/subtitles/tags)
    mods = {}
    corpus = []
    for key, pg in P.items():
        for s in pg["sections"]:
            corpus += [(f"page:{key}", t) for t in all_texts(s["blocks"])]
    for p in posts:
        corpus += [(f"blog:{p['path']}", x) for x in [p["title"], p.get("subtitle") or ""] + p["tags"]]
        corpus += [(f"blog:{p['path']}", t) for t in all_texts(p["body"])]
    for name, rx in ODOO_APPS.items():
        r = re.compile(rx, re.I)
        where = sorted({src for src, t in corpus if r.search(t)})
        if where:
            mods[name] = {"pages": [w for w in where if w.startswith("page:")],
                          "blog_posts_count": sum(1 for w in where if w.startswith("blog:"))}
    inv["odoo_apps_and_topics_mentioned"] = mods
    # clients
    refs = []
    for s in P.get("services", {}).get("sections", []):
        if s["snippet"] == "s_references":
            for b in s["blocks"]:
                if b["type"] == "image":
                    fn = urllib.parse.unquote(b["src"].rsplit("/", 1)[-1])
                    ref = {"logo": b, "name_from_filename": re.sub(r"(?i)\.(png|jpe?g|webp|svg)$", "", fn)}
                    for k, v in LOGO_TEXT.items():
                        if k in fn:
                            ref["text_visible_in_logo"] = v
                    refs.append(ref)
    inv["client_logos"] = refs
    cases = []
    for p in posts:
        if p.get("category") and p["category"]["path"] and "cas-client" in p["category"]["path"] + p["path"] or "client-case" in p["path"]:
            strongs = []
            cases.append({"title": p["title"], "subtitle": p.get("subtitle"), "path": p["path"], "date": p["date_display"],
                          "first_paragraph": next(iter(all_texts(p["body"])), None)})
    inv["client_cases"] = cases
    # team
    team = []
    about = P.get("aboutus")
    if about:
        for s in about["sections"]:
            if s["snippet"] != "s_company_team_basic":
                continue
            cur = None
            for b in s["blocks"]:
                if b["type"] == "image":
                    cur = {"photo": b, "lines": []}
                    team.append(cur)
                elif cur is not None and b["type"] == "text":
                    ltexts = {l["text"] for l in b.get("links", []) if l.get("text")}
                    cur["lines"] += [x for x in b["text"].split("\n") if x not in ltexts]
                    for l in b.get("links", []):
                        if l.get("path") and l["path"] != "/":
                            cur["bio_path"], cur["bio_link_label"] = l["path"], l["text"]
                elif cur is not None and b["type"] == "heading" and b["text"]:
                    cur["lines"].append(b["text"])
                elif cur is not None and b["type"] == "link" and b.get("path") and b["path"] != "/":
                    cur["bio_path"] = b["path"]
                    cur["bio_link_label"] = b["text"]
    members = []
    for m in team:
        lines = [l for l in m["lines"] if l]
        mem = {"name": lines[0] if lines else None, "role": lines[1] if len(lines) > 1 else None,
               "certifications": lines[2] if len(lines) > 2 else None, "photo": m["photo"],
               "bio_path": m.get("bio_path"), "bio_link_label": m.get("bio_link_label")}
        bp = P.get(page_key_of(m.get("bio_path") or "")) if m.get("bio_path") else None
        if bp:
            bio = []
            linkedin = None
            for s in bp["sections"]:
                for b in s["blocks"]:
                    if b["type"] == "link" and "linkedin" in (b.get("href") or ""):
                        linkedin = b["href"]
                    for l in b.get("links", []):
                        if "linkedin" in (l.get("href") or ""):
                            linkedin = l["href"]
                if s["snippet"] != "s_company_team_basic":
                    bio += [b for b in s["blocks"] if b["type"] in ("text", "list", "heading")]
            mem["linkedin"] = linkedin
            mem["bio"] = bio
        members.append(mem)
    inv["team"] = members
    # partners (aboutus "Nos partenaires" columns)
    partners = []
    if about:
        for s in about["sections"]:
            if s["snippet"] == "s_three_columns":
                logo = None
                cur = None
                for b in s["blocks"]:
                    if b["type"] == "image":
                        logo = b
                    elif b["type"] in ("heading", "link") and b.get("heading_level") or (b["type"] == "heading" and b["text"]):
                        cur = {"name": b["text"], "website": b.get("href"), "logo": logo, "content": []}
                        partners.append(cur)
                        logo = None
                    elif cur is not None:
                        cur["content"].append(b)
    inv["partners"] = partners
    # certifications mentioned (team cards + partner texts)
    certs = sorted({c.strip() for m in members if m.get("certifications")
                    for c in re.sub(r"^(Certifié[e]?|Certified)\s*|\s*Certified$", "", m["certifications"]).split(",")
                    if c.strip()})
    inv["certifications_mentioned"] = {"from_team_cards": certs,
                                       "team_card_lines": sorted({m["certifications"] for m in members if m.get("certifications")})}
    # stats & figures: sentences with digits on the main pages
    stats = []
    for key in ("home", "aboutus", "services", "devops", "integrateurdelogiciel", "prqdarbodoo", "contactus"):
        for s in P.get(key, {}).get("sections", []):
            for t in all_texts(s["blocks"]):
                if (re.search(r"\b\d{2,4}\b|\bdécennie\b|\bdecade\b", t) and len(t) > 40
                        and not re.search(r"\+\d{2,3} ?\d|\bAv\.|\bAve\b", t)):
                    stats.append({"page": key, "text": t})
    inv["stats_and_figures"] = stats
    inv["testimonials"] = []
    # contact
    emails, phones = {}, {}
    for key, pg in P.items():
        for s in pg["sections"]:
            for t in all_texts(s["blocks"]):
                for e in re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", t):
                    emails.setdefault(e.lower().rstrip("."), set()).add(key)
                for ph in re.findall(r"\+\d{2,3}[\d .]{7,16}\d", t):
                    phones.setdefault(re.sub(r"\s+", " ", ph), set()).add(key)
            for b in s["blocks"]:
                for l in [b] + b.get("links", []):
                    h = l.get("href") or ""
                    if h.startswith("mailto:"):
                        emails.setdefault(h[7:].lower(), set()).add(key)
    contact = {}
    cp = P.get("contactus")
    if cp:
        offices = []
        for s in cp["sections"]:
            for g in group_by_heading(s["blocks"]):
                if g["level"] if "level" in g else False:
                    lines = [l for b in g["blocks"] if b.get("text") for l in b["text"].split("\n") if l.strip()]
                    if any(re.search(r"T[ée]l", l) for l in lines):
                        offices.append({"name": g["heading"], "lines": lines})
            if s.get("forms"):
                contact["form"] = s["forms"][0]
                contact["form_section_text"] = [b["text"] for b in s["blocks"] if b["type"] == "text"][:40]
        contact["offices_contact_page"] = offices
    contact["emails_found"] = {e: sorted(v) for e, v in sorted(emails.items())}
    contact["phones_found"] = {p: sorted(v) for p, v in sorted(phones.items())}
    inv["contact"] = contact
    # jobs
    jobs = []
    for key, pg in P.items():
        if key.startswith("jobs__") and not key.startswith("jobs__apply__"):
            h1 = next((b["text"] for s in pg["sections"] for b in s["blocks"] if b["type"] == "heading" and b["level"] == 1), None)
            loc = next((b["text"] for s in pg["sections"] for b in s["blocks"] if b["type"] == "heading" and b["level"] == 5), None)
            apply = next((b for s in pg["sections"] for b in s["blocks"] if b["type"] == "link" and "/jobs/apply/" in (b.get("href") or "")), None)
            body = []
            for s in pg["sections"][1:]:
                body += [b for b in s["blocks"] if not (b["type"] == "link" and "/jobs/apply/" in (b.get("href") or ""))]
            jobs.append({"title": h1, "location": one_line(loc) if loc else None, "detail_path": pg["path"],
                         "apply": apply, "description": body,
                         "_missing": True if pg.get("_missing") else None})
    inv["jobs"] = jobs
    apply_pg = next((pg for k, pg in P.items() if k.startswith("jobs__apply__")), None)
    if apply_pg:
        inv["job_application_form"] = next((s["forms"][0] for s in apply_pg["sections"] if s.get("forms")), None)
    return inv


# ----------------------------------------------------------------- assets
SKIP_ASSET = [
    (r"/country_flags/", "language flag (Odoo default)"),
    (r"odoo_logo_tiny", "'Powered by Odoo' badge"),
    (r"/web_editor/shape/", "decorative theme shape"),
    (r"website\.library_image_", "Odoo stock placeholder image"),
    (r"website\.s_[a-z_]+default_image|/s_[a-z_]+_default_image", "Odoo snippet placeholder image"),
    (r"/author_avatar/", "generic blog author avatar"),
    (r"/web/image/website/1/favicon", None),
]


def slugify(s, maxlen=60):
    s = unicodedata.normalize("NFKD", urllib.parse.unquote(s)).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s[:maxlen].strip("-") or "image"


EXT = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp", "image/gif": ".gif",
       "image/svg+xml": ".svg", "image/vnd.microsoft.icon": ".ico", "image/x-icon": ".ico"}


def download(url):
    req = urllib.request.Request(urllib.parse.quote(url, safe=":/?=&%#"), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        ctype = r.headers.get("Content-Type", "").split(";")[0].strip()
        data = r.read(MAX_ASSET_BYTES + 1)
    return ctype, data


def unwrap_svg(data):
    """Odoo shape-masked images are SVGs embedding one base64 raster: return it."""
    m = re.search(rb'href="data:(image/[a-z+]+);base64,([A-Za-z0-9+/=\s]+)"', data)
    if m and data.count(b"data:image/") == 1:
        return m.group(1).decode(), base64.b64decode(re.sub(rb"\s+", b"", m.group(2)))
    return None, None


def categorise(img):
    u, page, sec = img["url"], img.get("page"), img.get("section")
    if img.get("category"):
        return img["category"]
    if page == "services" and img.get("snippet") == "s_references":
        return "clients"
    if page == "aboutus" and img.get("snippet") == "s_company_team_basic":
        return "team"
    if page == "aboutus" and img.get("snippet") == "s_three_columns":
        return "partners"
    if img.get("snippet") == "s_company_team_basic":
        return "team-bio"
    if page and page.startswith("blog"):
        return "blog"
    if page and page.startswith("jobs"):
        return "jobs"
    return "pages"


def process_assets(images_by_lang, offline):
    manifest, by_url = [], {}
    os.makedirs(ASSETS, exist_ok=True)
    cache_path = os.path.join(ASSETS, ".cache.json")
    cache = json.load(open(cache_path, encoding="utf-8")) if os.path.exists(cache_path) and "--refresh" not in sys.argv else {}
    skipped = {}
    for lang, images in images_by_lang.items():
        for img in images:
            url = img["url"]
            if url.startswith("data:"):
                continue
            reason = next((r for rx, r in SKIP_ASSET if re.search(rx, url)), "")
            if reason and img.get("category") != "brand":
                skipped.setdefault(reason, set()).add(url)
                continue
            cat = categorise(img)
            if cat == "blog" and img.get("section") != "cover":
                skipped.setdefault("blog article inline image (not downloaded)", set()).add(url)
                continue
            if cat == "blog" and not img.get("_download"):
                skipped.setdefault("blog cover of an older post (only client cases + 12 latest kept); "
                                   "URL stays in blog.*.json cover_image.src", set()).add(url)
                continue
            if cat == "team-bio":
                skipped.setdefault("team bio-page photo (same person as about-us card photo)", set()).add(url)
                continue
            if cat == "jobs":
                cat = "pages"
            ent = by_url.get(url)
            if ent is None:
                ent = {"id": None, "category": cat, "original_url": url, "local_path": None, "alt": {},
                       "used_in": []}
                by_url[url] = ent
                manifest.append(ent)
            if img.get("_name"):
                ent["_name"] = img["_name"]
            if img.get("alt"):
                ent["alt"][lang] = img["alt"]
            use = f"{lang}:{img.get('page')}#{img.get('section')}"
            if use not in ent["used_in"]:
                ent["used_in"].append(use)
            ent.setdefault("_blocks", []).append(img["block"])
    # name + download
    used_names = set()
    for ent in manifest:
        url, cat = ent["original_url"], ent["category"]
        fn = url.split("?")[0].rstrip("/").rsplit("/", 1)[-1]
        if cat == "brand":
            base = "logo" if "/logo" in url else "favicon"
        elif cat == "blog":
            pg = ent["used_in"][0].split(":", 1)[1].split("#")[0]
            pid = re.search(r"-(\d+)$", pg)
            base = f"post-{pid.group(1) if pid else slugify(pg, 20)}-cover"
        elif cat == "team":
            b = ent["_blocks"][0]
            base = None
        else:
            base = slugify(re.sub(r"\.(png|jpe?g|webp|svg|gif)$", "", fn, flags=re.I), 50)
        ent["_base"] = base
    # team names come from inventory (filled by caller via ent["_name"])
    for ent in manifest:
        base = ent.get("_name") or ent["_base"] or slugify(ent["original_url"].rsplit("/", 1)[-1], 40)
        name = base
        i = 2
        while f"{ent['category']}/{name}" in used_names:
            name = f"{base}-{i}"
            i += 1
        used_names.add(f"{ent['category']}/{name}")
        ent["id"] = f"{ent['category']}/{name}"
        c = cache.get(ent["original_url"])
        if c and os.path.exists(os.path.join(DATA, c["local_path"])):
            ent.update({k: v for k, v in c.items() if v is not None})
        elif not offline:
            try:
                src = ent["original_url"]
                note = None
                if ent["category"] == "blog":  # covers are ~2 MB PNGs: ask Odoo for a 480px-wide copy
                    src = re.sub(r"(/web/image/\d+-[0-9a-f]+)/", r"\1/480x0/", src, count=1)
                    if src != ent["original_url"]:
                        ent["downloaded_from"] = src
                        note = "resized by Odoo to 480px wide; original_url is full size"
                ctype, data = download(src)
                if len(data) > MAX_ASSET_BYTES:
                    ent["skipped"] = f"larger than {MAX_ASSET_BYTES} bytes"
                    continue
                if ctype == "image/svg+xml":
                    rtype, raster = unwrap_svg(data)
                    if raster:
                        ctype, data, note = rtype, raster, "raster extracted from Odoo shape-masked SVG wrapper"
                ext = EXT.get(ctype, os.path.splitext(ent["original_url"].split("?")[0])[1] or ".bin")
                digest = hashlib.sha1(data).hexdigest()
                same = next((e for e in manifest if e is not ent and e.get("sha1") == digest and e.get("local_path")), None)
                if same:  # identical file already saved under another URL
                    rel = same["local_path"]
                    note = (note + "; " if note else "") + f"identical to {same['id']}"
                else:
                    rel = f"assets/{ent['category']}/{name}{ext}"
                    os.makedirs(os.path.dirname(os.path.join(DATA, rel)), exist_ok=True)
                    with open(os.path.join(DATA, rel), "wb") as f:
                        f.write(data)
                ent.update({"local_path": rel, "content_type": ctype, "bytes": len(data), "sha1": digest})
                if note:
                    ent["note"] = note
                cache[ent["original_url"]] = {k: ent.get(k) for k in ("local_path", "content_type", "bytes", "note",
                                                                       "sha1", "downloaded_from")}
                time.sleep(0.15)
            except Exception as e:  # keep going, record the failure
                ent["error"] = str(e)
        for b in ent.get("_blocks", []):
            if ent.get("local_path"):
                b["asset"] = ent["local_path"]
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=1)
    for ent in manifest:
        for k in ("_blocks", "_base", "_name"):
            ent.pop(k, None)
    return manifest, {k: sorted(v) for k, v in skipped.items()}


# ----------------------------------------------------------------- main
def main():
    offline = "--no-assets" in sys.argv
    index = json.load(open(os.path.join(RAW, "pages.json"), encoding="utf-8"))
    out, blogs, images_by_lang = {}, {}, {}
    # Redirect aliases, computed on the French site (paths are language-neutral there)
    fr_paths = {r["path"] for r in index if r["lang"] == "fr"}
    redirects = {}
    for r in index:
        if r["lang"] == "fr" and r["status"] == 200:
            final = site_path(r["final_url"], "fr")
            if final != r["path"] and final in fr_paths:
                redirects[r["path"]] = final
    for lang in ("fr", "en"):
        images = []
        images_by_lang[lang] = images
        site = None
        pages, posts, aliases = {}, [], {}
        for rec in [r for r in index if r["lang"] == lang]:
            path = rec["path"]
            if rec["status"] != 200:
                continue
            if site is not None and path in redirects:
                aliases[path] = redirects[path]  # e.g. /blog/cas-client-4 -> /blog/cas-clients-4
                continue
            root, page = extract_page(path, lang, images)
            page["final_url"] = rec["final_url"]
            if site is None:
                site = extract_site(root, lang, images)
            if re.match(r"^/blog/[^/]+/[^/]+$", path) and not path.endswith("/feed"):
                posts.append(blog_post(root, page, lang, images))
                continue
            pages[page_key_of(path)] = page
        posts.sort(key=lambda p: p.get("published_time") or "", reverse=True)
        # Blog covers: only download the client cases + the 12 most recent posts
        keep = {p["path"] for i, p in enumerate(posts)
                if i < 12 or (p.get("category") and re.search(r"cas-client|client-case", p["category"]["path"] or ""))}
        for img in images:
            if img.get("section") == "cover" and img.get("category") == "blog":
                img["_download"] = img["page"] in {page_key_of(k) for k in keep}
        inv = build_inventory(pages, posts, lang)
        # name team images after the person
        for m in inv["team"]:
            m["photo"]["_person"] = slugify(m["bio_path"].strip("/") if m.get("bio_path") else (m["name"] or "member"))
        for img in images:
            if isinstance(img.get("block"), dict) and img["block"].get("_person"):
                img["category"] = "team"
        blogs[lang] = {"_meta": {"lang": lang, "source": BASE, "count": len(posts)},
                       "categories": sorted({(p["category"]["name"], p["category"]["path"]) for p in posts if p.get("category")}),
                       "posts": posts}
        out[lang] = {"_meta": {"lang": lang, "source": BASE + ("/en" if lang == "en" else "/"),
                               "scraped_at": datetime.date.today().isoformat(),
                               "generator": "scripts/extract.py",
                               "notes": "Exact wording from the live site. Blocks with \"_missing\": true are shown "
                                        "on the live site in the other language (untranslated in Odoo); "
                                        "\"_text_lang\" gives that language."},
                     "site": site, "pages": pages, "page_aliases": aliases, "inventory": inv,
                     "blog_index": [{k: p.get(k) for k in ("title", "subtitle", "path", "url", "category", "date_display",
                                                            "published_time", "author", "cover_image", "excerpt", "tags",
                                                            "_missing")} for p in posts]}
    # asset names for team members
    for imgs in images_by_lang.values():
        for img in imgs:
            b = img.get("block")
            if isinstance(b, dict) and b.get("_person"):
                img["_name"] = b["_person"]
    manifest, skipped = process_assets(images_by_lang, offline)
    for lang in ("fr", "en"):
        # strip helper keys
        def strip(o):
            if isinstance(o, dict):
                o.pop("_person", None)
                for v in o.values():
                    strip(v)
            elif isinstance(o, list):
                for v in o:
                    strip(v)
        strip(out[lang])
        strip(blogs[lang])
        for p in blogs[lang]["posts"]:
            for k in [k for k, v in p.items() if v is None]:
                p.pop(k)
        with open(os.path.join(DATA, f"content.{lang}.json"), "w", encoding="utf-8") as f:
            json.dump(out[lang], f, ensure_ascii=False, indent=1)
        with open(os.path.join(DATA, f"blog.{lang}.json"), "w", encoding="utf-8") as f:
            json.dump(blogs[lang], f, ensure_ascii=False, indent=1)
    with open(os.path.join(DATA, "assets.json"), "w", encoding="utf-8") as f:
        json.dump({"_meta": {"generated": datetime.date.today().isoformat(),
                             "notes": "local_path is relative to data/. used_in = lang:pageKey#sectionId."},
                   "assets": manifest, "not_downloaded": skipped}, f, ensure_ascii=False, indent=1)
    print("pages fr/en:", len(out["fr"]["pages"]), len(out["en"]["pages"]),
          "posts:", len(blogs["fr"]["posts"]), len(blogs["en"]["posts"]),
          "assets:", sum(1 for a in manifest if a.get("local_path")), "/", len(manifest))


if __name__ == "__main__":
    main()
