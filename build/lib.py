"""Shared engine for the DarbTech static site generator: routes, layout, components, icons.

Standard library only. Page content lives in pages.py; build.py orchestrates.
"""
import html
import json
import posixpath

SITE_URL = "https://www.darbtech.net"
FONTS_URL = ("https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700"
             "&family=Geist+Mono:wght@500&family=Instrument+Serif:ital@0;1&display=swap")
GOLD_DATE = {"fr": "22/09/2026", "en": "22/09/2026"}

# page id -> (FR directory, EN directory). "" = site root. A value ending in .html is a file.
ROUTES = {
    "home": ("", "en/"),
    "odoo": ("odoo/", "en/odoo/"),
    "odoo_impl": ("odoo/implementation/", "en/odoo/implementation/"),
    "odoo_migration": ("odoo/migration/", "en/odoo/migration/"),
    "odoo_custom": ("odoo/developpement-sur-mesure/", "en/odoo/custom-development/"),
    "odoo_integrations": ("odoo/integrations/", "en/odoo/integrations/"),
    "odoo_support": ("odoo/support-formation/", "en/odoo/support-training/"),
    "odoo_apps": ("odoo/applications/", "en/odoo/apps/"),
    "dev": ("developpement/", "en/development/"),
    "cases": ("references/", "en/case-studies/"),
    "case_puthod": ("references/puthod/", "en/case-studies/puthod/"),
    "case_cameleon": ("references/cameleon/", "en/case-studies/cameleon/"),
    "method": ("methode/", "en/approach/"),
    "about": ("a-propos/", "en/about/"),
    "team": ("a-propos/equipe/", "en/about/team/"),
    "careers": ("carrieres/", "en/careers/"),
    "contact": ("contact/", "en/contact/"),
    "legal": ("mentions-legales/", "en/legal-notice/"),
    "privacy": ("confidentialite/", "en/privacy/"),
    "terms": ("cgv/", "en/terms/"),
    "404": ("404.html", "en/404.html"),
}

BLOG_URL = {"fr": SITE_URL + "/blog", "en": SITE_URL + "/en/blog"}
LINKEDIN = "https://www.linkedin.com/company/darbtech/"
EMAIL = "bonjour@darbtech.net"
OFFICES = {
    "paris": {
        "entity": "DarbTech Labs",
        "city": {"fr": "Paris", "en": "Paris"},
        "country": {"fr": "France", "en": "France"},
        "street": "122 Av. Daumesnil",
        "postcode": "75012",
        "locality": "Paris",
        "phone": "+33 1 88 33 41 64",
        "tel": "+33188334164",
        "cc": "FR",
    },
    "rabat": {
        "entity": "DarbTech",
        "city": {"fr": "Rabat", "en": "Rabat"},
        "country": {"fr": "Maroc", "en": "Morocco"},
        "street": "Résidence Oum Kalthoum, Bd Hassan II, Agdal",
        "postcode": "10120",
        "locality": "Rabat",
        "phone": "+212 770 86 2295",
        "tel": "+212770862295",
        "cc": "MA",
    },
}


def esc(s):
    return html.escape(str(s), quote=True)


def out_file(page_id, lang):
    d = ROUTES[page_id][0 if lang == "fr" else 1]
    return d if d.endswith(".html") else d + "index.html"


def public_url(page_id, lang):
    d = ROUTES[page_id][0 if lang == "fr" else 1]
    return SITE_URL + "/" + d


class Ctx:
    """Per-page rendering context: language + relative link helpers."""

    def __init__(self, page_id, lang, data):
        self.page_id = page_id
        self.lang = lang
        self.data = data
        self.file = out_file(page_id, lang)
        self.dir = posixpath.dirname(self.file)

    @property
    def other(self):
        return "en" if self.lang == "fr" else "fr"

    def t(self, fr, en):
        return fr if self.lang == "fr" else en

    def rel(self, target_file):
        r = posixpath.relpath(target_file, self.dir or ".")
        return r

    def href(self, page_id, lang=None, anchor=None):
        h = self.rel(out_file(page_id, lang or self.lang))
        return h + ("#" + anchor if anchor else "")

    def asset(self, path):
        return self.rel("assets/" + path)


