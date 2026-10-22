# DarbTech content scrape: notes

Source: https://www.darbtech.net (Odoo website). Scraped on 2026-10-22.
French is the default language and has no URL prefix. English is served under `/en/`.
French pages were fetched with the cookie `frontend_lang=fr_FR`; without it the server redirects to `/en/`.

## Files

| File | What it holds |
|---|---|
| `content.fr.json` / `content.en.json` | `site` (nav, header phone + CTA, languages, logo, favicon, footer), `pages` (page key → meta + `sections[]` → `blocks[]`), `page_aliases` (redirecting URLs), `inventory` (services, clients, client cases, team, partners, certifications, stats, contact, forms, jobs), `blog_index` |
| `blog.fr.json` / `blog.en.json` | All 53 articles with full body blocks, date, author, category, cover |
| `assets.json` | Manifest of the 77 kept image references (73 unique files): `local_path`, `original_url`, `alt` per language, `used_in`. `not_downloaded` lists the skipped URLs, grouped by reason |
| `assets/` | `brand/`, `clients/`, `partners/`, `team/`, `pages/`, `blog/` |
| `raw/fr/*.html`, `raw/en/*.html` | Raw HTML (untrusted data), `raw/pages.json` = fetch index, `raw/sitemap.xml` |
| `scripts/fetch.py`, `scripts/extract.py` | Reproduce the scrape (see the end of this file) |

### Block model (for rendering)
- `heading` {level, text}
- `text` {text, links?}: the text can contain `\n` where the source used `<br>`.
- `list` {ordered, items[{text, links?}]}
- `link` {text, href, path?, button?, new_tab?}: `path` is the language-neutral internal path; `button: true` marks an Odoo `.btn` CTA.
- `image` / `background_image` {src, alt, asset?, decorative_or_placeholder?}: `asset` is the local file. `decorative_or_placeholder` marks Odoo theme shapes and stock placeholders, which should not be reused.
- `"_missing": true, "_text_lang": "fr"|"en"`: the live site shows this text in the other language because the Odoo translation is missing. The text kept is the text the site actually displays.
- Page-level `translation` gives counts; `meta_fields_in_other_language` flags an untranslated title or description. A page or post where more than half of the blocks are untranslated gets `"_missing": true`.
- The language detection is a stop-word heuristic, so short labels such as "CGU" or "Cas Clients" cannot be classified. A few false positives are possible, e.g. "Maintenance prédictive (industrie, IT)".

## Pages scraped (identical set in FR and EN: 53 pages + 53 blog posts per language)

- **Core:** `/` (home), `/services`, `/devops`, `/integrateurdelogiciel` (Software integrator), `/prqdarbodoo` (Why DarbTech / Why Odoo), `/aboutus` (About + team + partners), `/contactus`, `/cgu` (legal notice / terms of use), `/terms` (standard terms of sale)
- **Team bios (21):** abdellatif, anis, douae, elmehdi, fatima-zahra, fred, frederic, hatim, hosni, kamal, khadija-a, khadija-r, maria, marwa, mohammed, ouail, sally, salma, thomas, viet, zoubida
- **Jobs:** `/jobs` + 7 job pages (`/jobs/<slug>`) + 7 application forms (`/jobs/apply/<slug>`)
- **Blog:** `/blog` + category pages (tech-odoo-3, cas-clients-4, gestion-d-entreprise-1, actualites-5, success-stories-6) + 53 articles
- **Odoo default / empty:** `/appointment` ("Il n'y a actuellement aucun rendez-vous disponible"), `/shop` ("Aucun produit défini")
- **Aliases (redirects):** `/calendar` → `/appointment`; `/jobs/detail/<slug>` → `/jobs/<slug>`; `/blog/cas-client-4` (used in the main nav) → `/blog/cas-clients-4`
- **Not scraped:** blog RSS feeds, `/shop/cart`, `/website/info`. Pagination of blog listings was also skipped, because every article is fetched directly from the sitemap.

## Content inventory (summary; full data in `inventory`)

- **Services:**
  - **ERP and CRM** (Odoo): ERP project implementation with Odoo
  - **DevOps**
  - **Development:** full stack web development, SaaS software development (JavaScript | PHP | Python...), mobile apps (iOS & Android), web services, web apps
  - **Software integrator / "Editeur de logiciel"** (CRM and ERP pages)
  - **Offshoring** ("Excellence dans l'Offshoring")
  - **CRM benefit blocks:** "Boostez votre croissance", "Gagnez en productivité", "Pilotez vos équipes commerciales", and others
  - **Method on `/prqdarbodoo`:** 1. study and analysis, 2. adaptation, 3. module implementation, 4. training, 5. maintenance
  - **About-page methodology:** DevOps, Agile-Scrum, Transparence, Engagement
