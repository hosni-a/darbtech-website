# DarbTech: redesign proposal (static site, FR/EN)

A static, bilingual redesign of darbtech.net, centred on the **Odoo Gold Partner** status (since 22/09/2026).
It is plain HTML, CSS and JS, with no framework and no build step needed to view it.

## Viewing the site

- **From disk:** open `site/index.html` (French) or `site/en/index.html` (English) in a browser. Every link is relative and points to an explicit `index.html`, so `file://` works.
- **Over HTTP:** run `python -m http.server 8000 --directory site`, then open http://localhost:8000/.

## Rebuilding

The pages are generated from the scraped data in `data/` by a Python script that uses only the standard library:

```
python build/build.py            # re-render all 42 pages, sitemap.xml and robots.txt
python build/build.py --images   # also regenerate optimised images and OG images (needs Pillow)
python build/check.py            # validate links, anchors, H1s, alt text, titles, hreflang and CSS+JS weight
```

| File | Role |
|---|---|
| `build/lib.py` | Routes (FR/EN slugs), relative-link helper, icons, header, footer, `<head>` (SEO, hreflang, OG, JSON-LD) |
| `build/pages_common.py` | Shared sections: Gold panel, 5-step method, values, apps catalogue, case data, logo marquee |
| `build/pages_main.py` | Home, Odoo hub, the 5 Odoo service pages, Apps |
| `build/pages_other.py` | Development, case studies, approach, about, team, careers, contact, legal pages, 404 |
| `site/assets/css/styles.css` | Design system: tokens as CSS custom properties, components, motion |
| `site/assets/js/main.js` | Interactions: header, menus, reveal, counters, particles, team modal, form demo |

The copy sits next to its translation in the page modules, for example `c.t("FR text", "EN text")`.
The generated HTML is committed, so editing the site does not require Python.

## Pages (21 per language)

| FR | EN |
|---|---|
| `/` | `/en/` |
| `/odoo/` | `/en/odoo/` |
| `/odoo/implementation/` | `/en/odoo/implementation/` |
| `/odoo/migration/` | `/en/odoo/migration/` |
| `/odoo/developpement-sur-mesure/` | `/en/odoo/custom-development/` |
| `/odoo/integrations/` | `/en/odoo/integrations/` |
| `/odoo/support-formation/` | `/en/odoo/support-training/` |
| `/odoo/applications/` | `/en/odoo/apps/` |
| `/developpement/` | `/en/development/` |
| `/references/` (+ `puthod/`, `cameleon/`) | `/en/case-studies/` (+ `puthod/`, `cameleon/`) |
| `/methode/` | `/en/approach/` |
| `/a-propos/`, `/a-propos/equipe/` | `/en/about/`, `/en/about/team/` |
| `/carrieres/` | `/en/careers/` |
| `/contact/` | `/en/contact/` |
| `/mentions-legales/`, `/confidentialite/`, `/cgv/` | `/en/legal-notice/`, `/en/privacy/`, `/en/terms/` |
| `/404.html` | `/en/404.html` |

There is no Industries page. Real content supports only two confirmed sectors (landscaping and events), short of the four required.
The blog stays on Odoo, so the Blog links and "Latest articles" cards point to the live darbtech.net posts.
Job openings link to the live Odoo `/jobs` pages.

## Design system

- **Palette:** DarbTech blue `#0047BB` and orange `#D86018` are the anchors. The orange is decorative only; buttons use `#B84E0E`, which gives 5.1:1 contrast with white. A gold scale (`#F3D58A` → `#B8862A`, with `#7A5812` for text on light backgrounds) marks the Gold identity. Hero and dark sections use a deep ink navy (`#050A1C`).
- **Type:** Geist for text and UI, Instrument Serif italic for accent words, Geist Mono for labels. All three load from Google Fonts.
- **Gold label:** a typographic "✦ Odoo Gold Partner · depuis 09/2026" chip with a shimmer. It is not a seal and does not use the Odoo logo. The scraped Odoo logo appears only in the About page's partners section.
- **Motion:** animated gradient mesh, a masked grid and a canvas particle network in the hero; an orbit of Odoo apps around a "Gold Partner" core; word-by-word headline reveal; scroll reveal; number counters; client logo marquee; card spotlight and lift; magnetic CTAs; a header that shrinks on scroll and hides on fast scroll; a scroll-linked 5-step timeline; a rotating gold border; page fade or cross-document View Transitions. Everything respects `prefers-reduced-motion`, and the canvas pauses when it is off-screen.

## Placeholders left visible on purpose

- `[Témoignage à collecter]` / `[Testimonial to collect]`: on the Home page and on both case study pages.
- `[Études de cas à rédiger]`: on the case studies index, for other clients.
- `[Offres de support à préciser…]`: on the Support & training page, and in its FAQ.
- Legal notice: `[À compléter]` for the publication director and the host, and for DarbTech SARL's legal identifiers (RC, ICE).
- Terms of sale: `[Entité contractante à confirmer…]` (DarbTech Labs SAS or DarbTech SARL).
- Privacy policy: the cookies and third-party note must be validated against the tools actually used.
- Apps page: the list is labelled as indicative. DarbTech should confirm which apps it actually delivers.

## Known limitations

- The contact form is a demo. It validates the fields and shows a success state but sends nothing. Connect it to Odoo (`/website/form/` with `crm.lead`) or another endpoint before launch.
- The images are the ones scraped from the old site. The team portraits are AI-generated, according to the audit, and the logo is a 475 px PNG. Ask DarbTech for real photos and an SVG logo.
- On a web server, `404.html` uses a tiny script that inserts `<base href="/">` (or `/en/`) so that its relative links work at any depth. This assumes the site is deployed at the domain root.
- Canonical, hreflang, OG and sitemap URLs assume production at `https://www.darbtech.net/` with the slugs above. The 301 redirects from the old URLs (ANALYSIS.md §6) still need to be set up on the host.