# ---------------------------------------------------------------------------
# Icons (24px grid, stroke = currentColor). Drawn for this site.
# ---------------------------------------------------------------------------
ICONS = {
    "arrow-right": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "arrow-up-right": '<path d="M7 17 17 7M8 7h9v9"/>',
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 13 9 5 9-5"/><path d="m3 17.5 9 5 9-5" opacity=".5"/>',
    "migrate": '<path d="M4 12a8 8 0 0 1 14-5.3L20 9"/><path d="M20 4v5h-5"/><path d="M20 12a8 8 0 0 1-14 5.3L4 15"/><path d="M4 20v-5h5"/>',
    "code": '<path d="m8 7-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>',
    "plug": '<path d="M9 2v6M15 2v6M6 8h12v4a6 6 0 0 1-12 0V8ZM12 18v4"/>',
    "lifebuoy": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="m5.6 5.6 3.6 3.6M14.8 14.8l3.6 3.6M18.4 5.6l-3.6 3.6M9.2 14.8l-3.6 3.6"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="3" width="7" height="7" rx="2"/><rect x="3" y="14" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/>',
    "phone-device": '<rect x="7" y="2" width="10" height="20" rx="2.5"/><path d="M11 18h2"/>',
    "cloud": '<path d="M7 18a5 5 0 1 1 .9-9.9A6 6 0 0 1 19 10a4 4 0 0 1-1 8H7Z"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "users": '<circle cx="9" cy="8" r="4"/><path d="M2 21a7 7 0 0 1 14 0M16 4a4 4 0 0 1 0 8M22 21a7 7 0 0 0-4.5-6.5"/>',
    "shield": '<path d="M12 3 20 6v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3Z"/><path d="m9 12 2 2 4-4"/>',
    "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2" fill="currentColor"/>',
    "infinity": '<path d="M7 8a4 4 0 1 0 0 8c3 0 7-8 10-8a4 4 0 1 1 0 8c-3 0-7-8-10-8Z"/>',
    "repeat": '<path d="m17 2 4 4-4 4"/><path d="M3 11V9a3 3 0 0 1 3-3h15"/><path d="m7 22-4-4 4-4"/><path d="M21 13v2a3 3 0 0 1-3 3H3"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6.2 6.2l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 1.9Z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2.5"/><path d="m22 7-10 6L2 7"/>',
    "pin": '<path d="M12 22s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12Z"/><circle cx="12" cy="10" r="2.5"/>',
    "linkedin": '<path fill="currentColor" stroke="none" d="M4 9h3.2v11H4V9Zm1.6-5a1.8 1.8 0 1 1 0 3.6 1.8 1.8 0 0 1 0-3.6ZM9.6 9h3.1v1.5c.5-.9 1.6-1.8 3.3-1.8 3.4 0 4 2.2 4 5V20h-3.2v-5.5c0-1.3 0-3-1.8-3s-2.1 1.4-2.1 2.9V20H9.6V9Z"/>',
    "chart": '<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 5-6"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "sliders": '<path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6"/>',
    "graduation": '<path d="M22 10 12 5 2 10l10 5 10-5Z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9l-3.8 3.8Z"/>',
    "sparkle": '<path fill="currentColor" stroke="none" d="M12 1.5c.5 4.9 2.6 8 9.5 10.5-6.9 2.5-9 5.6-9.5 10.5-.5-4.9-2.6-8-9.5-10.5C9.4 9.5 11.5 6.4 12 1.5Z"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2.5"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2.5"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/>',
    "database": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "tag": '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8Z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    "receipt": '<path d="M5 2h14v20l-3-2-2 2-2-2-2 2-2-2-3 2V2Z"/><path d="M9 7h6M9 11h6M9 15h4"/>',
    "box": '<path d="m21 8-9-5-9 5v8l9 5 9-5V8Z"/><path d="m3 8 9 5 9-5M12 13v8"/>',
    "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.7 12.4a2 2 0 0 0 2 1.6h7.6a2 2 0 0 0 2-1.6L21 7H6"/>',
    "factory": '<path d="M2 20V9l6 4V9l6 4V5h8v15H2Z"/><path d="M6 17h2M11 17h2M16 17h2"/>',
    "headset": '<path d="M3 14v-2a9 9 0 0 1 18 0v2"/><path d="M3 14h3v6H4a1 1 0 0 1-1-1v-5ZM21 14h-3v6h2a1 1 0 0 0 1-1v-5Z"/>',
    "kanban": '<rect x="3" y="3" width="18" height="18" rx="2.5"/><path d="M8 7v7M12 7v4M16 7v10"/>',
    "wallet": '<path d="M20 7H5a2 2 0 0 1 0-4h13v4"/><path d="M3 5v14a2 2 0 0 0 2 2h15V7"/><path d="M16 14h.01"/>',
    "user-plus": '<circle cx="9" cy="8" r="4"/><path d="M2 21a7 7 0 0 1 14 0M19 8v6M16 11h6"/>',
    "bag": '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4H6Z"/><path d="M3 6h18M16 10a4 4 0 0 1-8 0"/>',
    "monitor": '<rect x="2" y="3" width="20" height="14" rx="2.5"/><path d="M8 21h8M12 17v4"/>',
    "megaphone": '<path d="M3 11v2a1 1 0 0 0 1 1h3l5 4V6L7 10H4a1 1 0 0 0-1 1Z"/><path d="M16 9a4 4 0 0 1 0 6M19 6a8 8 0 0 1 0 12"/>',
    "card": '<rect x="2" y="5" width="20" height="14" rx="2.5"/><path d="M2 10h20M6 15h4"/>',
    "mic": '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v4"/>',
    "server": '<rect x="3" y="3" width="18" height="7" rx="2"/><rect x="3" y="14" width="18" height="7" rx="2"/><path d="M7 6.5h.01M7 17.5h.01"/>',
    "flow": '<rect x="3" y="3" width="6" height="6" rx="1.5"/><rect x="15" y="15" width="6" height="6" rx="1.5"/><path d="M6 9v3a3 3 0 0 0 3 3h6"/>',
    "book": '<path d="M4 19.5V5a2 2 0 0 1 2-2h14v16H6.5A2.5 2.5 0 0 0 4 21.5v-2Z"/><path d="M8 7h8"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "heart": '<path d="M12 21s-8-5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 6-8 11-8 11Z"/>',
    "coffee": '<path d="M4 8h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5V8ZM17 9h1.5a2.5 2.5 0 0 1 0 5H17M7 2v3M11 2v3"/>',
    "dumbbell": '<path d="M6 7v10M18 7v10M3 10v4M21 10v4M6 12h12"/>',
    "home": '<path d="M3 11 12 3l9 8v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1v-9Z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6Z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 4 13c0-6 6-10 16-10 0 10-4 16-10 16"/><path d="M4 21c3-5 6-8 11-11"/>',
    "star": '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9L12 3Z"/>',
}


