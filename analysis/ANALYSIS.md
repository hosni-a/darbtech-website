# DarbTech website analysis (FR / EN)

**Site audited:** https://www.darbtech.net (Odoo Website, theme "Cobalt") · **Crawl date:** 2026-10-22 · **Raw HTML:** `analysis/raw/` · **Extracts:** `analysis/extracted/` · **Link check:** `analysis/link_status.txt`

> Labels: **[FACT]** = seen on the live site (URL cited). **[ASSUMPTION]** = an inference or proposal DarbTech must confirm. The current site says nothing about Gold Partner status (date awarded, number of certified people, client references), so every such value below is a placeholder.

## 1. Discovery
- **Platform:** Odoo Website (`generator=Odoo`), theme Cobalt. Active modules: Blog, Jobs, eCommerce (empty), Appointment, and a website form that creates CRM leads (`crm.lead`).
- **Languages:** French is the default at `/` (x-default); English is at `/en/...`. Static English pages keep French slugs.
- **robots.txt:** contains only `Allow: /social_instagram/` and the sitemap line, so nothing is disallowed.
- **sitemap.xml:** 120 URLs, all French. It includes low-value pages: /shop, /appointment, /calendar, /website/info, /terms, 7 job-apply and 7 job-detail pages, 23 team bios and 63 blog URLs.
- **Header menu** (same in FR and EN, labels translated): Accueil/Home · Services ▾ (only DevOps and Intégrateur de Logiciel/Software Integrator) · Cas Clients/Client Cases · Blog · Notre Equipe/Our Team · Postes/Jobs · cart icon · phone +33 1 88 33 41 64 · "Contactez-nous/Contact us" button · language flags.
- **Footer** ("Explorateur"): Accueil, Nos services, A propos, Blog, Interventions (no link), Cas Clients, Pourquoi Nous Choisir, Pourquoi Choisir Odoo, CGU · LinkedIn · Paris (122 Av. Daumesnil, 75012) and Rabat (Agdal) · "Copyright © DarbTech Labs" · "Généré par Odoo".

## 2. Page inventory

