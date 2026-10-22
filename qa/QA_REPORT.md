# DarbTech redesign: QA report

Audit date: 22/10/2026. Scope: the 42 generated pages (21 FR + 21 EN) in `site/`, the generator in `build/`, and `site/assets/` CSS and JS.
Tools used: `build/check.py`, my own crawler (links, anchors, srcset, language switcher, hreflang and canonical, JSON-LD parsing, heading order), curl, and headless Chrome 155 driven over CDP. The CDP driver captured screenshots, console errors, failed requests, keyboard tests and reduced-motion emulation.

## Verdict

**Ready to show the client: YES**, as a review prototype. All 42 pages render without JS errors or failed requests, over both `file://` and `python -m http.server`. Every internal link, anchor and language-switch pairing resolves. Responsive layouts hold from 390 px to 1440 px with no horizontal overflow. The design looks modern and premium.

**Not ready for public launch.** These items are outside QA's remit:
- the visible placeholders (listed at the end)
- the demo contact form, which sends nothing
- the missing legal identifiers
- real photos, logos and an SVG logo
- the 301 redirects from the old URLs

I fixed 12 issues (2 high, 3 medium, 7 low) in the generator, CSS and JS, then rebuilt. `check.py` and my crawler now report **0 errors**.

---

## Issues

Severity: **High** means visible to visitors or able to hide content. **Medium** means a factual or layout problem. **Low** means polish or a standards issue.

### Fixed