def icon(name, cls=""):
    body = ICONS[name]
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{body}</svg>')


# ---------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------
def gold_chip(c, variant="", meta=True, tag="span", href=None):
    cls = "gold-chip" + (" gold-chip--" + variant if variant else "")
    if variant == "sm-light":
        cls = "gold-chip gold-chip--light gold-chip--sm"
    m = (f'<span class="gold-chip__meta">{c.t("depuis 09/2026", "since 09/2026")}</span>' if meta else "")
    inner = (icon("sparkle", "gold-chip__icon")
             + '<span class="gold-chip__label">Odoo Gold Partner</span>' + m)
    if href:
        return f'<a class="{cls}" href="{href}">{inner}</a>'
    return f'<{tag} class="{cls}">{inner}</{tag}>'


def btn(href, label, variant="primary", arrow=True, extra="", magnetic=False):
    mag = " data-magnetic" if magnetic else ""
    a = icon("arrow-right") if arrow else ""
    return f'<a class="btn btn--{variant}" href="{href}"{mag}{extra}>{label}{a}</a>'


def eyebrow(text, light=False):
    return f'<span class="eyebrow{" eyebrow--light" if light else ""}">{text}</span>'


def section_head(eyebrow_text, title, lead=None, center=False, light=False, level=2, extra_cls=""):
    cls = "section-head" + (" section-head--center" if center else "") + (" " + extra_cls if extra_cls else "")
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    eb = eyebrow(eyebrow_text, light) if eyebrow_text else ""
    return (f'<div class="{cls}" data-reveal>{eb}<h{level}>{title}</h{level}>{lead_html}</div>')


def checklist(items, cls="", ic="check"):
    lis = "".join(f'<li>{icon(ic)}<span>{i}</span></li>' for i in items)
    return f'<ul class="checklist {cls}">{lis}</ul>'