| # | Page | FR | EN | Purpose | Status / notes |
|---|---|---|---|---|---|
| 1 | Home | `/` | `/en` | Brand intro, ERP/CRM teaser, blog teaser | Hero hidden by conditional visibility; EN title and meta are in French |
| 2 | About / Team | `/aboutus` | `/en/aboutus` | Story, methodology, 21 team cards, partners (Odoo, Ringover, Leexi) | Title "aboutUs \| DarbTech" |
| 3 | Services | `/services` | `/en/services` | Catch-all: dev, integrator, ERP/CRM, cases, client logos | Not in header menu. ERP button → `/erpodoo` 404; CRM button → `#`; cases button → `/cas-clients` 404 |
| 4 | DevOps | `/devops` | `/en/devops` | Mobile apps, web services, web apps, custom dev | Content is really custom development; mentions a form that does not exist |
| 5 | Software integrator | `/integrateurdelogiciel` | `/en/integrateurdelogiciel` | Generic CRM vs ERP explanation | Two H1s; never mentions Odoo; EN title untranslated |
| 6 | Why us / Why Odoo | `/prqdarbodoo` | `/en/prqdarbodoo` | 5-step implementation process and 7 Odoo benefits | Linked from footer only; EN closing block still French |
| 7 | Contact | `/contactus` | `/en/contactus` | Lead form and the two offices | FR title "Contact Us"; postcode 75012 (FR) vs 75013 (EN); Rabat phone differs from footer |
| 8 | Client cases | `/blog/cas-clients-4` (menu links `/blog/cas-client-4`, 301) | `/en/blog/client-cases-4` | 4 posts | Puthod, Cameleon, an Odoo-for-SMEs post and a misfiled AI article; case bodies are French on EN |
| 9 | Blog | `/blog` | `/en/blog` | ~60 posts in 6 categories | No H1; latest post 26 Feb 2026 |
| 10–13 | Blog categories | tech-odoo-3 (20), gestion-d-entreprise-1 (33), actualites-5 (0), success-stories-6 (0) | translated slugs | | Two categories are empty |
| 14 | Jobs | `/jobs` | `/en/jobs` | 7 openings, all in Rabat | EN mixes French and English; one offer fully French |
| 15 | Job detail / apply | `/jobs/detail/*`, `/jobs/apply/*` | `/en/...` | Odoo defaults | French slugs on EN |
| 16 | Team bios (23) | `/hosni`, `/anis`, `/fred`, `/frederic`, `/viet`, `/thomas`, `/maria`, `/marwa`, `/fatima-zahra`, `/abdellatif`, `/zoubida`, `/khadija-a`, `/khadija-r`, `/hatim`, `/mohammed`, `/salma`, `/sally`, `/ouail`, `/kamal`, `/elmehdi`, `/douae`, … | `/en/<same>` | Photo, role, bio | Thin pages; no H1 or meta; "Suivez-nous sur" with no links |
| 17 | Legal notice / CGU | `/cgu` | `/en/cgu` | DarbTech Labs SAS, capital €10,000, RCS Paris 850 857 046, dpo@darbtech.net | EN body is French |
| 18 | Terms of sale | `/terms` | `/en/terms` | Standard terms (DarbTech SARL, invoices due in 21 working days) | FR page shows English text; not linked in footer |
| 19 | Shop | `/shop` | `/en/shop` | "Aucun produit défini" | Cart icon appears on every page |
| 20 | Appointment | `/appointment` (`/calendar` 301) | `/en/appointment` | Odoo booking | No slots available |
| 21 | Odoo info | `/website/info` | `/en/website/info` | Lists installed Odoo apps | Should not be public |
| — | Broken | `/erpodoo`, `/cas-clients` | `/en/...` | | 404 |

## 3. Per-page findings

### 3.1 Home
**Sections, in order:**
1. "À la Recherche de l'Excellence / Seek Excellence", "À propos" button. **Hidden** (`data-visibility="conditional"`).
2. "l'accompagnement parfait… / Suitable for your business". Hidden on mobile (`d-none d-lg-block`).
3. "Excellence dans l'Offshoring" ("Nos équipes certifiées…").
4. ERP and CRM colour blocks, each with "Plus de détails" → `/services`.
5. "Boostez votre entreprise", "Géré par des experts", "Optimisez vos résultats": three generic one-liners over stock images.
6. H1 "Découvrez nos derniers articles" and a gallery.

**Observations:** no visible heading mentions Odoo; no figures, client logos, testimonials or partner badge; only CTA is "Contactez-nous" in the header; 10/24 images lack alt; EN title/description/OG tags are French; FR keywords meta contains junk ("Septembre 2026 - Sept - 09/26"); literal EN ("Our certified teams are entitled to respond…"); mobile visitors land directly on "Excellence in Offshoring".

### 3.2 About (`/aboutus`)
- Story: offices in Paris and Rabat, serving SMEs in French- and English-speaking regions, through CRM/ERP digitalisation and dedicated development teams.
- Methodology: DevOps, Agile-Scrum, Transparence, Engagement.
- 21 team cards.
- Partners: **Odoo** ("DarbTech, Partenaire Certifié Odoo depuis 2015 !", V8 to latest, Enterprise and Community) · **Ringover** (official partner: CTI, IVR, analytics) · **Leexi.ai** (meeting AI with native Odoo integration).