- **Odoo apps and topics mentioned:** CRM, ERP, MRP/manufacturing, Helpdesk, Planning, Sales, Purchase, Inventory, Accounting, Invoicing, HR, Payroll, eCommerce, Website, Project, Marketing automation, Recruitment, CTI, PoS. `inventory.odoo_apps_and_topics_mentioned` lists them with the pages and blog-post counts.
- **Client logos** (services page, no alt text): netiwan GROUPE, CMT GROUP, PUTHOD PÉPINIÈRES, L'AMBASSADE DES LANGUES PARIS, ACSP Conseil, tionis. The names were read off the logos (`text_visible_in_logo`) because the file names are vague.
- **Named client cases (blog "Cas Clients"):**
  - PUTHOD (landscaping, Pays de Savoie): business-process digitalisation, ERP Odoo
  - CAMELEON (events, Pays de Savoie): CRM lead and offer tracking
  - The category also holds an AI-method article and "Applicatifs d'Odoo dans la digitalisation des PME" (ten generic industry examples, not DarbTech clients).
  - The services-page masonry block also lists "Planning odoo – Gestion et suivi du planning de production et fabrication", but its "En savoir plus" link goes to the generic blog category.
- **Partners** (about page): Odoo ("Partenaire Certifié Odoo depuis 2015"), Ringover (CTI, SVI, analytics, collaborative tools), Leexi.ai (AI meeting notes, native Odoo integration, GDPR compliant, ISO 27001)
- **Certifications on team cards:** Odoo (most members), ISTQB (Anis), RingOver, LSS, SAFe, CSPO (Fred)
- **Stats and figures:** none presented as a stats block. The only figures in the copy:
  - Odoo partner "depuis 2015"
  - "près d'une décennie", "de la V8 aux dernières éditions"
  - The DevOps page smartphone stats (150 checks a day, 46 apps installed, 19 used)
  - Team size, implied: 21 profiles on `/aboutus`
- **Testimonials:** none on the site.
- **Team (21):**
  - Viet (CEO & Fondateur)
  - Fred (Directeur Associé Consulting & Production)
  - Thomas and Kamal (Directeurs de Projets)
  - Maria, Frédéric (consultants)
  - Marwa (admin & commercial)
  - Anis (QA)
  - Hosni (Senior Odoo dev)
  - Abdellatif (Lead dev)
  - Zoubida (tech solutions manager)
  - Fatima Zahra, Khadija R., Mohammed, Salma (confirmed ERP engineers)
  - Khadija A., Hatim, Ouail, El Mehdi, Douae, Salma ("sally") (junior ERP engineers)
  - Each profile has a bio (3–6 paragraphs) and a LinkedIn link.
- **Contact:**
  - **Paris:** DarbTech Labs, 122 Av. Daumesnil, 75012 Paris, +33 1 88 33 41 64 (also the phone in the header)
  - **Rabat:** DarbTech, Résidence Oum Kalthoum, Boulevard Hassan II, Agdal, 10120 Rabat. The contact page gives +212 5 22 58 48 26 and the footer gives +212 770 86 2295.
  - **Emails:** rh@darbtech.net (jobs), bonjour@darbtech.net and dpo@darbtech.net (CGU), plus one email per job ad.
  - **Social:** LinkedIn https://www.linkedin.com/company/darbtech/
  - **Contact form** (`crm.lead`): name, company, position, phone, email, request type (Commercial / Support Technique / Emploi), "when to call" select, subject, question
  - **Job application form** (`hr.applicant`): name, email, phone, LinkedIn, CV, introduction
- **Legal** (CGU): DarbTech Labs SAS, share capital €10,000, RCS Paris 850 857 046, VAT FR 48 850 857 046, registered office 36 rue Boussingault 75013 Paris. The `/terms` page names "DarbTech SARL" under Moroccan law.
- **Brand:** the logo PNG (`assets/brand/logo.png`) contains the tagline "Solutions for a digitalised world". The theme accent colour in the Odoo shapes is #0047BB.

## Gaps and inconsistencies to resolve before reuse

1. **Untranslated EN content:**
   - The EN homepage `<title>` and meta description are in French.
   - All 7 job descriptions are French on `/en/` (titles are translated); the `/en/jobs` listing shows 18 French blocks.
   - CGU has 3 French paragraphs inside the English text.
   - Also French on `/en/`: one DevOps paragraph, the `/prqdarbodoo` "Rejoignez-nous!" CTA, the services "Quelques exemples…" line, Salma's card subtitle, the footer "Nos services" / "Cas Clients" / "CGU" labels, and 2 paragraphs of blog post 13.