def tags(items, variant=""):
    v = f" tag--{variant}" if variant else ""
    return '<ul class="tags">' + "".join(f'<li class="tag{v}">{esc(i)}</li>' for i in items) + "</ul>"


def faq(items):
    out = []
    for q, a in items:
        out.append(f'<details><summary>{q}{icon("plus")}</summary><div class="faq__answer"><p>{a}</p></div></details>')
    return '<div class="faq" data-reveal>' + "".join(out) + "</div>"


def placeholder(c, label=None, text=None):
    label = label or c.t("[Témoignage à collecter]", "[Testimonial to collect]")
    text = text or c.t("Emplacement réservé à une citation client validée. Aucun témoignage n'est inventé.",
                       "Reserved for an approved client quote. No testimonial has been made up.")
    return f'<div class="placeholder-slot" data-reveal><strong>{label}</strong><span>{text}</span></div>'


def hero_bg(canvas=False, grid=True):
    cv = '<canvas class="hero__canvas" aria-hidden="true"></canvas>' if canvas else ""
    g = '<div class="bg-grid"></div>' if grid else ""
    return ('<div class="hero__bg" aria-hidden="true"><div class="mesh">'
            '<span class="mesh__blob mesh__blob--1"></span><span class="mesh__blob mesh__blob--2"></span>'
            '<span class="mesh__blob mesh__blob--3"></span><span class="mesh__blob mesh__blob--4"></span></div>'
            f'{g}<div class="hero__noise"></div>{cv}<div class="hero__fade"></div></div>')


def breadcrumbs(c, trail):
    """trail: list of (label, page_id or None)."""
    items = [f'<li><a href="{c.href("home")}">{c.t("Accueil", "Home")}</a></li>']
    for label, pid in trail:
        if pid and pid != c.page_id:
            items.append(f'<li><a href="{c.href(pid)}">{label}</a></li>')
        else:
            items.append(f'<li><span aria-current="page">{label}</span></li>')
    return f'<nav class="breadcrumbs" aria-label="{c.t("Fil d’Ariane", "Breadcrumb")}"><ol>{"".join(items)}</ol></nav>'


def page_hero(c, trail, eyebrow_text, title, lead, ctas="", aside="", chip=False):
    chip_html = gold_chip(c) if chip else ""
    eb = eyebrow(eyebrow_text, True) if eyebrow_text else ""
    has_aside = " has-aside" if aside else ""
    aside_html = f'<div class="page-hero__aside" aria-hidden="true">{aside}</div>' if aside else ""
    return (f'<section class="hero page-hero">{hero_bg()}<div class="container page-hero__inner{has_aside}">'
            f'<div class="page-hero__content">{breadcrumbs(c, trail)}{chip_html}{eb}'
            f'<h1 data-split>{title}</h1><p class="lead">{lead}</p>'
            f'{"<div class=hero__ctas>" + ctas + "</div>" if ctas else ""}</div>{aside_html}</div></section>')


def hero_tile(name):
    return f'<div class="hero-tile">{icon(name)}</div>'


def cta_band(c, title=None, text=None):
    title = title or c.t('Parlons de votre <span class="accent accent--gold">projet Odoo</span>',
                         'Let’s talk about your <span class="accent accent--gold">Odoo project</span>')
    text = text or c.t("Un consultant certifié vous rappelle pour comprendre vos enjeux, sans engagement. "
                       "Nos équipes travaillent depuis Paris et Rabat.",
                       "A certified consultant will call you back to understand your needs, with no commitment. "
                       "Our teams work from Paris and Rabat.")
    p, r = OFFICES["paris"], OFFICES["rabat"]
    return (f'<section class="section section--tight" aria-labelledby="cta-title"><div class="container">'
            f'<div class="cta-band" data-reveal="scale"><div class="bg-grid"></div><div class="cta-band__inner">'
            f'<div><h2 id="cta-title">{title}</h2><p>{text}</p></div>'
            f'<div class="cta-band__actions">'
            f'{btn(c.href("contact"), c.t("Parler à un expert", "Talk to an expert"), "primary", magnetic=True)}'
            f'<div class="cta-band__phones"><span>Paris <a href="tel:{p["tel"]}">{p["phone"]}</a></span>'
            f'<span>Rabat <a href="tel:{r["tel"]}">{r["phone"]}</a></span></div>'
            f'</div></div></div></div></section>')