**Team cards [FACT]:** Viet (CEO & Founder) · Fred (Associate Director, Consulting & Production; Odoo, RingOver, LSS, SAFe, CSPO) · Thomas, Kamal (Project Directors / Digital Transformation, Odoo certified) · Maria (digital management consultant) · Frédéric (performance consultant) · Marwa (admin & sales) · Anis (QA, ISTQB + Odoo) · Fatima Zahra, Khadija, Mohammed, Salma (confirmed ERP engineers, Odoo certified) · Hosni (senior Odoo developer, certified) · Abdellatif (lead dev & consultant, certified) · Zoubida (head of technology solutions, certified) · Khadija, Hatim (junior ERP engineers, certified) · Ouail, El Mehdi, Douae, Salma (junior ERP engineers). 13 cards say "Certifié(e) Odoo".

**Issues:** title "aboutUs", no meta description; "Partenaire Certifié" outdated; 28/40 images lack alt; AI-generated portraits ("ChatGPT Image 15 mai 2026…"); very long page; header and footer both point here under different labels.

### 3.3 Services (`/services`)
DevOps paragraph · band "Implémentation de Projets ERP avec Odoo / Full Stack / SaaS / JavaScript, PHP, Python" · mobile, web services, web apps · "Developpement" (typo) · "Editeur de logiciel" heading over "intégrateur" text · 4 benefit cards · ERP/CRM blocks duplicated from home · 3 case tiles (ERP odoo – Puthod, CRM odoo – Cameleon, Planning odoo) · client logos Netiwan, CMT company, Puthod, ACSP Conseil, Tionis + one unnamed, all with empty alt.

**Broken links:** ERP → `/erpodoo` (404); CRM → `#`; Cases → `/cas-clients` (404); "Planning odoo – En savoir plus" → a blog category.

### 3.4 DevOps (`/devops`)
Mobile apps (unsourced stats: 150 checks/day, 46 apps installed, 19 used), web services/microservices, web apps, development; 5 "Contactez-nous" buttons; mentions "formulaire en bas de cette page" but no form; content is custom development, not DevOps; title "devops"; EN says "Developpement".

### 3.5 Software integrator (`/integrateurdelogiciel`)
Generic CRM/ERP copy, never mentions Odoo; a "Contactez-nous" button is an H1 (two H1s); typos ("Ressource", "circulants"); EN title "IntégrateurDeLogiciel".

### 3.6 Why us / Why Odoo (`/prqdarbodoo`)
- **5-step process:** (1) study and analysis; (2) align processes with the ERP; (3) standard plus specific modules; (4) training; (5) maintenance.
- **7 Odoo benefits:** integration, online access, user interface, interoperability, fast deployment, open source, community and updates.
- Best content on the site, reachable only from the footer, cryptic title. EN still says "Rejoignez-nous! Contactez-nous ici…".

### 3.7 Contact (`/contactus`)
Form (creates CRM lead → `/contactus-thank-you`): Name*, Company*, Job title*, Phone*, Email*, Request type* (Commercial/Support/Emploi), When to reach you, Subject*, Question*. Eight required fields; no GDPR consent, no privacy link, no visible captcha.
Offices: Paris 75012 (FR) vs 75013 (EN); Rabat +212 5 22 58 48 26 here vs +212 770 86 2295 in the footer.
EN wording: "Occupied position", "At what time can we join you?", "Mail", "Job". No map, email, booking link or response-time promise.

### 3.8 Blog
Mostly by "DarbTech SARL, Frédéric Phan". Duplicates: AI-method article twice (IDs 70, 73), Odoo-for-SMEs near-duplicates (56, 57). Actualités and Success Stories empty. EN partially translated (ID 72 full; IDs 18, 19 French bodies). Blog index has no H1; categories no meta.

### 3.9 Client cases
- **Puthod** (Pays de Savoie, landscaping): paper forms replaced by standard Odoo + specific modules.
- **Cameleon** (Pays de Savoie, events): lead and quote tracking in Odoo CRM.
- Problem/solution lists with no metrics, quote, apps list or visuals.

### 3.10 Jobs
7 roles in Rabat: junior Odoo developer, confirmed Odoo developer, end-of-studies intern, technical/functional consultant, Agile project manager, QA tester, sales/admin assistant. Flex office (2 days on site), Odoo certification on hiring. Applications to rh@, pfe@, pm@, qa@… @darbtech.net. EN has French headings; one offer fully French.

