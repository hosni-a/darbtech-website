"""DarbTech static site generator.

Usage (from the project root):
    python build/build.py            # render all pages into site/
    python build/build.py --images   # also (re)generate optimised images (needs Pillow)

Standard library only for page rendering. Image optimisation uses Pillow when --images is passed.
Reads data/*.json (scraped content) and writes site/**/index.html for FR (root) and EN (/en/).
"""
import json
import os
import re
import shutil
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
SITE = os.path.join(ROOT, "site")
sys.path.insert(0, HERE)

from lib import Ctx, ROUTES, document, out_file, public_url, SITE_URL  # noqa: E402
import pages_main as pm  # noqa: E402
import pages_other as po  # noqa: E402

LANGS = ("fr", "en")

PAGES = {
    "home": pm.page_home,
    "odoo": pm.page_odoo,
    "odoo_impl": pm.page_odoo_impl,
    "odoo_migration": pm.page_odoo_migration,
    "odoo_custom": pm.page_odoo_custom,
    "odoo_integrations": pm.page_odoo_integrations,
    "odoo_support": pm.page_odoo_support,
    "odoo_apps": pm.page_odoo_apps,
    "dev": po.page_dev,
    "cases": po.page_cases,
    "case_puthod": lambda c: po.page_case(c, "puthod"),
    "case_cameleon": lambda c: po.page_case(c, "cameleon"),
    "method": po.page_method,
    "about": po.page_about,
    "team": po.page_team,
    "careers": po.page_careers,
    "contact": po.page_contact,
    "legal": po.page_legal,
    "privacy": po.page_privacy,
    "terms": po.page_terms,
    "404": po.page_404,
}

# Team: display names (disambiguates the two Khadija / Salma) and groups for the filter
TEAM_META = {
    "viet": ("Viet", ["lead"]),
    "fred": ("Fred", ["lead", "consult"]),
    "thomas": ("Thomas", ["lead", "consult"]),
    "kamal": ("Kamal", ["lead", "consult"]),
    "maria": ("Maria", ["consult"]),
    "frederic": ("Frédéric", ["consult"]),
    "marwa": ("Marwa", ["admin"]),
    "anis": ("Anis", ["tech"]),
    "hosni": ("Hosni", ["tech"]),
    "abdellatif": ("Abdellatif", ["tech", "consult"]),
    "zoubida": ("Zoubida", ["tech"]),
    "fatima-zahra": ("Fatima Zahra", ["erp"]),
    "khadija-r": ("Khadija R.", ["erp"]),
    "mohammed": ("Mohammed", ["erp"]),
    "salma": ("Salma K.", ["erp"]),
    "khadija-a": ("Khadija A.", ["erp"]),
    "hatim": ("Hatim", ["erp"]),
    "ouail": ("Ouail", ["erp"]),
    "elmehdi": ("El Mehdi", ["erp"]),
    "douae": ("Douae", ["erp"]),
    "sally": ("Salma E.", ["erp"]),
}
TEAM_ORDER = ["viet", "fred", "thomas", "kamal", "maria", "frederic", "zoubida", "abdellatif", "hosni", "anis",
              "fatima-zahra", "khadija-r", "mohammed", "salma", "khadija-a", "hatim", "ouail", "elmehdi", "douae",
              "sally", "marwa"]

# EN role fixes (literal translations on the live site)
ROLE_EN = {"Advanced ERP Engineer": "Senior ERP Engineer", "Administrative and Commercial Officer": "Sales & Administrative Officer"}
ROLE_FR = {"Lead développeur et Consultant": "Lead développeur et consultant"}

# Images: (source in data/assets, destination in site/assets/img, max width, format)
IMAGES = [
    ("brand/logo.png", "brand/logo.png", None, "copy"),
    ("brand/favicon.ico", "brand/favicon.ico", None, "copy"),
    ("clients/logo-netiwan.png", "clients/netiwan.png", 320, "png"),
    ("clients/logo-cmt-company.png", "clients/cmt-group.png", 320, "png"),
    ("clients/logo-puthod.jpg", "clients/puthod.png", 320, "png"),
    ("clients/1-logo-original.png", "clients/ambassade-des-langues.png", 320, "png"),
    ("clients/acsp-conseil.png", "clients/acsp-conseil.png", 320, "png"),
    ("clients/logo-tionis.png", "clients/tionis.png", 320, "png"),
    ("partners/odoo-logo-svg.webp", "partners/odoo.webp", 360, "webp"),
    ("partners/logo-ringover.png", "partners/ringover.png", 160, "png"),
    ("partners/leexi.webp", "partners/leexi.webp", 300, "webp"),
    ("pages/asilahdt2023.webp", "team/asilah-2023.webp", 900, "webp"),
    ("blog/post-18-cover.jpg", "cases/puthod.webp", 900, "webp"),
    ("blog/post-19-cover.jpg", "cases/cameleon.webp", 900, "webp"),
]
BLOG_COVERS = ["73", "72", "69"]


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def asset_index():
    """Only files listed in assets.json may be used."""
    a = load("assets.json")
    return {x["local_path"].replace("assets/", "", 1) for x in a["assets"]}