def post_card(c, post, i=0):
    img = (f'<div class="post-card__media"><img src="{c.asset(post["img"])}" alt="" loading="lazy" '
           f'decoding="async" width="800" height="500"></div>') if post.get("img") else ""
    return (f'<a class="post-card" href="{esc(post["url"])}" data-reveal style="--i:{i}">{img}'
            f'<div class="post-card__body"><div class="post-card__meta"><span>{esc(post["category"])}</span>'
            f'<span aria-hidden="true">·</span><time datetime="{post["iso"]}">{esc(post["date"])}</time></div>'
            f'<h3 class="post-card__title">{esc(post["title"])}</h3></div>'
            f'<span class="post-card__ext">{c.t("Lire sur le blog", "Read on the blog")}{icon("arrow-up-right")}'
            f'<span class="visually-hidden"> {c.t("(site darbtech.net)", "(darbtech.net website)")}</span></span></a>')


# ---------------------------------------------------------------------------
# Navigation data
# ---------------------------------------------------------------------------
def odoo_menu(c):
    return [
        ("odoo_impl", "layers", c.t("Implémentation", "Implementation"),
         c.t("Déployer Odoo, de l’analyse au go-live", "Roll out Odoo, from analysis to go-live")),
        ("odoo_migration", "migrate", c.t("Migration", "Migration"),
         c.t("Passer à la dernière version, de la V8 à aujourd’hui", "Upgrade to the latest version, from V8 onwards")),
        ("odoo_custom", "code", c.t("Développement sur mesure", "Custom development"),
         c.t("Modules spécifiques, rapports, automatisations", "Custom modules, reports, automations")),
        ("odoo_integrations", "plug", c.t("Intégrations", "Integrations"),
         c.t("Téléphonie Ringover, IA Leexi, API métiers", "Ringover telephony, Leexi AI, business APIs")),
        ("odoo_support", "lifebuoy", c.t("Support & formation", "Support & training"),
         c.t("Former vos équipes et faire évoluer l’outil", "Train your teams and keep Odoo evolving")),
        ("odoo_apps", "grid", c.t("Applications Odoo", "Odoo apps"),
         c.t("CRM, ventes, stock, compta, MRP, RH…", "CRM, sales, inventory, accounting, MRP, HR…")),
    ]


def about_menu(c):
    return [
        ("about", "users", c.t("À propos", "About us"), c.t("Notre histoire, nos valeurs, nos partenaires", "Our story, values and partners")),
        ("team", "star", c.t("L’équipe", "Team"), c.t("21 experts entre Paris et Rabat", "21 experts in Paris and Rabat")),
        ("careers", "briefcase", c.t("Carrières", "Careers"), c.t("7 postes ouverts à Rabat", "7 open roles in Rabat")),
    ]