### 3.11 Team bios
Card + 4–5 paragraph bio; no H1, meta or structured data. `/fred` vs `/frederic`, and `/sally` (a second Salma) are confusing.

### 3.12 Legal
CGU: DarbTech Labs SAS. Terms: DarbTech SARL (two legal entities). No privacy or cookie policy page.

### 3.13 Exposed Odoo defaults
`/shop`, header cart icon, `/appointment`, `/website/info`, "Le #1 Open Source eCommerce" footer line.

## 4. Global assessment

### 4.1 Information architecture
No service taxonomy (Services menu has 2 pages; `/services` and `/prqdarbodoo` off-menu); no Odoo page, apps, industries, methodology page, FAQ or testimonials; "Cas Clients" is a blog category; ERP/CRM and dev blocks duplicated; several dead ends.

### 4.2 Brand tokens
| Token | Hex | Usage |
|---|---|---|
| o-color-1 primary | **#0047BB** | buttons, links, footer |
| o-color-2 accent | **#D86018** | secondary buttons, orange band |
| o-color-3 | **#F0F4F5** | light backgrounds |
| o-color-4 | **#FFFFFF** | page and header background |
| o-color-5 | **#003FA7** | dark blue headings and backgrounds |
| text | #212529 | body text and headings |
| link on #F0F4F5 | #003DA2 | |
| link on orange | #00173C | |

- **Fonts:** headings Lato (600); body system stack. Playfair Display and Roboto loaded but unused. Icons: Font Awesome 4.7.
- **Header:** boxed, "pills" links, #0047BB shadow.
- **Logo:** 33 KB PNG at 95×40 px — person pictogram over blue/grey clouds with orange accents, blue "DarbTech" wordmark, orange line, tagline "Solutions for a digitalised world". Ask for SVG.

### 4.3 UX
No hero or value proposition; stock imagery and AI portraits; generic copy with no proof; heavy contact form, no booking alternative; misleading cart icon; zero-width characters in link text.

### 4.4 Mobile
Home hides sections 1–2 on mobile; 21 team cards + long partner texts = very long scroll; viewport meta present. Run Lighthouse mobile on the new build.

### 4.5 SEO
Slug-like titles; only home has a meta description (EN one in French); H1 problems; hreflang/canonical correct but sitemap FR-only with junk; no "Odoo Gold Partner" / "intégrateur Odoo Paris/Maroc" targeting; no Organization/LocalBusiness JSON-LD; duplicate posts.

### 4.6 Performance
JS bundle ~4.6 MB, CSS ~1.1 MB; JPG/PNG or bitmaps in SVG; 3 font families loaded, 1 used. **Target:** <200 KB JS+CSS, WebP/AVIF with srcset, self-hosted font subsets.

### 4.7 Accessibility
Missing alt: Home 10/24, About 28/40, Services 13/26. Zero-width chars in link labels; broken heading order; form fields named after labels; no consent text; white on #D86018 ≈ 3.6:1 (fails AA normal text); white on #0047BB ≈ 8.6:1 (passes). Skip link present.

### 4.8 Broken and problematic links
`/erpodoo`, `/cas-clients` (FR+EN) 404 · CRM button `#` · menu `/blog/cas-client-4` 301 · `/calendar` 301 to empty appointment · footer "Interventions" no link · `/devops` "form below" missing · EN blog links use FR slugs then 301.

### 4.9 English translation gaps
Home title/meta/OG · footer labels · `/en/prqdarbodoo` closing block · `/en/cgu` body · `/terms` (English on FR page) · one job offer and several posts · `/en/integrateurdelogiciel` title · FR slugs on static pages · literal wording · Paris postcode 75012 vs 75013.

## 5. Where Gold Partner status belongs
Currently only "Partenaire Certifié Odoo depuis 2015" on `/aboutus`.