2. **Untranslated FR content:** `/terms` is entirely in English on the French site.
3. **Address conflicts:**
   - Paris postcode: 75012 (FR contact page + footer) vs 75013 (EN contact page).
   - Registered office (CGU, 36 rue Boussingault 75013) differs from the contact address.
4. **Phone conflict:** two different Rabat numbers (see Contact).
5. **Email domains:** job emails are inconsistent. The `/jobs` listing uses `@darbtech.net`; the job pages use `@darbtech-labs.odoo.com` (and `adminops@darbtech-labs.com`).
6. **Broken or placeholder links:**
   - Services "ERP → PLUS DE DÉTAILS" points to `/erpodoo` (404).
   - Services "Cas clients → Plus de détails" points to `/cas-clients` (404).
   - The CRM "PLUS DE DÉTAILS" link is `#`, and so are the social icons on the team cards.
   - The Leexi logo links to liteconsulting.fr.
   - The nav uses `/blog/cas-client-4`, which redirects.
7. **Placeholder imagery:**
   - Odoo stock "library_image" pictures on the homepage "Découvrez nos derniers articles" wall (all linking to `/blog`)
   - Default snippet images: services three-column cards, `/prqdarbodoo` hero, `/integrateurdelogiciel` cover
   - The homepage has one empty `s_text_image` section.
8. **AI-generated imagery:** team photos (source file names "ChatGPT Image … mai 2026"), most blog covers (DALL·E). Check whether real photos are wanted.
9. **Empty features:** Appointment (no slots), Shop (no products), blog categories "Actualités" and "Success Stories" (no posts).
10. **Odoo defaults left on the site:**
    - "Powered by Odoo – The #1 Open Source eCommerce" footer badge
    - The job application button reads "J'ai de la chance" / "I'm feeling lucky"
    - Generic page titles such as "aboutUs | DarbTech", "PrqDarbOdoo | DarbTech", "IntégrateurDeLogiciel | DarbTech"
    - Most pages have no meta description.
11. **Odd meta keywords on the homepage:** "Facturation Electronique, Septembre 2026 - Sept - 09/26".
12. **Typos in the source** (kept verbatim): "Developpement", "particpations", "Cconformément", "Boulevard HassanII". Zero-width spaces were stripped.
13. **Duplicate articles:**
    - "Méthode infaillible … IA" appears twice (posts 70 in Cas Clients and 73 in Gestion d'entreprise).
    - Posts 56 and 57 are near-duplicate "Odoo … ERP champion … PME" articles.
14. **Blog body formatting:** about 12 older "Gestion d'entreprise" articles are single `<br>`-separated text blocks with no `<p>`/`<h>`. Their body comes out as 1 block with `\n` line breaks.

## Possibly outdated content

- "DarbTech, Partenaire Certifié Odoo depuis 2015 !" and "Depuis près d'une décennie…": superseded by the new partner level, which the design agent will handle.
- Blog: the latest post is dated 26 Feb 2026, and most posts date from January–August 2024. Several titles are dated: "Les 5 défis majeurs de 2024…", "Odoo V17…", "post-pandémique".
- The services page (sitemap lastmod 2024-01-29), `/integrateurdelogiciel` (2024-08) and `/devops` (2025-05) have not been updated recently. The team and about pages were updated in Sept–Oct 2026.
- The DevOps smartphone statistics have no source or date.
- Ringover, Leexi and Odoo partner texts: check that they are current.

## Assets

- **Downloaded:**
  - brand (logo, favicon)
  - 6 client logos
  - 3 partner logos (Odoo, Ringover, Leexi)
  - 21 team photos (from the about-page cards)
  - 30 page-image references, 26 unique files (home, services, devops, integrator, about, jobs incl. the Asilah team photo `asilahdt2023`)
  - 15 blog-cover references, 14 unique files (client cases + 12 latest, resized to 480 px by Odoo)
  - Odoo shape-masked SVG wrappers were unwrapped to their embedded raster.
- **Not downloaded** (listed in `assets.json → not_downloaded`): theme shapes, Odoo placeholders, flags, the Odoo badge, author avatars, inline blog images, team bio-page duplicates, and the covers of older blog posts (their URL stays in `blog.*.json`).
- **Stale files:** `data/assets/` still contains about 60 files from a first download pass that the manifest no longer references. They are full-size blog covers of up to 2.2 MB and team photos under older names such as `team/fred-fred.webp`. They could not be deleted automatically, so delete them by hand. Every file that `assets.json` does not reference is safe to remove.

## Re-running the scrape

```
cd data/scripts
python -I fetch.py        # raw HTML for FR + EN (≈230 requests, ~2 min)
python -I extract.py      # JSON + assets (downloads are cached in assets/.cache.json; --refresh ignores the cache, --no-assets skips network)
```
Both scripts use only the Python 3 standard library and resolve paths relative to their own folder.