def header(c):
    cur = c.page_id
    odoo_ids = {"odoo", "odoo_impl", "odoo_migration", "odoo_custom", "odoo_integrations", "odoo_support", "odoo_apps"}
    about_ids = {"about", "team", "careers"}
    case_ids = {"cases", "case_puthod", "case_cameleon"}

    def aria(pid, group=None):
        if (group and cur in group) or cur == pid:
            return ' aria-current="page"'
        return ""

    odoo_items = "".join(
        f'<li><a class="dropdown__link" href="{c.href(pid)}"{aria(pid)}><span class="dropdown__icon">{icon(ic)}</span>'
        f'<span><span class="dropdown__title">{t}</span><span class="dropdown__desc">{d}</span></span></a></li>'
        for pid, ic, t, d in odoo_menu(c))
    about_items = "".join(
        f'<li><a class="dropdown__link" href="{c.href(pid)}"{aria(pid)}><span class="dropdown__icon">{icon(ic)}</span>'
        f'<span><span class="dropdown__title">{t}</span><span class="dropdown__desc">{d}</span></span></a></li>'
        for pid, ic, t, d in about_menu(c))
    about_items += (f'<li><a class="dropdown__link" href="{BLOG_URL[c.lang]}"><span class="dropdown__icon">{icon("book")}</span>'
                    f'<span><span class="dropdown__title">Blog {icon("arrow-up-right", "ext-ic")}</span>'
                    f'<span class="dropdown__desc">{c.t("Articles Odoo, IA et gestion", "Articles on Odoo, AI and management")}</span></span></a></li>')

    mega_aside = (f'<div class="dropdown__aside">{gold_chip(c, meta=False)}'
                  f'<div><strong>{c.t("Partenaire Odoo depuis 2015, Gold depuis le 22/09/2026", "Odoo partner since 2015, Gold since 22/09/2026")}</strong>'
                  f'<p>{c.t("Toutes nos équipes de conseil et de développement sont certifiées Odoo.", "All our consulting and development staff are Odoo-certified.")}</p></div>'
                  f'<a class="link-arrow" href="{c.href("odoo")}">{c.t("Vue d’ensemble Odoo", "Odoo overview")}{icon("arrow-right")}</a></div>')

    nav = (f'<nav class="nav" aria-label="{c.t("Navigation principale", "Main navigation")}"><ul class="nav__list">'
           f'<li class="nav__item" data-dropdown><button class="nav__trigger{" is-current" if cur in odoo_ids else ""}" type="button" aria-expanded="false" aria-controls="dd-odoo">Odoo{icon("chevron-down")}</button>'
           f'<div class="dropdown dropdown--mega" id="dd-odoo"><ul class="dropdown__list">{odoo_items}</ul>{mega_aside}</div></li>'
           f'<li class="nav__item"><a class="nav__link" href="{c.href("dev")}"{aria("dev")}>{c.t("Développement", "Development")}</a></li>'
           f'<li class="nav__item"><a class="nav__link" href="{c.href("cases")}"{aria("cases", case_ids)}>{c.t("Références", "Case studies")}</a></li>'
           f'<li class="nav__item"><a class="nav__link" href="{c.href("method")}"{aria("method")}>{c.t("Méthode", "Approach")}</a></li>'
           f'<li class="nav__item" data-dropdown><button class="nav__trigger{" is-current" if cur in about_ids else ""}" type="button" aria-expanded="false" aria-controls="dd-about">{c.t("À propos", "About")}{icon("chevron-down")}</button>'
           f'<div class="dropdown" id="dd-about"><ul class="dropdown__list">{about_items}</ul></div></li>'
           f'</ul></nav>')

    lang_switch = (f'<div class="lang-switch" role="group" aria-label="{c.t("Langue", "Language")}">'
                   + (f'<span aria-current="true" lang="fr">FR</span><a href="{c.href(cur, "en")}" hreflang="en" lang="en" aria-label="English version">EN</a>'
                      if c.lang == "fr" else
                      f'<a href="{c.href(cur, "fr")}" hreflang="fr" lang="fr" aria-label="Version française">FR</a><span aria-current="true" lang="en">EN</span>')
                   + '</div>')

    # Mobile nav
    i = 0

    def mi(content):
        nonlocal i
        i += 1
        return f'<li class="mobile-nav__item" style="--i:{i}">{content}</li>'

    m_odoo = "".join(mi(f'<a href="{c.href(pid)}"{aria(pid)}>{t}</a>') for pid, ic, t, d in odoo_menu(c))
    m_main = "".join(mi(f'<a href="{c.href(pid)}"{aria(pid)}>{t}</a>') for pid, t in [
        ("home", c.t("Accueil", "Home")), ("odoo", c.t("Odoo : vue d’ensemble", "Odoo overview")),
        ("dev", c.t("Développement", "Development")), ("cases", c.t("Références", "Case studies")),
        ("method", c.t("Méthode", "Approach"))])
    m_about = "".join(mi(f'<a href="{c.href(pid)}"{aria(pid)}>{t}</a>') for pid, ic, t, d in about_menu(c))
    m_about += mi(f'<a href="{BLOG_URL[c.lang]}">Blog ↗</a>')
    mobile = (f'<div class="mobile-nav" id="mobile-nav" aria-hidden="true">'
              f'<nav aria-label="{c.t("Navigation mobile", "Mobile navigation")}">'
              f'<div class="mobile-nav__group"><ul>{m_main}</ul></div>'
              f'<div class="mobile-nav__group mobile-nav__sub"><p class="mobile-nav__label">{c.t("Services Odoo", "Odoo services")}</p><ul>{m_odoo}</ul></div>'
              f'<div class="mobile-nav__group mobile-nav__sub"><p class="mobile-nav__label">{c.t("Entreprise", "Company")}</p><ul>{m_about}</ul></div>'
              f'<div class="mobile-nav__foot">{gold_chip(c)}'
              f'{btn(c.href("contact"), c.t("Parler à un expert", "Talk to an expert"), "primary")}'
              f'<a class="btn btn--ghost" href="tel:{OFFICES["paris"]["tel"]}">{icon("phone")}{OFFICES["paris"]["phone"]}</a>'
              f'</div></nav></div>')

    return (f'<header class="site-header"><div class="container"><div class="site-header__bar">'
            f'<a class="brand" href="{c.href("home")}" aria-label="{c.t("DarbTech, accueil", "DarbTech, home")}">'
            f'<img src="{c.asset("img/brand/logo.png")}" alt="DarbTech" width="150" height="38"></a>'
            f'{nav}<div class="header-actions">{gold_chip(c, "light", meta=False, href=c.href("odoo"))}{lang_switch}'
            f'<a class="btn btn--primary btn--sm header-cta" href="{c.href("contact")}"{aria("contact")}>{c.t("Parler à un expert", "Talk to an expert")}</a>'
            f'<button class="burger" type="button" aria-expanded="false" aria-controls="mobile-nav" '
            f'aria-label="{c.t("Ouvrir le menu", "Open menu")}" data-open="{c.t("Ouvrir le menu", "Open menu")}" data-close="{c.t("Fermer le menu", "Close menu")}"><span></span></button>'
            f'</div></div></div></header>{mobile}')