| Placement | Content |
|---|---|
| Header | Small "Odoo Gold Partner" badge |
| Home hero | H1 about Gold Partner and Odoo, badge, 2 buttons |
| Trust bar | Gold badge · partner since 2015 [FACT] · 13+ Odoo-certified consultants [FACT from cards, confirm] · Paris and Rabat · V8 to latest · Ringover and Leexi partners |
| Certifications | Odoo, ISTQB, SAFe, CSPO, LSS, Ringover |
| Odoo hub and sub-pages | Implementation, migration, development, integrations, training & support, hosting |
| Apps coverage | CRM, Sales, Accounting/Invoicing, Inventory, Purchase, MRP, Helpdesk, Project/Planning, HR/Recruitment, eCommerce/Website, Documents, Studio, AI, Ringover, Leexi [delivered apps TO CONFIRM] |
| Industries | Landscaping (Puthod), events (Cameleon), manufacturing (MRP articles); others [TO CONFIRM] |
| Case studies | Context, challenge, apps, results, quote; possibly Netiwan, CMT, ACSP Conseil, Tionis [TO CONFIRM] |
| Methodology | 5 steps from `/prqdarbodoo` + 4 values from `/aboutus` |
| Testimonials | To collect |
| Team | Leadership, number certified, real photos |
| Contact | "Talk to a Gold Partner expert", booking, both offices |
| Footer | Badge, Odoo partner directory link [URL TO CONFIRM], legal entities |
| SEO | Titles/meta mentioning Odoo Gold Partner Paris/Rabat; Organization JSON-LD |

## 6. Recommended sitemap
FR at `/` (x-default), EN at `/en/` with translated slugs. [ASSUMPTION: static hosting supports this.]

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
| `/secteurs/` | `/en/industries/` |
| `/references/`, `/references/<client>/` | `/en/case-studies/`, `/en/case-studies/<client>/` |
| `/methode/` | `/en/approach/` |
| `/a-propos/` | `/en/about/` |
| `/a-propos/equipe/` | `/en/about/team/` |
| `/carrieres/` | `/en/careers/` |
| `/blog/` (stays on Odoo) | `/en/blog/` |
| `/contact/` | `/en/contact/` |
| `/mentions-legales/` | `/en/legal-notice/` |
| `/confidentialite/` | `/en/privacy/` |
| `/cgv/` | `/en/terms/` |

**Main menu:**
- FR: Odoo ▾ · Développement · Secteurs · Références · Méthode · À propos ▾ (Équipe, Carrières, Blog) · orange [Prendre rendez-vous] · FR/EN
- EN: Odoo ▾ · Development · Industries · Case studies · Approach · About ▾ · [Book a call] · FR/EN

**Proposed 301 redirects:** `/aboutus`→`/a-propos/` · `/services`→`/odoo/` · `/devops`→`/developpement/` · `/integrateurdelogiciel`→`/odoo/` · `/prqdarbodoo`→`/methode/` · `/contactus`→`/contact/` · `/cgu`→`/mentions-legales/` · `/terms`→`/cgv/` · `/blog/cas-clients-4`→`/references/` · `/<name>`→`/a-propos/equipe/#<name>`. Remove `/shop`, `/appointment`, `/website/info` from the index.

## 7. Page blueprints

### 7.1 Home
1. **Hero:** Gold badge, H1, subline, two buttons.
   - FR H1: « Votre partenaire Odoo Gold, de l'analyse au go-live ». Subline: « Intégration, migration et développement Odoo pour PME et ETI, depuis Paris et Rabat. » Buttons: « Prendre rendez-vous » / « Découvrir nos services Odoo ».
   - EN H1: "Your Odoo Gold Partner, from analysis to go-live". Subline: "Odoo implementation, migration and development for SMEs and mid-market companies, from Paris and Rabat." Buttons: "Book a call" / "Explore our Odoo services".