def parse_certs(s):
    if not s:
        return ["Odoo"]
    s = re.sub(r"(?i)certifi(?:ed|ée|é)", "", s)  # "Certified"/"Certifié(e)"; the old pattern left a stray "d"
    toks = [t.strip() for t in s.split(",") if t.strip()]
    toks = ["Ringover" if t.lower() == "ringover" else t for t in toks]
    out = ["Odoo"] + [t for t in toks if t != "Odoo"]   # DECISIONS.md: every team member is Odoo-certified
    return out


def build_team(content, lang):
    team = []
    by_slug = {m["bio_path"].strip("/"): m for m in content["inventory"]["team"]}
    for slug in TEAM_ORDER:
        m = by_slug[slug]
        display, groups = TEAM_META[slug]
        role = m["role"]
        role = (ROLE_EN if lang == "en" else ROLE_FR).get(role, role)
        bio = [b["text"] for b in m.get("bio", []) if b.get("type") == "text" and b.get("text")]
        team.append(dict(slug=slug, name=m["name"], display=display, role=role, certs=parse_certs(m.get("certifications")),
                         photo="img/team/%s.webp" % slug, linkedin=m.get("linkedin") or "", bio=bio, groups=groups))
    return team


MONTHS = {"fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
          "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]}


def build_posts():
    posts = {}
    for lang in LANGS:
        blog = load("blog.%s.json" % lang)
        for p in blog["posts"]:
            pid = p["url"].rstrip("/").rsplit("-", 1)[-1]
            dt = datetime.strptime(p["published_time"][:10], "%Y-%m-%d")
            date = ("%d %s %d" % (dt.day, MONTHS[lang][dt.month - 1], dt.year)) if lang == "fr" else ("%s %d, %d" % (MONTHS[lang][dt.month - 1], dt.day, dt.year))
            img = ("img/blog/post-%s.webp" % pid) if pid in BLOG_COVERS else None
            posts.setdefault(pid, {})[lang] = dict(title=p["title"].strip(), url=p["url"], date=date, iso=dt.strftime("%Y-%m-%d"),
                                                   category=p["category"]["name"], img=img)
    return posts


def make_images(allowed):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow not installed: images not regenerated (committed copies are used).")
        return
    src_root = os.path.join(DATA, "assets")
    dst_root = os.path.join(SITE, "assets", "img")
    jobs = list(IMAGES)
    for slug in TEAM_ORDER:
        jobs.append(("team/%s.webp" % slug, "team/%s.webp" % slug, 480, "portrait"))
    for pid in BLOG_COVERS:
        ext = "webp"
        jobs.append(("blog/post-%s-cover.%s" % (pid, ext), "blog/post-%s.webp" % pid, 800, "webp"))
    for src, dst, width, fmt in jobs:
        if src not in allowed:
            raise SystemExit("Image not listed in assets.json: " + src)
        s = os.path.join(src_root, src)
        d = os.path.join(dst_root, dst)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        if fmt == "copy":
            shutil.copyfile(s, d)
            continue
        im = Image.open(s)
        if fmt == "portrait":
            im = im.convert("RGB")
            w, h = im.size
            # 4:5 crop, centred horizontally, biased to the top (faces)
            tw = w
            th = int(w * 5 / 4)
            if th > h:
                th = h
                tw = int(h * 4 / 5)
            left = (w - tw) // 2
            im = im.crop((left, 0, left + tw, th))
            im = im.resize((width, int(width * 5 / 4)), Image.LANCZOS)
            im.save(d, "WEBP", quality=76, method=6)
            continue
        if width and im.width > width:
            im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
        if fmt == "webp":
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGBA")
            im.save(d, "WEBP", quality=78, method=6)
        else:
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGBA")
            im.save(d, "PNG", optimize=True)
    # Open Graph images (generated, brand colours)
    for lang, line2 in (("fr", "Intégrateur Odoo à Paris et Rabat"), ("en", "Odoo integrator in Paris and Rabat")):
        og = Image.new("RGB", (1200, 630), (5, 10, 28))
        px = og.load()
        for y in range(630):
            for x in range(0, 1200, 2):
                bx = max(0.0, 1 - ((x - 950) ** 2 + (y - 80) ** 2) / 260000)
                ox = max(0.0, 1 - ((x - 1150) ** 2 + (y - 600) ** 2) / 200000)
                r = int(5 + 0 * bx + 216 * ox * .45)
                g = int(10 + 71 * bx * .9 + 96 * ox * .45)
                b = int(28 + 187 * bx * .9 + 24 * ox * .45)
                px[x, y] = (min(r, 255), min(g, 255), min(b, 255))
                if x + 1 < 1200:
                    px[x + 1, y] = px[x, y]
        dr = ImageDraw.Draw(og)
        fonts = "C:/Windows/Fonts/"

        def font(name, size):
            for n in (name, "arialbd.ttf", "DejaVuSans-Bold.ttf"):
                try:
                    return ImageFont.truetype(os.path.join(fonts, n) if os.path.exists(os.path.join(fonts, n)) else n, size)
                except OSError:
                    continue
            return ImageFont.load_default()
        f_big = font("arialbd.ttf", 84)
        f_mid = font("arial.ttf", 40)
        f_chip = font("arialbd.ttf", 30)
        dr.rounded_rectangle((80, 120, 520, 180), radius=30, outline=(233, 196, 106), width=2, fill=(30, 24, 8))
        dr.text((110, 132), "Odoo Gold Partner", font=f_chip, fill=(243, 213, 138))
        dr.text((80, 230), "DarbTech", font=f_big, fill=(255, 255, 255))
        dr.text((80, 340), line2, font=f_mid, fill=(200, 210, 235))
        dr.text((80, 400), "2015 → 22/09/2026 Gold", font=f_mid, fill=(233, 196, 106))
        logo = Image.open(os.path.join(src_root, "brand/logo.png")).convert("RGBA")
        wl = Image.new("RGBA", logo.size, (255, 255, 255, 255))
        wl.putalpha(logo.split()[3])
        wl = wl.resize((316, 80))
        og.paste(wl, (80, 500), wl)
        og.save(os.path.join(dst_root, "og-%s.png" % lang), optimize=True)
    print("Images generated.")


def fr_typography(html):
    """French typography (QA fix): no-break space before : ; ? ! and inside guillemets, so the punctuation
    never starts a new line. Only touches text between tags, never <script>/<style> content or attributes."""
    parts = re.split(r"(<script\b.*?</script>|<style\b.*?</style>)", html, flags=re.S)

    def fix_text(m):
        t = m.group(1)
        t = re.sub(r" ([:;?!\u00bb])", "\u00a0\\1", t)
        t = t.replace("\u00ab ", "\u00ab\u00a0")
        return ">" + t + "<"
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r">([^<]+)<", fix_text, parts[i])
    return "".join(parts)