def footer(c):
    p, r = OFFICES["paris"], OFFICES["rabat"]
    odoo_links = "".join(f'<li><a href="{c.href(pid)}">{t}</a></li>' for pid, ic, t, d in odoo_menu(c))
    company = [("about", c.t("À propos", "About us")), ("team", c.t("L’équipe", "Team")),
               ("method", c.t("Méthode", "Approach")), ("cases", c.t("Références", "Case studies")),
               ("dev", c.t("Développement", "Development")), ("careers", c.t("Carrières", "Careers"))]
    company_links = "".join(f'<li><a href="{c.href(pid)}">{t}</a></li>' for pid, t in company)
    company_links += f'<li><a href="{BLOG_URL[c.lang]}">Blog ↗</a></li>'

    def office(o):
        return (f'<address class="footer__office"><strong>{o["entity"]} · {o["city"][c.lang]}</strong>'
                f'<span>{o["street"]}, {o["postcode"]} {o["locality"]}, {o["country"][c.lang]}</span>'
                f'<a href="tel:{o["tel"]}">{o["phone"]}</a></address>')

    legal = [("legal", c.t("Mentions légales", "Legal notice")), ("privacy", c.t("Confidentialité", "Privacy")),
             ("terms", c.t("CGV", "Terms of sale"))]
    legal_links = "".join(f'<li><a href="{c.href(pid)}">{t}</a></li>' for pid, t in legal)
    return (f'<footer class="site-footer on-dark"><div class="container">'
            f'<div class="footer__top">'
            f'<div class="footer__brand"><img src="{c.asset("img/brand/logo.png")}" alt="DarbTech" width="158" height="40" loading="lazy">'
            f'<p>{c.t("Intégrateur et partenaire Odoo depuis 2015. Conseil, intégration et développement pour les PME et ETI, depuis Paris et Rabat.", "Odoo integrator and partner since 2015. Consulting, implementation and development for SMEs and mid-market companies, from Paris and Rabat.")}</p>'
            f'{gold_chip(c)}</div>'
            f'<div class="footer__col"><h2>Odoo</h2><ul><li><a href="{c.href("odoo")}">{c.t("Vue d’ensemble", "Overview")}</a></li>{odoo_links}</ul></div>'
            f'<div class="footer__col"><h2>{c.t("Entreprise", "Company")}</h2><ul>{company_links}</ul></div>'
            f'<div class="footer__col"><h2>{c.t("Contact", "Contact")}</h2>{office(p)}{office(r)}'
            f'<p style="margin-top:18px"><a href="mailto:{EMAIL}">{EMAIL}</a></p>'
            f'<p style="margin-top:6px"><a href="{c.href("contact")}">{c.t("Formulaire de contact", "Contact form")} →</a></p></div>'
            f'</div>'
            f'<div class="footer__bottom"><span>© <span data-year>2026</span> DarbTech Labs SAS · DarbTech SARL</span>'
            f'<ul class="footer__legal">{legal_links}</ul>'
            f'<a class="footer__social" href="{LINKEDIN}" rel="noopener" target="_blank">{icon("linkedin")}LinkedIn<span class="visually-hidden"> {c.t("(nouvel onglet)", "(new tab)")}</span></a>'
            f'</div></div><div class="footer__word" aria-hidden="true">DarbTech</div></footer>')