2. **Trust bar:** Gold Partner · since 2015 · [13+] certified [TO CONFIRM] · Paris and Rabat · Ringover and Leexi.
3. **Client logos** (permission to confirm).
4. **6 Odoo service cards:** implementation, migration, custom development, integrations, training & support, hosting/DevOps.
5. **Apps strip.**
6. **Why DarbTech:** Agile-Scrum, transparency, commitment, DevOps industrialisation, Gold Partner benefits, nearshore team in Rabat.
7. **5-step method.**
8. **2–3 featured cases.**
9. **Testimonials** (to collect).
10. **Industries teaser.**
11. **3 latest articles.**
12. **CTA band:** « Parlons de votre projet Odoo » / "Let's talk about your Odoo project".
13. **Footer:** badge, both offices, legal entities.

### 7.2 Odoo hub
Hero with Gold badge · why Odoo (7 benefits, condensed) · why DarbTech (Gold, since 2015, V8 to latest, Community & Enterprise) · service cards · apps grid · editions & hosting (Online, Odoo.sh, on-premise) [TO CONFIRM] · cases · FAQ · CTA.

### 7.3 Odoo sub-pages
Hero with outcome · who it is for · scope · steps & deliverables · related apps · related case · FAQ · CTA. Integrations page covers Ringover (CTI, IVR, analytics) and Leexi (meeting AI with Odoo CRM sync).

### 7.4 Apps page
- Sales & CRM: CRM, Sales, Invoicing, eCommerce, Website, Email Marketing
- Finance: Accounting, Expenses
- Operations: Inventory, Purchase, MRP, Maintenance, Planning, Project, Timesheets, Helpdesk
- HR: Employees, Time Off, Recruitment
- Productivity: Documents, Knowledge, Studio, AI
- Integrations: Ringover, Leexi

Drawn from blog topics and DarbTech's own instance (`/website/info`); confirm delivered apps.

### 7.5 Development
Web, mobile (iOS/Android), APIs & microservices, SaaS, DevOps/CI-CD, stack (Python, JavaScript, PHP) · engagement: dedicated team or nearshore from Rabat.

### 7.6 Industries
Sector cards with pain points, Odoo apps, linked case. Drop if fewer than 4 sectors confirmed.

### 7.7 Case studies
Index with sector/app filters + logo grid. Detail: client & sector · challenge · solution · results · quote · related. Seed: Puthod, Cameleon.

### 7.8 Approach
5-step timeline with deliverables · Agile sprints · DevOps · transparency · commitment · QA with ISTQB-certified engineer · post-go-live support.
- FR: « Une méthode Agile, transparente et industrialisée »
- EN: "An Agile, transparent and industrialised approach"

### 7.9 About
Story · what Gold status means for clients · key figures [TO CONFIRM] · values · partners · offices with map.

### 7.10 Team
Leadership row (Viet, Fred, Thomas, Kamal) · certified experts filterable by role with certification chips · bios in modals (replacing 23 thin pages) · real photos.

### 7.11 Careers
Gold Partner training & certification path · flex office · Agile projects · links to Odoo `/jobs` · internship · spontaneous applications.

### 7.12 Contact
Short form (name, email, company, phone optional, topic, message, GDPR consent) · booking link · offices (Paris 75012 assumed; Rabat one confirmed phone) · response-time promise · Gold badge.

### 7.13 Legal
Legal notice (DarbTech Labs SAS; add DarbTech SARL) · new privacy & cookie policy · terms of sale in proper French.

## 8. Open questions for DarbTech
1. Date Gold status was awarded, official badge artwork, Odoo partner directory URL.
2. Exact number of certified consultants and which Odoo versions.
3. Clients that may be named publicly, with metrics and quotes.
4. Industries to feature.
5. Correct Rabat phone number and Paris postcode.
6. Which legal entity contracts with clients: DarbTech Labs SAS or DarbTech SARL.
7. SVG logo; whether the tagline stays (and in which language).
8. Hosting and support packages offered.