| # | Sev. | Page(s) | Problem | Fix |
|---|---|---|---|---|
| 1 | High | EN Team (`/en/about/team/`): cards and bio modal | Certification tags read **"Odoo d", "d Odoo", "d ISTQB"** on 13 people. The regex in `parse_certs` stripped "Certifie" from "Certified" and left a stray "d". | `build/build.py`: the regex now matches `certifi(ed\|ée\|é)`. |
| 2 | High | All pages; Home is the worst | If `main.js` fails to load or throws, the inline `html.js` class keeps **every `[data-reveal]` block at opacity 0 for good**. On Home, 30 of 30 blocks below the hero were blank in the test with `main.js` blocked. | `build/lib.py`: an inline guard drops the `js` class after 3.5 s unless `main.js` sets `window.__dtReady`, which it does once reveals are wired. Verified: 30 blocks hidden at 0.5 s, 0 at 4.3 s. Screenshot: `home-fr-1440-main-js-blocked.png`. |
| 3 | Medium | Home, Odoo hub, About | If IntersectionObserver never reports (some webviews or embeds), all reveals stay hidden and the hero counters read **"2000 / 0 / 0 %"**. | `main.js`: a 2.5 s safety net reveals everything. Counters keep their real values in the markup and are only reset to the start value once the observer reports them off-screen. Verified with a stubbed observer: 0 blocks hidden, counters show 2015/21/100. |
| 4 | Medium | Home hero at ≤600 px | Orbit chips on ring 2 were **clipped at both screen edges** at 390 px ("Pr…", "Manufacturin…"). | CSS: on mobile the orbit is 340 px wide and ring 2's inset is 12 %. Rechecked at 390 px: every chip is inside the viewport. |
| 5 | Medium | Integrations, plus the Gold panel on Home, Odoo hub and About | The site said **"Partenaires officiels de Ringover et de Leexi.ai"**, "Deux partenariats officiels" and "official Ringover and Leexi partner" in the meta description. The source calls only Ringover "Partenaire Officiel"; Leexi is described as "a partnership". | Reworded in `pages_main.py` and `pages_common.py`. The site now says "official Ringover partner and Leexi.ai partner" or "Ringover and Leexi.ai partners", and the heading reads "Deux partenariats au service de votre Odoo". |
| 6 | Low | Apps page (FR/EN) | The heading order jumped from h1 to h3: group titles were h3 and cards h4. | Groups are now h2 and cards h3. The CSS selectors were updated, so the visuals are unchanged. |
| 7 | Low | Header, all pages | The inactive FR/EN label (#5A6478 on the frosted bar over the dark hero) had a contrast of **3.7:1** at 12 px, which fails AA. | Now #344055, at **7.1:1**. |
| 8 | Low | Contact | Input and textarea borders (#CFD6E2) had **1.46:1** against white. WCAG 1.4.11 requires 3:1 for control boundaries. | Now #8A94A6, at **3.06:1**. |
| 9 | Low | Case studies at 960–1199 px | The floating "Odoo" card sat 4 px off-screen at 1024 px. | The −36 px offset now applies only from 1200 px. |
| 10 | Low | Implementation and Approach (5-step timeline) | Deliverable tags were capitalised inconsistently: "Analyse de l’existant" next to "cartographie des flux" and "tests". | The first letter of each tag is capitalised. |
| 11 | Low | All FR pages | Ordinary spaces before `: ; ? !` let the punctuation wrap to a new line, which is a French typography error. | `build/build.py` `fr_typography()` inserts no-break spaces in FR text nodes only. Script, style and attribute content are left alone. |
| 12 | Low | EN Odoo hub | The sentence "We have watched this ERP, designed for small businesses, SMEs and groups, grow, and played our part in it" was clumsy. | Rewritten: "Odoo is built for small businesses, SMEs and groups. We have watched it grow and played our part in it." |

Files changed:
- `build/build.py`
- `build/lib.py`
- `build/pages_common.py`
- `build/pages_main.py`
- `site/assets/css/styles.css`
- `site/assets/js/main.js`

Then rebuilt with `python build/build.py`. The site was confirmed reproducible before any edit: a rebuild of the untouched sources gave a byte-identical `site/`.

### Not fixed (remaining)

| Sev. | Page(s) | Problem | Recommendation |
|---|---|---|---|
| Low | 404 served at depth, e.g. `/en/some/missing/page` | The page renders correctly: CSS, fonts and the home and switcher links all resolve. However, Chrome's preload scanner fetches the relative assets before the inline `<base>` script runs, which costs 3 wasted 404 requests per hit. | On the production host, configure the error page with a server rule, or generate the deployed 404 pages with root-absolute asset URLs. |
| Low | Home hero orbit (all widths) | Chips on rings 1 and 2 rotate at different speeds, so they overlap for a few seconds now and then (for example "Projet" over "Comptabilité"). | Use the same angular speed for both rings, or hide the labels on the inner ring at the crossing angles. |
| Low | 7 pages | Meta descriptions run 164–178 characters (FR and EN Home, Développement, FR Odoo hub, Migration, both CAMELEON pages), so Google will truncate them. | Trim to about 155 characters. |
| Low | Team | Each member button's accessible name repeats the name ("Portrait de Viet Viet CEO & Fondateur…"). | Use `alt=""` on the card photo, since the name is already in the button. Keep the alt text in the modal. |
| Low | Team (CTA band) | "Envie de travailler avec nous ?" is paired with the sales text and the "Parler à un expert" button. It is ambiguous between recruitment and becoming a client. | Either point it at careers or reword it as a client CTA. |
| Info | Team (bio modal) | Uses native `<dialog>.showModal()`. Escape closes it and focus returns to the card. Tab cycles through the dialog and the browser UI, and the rest of the page is inert. | Acceptable as is. |
| Info | Home, References | The CMT GROUP and netiwan logos are tiny and low-resolution, so they are hard to read in the marquee. CAMELEON is shown as a wordmark tile. | Ask for SVG or high-resolution logos. |
| Info | Positioning | "ETI / mid-market" and "centre de compétences nearshore" do not appear in the scraped copy, which says TPE, PME and groupes. They are positioning choices from ANALYSIS.md, not facts. | The client should confirm them. |
| Info | Team | The modal tags use inclusive writing ("Certifié·e Odoo"). | Check the client is comfortable with it. |
| Info | Blog cards (EN) | Post titles come verbatim from the live blog, for example "Foolproof method for identifying and detecting AI subjects…", and read awkwardly. | Edit them on the Odoo blog if desired. |
| Info | Perf | `styles.css` (about 70 KB) is not minified, and Google Fonts adds a third-party, render-blocking request. | Minify, and consider self-hosting Geist and Instrument Serif. That helps both performance and GDPR, since the privacy page already flags the Google IP transfer. |

---

## What was verified

### Functional
- **check.py**: 42 pages, 0 errors (links, anchors, one H1 per page, alt text, unique titles and descriptions, hreflang and canonical). CSS+JS total 90.6 KB.
- **My own crawler** covered every `href`, `src` and `srcset` on all 42 pages, including fragment anchors.
  - It flags links that point to a directory, which would break on `file://`. There are none.
  - **Language switcher:** all 42 pages map to their exact counterpart by route ID. For example `odoo/developpement-sur-mesure/` ↔ `en/odoo/custom-development/`, and `404.html` ↔ `en/404.html`. On `file://` the switch was clicked both ways in Chrome and worked.
  - `<html lang>` is correct on every page.
  - On every page, the canonical equals the self hreflang, and both hreflang targets exist.
- **External links (curl):** all 32 darbtech.net URLs return HTTP 200. They are 7 FR and 7 EN job pages, 2 blog indexes and 16 blog posts (8 per language). I spot-checked page titles on job pages, and they were right. A made-up job URL returned 404, so the check is real. LinkedIn returns 999 (bot blocking), which is expected and was not counted.
- **404:** tested at `/old/page/deep/`, at `/en/some/missing/page` and directly. The title, CSS, fonts and links are right and the switcher goes to the other 404. It carries `noindex` and is excluded from the sitemap.
- **file:// and `python -m http.server`:** Home, Team, Integrations and 404 were loaded both ways with 0 failed requests and 0 console errors.
- **Console:** 0 errors or exceptions and 0 failed requests across all 48 screenshot loads and every interaction run.

### Content accuracy (against DECISIONS.md and the scraped data)
- **Gold date:** consistent everywhere, in the formats 22/09/2026, 22.09.2026, "22 septembre 2026" and the chip "depuis 09/2026". Partner since 2015 is also consistent. "Tous certifiés Odoo" and "100 %" match decision 2.
- **Phones:** +33 1 88 33 41 64 and +212 770 86 2295 everywhere. The old Rabat number (+212 5 22 58 48 26) appears nowhere.
- **Addresses:** 75012 everywhere. 75013 appears only as the registered office (36 rue Boussingault) in the legal notice, which is correct per the CGU.
- **Clients:** all 7 appear in the marquee, on the References wall and in the case-study card: netiwan GROUPE, CMT GROUP, PUTHOD PÉPINIÈRES, L’AMBASSADE DES LANGUES PARIS, ACSP Conseil, tionis and CAMELEON.
- **No invented facts.** I checked the figures and claims against the source:
  - 21 people, V8 to the latest versions, Community and Enterprise
  - Leexi supports Meet, Teams, Zoom and in-person meetings, and is GDPR-compliant and ISO 27001-certified
  - flex office 2 days a week, a 6-month internship with a path to hiring, and training and certification on hiring
  - case-study challenges, solutions and outcomes, and the Pays de Savoie location for both clients

  All of them trace back to the scrape. There are no numeric outcomes and no testimonials; testimonial slots are visible placeholders. The one overstatement ("official" Leexi partnership) is fixed.
- **Language:** a stop-word scan of every text node and of alt, aria-label, placeholder and meta content found no FR text on EN pages and no EN text on FR pages. Team roles and bios are in the right language. French spelling and grammar in the generator copy is clean. English is idiomatic apart from the one fixed sentence.

### Visual and responsive
I took 48 full-page screenshots: Home, Odoo hub, Implementation, the PUTHOD case, Team and Contact, at 1440, 1024, 768 and 390 px, in FR and EN. They are in `qa/screenshots/` and named `{page}-{lang}-{width}.png`. I also took `home-fr-1440-reduced-motion.png` and `home-fr-1440-main-js-blocked.png`.

I reviewed them by eye. The DOM checks found no horizontal scroll, no elements extending past the viewport and no unrevealed blocks after scrolling. Images loaded everywhere.

### Interaction and animation (headless Chrome, real key events)
- **Mobile menu:** opens and moves focus to the first link. Tab cycles between the burger and the menu, and Escape closes it and returns focus to the burger. The menu is `inert` while closed and the body scroll is locked. Per the code, it also closes when the viewport is resized to ≥1080 px; I did not test that.
- **Desktop dropdown:** Enter opens it, Tab moves into the links, Escape closes it and returns focus to the trigger, and it closes on hover-out or a click outside.
- **Team filter:** "Tech & QA" shows 4 of 21 people, `aria-pressed` updates, and the live region announces "4 personnes affichées". "All" brings back all 21.
- **Team modal:** opens with Enter and focuses the h2. Escape and the close button both work, and focus returns to the trigger card. A deep link such as `#hosni` opens the matching bio.
- **Contact form:**
  - Submitting it empty flags 5 fields, sets `aria-invalid`, and focuses the first invalid field.
  - A bad email flags only the email field.
  - A valid submission shows the success state and moves focus to it.
  - "Envoyer un autre message" resets the form.
- **Counters** count 2000→2015, 0→21 and 0→100 when scrolled into view. The **marquee** moves, and **scroll reveals** fire. The marquee's pause on hover and the canvas pausing off-screen are confirmed in the code but were not tested.
- **prefers-reduced-motion:**
  - 0 hidden blocks, and no word-split animation.
  - The marquee animation is off and the logos wrap in a static grid.
  - The canvas is hidden, and the mesh, orbit and border animations are reduced to about 0.01 ms.
  - The counters show their final values straight away.
- **JS failure and dead IntersectionObserver:** previously content stayed hidden. Both are now handled (fixes 2 and 3).

### Accessibility and SEO
- **Landmarks:** there is a skip link (visible on focus, top-left), then header, nav (labelled), main (`#main`, tabindex −1), footer, and an aside on Contact. Breadcrumbs sit in a labelled `nav`.
- **Focus ring:** a 2 px #4C8DFF outline on all interactive elements.
- **Heading order:** fine on all pages, after the Apps fix.
- **Alt text:**
  - Real alt text on logos, partner logos, portraits and the team photo.
  - Decorative images such as case-card backgrounds and post covers use `alt=""`, because the card text carries the meaning.
  - The orbit has `role="img"` and an aria-label.
- **Form:** every field has a label, the topics sit in a `fieldset`/`legend`, errors are tied to fields with `aria-describedby`, and the success message has `role="status"`.
- **Contrast** (WCAG ratios I computed):

| Pair | Ratio |
|---|---|
| Body text / white | 18.7 |
| text-2 / white | 10.4 |
| Muted / white | 5.95 |
| Muted / paper | 5.6 |
| Muted text on dark (#A3AEC7 on #050A1C) | 8.85 |
| White on orange button #B84E0E | 5.08 |
| Blue #0047BB / white | 8.0 |
| Blue-300 on dark | 9.55 |
| Gold-ink on gold-100 | 5.76 |
| Gold-300 on dark | 13.8 |
| Placeholder label (orange-ink) / white | 5.08 |
| Error red / white | 6.57 |

  Case-card text over photos is about 4.4:1 in the worst case, on the lightest part of a photo behind the gradient. That is acceptable for 1.05 rem and above, but worth watching if the photos are swapped.
- **SEO:**
  - Every page has a unique title and description, a self canonical, hreflang for fr, en and x-default (FR), Open Graph and Twitter tags, and FR and EN OG images (1200×630).
  - **JSON-LD** parses on every page: Organization on all of them, BreadcrumbList on interior pages, Article on case studies and ContactPage on Contact.
  - `sitemap.xml` is valid XML with 40 URLs and `xhtml:link` alternates. `robots.txt` points to it.

### Performance
- **Page weight**, counting HTML plus every local CSS, JS and image file the page references, but not Google Fonts:

| Page | Weight |
|---|---|
| Home | about 620 KB, the heaviest |
| References | about 405 KB |
| Most interior pages | 150–310 KB |

  Team modal photos sit in `<template>` and load only on demand.
- **Images:** none over 300 KB. The largest are the OG PNGs (110 KB, not loaded by pages) and the PUTHOD cover (110 KB WebP). The total image folder is about 1 MB. Below-the-fold images use `loading="lazy"` and `decoding="async"`.
- **Render-blocking:** the Google Fonts CSS and `styles.css` only. `main.js` is `defer`, and the JSON-LD is inert.
- **Fonts:** Google Fonts with `preconnect` to both origins and `display=swap`. That is 3 families: Geist in 4 weights, Geist Mono in 1, and Instrument Serif. Only the italic face of Instrument Serif is used, and the browser downloads only the faces in use.

---

## Design and modernity assessment

**Overall: modern and premium, about 8/10. It clearly impresses on first view.**

The Home hero sets the tone: a deep ink-navy field with a drifting mesh gradient, a particle network, an orbit of Odoo apps around a "Gold Partner" core, and the "Odoo Gold" accent in a gold serif italic. It reads like a top-tier SaaS or agency site rather than a typical Odoo-integrator template.

The system is consistent across both languages and all breakpoints:
- Geist with Instrument Serif accents and mono eyebrows
- a disciplined blue, orange and gold palette, with the gold reserved for the Gold Partner identity
- a bento services grid, the rotating gold border on the Gold panel, and the scroll-linked 5-step timeline
- the large ghost "DarbTech" wordmark in the footer

Motion is rich but tasteful, and it switches off cleanly under reduced-motion. Mobile layouts are well handled: stacked bento, a 2-column stats grid and a full-screen menu.

**Weakest spots:**
1. **Case-study pages** are the weakest template.
   - The hero has no visual.
   - The images are scraped blog covers (a tulip park and a watermarked photo) rather than project imagery.
   - The "Solution" section pairs the checklist with a lone dashed placeholder box.
   - The "Toutes nos références" card is mostly empty space.
   - There are no outcome figures, which cannot be invented.
2. **Interior heroes repeat one device**, a tilted icon tile, on about 10 pages (Odoo hub, the 5 services, Apps, Development, References, Approach, About). It starts to feel templated.
3. **Client logos** are low-resolution and greyscale. CMT and netiwan are illegible at marquee size, which weakens the "Ils nous font confiance" proof.
4. **Brand assets.** The header logo is a 475 px PNG whose tagline is unreadable at 38 px. The team portraits are AI-generated, according to the audit, and shown in greyscale, which is a credibility risk once visitors notice.
5. **Visible placeholders on Home** ([Témoignage à collecter]) are fine for a client review but look unfinished to real visitors. The orbit chips also overlap briefly from time to time.

**Top 5 improvements:**
1. **Replace scraped assets with real ones:**
   - an SVG logo
   - real team photos, in colour or with a consistent treatment
   - SVG or high-resolution client logos
   - real project photos or Odoo screenshots for PUTHOD and CAMELEON
2. **Rework the case-study template.**
   - Add a hero with the project image and an "at a glance" bar.
   - Add a before/after diagram (paper forms → Odoo; per-site spreadsheets → shared CRM).
   - Swap the empty placeholder for a CTA until a quote exists.
3. **Give each service page a bespoke hero visual.** Move the existing mock visuals (kanban board, version chain, code window, integration hub, support bars) into the hero in place of the generic icon tile.
4. **Add a proof layer**, the biggest lever for "impressing visitors":
   - 2–3 approved testimonials
   - a few client-approved figures (projects delivered, go-lives, users trained)
   - a link to DarbTech's entry in the official Odoo partner directory once it shows Gold
5. **Polish and performance:**
   - Synchronise the orbit rings so the chips never collide.
   - Tighten the length of Home: the Home case-study and team sections could be more compact.
   - Minify the CSS and self-host the fonts.

---

## Placeholders the client must fill before launch

| Where | Placeholder |
|---|---|
| Home; PUTHOD and CAMELEON case studies (FR and EN) | `[Témoignage à collecter]` / `[Testimonial to collect]`: an approved client quote |
| References index | `[Études de cas à rédiger]` / `[Case studies to write]`: further case studies, written with the clients' agreement |
| Support & training page and its FAQ | `[Offres de support à préciser : formules, volumes et délais d’intervention.]` and `[Détail des offres à confirmer par DarbTech.]` |
| Legal notice | Publication director `[À compléter]`; host name, address and phone `[… à compléter]`; DarbTech SARL legal identifiers (RC, ICE) |
| Terms of sale (CGV) | `[Entité contractante à confirmer : DarbTech Labs SAS (France) ou DarbTech SARL (Maroc).]` |
| Privacy policy | `[À valider par DarbTech avant mise en ligne, selon les outils réellement utilisés.]`: the cookies and third-party note |
| Apps page | The list is labelled "indicative". DarbTech should confirm which apps it actually delivers. |
| Contact form | Demo only: it validates and shows success but sends nothing. Connect it to Odoo (`/website/form/` with `crm.lead`) or another endpoint. |
| Assets | Real team photos, an SVG logo, high-resolution client logos, and project imagery for the case studies |
| Positioning to confirm | "ETI / mid-market" and "centre de compétences nearshore" wording |
| Hosting | 301 redirects from the old Odoo URLs (ANALYSIS.md §6), and the error-page rule (see the 404 note) |