# ---------------------------------------------------------------------------
# Document shell
# ---------------------------------------------------------------------------
def org_jsonld():
    addr = []
    contacts = []
    for o in OFFICES.values():
        addr.append({"@type": "PostalAddress", "streetAddress": o["street"], "postalCode": o["postcode"],
                     "addressLocality": o["locality"], "addressCountry": o["cc"]})
        contacts.append({"@type": "ContactPoint", "telephone": o["phone"], "contactType": "sales",
                         "areaServed": o["cc"], "availableLanguage": ["French", "English"]})
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": SITE_URL + "/#organization",
        "name": "DarbTech",
        "legalName": "DarbTech Labs SAS",
        "url": SITE_URL + "/",
        "logo": SITE_URL + "/assets/img/brand/logo.png",
        "email": EMAIL,
        "sameAs": [LINKEDIN],
        "address": addr,
        "contactPoint": contacts,
        "numberOfEmployees": {"@type": "QuantitativeValue", "value": 21},
        "knowsAbout": ["Odoo", "ERP", "CRM", "Odoo implementation", "Odoo migration", "Custom software development"],
        "description": "Odoo Gold Partner (since 22/09/2026) and Odoo partner since 2015, with offices in Paris and Rabat.",
        "vatID": "FR48850857046",
    }


def breadcrumb_jsonld(c, trail):
    items = [{"@type": "ListItem", "position": 1, "name": c.t("Accueil", "Home"), "item": public_url("home", c.lang)}]
    for n, (label, pid) in enumerate(trail, start=2):
        pid = pid or c.page_id
        items.append({"@type": "ListItem", "position": n, "name": html.unescape(label), "item": public_url(pid, c.lang)})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def document(c, title, description, body, trail=None, extra_jsonld=None, noindex=False):
    fr_url, en_url = public_url(c.page_id, "fr"), public_url(c.page_id, "en")
    canonical = fr_url if c.lang == "fr" else en_url
    og_locale, og_alt = ("fr_FR", "en_US") if c.lang == "fr" else ("en_US", "fr_FR")
    ld = [org_jsonld()]
    if trail:
        ld.append(breadcrumb_jsonld(c, trail))
    if extra_jsonld:
        ld.extend(extra_jsonld)
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    base_fix = ""
    if c.page_id == "404":
        # On a web server the 404 page is served at arbitrary depths: pin relative URLs to its real folder.
        # GitHub Pages project sites live under /<repo>/, so keep that first path segment as the root.
        base_fix = ('<script>if(/^https?:$/.test(location.protocol)){var r="/",s=location.pathname.split("/")[1];'
                    'if(/\\.github\\.io$/.test(location.hostname)&&s)r="/"+s+"/";'
                    'document.write(\'<base href="\'+r+\'' + ("en/" if c.lang == "en" else "") + '">\')}</script>')
    return f"""<!doctype html>
<html lang="{c.lang}">
<head>
<meta charset="utf-8">
{base_fix}<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
{robots}<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="fr" href="{fr_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{fr_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DarbTech">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}/assets/img/og-{c.lang}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{og_locale}">
<meta property="og:locale:alternate" content="{og_alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#050A1C">
<link rel="icon" href="{c.asset("img/brand/favicon.ico")}" sizes="any">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS_URL}">
<link rel="stylesheet" href="{c.asset("css/styles.css")}">
<script>document.documentElement.classList.add('js');setTimeout(function(){{if(!window.__dtReady)document.documentElement.classList.remove('js')}},3500)</script>
<script src="{c.asset("js/main.js")}" defer></script>
{ld_html}
</head>
<body>
<a class="skip-link" href="#main">{c.t("Aller au contenu", "Skip to content")}</a>
{header(c)}
<main id="main" tabindex="-1">
{body}
</main>
{footer(c)}
</body>
</html>
"""