def write(rel, html):
    path = os.path.join(SITE, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)


def main():
    allowed = asset_index()
    if "--images" in sys.argv:
        make_images(allowed)
    data = {"posts": build_posts(), "team": {}, "partners": {}}
    for lang in LANGS:
        content = load("content.%s.json" % lang)
        data["team"][lang] = build_team(content, lang)
        data["partners"][lang] = {p["name"]: p for p in content["inventory"]["partners"]}
    count = 0
    for pid, fn in PAGES.items():
        for lang in LANGS:
            c = Ctx(pid, lang, data)
            r = fn(c)
            html = document(c, r["title"], r["desc"], r["body"], trail=r.get("trail"),
                            extra_jsonld=r.get("ld"), noindex=r.get("noindex", False))
            if lang == "fr":
                html = fr_typography(html)
            write(out_file(pid, lang), html)
            count += 1
    # sitemap + robots
    urls = []
    for pid in PAGES:
        if pid == "404":
            continue
        for lang in LANGS:
            alts = "".join('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (l, public_url(pid, l)) for l in LANGS)
            alts += '<xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % public_url(pid, "fr")
            urls.append("<url><loc>%s</loc>%s</url>" % (public_url(pid, lang), alts))
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
    write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE_URL)
    print("Rendered %d pages into %s" % (count, SITE))


if __name__ == "__main__":
    main()
