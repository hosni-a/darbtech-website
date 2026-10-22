"""Development, case studies, approach, about, team, careers, contact, legal and 404 pages."""
from lib import (esc, icon, btn, gold_chip, section_head, checklist, tags, faq, placeholder, hero_bg,
                 page_hero, hero_tile, cta_band, OFFICES, EMAIL, LINKEDIN, BLOG_URL)
from pages_common import (method_steps, values_cards, gold_panel, stats_light, logo_tiles, case_card,
                          offices_cards, team_teaser, apps_cloud, CASES, CLIENTS)
from pages_main import mock_code


# ---------------------------------------------------------------------------
# Development
# ---------------------------------------------------------------------------
def page_dev(c):
    trail = [(c.t("Développement", "Development"), None)]
    cards = [
        ("monitor", c.t("Applications web", "Web applications"),
         c.t("Accessibles depuis tous les écrans, installées on-premise ou en SaaS : chaque service travaille dans une application unique et partagée.", "Available on every screen, on-premise or SaaS: every department works in one shared application.")),
        ("phone-device", c.t("Applications mobiles", "Mobile apps"),
         c.t("Des applications multi-plateformes iOS et Android, pensées pour l’usage quotidien.", "Cross-platform iOS and Android apps, designed for everyday use.")),
        ("server", c.t("Web services et microservices", "Web services and microservices"),
         c.t("Nous développons, exploitons et connectons les web services dont vos applications ont besoin, pour plus de souplesse et d’interopérabilité.", "We build, run and connect the web services your apps rely on, for more flexibility and interoperability.")),
        ("cloud", c.t("Logiciels SaaS", "SaaS software"),
         c.t("Conception et développement de logiciels en mode SaaS, full stack.", "Full-stack design and development of SaaS software.")),
        ("infinity", "DevOps",
         c.t("De l’automatisation au déploiement continu : des livraisons plus fiables, des coûts maîtrisés.", "From automation to continuous deployment: more reliable releases, costs under control.")),
        ("users", c.t("Équipes dédiées", "Dedicated teams"),
         c.t("Des développeurs expérimentés mis à votre disposition pour mener vos projets, pendant que vous vous concentrez sur votre métier.", "Experienced developers assigned to your projects, so you can focus on your core business.")),
    ]
    grid = "".join(f'<article class="card" data-reveal style="--i:{i % 3}"><span class="card__icon{" card__icon--orange" if i == 4 else ""}">{icon(ic)}</span><h3 class="card__title">{t}</h3><p class="card__text">{d}</p></article>'
                   for i, (ic, t, d) in enumerate(cards))
    code = mock_code([(36, "#8DB5FF"), (64, "#A3AEC7"), (52, "#E9C46A"), (28, "#FFB27F"), (70, "#A3AEC7"), (44, "#8DB5FF"), (58, "#A3AEC7")])
    body = page_hero(c, trail, c.t("Développement", "Development"),
                     c.t('Web, mobile et API : <span class="accent accent--gold">vos projets, notre équipe</span>', 'Web, mobile and APIs: <span class="accent accent--gold">your projects, our team</span>'),
                     c.t("Au-delà d’Odoo, nos développeurs conçoivent applications web, mobiles et web services. Nous mettons à votre disposition des équipes expérimentées pour mener vos projets, pendant que vous vous concentrez sur votre cœur de métier.",
                         "Beyond Odoo, our developers build web apps, mobile apps and web services. We provide experienced teams to deliver your projects while you focus on your core business."),
                     btn(c.href("contact"), c.t("Soumettre un projet", "Submit a project"), "primary", magnetic=True),
                     aside=hero_tile("code"))
    body += f'''<section class="section" aria-labelledby="dev-title"><div class="container">
{section_head(c.t("Expertises", "Expertise"), c.t("Du back-end au mobile, en mode Agile", "From back end to mobile, the Agile way"), c.t("Ces sujets vous sont peut-être familiers. Trouver le temps de tous les mener à bien est une autre affaire : c’est là que nous intervenons.", "These topics may sound familiar. Finding the time to deliver them all is another matter: that is where we come in."))}
<div class="grid grid--3">{grid}</div>
</div></section>'''
    body += f'''<section class="section section--dark" aria-labelledby="stack-title"><div class="bg-grid"></div><div class="container" style="position:relative">
<div class="split"><div class="split__text on-dark" data-reveal>
<span class="eyebrow">{c.t("Stack et engagement", "Stack and engagement")}</span>
<h2 id="stack-title">{c.t('Full stack, <span class="accent accent--gold">industrialisé</span>', 'Full stack, <span class="accent accent--gold">industrialised</span>')}</h2>
<p class="lead">{c.t("Notre méthodologie DevOps industrialise nos procédés : automatisation, intégration et déploiement continus, amélioration continue. Nos cycles Agile courts vous gardent impliqué à chaque étape.",
                     "Our DevOps methodology industrialises how we work: automation, continuous integration and deployment, continuous improvement. Short Agile cycles keep you involved at every step.")}</p>
<ul class="tags">{"".join(f'<li class="tag tag--dark">{t}</li>' for t in ["Python", "JavaScript", "PHP", "Full stack", "SaaS", "iOS", "Android", "Web services", "DevOps", "Agile-Scrum"])}</ul>
{checklist([c.t("Votre projet : nous l’étudions et le réalisons de bout en bout.", "Your project: we scope it and deliver it end to end."),
            c.t("Votre équipe dédiée : des développeurs expérimentés, depuis Rabat, intégrés à votre organisation.", "Your dedicated team: experienced developers in Rabat, embedded in your organisation.")])}
</div>
<div data-reveal="scale">{code}</div></div>
</div></section>'''
    body += f'''<section class="section" aria-labelledby="dev-faq"><div class="container container--narrow">
{section_head("FAQ", c.t("Questions fréquentes", "Frequently asked questions"))}
{faq([(c.t("Développez-vous uniquement autour d’Odoo ?", "Do you only build around Odoo?"),
        c.t("Non. Odoo est notre cœur d’expertise, mais nous développons aussi des applications web, mobiles, des web services et des logiciels SaaS.", "No. Odoo is our core expertise, but we also build web and mobile apps, web services and SaaS software.")),
       (c.t("Comment vous soumettre un projet ?", "How do I submit a project?"),
        c.t("Décrivez-le nous via le formulaire de contact : un consultant vous rappelle pour en discuter.", "Describe it through the contact form and a consultant will call you back to discuss it.")),
       (c.t("Où travaillent vos développeurs ?", "Where do your developers work?"),
        c.t("Principalement à Rabat, en lien étroit avec nos consultants à Paris et avec vos équipes.", "Mainly in Rabat, working closely with our consultants in Paris and with your teams."))])}
</div></section>'''
    body += cta_band(c, c.t('Un projet de développement ? <span class="accent accent--gold">Dites-nous tout</span>', 'A development project? <span class="accent accent--gold">Tell us everything</span>'))
    return dict(title=c.t("Développement web, mobile, API et DevOps | DarbTech", "Web, mobile, API and DevOps development | DarbTech"),
                desc=c.t("Applications web et mobiles (iOS, Android), web services, SaaS et DevOps : DarbTech met à votre disposition des équipes de développeurs expérimentés, depuis Paris et Rabat.",
                         "Web and mobile apps (iOS, Android), web services, SaaS and DevOps: DarbTech provides experienced development teams, from Paris and Rabat."),
                body=body, trail=trail)


# ---------------------------------------------------------------------------
# Case studies
# ---------------------------------------------------------------------------
def page_cases(c):
    trail = [(c.t("Références", "Case studies"), None)]
    wall = "".join(
        (f'<li class="logo-tile"><img src="{c.asset(img)}" alt="{esc(name)}" loading="lazy"></li>' if img else f'<li class="logo-tile logo-tile--word">{esc(name)}</li>')
        for name, img in CLIENTS)
    body = page_hero(c, trail, c.t("Références", "Case studies"),
                     c.t('Ils ont choisi Odoo <span class="accent accent--gold">avec DarbTech</span>', 'They chose Odoo <span class="accent accent--gold">with DarbTech</span>'),
                     c.t("PME de services, de conseil, de formation ou d’événementiel : nos clients ont digitalisé leurs processus avec Odoo. Découvrez deux projets en détail.",
                         "Service firms, consultancies, training and event companies: our clients have digitised their processes with Odoo. Explore two projects in detail."),
                     aside=hero_tile("star"))
    body += f'''<section class="section" aria-labelledby="cs-title"><div class="container">
{section_head(c.t("Études de cas", "Case studies"), c.t("Deux projets, deux métiers", "Two projects, two trades"))}
<div class="grid grid--2">{case_card(c, "puthod", 0)}{case_card(c, "cameleon", 1)}</div>
<div style="margin-top:18px">{placeholder(c, c.t("[Études de cas à rédiger]", "[Case studies to write]"), c.t("Emplacements réservés à d’autres projets clients, à documenter avec leur accord.", "Reserved for further client projects, to be written up with their approval."))}</div>
</div></section>'''
    body += f'''<section class="section section--paper" aria-labelledby="clients-title"><div class="container">
{section_head(c.t("Clients", "Clients"), c.t("Ils nous font confiance", "Trusted by"), center=True)}
<ul class="apps-cloud" style="justify-content:center;gap:14px" data-reveal>{wall}</ul>
</div></section>'''
    body += cta_band(c, c.t('Et si votre projet était <span class="accent accent--gold">le prochain</span> ?', 'Could your project be <span class="accent accent--gold">the next one</span>?'))
    return dict(title=c.t("Références et études de cas Odoo | DarbTech", "Odoo case studies and clients | DarbTech"),
                desc=c.t("Études de cas Odoo de DarbTech : digitalisation des processus chez PUTHOD, CRM multi-sites chez CAMELEON. Ils nous font confiance : netiwan, CMT GROUP, tionis…",
                         "DarbTech Odoo case studies: process digitisation at PUTHOD, multi-site CRM at CAMELEON. Trusted by netiwan, CMT GROUP, tionis and more."),
                body=body, trail=trail)


def page_case(c, key):
    cs = CASES[key]
    d = cs[c.lang]
    post = c.data["posts"][cs["post"]][c.lang]
    other = "cameleon" if key == "puthod" else "puthod"
    trail = [(c.t("Références", "Case studies"), "cases"), (cs["client"], None)]
    facts = [(c.t("Client", "Client"), cs["client"]), (c.t("Secteur", "Sector"), d["sector"]),
             (c.t("Région", "Region"), d["region"]), (c.t("Périmètre", "Scope"), d["scope"])]
    fact_html = "".join(f'<li class="stat"><span class="stat__label">{k}</span><span style="font-weight:600;font-size:1.05rem;color:var(--text)">{esc(v)}</span></li>' for k, v in facts)
    body = page_hero(c, trail, c.t("Étude de cas", "Case study"), esc(d["title"]), esc(d["lead"]))
    body += f'''<section class="section section--tight" aria-label="{c.t("Fiche projet", "Project facts")}"><div class="container">
<ul class="stats stats--light" data-reveal>{fact_html}</ul>
</div></section>
<section class="section" style="padding-top:0" aria-labelledby="ch-title"><div class="container">
<div class="split">
<div class="split__media" data-reveal="scale"><img src="{c.asset(cs["img"])}" alt="{esc(c.t("Illustration de l’étude de cas ", "Case study illustration: ") + cs["client"])}" loading="lazy">
<div class="float-card"><span class="card__icon card__icon--gold">{icon("sparkle")}</span><div><strong>Odoo</strong><span class="muted">{esc(d["scope"])}</span></div></div></div>
<div class="split__text" data-reveal>
<span class="eyebrow">{c.t("Le défi", "The challenge")}</span>
<h2 id="ch-title">{c.t("Ce qui bloquait", "What was holding them back")}</h2>
{checklist(d["challenge"], "checklist--x", "x")}
</div></div></div></section>
<section class="section section--paper" aria-labelledby="sol-title"><div class="container">
<div class="split split--reverse">
<div class="split__text" data-reveal>
<span class="eyebrow">{c.t("La solution", "The solution")}</span>
<h2 id="sol-title">{c.t("Ce que nous avons mis en place", "What we put in place")}</h2>
{checklist(d["solution"])}
<p class="lead" style="margin-top:8px">{esc(d["outcome"])}</p>
<a class="link-arrow" href="{esc(post["url"])}">{c.t("Lire l’article d’origine sur le blog", "Read the original article on the blog")}{icon("arrow-up-right")}</a>
</div>
<div data-reveal>{placeholder(c)}</div>
</div></div></section>
<section class="section" aria-labelledby="next-title"><div class="container">
{section_head(c.t("Autre référence", "Another case study"), c.t("Continuer la lecture", "Keep reading"))}
<div class="grid grid--2">{case_card(c, other, 0)}
<a class="card card--accent" href="{c.href("cases")}" data-reveal style="--i:1;justify-content:flex-end;min-height:260px"><span class="card__icon">{icon("star")}</span><h3 class="card__title">{c.t("Toutes nos références", "All case studies")}</h3><p class="card__text">{c.t("netiwan GROUPE, CMT GROUP, PUTHOD, L’Ambassade des Langues, ACSP Conseil, tionis, CAMELEON.", "netiwan GROUPE, CMT GROUP, PUTHOD, L’Ambassade des Langues, ACSP Conseil, tionis, CAMELEON.")}</p><span class="card__foot"><span class="card__more">{c.t("Voir", "View")}{icon("arrow-right")}</span></span></a>
</div></div></section>'''
    body += cta_band(c)
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": d["title"], "about": cs["client"],
           "author": {"@id": "https://www.darbtech.net/#organization"}, "publisher": {"@id": "https://www.darbtech.net/#organization"},
           "inLanguage": c.lang}]
    return dict(title=f'{d["title"]} | DarbTech',
                desc=c.t(f"Étude de cas Odoo : {d['short']} Projet mené par DarbTech, Odoo Gold Partner.",
                         f"Odoo case study: {d['short']} A project delivered by DarbTech, Odoo Gold Partner."),
                body=body, trail=trail, ld=ld)


# ---------------------------------------------------------------------------
# Approach / Méthode
# ---------------------------------------------------------------------------
def page_method(c):
    trail = [(c.t("Méthode", "Approach"), None)]
    body = page_hero(c, trail, c.t("Méthode", "Approach"),
                     c.t('Une méthode Agile, <span class="accent accent--gold">transparente et industrialisée</span>', 'An Agile, <span class="accent accent--gold">transparent and industrialised</span> approach'),
                     c.t("Cinq étapes pour mettre en place Odoo, quatre principes pour les mener : c’est ainsi que nous accompagnons nos clients depuis 2015, du cadrage à la maintenance.",
                         "Five steps to roll out Odoo and four principles to run them: this is how we have supported our clients since 2015, from scoping to maintenance."),
                     btn(c.href("contact"), c.t("Parler de votre projet", "Discuss your project"), "primary", magnetic=True),
                     aside=hero_tile("repeat"))
    body += f'''<section class="section" aria-labelledby="steps-title"><div class="container"><div class="method">
<div class="method__intro" data-reveal><span class="eyebrow">{c.t("Les 5 étapes", "The 5 steps")}</span>
<h2 id="steps-title">{c.t("Nous vous accompagnons durant toute la mise en place", "We support you throughout the roll-out")}</h2>
<p class="lead">{c.t("De l’étude de votre activité à la maintenance de votre nouvel outil, chaque étape produit des livrables concrets que vous validez.", "From studying your business to maintaining your new tool, each step produces concrete deliverables that you sign off.")}</p></div>
{method_steps(c, detailed=True)}</div></div></section>'''
    body += f'''<section class="section section--paper" aria-labelledby="values-title"><div class="container">
{section_head(c.t("Nos principes", "Our principles"), c.t('Quatre principes, <span class="accent accent--blue">sur chaque projet</span>', 'Four principles, <span class="accent accent--blue">on every project</span>'), c.t("Ils guident nos équipes au quotidien, à Paris comme à Rabat.", "They guide our teams every day, in Paris and in Rabat."))}
{values_cards(c)}
</div></section>'''
    qa = [
        ("shield", c.t("Qualité et tests", "Quality and testing"), c.t("Plans de test, tests fonctionnels, de régression et d’acceptation, menés avec notre ingénieur QA certifié ISTQB et Odoo.", "Test plans, plus functional, regression and acceptance testing, led with our ISTQB- and Odoo-certified QA engineer.")),
        ("users", c.t("Des ressources dédiées", "Dedicated resources"), c.t("Nous pouvons dédier des ressources exclusivement à votre projet, ou travailler avec nos partenaires et réseaux d’experts.", "We can dedicate resources exclusively to your project, or work with our partners and expert networks.")),
        ("lifebuoy", c.t("Après le go-live", "After go-live"), c.t("Formation, maintenance et évolutions : l’outil suit vos nouvelles activités et vos nouvelles méthodes.", "Training, maintenance and enhancements: the tool keeps up with new activities and new methods.")),
    ]
    body += f'''<section class="section" aria-labelledby="qa-title"><div class="container">
{section_head(c.t("Et aussi", "And also"), c.t("Ce qui fait la différence au quotidien", "What makes the difference day to day"))}
<div class="grid grid--3">{"".join(f'<article class="card" data-reveal style="--i:{i}"><span class="card__icon">{icon(ic)}</span><h3 class="card__title">{t}</h3><p class="card__text">{d}</p></article>' for i, (ic, t, d) in enumerate(qa))}</div>
</div></section>'''
    body += cta_band(c)
    return dict(title=c.t("Notre méthode : Agile, transparente, industrialisée | DarbTech", "Our approach: Agile, transparent, industrialised | DarbTech"),
                desc=c.t("La méthode DarbTech pour vos projets Odoo : 5 étapes, de l’analyse à la maintenance, et 4 principes : Agile-Scrum, DevOps, transparence et engagement.",
                         "DarbTech’s approach to Odoo projects: 5 steps from analysis to maintenance, and 4 principles: Agile-Scrum, DevOps, transparency and commitment."),
                body=body, trail=trail)


# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------
def page_about(c):
    trail = [(c.t("À propos", "About"), None)]
    team = c.data["team"][c.lang]
    body = page_hero(c, trail, c.t("À propos", "About us"),
                     c.t('Des experts Odoo, <span class="accent accent--gold">entre Paris et Rabat</span>', 'Odoo experts, <span class="accent accent--gold">across Paris and Rabat</span>'),
                     c.t("DarbTech accompagne les TPE, PME et ETI des régions francophones et anglophones dans leur transformation digitale, avec Odoo et des équipes de développement dédiées.",
                         "DarbTech helps small, medium and mid-market businesses across French- and English-speaking regions with their digital transformation, through Odoo and dedicated development teams."),
                     chip=True, aside=hero_tile("users"))
    body += f'''<section class="section" aria-labelledby="story-title"><div class="container">
<div class="split"><div class="split__text" data-reveal>
<span class="eyebrow">{c.t("Notre histoire", "Our story")}</span>
<h2 id="story-title">{c.t("Fluidifier les échanges d’un monde interconnecté", "Making an interconnected world work more smoothly")}</h2>
<p class="lead">{c.t("DarbTech est née de la volonté de ses fondateurs d’apporter des services à forte valeur ajoutée en fluidifiant les échanges dans ce grand village qu’est devenu notre monde interconnecté.",
                     "DarbTech was founded to deliver high-value services by making exchanges smoother in the global village our interconnected world has become.")}</p>
<p>{c.t("Présents à Paris et à Rabat, nous intervenons sur deux grands sujets :", "With offices in Paris and Rabat, we focus on two things:")}</p>
{checklist([c.t("la productivité de votre entreprise, grâce à la digitalisation avec un CRM et un ERP ;", "improving your company’s productivity through digitalisation with CRM and ERP;"),
            c.t("la mise à disposition d’équipes dédiées pour vos développements applicatifs spécifiques.", "providing dedicated teams for your custom application development.")])}
</div>
<div class="split__media" data-reveal="scale"><img src="{c.asset("img/team/asilah-2023.webp")}" alt="{c.t("Une partie de l’équipe DarbTech au coucher du soleil, sur une terrasse face à l’océan", "Part of the DarbTech team at sunset, on a terrace overlooking the ocean")}" width="690" height="517" loading="lazy">
<div class="float-card"><span class="card__icon card__icon--gold">{icon("users")}</span><div><strong>{c.t("21 experts", "21 experts")}</strong><span class="muted">{c.t("tous certifiés Odoo", "all Odoo-certified")}</span></div></div></div>
</div>
<div style="margin-top:72px">{stats_light(c)}</div>
</div></section>'''
    body += gold_panel(c)
    body += f'''<section class="section section--paper" aria-labelledby="values-title"><div class="container">
{section_head(c.t("Nos valeurs", "Our values"), c.t("Notre méthodologie, nos engagements", "Our methodology, our commitments"))}
{values_cards(c)}
</div></section>'''
    partners = c.data["partners"]
    body += f'''<section class="section" aria-labelledby="partners-title"><div class="container">
{section_head(c.t("Partenaires", "Partners"), c.t("Nos partenaires", "Our partners"), c.t("Trois partenariats pour couvrir l’ERP, la téléphonie et l’IA de réunion.", "Three partnerships covering ERP, telephony and meeting AI."))}
<div class="grid grid--3">
<article class="card partner" data-reveal>
<div class="partner__logo"><img src="{c.asset("img/partners/odoo.webp")}" alt="Odoo" width="150" height="48" loading="lazy"></div>
<h3 class="card__title">{c.t("Odoo : partenaire depuis 2015, Gold depuis 2026", "Odoo: partner since 2015, Gold since 2026")}</h3>
<p class="card__text">{c.t("Depuis plus de dix ans, nous accompagnons nos clients à travers les versions d’Odoo, de la V8 aux dernières éditions Enterprise et Community. Nous avons été témoins et acteurs de l’évolution de cet ERP, pensé pour les TPE, PME et groupes.",
                           "For more than ten years we have guided our clients through Odoo’s versions, from V8 to the latest Enterprise and Community editions. We have watched this ERP, built for small businesses, SMEs and groups, evolve, and helped shape how it is used.")}</p>
{gold_chip(c, "sm-light")}
</article>
<article class="card partner" data-reveal style="--i:1">
<div class="partner__logo"><img src="{c.asset("img/partners/ringover.png")}" alt="Ringover" width="64" height="64" loading="lazy"></div>
<h3 class="card__title">{c.t("Ringover : partenaire officiel", "Ringover: official partner")}</h3>
<p class="card__text">{c.t("Avec Ringover, leader de la téléphonie cloud d’entreprise, nous optimisons l’expérience client et l’efficacité opérationnelle : CTI, SVI, statistiques avancées et outils collaboratifs.",
                           "With Ringover, a leader in business cloud telephony, we improve customer experience and operational efficiency: CTI, IVR, advanced analytics and collaboration tools.")}</p>
<a class="link-arrow" href="{c.href("odoo_integrations")}">{c.t("Intégration Odoo", "Odoo integration")}{icon("arrow-right")}</a>
</article>
<article class="card partner" data-reveal style="--i:2">
<div class="partner__logo"><img src="{c.asset("img/partners/leexi.webp")}" alt="Leexi.ai" width="120" height="63" loading="lazy"></div>
<h3 class="card__title">{c.t("Leexi.ai : productivité et collaboration", "Leexi.ai: productivity and collaboration")}</h3>
<p class="card__text">{c.t("L’IA conversationnelle de Leexi génère comptes rendus et actions à mener, et les fait remonter dans Odoo grâce à une intégration native. Conforme au RGPD, certifiée ISO 27001.",
                           "Leexi’s conversational AI produces meeting summaries and action items and pushes them into Odoo through a native integration. GDPR-compliant and ISO 27001-certified.")}</p>
<a class="link-arrow" href="{c.href("odoo_integrations")}">{c.t("Intégration Odoo", "Odoo integration")}{icon("arrow-right")}</a>
</article>
</div></div></section>'''
    body += f'''<section class="section section--paper" aria-labelledby="offices-title"><div class="container">
<div class="split"><div class="split__text" data-reveal>
<span class="eyebrow">{c.t("Nos bureaux", "Our offices")}</span>
<h2 id="offices-title">{c.t("Deux bureaux, une seule équipe", "Two offices, one team")}</h2>
<p class="lead">{c.t("Le conseil au plus près de nos clients en France, l’ingénierie ERP et le développement à Rabat.", "Consulting close to our clients in France, ERP engineering and development in Rabat.")}</p>
<div style="display:flex;align-items:center;gap:18px;flex-wrap:wrap">{team_teaser(c, team)}<a class="link-arrow" href="{c.href("team")}">{c.t("Rencontrer l’équipe", "Meet the team")}{icon("arrow-right")}</a></div>
</div>
<div class="grid" style="gap:14px">{offices_cards(c)}</div>
</div></div></section>'''
    body += cta_band(c)
    return dict(title=c.t("À propos de DarbTech, Odoo Gold Partner | Paris & Rabat", "About DarbTech, Odoo Gold Partner | Paris & Rabat"),
                desc=c.t("DarbTech, intégrateur Odoo à Paris et Rabat : notre histoire, nos valeurs (Agile, DevOps, transparence, engagement), nos partenaires Odoo, Ringover et Leexi.ai.",
                         "DarbTech, Odoo integrator in Paris and Rabat: our story, our values (Agile, DevOps, transparency, commitment) and our partners Odoo, Ringover and Leexi.ai."),
                body=body, trail=trail)


# ---------------------------------------------------------------------------
# Team
# ---------------------------------------------------------------------------
GROUPS = [
    ("all", "Tous", "All"),
    ("lead", "Direction", "Leadership"),
    ("consult", "Conseil", "Consulting"),
    ("erp", "Ingénierie ERP", "ERP engineering"),
    ("tech", "Tech & QA", "Tech & QA"),
    ("admin", "Admin & ventes", "Admin & sales"),
]


def page_team(c):
    trail = [(c.t("À propos", "About"), "about"), (c.t("Équipe", "Team"), None)]
    team = c.data["team"][c.lang]
    counts = {g[0]: 0 for g in GROUPS}
    for m in team:
        counts["all"] += 1
        for g in m["groups"]:
            counts[g] += 1
    filters = "".join(f'<button class="filter-btn" type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{fr if c.lang == "fr" else en}<span>{counts[k]}</span></button>'
                      for k, fr, en in GROUPS)
    cards, tpls = [], []
    for i, m in enumerate(team):
        certs = "".join(f'<span class="tag{" tag--gold" if x == "Odoo" else ""}">{esc(x)}</span>' for x in m["certs"])
        cards.append(f'''<li class="member" data-group="{" ".join(m["groups"])}" id="{m["slug"]}" data-reveal style="--i:{i % 4}">
<button class="member__btn" type="button" data-bio="bio-{m["slug"]}" aria-haspopup="dialog">
<span class="member__photo"><img src="{c.asset(m["photo"])}" alt="{esc(c.t("Portrait de ", "Portrait of ") + m["display"])}" loading="lazy" decoding="async" width="480" height="600"><span class="member__open">{icon("plus")}</span></span>
<span class="member__info"><span class="member__name">{esc(m["display"])}</span><span class="member__role">{esc(m["role"])}</span>
<span class="member__certs">{certs}</span><span class="visually-hidden">{c.t("Lire la biographie", "Read biography")}</span></span>
</button></li>''')
        bio = "".join(f"<p>{esc(p)}</p>" for p in m["bio"])
        tpls.append(f'''<template id="bio-{m["slug"]}"><div class="modal__grid">
<div class="modal__photo"><img src="{c.asset(m["photo"])}" alt="{esc(c.t("Portrait de ", "Portrait of ") + m["display"])}"></div>
<div class="modal__body"><h2 id="bio-title">{esc(m["display"])}</h2><p class="modal__role">{esc(m["role"])}</p>
<div class="tags">{"".join(f'<span class="tag{" tag--gold" if x == "Odoo" else ""}">{c.t("Certifié·e ", "Certified ") + esc(x)}</span>' for x in m["certs"])}</div>
<div class="modal__bio">{bio}</div>
<a class="btn btn--outline btn--sm" href="{esc(m["linkedin"])}" target="_blank" rel="noopener">{icon("linkedin")}LinkedIn<span class="visually-hidden"> {c.t("(nouvel onglet)", "(new tab)")}</span></a>
</div></div></template>''')
    body = page_hero(c, trail, c.t("L’équipe", "The team"),
                     c.t('21 experts, <span class="accent accent--gold">tous certifiés Odoo</span>', '21 experts, <span class="accent accent--gold">all Odoo-certified</span>'),
                     c.t("Direction, conseil, ingénierie ERP, développement et qualité : faites connaissance avec les personnes qui mènent vos projets, à Paris et à Rabat.",
                         "Leadership, consulting, ERP engineering, development and quality: meet the people who run your projects, in Paris and Rabat."),
                     btn(c.href("careers"), c.t("Nous rejoindre", "Join us"), "ghost", arrow=True), chip=True)
    body += f'''<section class="section" aria-labelledby="team-title"><div class="container">
<h2 id="team-title" class="visually-hidden">{c.t("Membres de l’équipe", "Team members")}</h2>
<div class="filters" role="group" aria-label="{c.t("Filtrer par pôle", "Filter by team")}">{filters}</div>
<p id="team-count" class="visually-hidden" aria-live="polite" data-tpl="{c.t("{n} personnes affichées", "{n} people shown")}"></p>
<ul class="team-grid">{"".join(cards)}</ul>
</div></section>
<dialog class="modal" id="bio-modal" aria-labelledby="bio-title">
<button class="modal__close" type="button" aria-label="{c.t("Fermer", "Close")}">{icon("x")}</button>
<div class="modal__content"></div>
</dialog>
{"".join(tpls)}'''
    body += cta_band(c, c.t('Envie de travailler <span class="accent accent--gold">avec nous</span> ?', 'Want to work <span class="accent accent--gold">with us</span>?'))
    return dict(title=c.t("L’équipe DarbTech : 21 experts certifiés Odoo", "The DarbTech team: 21 Odoo-certified experts"),
                desc=c.t("Rencontrez l’équipe DarbTech : direction, consultants, ingénieurs ERP, développeurs Odoo et QA, tous certifiés Odoo, à Paris et à Rabat.",
                         "Meet the DarbTech team: leadership, consultants, ERP engineers, Odoo developers and QA, all Odoo-certified, in Paris and Rabat."),
                body=body, trail=trail)


# ---------------------------------------------------------------------------
# Careers
# ---------------------------------------------------------------------------
JOBS = [
    ("odoo-developer-junior-1-an-d-experience-4",
     "Développeur Odoo junior (1 an d’expérience et +)", "Junior Odoo Developer (1+ year of experience)",
     "Développement et personnalisation de modules Odoo en Python, sur des projets Agile de digitalisation, d’automatisation, d’API et d’intégration d’IA.",
     "Develop and customise Odoo modules in Python on Agile projects covering digitalisation, automation, APIs and AI integration.",
     [], ["Python", "Odoo"]),
    ("odoo-developer-confirme-3-ans-d-experience-5",
     "Développeur Odoo confirmé (3 ans d’expérience et +)", "Experienced Odoo Developer (3+ years of experience)",
     "Conception et développement de modules Odoo avancés, intégrations via les API et optimisation des performances.",
     "Design and build advanced Odoo modules, API integrations and performance improvements.",
     [], ["Python", "Odoo", "API"]),
    ("stagiaire-odoo-stage-pfe-7",
     "Stagiaire Odoo : stage de fin d’études (PFE)", "Odoo Intern: final-year project",
     "Un stage au sein de l’équipe de développement Odoo, sur des projets clients réels.",
     "An internship in the Odoo development team, working on real client projects.",
     [], [("Stage", "Internship"), "Python"]),
    ("consultant-technique-et-fonctionnel-odoo-11",
     "Consultant technique et fonctionnel Odoo", "Odoo Technical & Functional Consultant",
     "Analyse des besoins clients, conception et paramétrage de solutions Odoo, accompagnement de leur mise en œuvre.",
     "Analyse client needs, design and configure Odoo solutions, and guide their roll-out.",
     [], [("Conseil", "Consulting"), "Odoo"]),
    ("chef-de-projet-odoo-agile-8",
     "Chef de projet Odoo Agile", "Agile Odoo Project Manager",
     "Pilotage complet de projets Odoo en Agile : objectifs, planification, budget, risques, ressources et relation client.",
     "End-to-end management of Agile Odoo projects: goals, planning, budget, risks, resources and client relationship.",
     [], ["Agile", "SAFe / PMP"]),
    ("odoo-tester-assurance-qualite-6",
     "Testeur Odoo : assurance qualité", "Odoo QA Tester",
     "Conception et exécution des plans de test des applications Odoo, suivi des anomalies avec l’équipe de développement.",
     "Design and run test plans for Odoo applications, and track defects with the development team.",
     [], ["QA", "ISTQB"]),
    ("charge-e-de-mission-commerciale-et-administrative-12",
     "Chargé(e) de mission commerciale et administrative (stage)", "Sales & Administrative Officer (internship)",
     "Stage de 6 mois minimum, avec perspective d’embauche : gestion commerciale, support administratif et outils digitaux, aux côtés de la direction.",
     "Internship of at least 6 months with a view to hiring: sales management, administrative support and digital tools, working with management.",
     [], [("Stage 6 mois", "6-month internship"), ("Hybride", "Hybrid")]),
]


EN_JOB_SLUGS = {  # live English URLs (analysis/link_status.txt, HTTP 200)
    "odoo-developer-junior-1-an-d-experience-4": "odoo-developer-junior-1-year-of-experience-4",
    "odoo-developer-confirme-3-ans-d-experience-5": "odoo-developer-advanced-3-years-of-experience-5",
    "stagiaire-odoo-stage-pfe-7": "odoo-internship-7",
    "consultant-technique-et-fonctionnel-odoo-11": "odoo-technical-functional-consultant-11",
    "chef-de-projet-odoo-agile-8": "odoo-agile-project-manager-8",
    "odoo-tester-assurance-qualite-6": "qa-tester-6",
    "charge-e-de-mission-commerciale-et-administrative-12": "administrative-assistant-12",
}


def page_careers(c):
    trail = [(c.t("Carrières", "Careers"), None)]
    perks = [
        ("graduation", c.t("Certifié·e Odoo", "Odoo-certified"), c.t("Formation et certification Odoo dès l’embauche.", "Odoo training and certification from day one.")),
        ("home", "Flex office", c.t("Deux jours par semaine sur site à Rabat, le reste en flexibilité.", "Two days a week on site in Rabat, the rest flexible.")),
        ("repeat", c.t("Projets Agile", "Agile projects"), c.t("Digitalisation, automatisation, API et intégration d’IA.", "Digitalisation, automation, APIs and AI integration.")),
        ("chart", c.t("Évolution", "Growth"), c.t("Des perspectives d’évolution au sein de l’entreprise.", "Room to grow within the company.")),
        ("users", c.t("Experts certifiés", "Certified experts"), c.t("Apprendre aux côtés de profils Odoo, ISTQB, SAFe et CSPO.", "Learn alongside Odoo, ISTQB, SAFe and CSPO-certified colleagues.")),
        ("globe", c.t("Clients internationaux", "International clients"), c.t("Des projets pour des entreprises francophones et anglophones.", "Projects for French- and English-speaking companies.")),
    ]
    perk_html = "".join(f'<article class="card" data-reveal style="--i:{i % 3}"><span class="card__icon{" card__icon--gold" if i == 0 else ""}">{icon(ic)}</span><h3 class="card__title">{t}</h3><p class="card__text">{d}</p></article>'
                        for i, (ic, t, d) in enumerate(perks))
    base = "https://www.darbtech.net" + ("/en" if c.lang == "en" else "")
    jobs = []
    for i, (slug, tfr, ten, sfr, sen, _unused, tg) in enumerate(JOBS):
        tl = [x if isinstance(x, str) else (x[0] if c.lang == "fr" else x[1]) for x in tg]
        meta = f'<span class="tag tag--blue">{icon("pin")}Rabat, {c.t("Maroc", "Morocco")}</span>' + "".join(f'<span class="tag">{esc(x)}</span>' for x in tl)
        url = base + "/jobs/" + (slug if c.lang == "fr" else EN_JOB_SLUGS[slug])
        jobs.append(f'''<li><a class="job" href="{url}" data-reveal style="--i:{i % 3}">
<div><h3 class="job__title">{tfr if c.lang == "fr" else ten}</h3><p class="job__summary">{sfr if c.lang == "fr" else sen}</p><div class="job__meta">{meta}</div></div>
<span class="job__cta">{c.t("Voir l’offre et postuler", "View and apply")}{icon("arrow-up-right")}</span></a></li>''')
    body = page_hero(c, trail, c.t("Carrières", "Careers"),
                     c.t('Rejoignez un partenaire <span class="accent accent--gold">Odoo Gold</span>', 'Join an <span class="accent accent--gold">Odoo Gold</span> partner'),
                     c.t("Développeurs, consultants, chefs de projet, testeurs : nous recrutons à Rabat des talents qui veulent grandir sur des projets Odoo exigeants.",
                         "Developers, consultants, project managers, testers: we are hiring in Rabat for people who want to grow on demanding Odoo projects."),
                     btn("#jobs", c.t("Voir les 7 offres", "See the 7 openings"), "primary", magnetic=True),
                     chip=True,
                     aside=f'<div class="hero-tile hero-tile--photo"><img src="{c.asset("img/team/asilah-2023.webp")}" alt="" width="690" height="517"></div>')
    body += f'''<section class="section" aria-labelledby="why-title"><div class="container">
{section_head(c.t("Pourquoi nous rejoindre", "Why join us"), c.t("Grandir avec une équipe certifiée", "Grow with a certified team"))}
<div class="grid grid--3">{perk_html}</div>
</div></section>
<section class="section section--paper" id="jobs" aria-labelledby="jobs-title"><div class="container">
{section_head(c.t("Offres", "Openings"), c.t("7 postes ouverts à Rabat", "7 open roles in Rabat"), c.t("Les candidatures se font sur notre espace emploi Odoo : chaque offre ouvre la page détaillée et le formulaire de candidature.", "Applications go through our Odoo jobs portal: each opening links to its full description and application form."))}
<ul class="jobs">{"".join(jobs)}</ul>
<div class="card" data-reveal style="margin-top:24px;flex-direction:row;flex-wrap:wrap;align-items:center;justify-content:space-between">
<div><h3 class="card__title">{c.t("Candidature spontanée", "Speculative application")}</h3><p class="card__text">{c.t("Aucune offre ne vous correspond ? Écrivez-nous.", "No opening fits? Write to us.")}</p></div>
<a class="btn btn--dark" href="mailto:rh@darbtech.net">{icon("mail")}rh@darbtech.net</a></div>
</div></section>'''
    body += cta_band(c, c.t('Une question sur un poste ? <span class="accent accent--gold">Parlons-en</span>', 'A question about a role? <span class="accent accent--gold">Let’s talk</span>'),
                     c.t("Notre équipe RH vous répond. Les candidatures se font via les offres ci-dessus ou par e-mail à rh@darbtech.net.",
                         "Our HR team will get back to you. Apply through the openings above or by email at rh@darbtech.net."))
    return dict(title=c.t("Carrières : 7 postes Odoo à Rabat | DarbTech", "Careers: 7 Odoo roles in Rabat | DarbTech"),
                desc=c.t("Rejoignez DarbTech, Odoo Gold Partner : développeurs Odoo, consultants, chef de projet Agile, testeur QA et stages à Rabat. Certification Odoo et flex office.",
                         "Join DarbTech, Odoo Gold Partner: Odoo developers, consultants, Agile project manager, QA tester and internships in Rabat. Odoo certification and flex office."),
                body=body, trail=trail)


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------
def page_contact(c):
    trail = [("Contact", None)]
    topics = [c.t("Projet Odoo", "Odoo project"), c.t("Migration", "Migration"), c.t("Développement", "Development"),
              c.t("Support", "Support"), c.t("Recrutement", "Careers"), c.t("Autre", "Other")]
    topic_html = "".join(f'<label class="topic"><input type="radio" name="topic" value="{esc(t)}" required{" checked" if i == 0 else ""}><span>{esc(t)}</span></label>'
                         for i, t in enumerate(topics))
    req = c.t("Ce champ est obligatoire.", "This field is required.")
    p, r = OFFICES["paris"], OFFICES["rabat"]
    bridge = f'''<div class="bridge" aria-hidden="true"><svg viewBox="0 0 400 170" fill="none">
<path class="bridge__path" d="M60 120 C 140 10, 260 10, 340 120" stroke="url(#bg)" stroke-width="2"/>
<defs><linearGradient id="bg" x1="60" x2="340" y1="0" y2="0" gradientUnits="userSpaceOnUse"><stop stop-color="#4C8DFF"/><stop offset="1" stop-color="#E9C46A"/></linearGradient></defs>
<circle cx="60" cy="120" r="7" fill="#4C8DFF"/><circle cx="60" cy="120" r="16" stroke="#4C8DFF" stroke-opacity=".35"/>
<circle cx="340" cy="120" r="7" fill="#E9C46A"/><circle cx="340" cy="120" r="16" stroke="#E9C46A" stroke-opacity=".35"/>
<text x="60" y="155" fill="#E8ECF7" font-size="14" text-anchor="middle" font-family="Geist, sans-serif">Paris</text>
<text x="340" y="155" fill="#E8ECF7" font-size="14" text-anchor="middle" font-family="Geist, sans-serif">Rabat</text>
</svg></div>'''
    body = page_hero(c, trail, "Contact",
                     c.t('Parlons de <span class="accent accent--gold">votre projet</span>', 'Let’s talk about <span class="accent accent--gold">your project</span>'),
                     c.t("Une question sur Odoo, un projet de migration ou de développement ? Laissez-nous quelques lignes : un consultant certifié vous recontacte rapidement.",
                         "A question about Odoo, a migration or a development project? Drop us a few lines and a certified consultant will get back to you shortly."),
                     chip=True)
    body += f'''<section class="section" aria-label="{c.t("Formulaire et coordonnées", "Form and contact details")}"><div class="container">
<div class="contact-grid">
<div class="form-card" data-reveal>
<form class="form" id="contact-form" action="#" method="post">
<div><h2 style="font-size:1.6rem">{c.t("Votre demande", "Your enquiry")}</h2><p class="muted" style="margin-top:6px">{c.t("Les champs marqués d’un astérisque (*) sont obligatoires.", "Fields marked with an asterisk (*) are required.")}</p></div>
<div class="form__row">
<div class="field"><label for="f-name">{c.t("Nom et prénom", "Full name")} *</label><input id="f-name" name="name" type="text" autocomplete="name" required aria-describedby="e-name"><span class="field__error" id="e-name">{req}</span></div>
<div class="field"><label for="f-email">{c.t("E-mail professionnel", "Work email")} *</label><input id="f-email" name="email" type="email" autocomplete="email" required aria-describedby="e-email"><span class="field__error" id="e-email">{c.t("Saisissez une adresse e-mail valide.", "Enter a valid email address.")}</span></div>
</div>
<div class="form__row">
<div class="field"><label for="f-company">{c.t("Entreprise", "Company")} *</label><input id="f-company" name="company" type="text" autocomplete="organization" required aria-describedby="e-company"><span class="field__error" id="e-company">{req}</span></div>
<div class="field"><label for="f-phone">{c.t("Téléphone", "Phone")} <span class="opt">({c.t("facultatif", "optional")})</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
</div>
<fieldset class="field"><legend>{c.t("Sujet", "Topic")} *</legend><div class="topics">{topic_html}</div></fieldset>
<div class="field"><label for="f-msg">{c.t("Votre message", "Your message")} *</label><textarea id="f-msg" name="message" required aria-describedby="e-msg" placeholder="{c.t("Votre contexte, vos objectifs, vos délais…", "Your context, goals and timeline…")}"></textarea><span class="field__error" id="e-msg">{req}</span></div>
<div class="field"><label class="consent"><input type="checkbox" name="consent" required aria-describedby="e-consent"><span>{c.t("J’accepte que DarbTech utilise ces informations pour répondre à ma demande, conformément à la ", "I agree that DarbTech may use this information to respond to my enquiry, in line with the ")}<a href="{c.href("privacy")}">{c.t("politique de confidentialité", "privacy policy")}</a>. *</span></label><span class="field__error" id="e-consent">{c.t("Votre accord est nécessaire pour traiter la demande.", "Your consent is needed to process the enquiry.")}</span></div>
<div style="display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between">
<button class="btn btn--primary" type="submit" data-magnetic>{c.t("Envoyer", "Send")}{icon("arrow-right")}</button>
<p class="form__note">{c.t("Démonstration statique : aucune donnée n’est envoyée.", "Static demo: no data is sent.")}</p>
</div>
</form>
<div class="form-success" role="status">
<span class="success-icon">{icon("check")}</span>
<h2>{c.t("Merci, c’est noté !", "Thank you, message received!")}</h2>
<p class="muted" style="max-width:44ch">{c.t("Un consultant certifié revient vers vous rapidement. (Version de démonstration : le message n’a pas été transmis.)", "A certified consultant will get back to you shortly. (Demo version: the message was not actually sent.)")}</p>
<button class="btn btn--outline btn--sm" type="button" data-form-reset>{c.t("Envoyer un autre message", "Send another message")}</button>
</div>
</div>
<aside class="grid" style="gap:14px" aria-label="{c.t("Coordonnées", "Contact details")}">
{bridge}
{offices_cards(c)}
<div class="office" data-reveal>
<a class="office__line" href="mailto:{EMAIL}">{icon("mail")}{EMAIL}</a>
<a class="office__line" href="{LINKEDIN}" target="_blank" rel="noopener">{icon("linkedin")}LinkedIn<span class="visually-hidden"> {c.t("(nouvel onglet)", "(new tab)")}</span></a>
<a class="office__line" href="{c.href("careers")}">{icon("briefcase")}{c.t("Candidatures : rh@darbtech.net", "Jobs: rh@darbtech.net")}</a>
</div>
</aside>
</div></div></section>'''
    ld = [{"@context": "https://schema.org", "@type": "ContactPage", "name": c.t("Contact DarbTech", "Contact DarbTech"),
           "about": {"@id": "https://www.darbtech.net/#organization"}}]
    return dict(title=c.t("Contact : parlez à un expert Odoo | DarbTech", "Contact: talk to an Odoo expert | DarbTech"),
                desc=c.t("Contactez DarbTech, Odoo Gold Partner, à Paris (+33 1 88 33 41 64) ou à Rabat (+212 770 86 2295) pour votre projet Odoo, de migration ou de développement.",
                         "Contact DarbTech, Odoo Gold Partner, in Paris (+33 1 88 33 41 64) or Rabat (+212 770 86 2295) about your Odoo, migration or development project."),
                body=body, trail=trail, ld=ld)


# ---------------------------------------------------------------------------
# Legal pages
# ---------------------------------------------------------------------------
def legal_layout(c, trail, title, lead, sections, updated=True):
    toc = "".join(f'<li><a href="#{sid}">{t}</a></li>' for sid, t, _ in sections)
    content = "".join(f'<h2 id="{sid}">{t}</h2>{html}' for sid, t, html in sections)
    upd = f'<p class="muted" style="font-size:.88rem">{c.t("Dernière mise à jour : octobre 2026", "Last updated: October 2026")}</p>' if updated else ""
    body = page_hero(c, trail, c.t("Informations légales", "Legal information"), title, lead)
    body += f'''<section class="section"><div class="container"><div class="legal-layout">
<aside><ul class="toc">{toc}</ul></aside>
<div class="prose">{upd}{content}</div>
</div></div></section>'''
    return body


def page_legal(c):
    trail = [(c.t("Mentions légales", "Legal notice"), None)]
    s = [
        ("editeur", c.t("Éditeur du site", "Website publisher"), f'''<dl>
<dt>{c.t("Société", "Company")}</dt><dd>DarbTech Labs SAS</dd>
<dt>{c.t("Capital social", "Share capital")}</dt><dd>10 000 €</dd>
<dt>RCS</dt><dd>850 857 046 RCS Paris</dd>
<dt>{c.t("TVA intracommunautaire", "EU VAT number")}</dt><dd>FR 48 850 857 046</dd>
<dt>{c.t("Siège social", "Registered office")}</dt><dd>36 rue Boussingault, 75013 Paris, France</dd>
<dt>{c.t("Bureaux", "Office")}</dt><dd>122 Av. Daumesnil, 75012 Paris, France</dd>
<dt>{c.t("Téléphone", "Phone")}</dt><dd><a href="tel:+33188334164">+33 1 88 33 41 64</a></dd>
<dt>E-mail</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
<dt>{c.t("Directeur de la publication", "Publication director")}</dt><dd>{c.t("[À compléter]", "[To be completed]")}</dd>
</dl>'''),
        ("maroc", c.t("Bureau de Rabat", "Rabat office"), f'''<p>DarbTech SARL, Résidence Oum Kalthoum, Bd Hassan II, Agdal, 10120 Rabat, {c.t("Maroc", "Morocco")}. {c.t("Tél.", "Phone")} <a href="tel:+212770862295">+212 770 86 2295</a>.</p>
<p class="note">{c.t("[Identifiants légaux de DarbTech SARL (RC, ICE) à compléter.]", "[DarbTech SARL legal identifiers (RC, ICE) to be completed.]")}</p>'''),
        ("hebergement", c.t("Hébergement", "Hosting"), f'<p class="note">{c.t("[Nom, adresse et téléphone de l’hébergeur à compléter.]", "[Host name, address and phone number to be completed.]")}</p>'),
        ("cgu", c.t("Conditions d’utilisation", "Terms of use"), c.t('''<p>Le site darbtech.net est le site vitrine de DarbTech Labs, qui présente les services du groupe. En y accédant, vous vous engagez à l’utiliser loyalement et dans le respect des lois et règlements en vigueur.</p>
<p>Nous pouvons modifier ces conditions à tout moment ; la version en vigueur est celle publiée sur cette page.</p>''', '''<p>darbtech.net is the corporate website of DarbTech Labs, presenting the group’s services. By using it, you agree to do so fairly and in compliance with applicable laws and regulations.</p>
<p>We may change these terms at any time; the version in force is the one published on this page.</p>''')),
        ("responsabilite", c.t("Responsabilité", "Liability"), c.t('''<p>Nous ne sommes pas responsables du contenu des sites tiers vers lesquels renvoient des liens présents sur le site. L’accès au site peut être interrompu, notamment pour maintenance ou mise à jour, sans que notre responsabilité puisse être engagée.</p>
<p>Vous êtes seul responsable de l’usage que vous faites du site et des informations qu’il contient, ainsi que de la protection de vos équipements contre d’éventuels virus.</p>''', '''<p>We are not responsible for the content of third-party websites linked from this site. Access to the site may be interrupted, in particular for maintenance or updates, without any liability on our part.</p>
<p>You alone are responsible for how you use the site and its information, and for protecting your equipment against viruses.</p>''')),
        ("pi", c.t("Propriété intellectuelle", "Intellectual property"), c.t('''<p>Le site, dans ses composantes techniques, graphiques, textuelles et de navigation, est la propriété de DarbTech Labs ou fait l’objet d’un droit d’utilisation. Toute reproduction ou exploitation non autorisée est interdite. Odoo, Ringover et Leexi sont des marques de leurs titulaires respectifs.</p>''', '''<p>The site, including its technical, graphic, text and navigation elements, is owned by DarbTech Labs or used under licence. Any unauthorised reproduction or use is prohibited. Odoo, Ringover and Leexi are trademarks of their respective owners.</p>''')),
        ("donnees", c.t("Données personnelles", "Personal data"), f'<p>{c.t("Le traitement de vos données est décrit dans notre ", "How we process your data is described in our ")}<a href="{c.href("privacy")}">{c.t("politique de confidentialité", "privacy policy")}</a>.</p>'),
        ("droit", c.t("Droit applicable", "Governing law"), c.t('<p>Les présentes mentions sont régies par le droit français. Tout litige relève de la compétence des tribunaux de Paris.</p>', '<p>This notice is governed by French law. Any dispute falls under the jurisdiction of the courts of Paris.</p>')),
    ]
    body = legal_layout(c, trail, c.t("Mentions légales", "Legal notice"), c.t("Informations sur l’éditeur du site darbtech.net et conditions d’utilisation.", "Information about the publisher of darbtech.net and terms of use."), s)
    return dict(title=c.t("Mentions légales | DarbTech", "Legal notice | DarbTech"),
                desc=c.t("Mentions légales de darbtech.net : éditeur DarbTech Labs SAS (RCS Paris 850 857 046), bureaux de Paris et Rabat, conditions d’utilisation.",
                         "Legal notice for darbtech.net: publisher DarbTech Labs SAS (RCS Paris 850 857 046), Paris and Rabat offices, terms of use."),
                body=body, trail=trail)


def page_privacy(c):
    trail = [(c.t("Confidentialité", "Privacy"), None)]
    s = [
        ("responsable", c.t("Responsable du traitement", "Data controller"), c.t(f'<p>DarbTech Labs SAS, 122 Av. Daumesnil, 75012 Paris. Contact : <a href="mailto:dpo@darbtech.net">dpo@darbtech.net</a>.</p>', f'<p>DarbTech Labs SAS, 122 Av. Daumesnil, 75012 Paris, France. Contact: <a href="mailto:dpo@darbtech.net">dpo@darbtech.net</a>.</p>')),
        ("donnees", c.t("Données collectées", "Data we collect"), c.t('''<p>Via le formulaire de contact : nom et prénom, e-mail, entreprise, téléphone (facultatif), sujet et message. Les champs marqués d’un astérisque sont obligatoires ; sans eux, nous ne pouvons pas répondre à votre demande.</p>''', '''<p>Through the contact form: full name, email, company, phone (optional), topic and message. Fields marked with an asterisk are required; without them we cannot answer your enquiry.</p>''')),
        ("finalites", c.t("Finalités et base légale", "Purposes and legal basis"), c.t('''<p>Vos données servent à répondre à votre demande et à gérer notre relation avec vous. Ce traitement repose sur votre consentement, recueilli dans le formulaire. Elles sont destinées exclusivement à DarbTech et à ses filiales.</p>''', '''<p>Your data is used to answer your enquiry and manage our relationship with you. This processing is based on your consent, given in the form. It is intended solely for DarbTech and its subsidiaries.</p>''')),
        ("conservation", c.t("Durée de conservation", "Retention"), c.t('<p>Trois (3) ans à compter de notre dernier contact.</p>', '<p>Three (3) years from our last contact.</p>')),
        ("droits", c.t("Vos droits", "Your rights"), c.t('''<p>Conformément à la loi Informatique et Libertés et au RGPD, vous disposez d’un droit d’accès, de rectification, d’effacement, d’opposition, de limitation et de portabilité, ainsi que du droit de définir des directives sur le sort de vos données après votre décès.</p>
<p>Pour les exercer, écrivez à <a href="mailto:dpo@darbtech.net">dpo@darbtech.net</a> ou à DarbTech Labs SAS, 122 Av. Daumesnil, 75012 Paris, en joignant une copie d’une pièce d’identité. Vous pouvez aussi introduire une réclamation auprès de la CNIL.</p>''', '''<p>Under the French Data Protection Act and the GDPR, you have the right to access, rectify, erase, object to, restrict and port your data, and to set instructions for what happens to it after your death.</p>
<p>To exercise these rights, write to <a href="mailto:dpo@darbtech.net">dpo@darbtech.net</a> or to DarbTech Labs SAS, 122 Av. Daumesnil, 75012 Paris, France, enclosing a copy of an ID document. You may also lodge a complaint with the CNIL, the French data protection authority.</p>''')),
        ("securite", c.t("Sécurité", "Security"), c.t('<p>Nous prenons les mesures nécessaires pour que vos données ne soient ni perdues, ni détournées, ni consultées, modifiées ou divulguées par des tiers non autorisés.</p>', '<p>We take the necessary measures so that your data is not lost, misused, or accessed, altered or disclosed by unauthorised third parties.</p>')),
        ("cookies", c.t("Cookies et services tiers", "Cookies and third-party services"), c.t('''<p>Ce site ne dépose pas de cookie de mesure d’audience ni de cookie publicitaire. Les polices de caractères sont chargées depuis Google Fonts, ce qui transmet votre adresse IP à Google. Si des cookies soumis à consentement étaient ajoutés, ils ne seraient déposés qu’après votre accord.</p>
<p class="note">[À valider par DarbTech avant mise en ligne, selon les outils réellement utilisés.]</p>''', '''<p>This site sets no analytics or advertising cookies. Fonts are loaded from Google Fonts, which sends your IP address to Google. If cookies requiring consent were ever added, they would only be set after you agree.</p>
<p class="note">[To be validated by DarbTech before launch, based on the tools actually in use.]</p>''')),
    ]
    body = legal_layout(c, trail, c.t("Politique de confidentialité", "Privacy policy"), c.t("Comment DarbTech collecte, utilise et protège vos données personnelles.", "How DarbTech collects, uses and protects your personal data."), s)
    return dict(title=c.t("Politique de confidentialité | DarbTech", "Privacy policy | DarbTech"),
                desc=c.t("Politique de confidentialité de DarbTech : données collectées, finalités, durée de conservation, droits RGPD et contact DPO (dpo@darbtech.net).",
                         "DarbTech privacy policy: data collected, purposes, retention, GDPR rights and DPO contact (dpo@darbtech.net)."),
                body=body, trail=trail)


def page_terms(c):
    trail = [(c.t("CGV", "Terms of sale"), None)]
    items_fr = [
        ("cg", "Conditions applicables", "Le client renonce expressément à ses propres conditions générales, même établies après les présentes. Toute dérogation doit être acceptée au préalable et par écrit."),
        ("paiement", "Paiement", "Nos factures sont payables sous 21 jours ouvrés, sauf autre délai indiqué sur la facture ou la commande. En cas de non-paiement à l’échéance, DarbTech se réserve le droit de demander une indemnité forfaitaire de 10 % de la somme restant due, et peut suspendre ses prestations sans préavis."),
        ("recouvrement", "Recouvrement", "Si un paiement reste dû plus de soixante (60) jours après son échéance, DarbTech se réserve le droit de faire appel à une société de recouvrement. Tous les frais de justice sont à la charge du client."),
        ("retenue", "Retenue à la source", "Certains pays appliquent une retenue à la source sur le montant des factures. Cette retenue est versée par le client aux autorités fiscales ; le montant de la facture reste intégralement dû à DarbTech."),
        ("obligations", "Obligations", "DarbTech s’engage à fournir des prestations de qualité dans les délais convenus. Ses obligations sont des obligations de moyens et non de résultat. DarbTech ne peut être appelée en garantie dans le cadre d’une réclamation formée contre le client par un consommateur final."),
        ("reclamations", "Réclamations", "Toute réclamation doit, pour être recevable, être notifiée par lettre recommandée au siège de DarbTech dans les 8 jours suivant la livraison ou la prestation."),
        ("droit", "Droit applicable", "Nos relations contractuelles sont régies exclusivement par le droit marocain."),
    ]
    items_en = [
        ("cg", "Applicable terms", "The client expressly waives its own general terms and conditions, even if drawn up after these terms. Any derogation must be agreed in advance and in writing."),
        ("paiement", "Payment", "Our invoices are payable within 21 working days, unless another timeframe is stated on the invoice or order. If payment is late, DarbTech may claim a fixed charge of 10% of the outstanding amount and may suspend its services without notice."),
        ("recouvrement", "Debt recovery", "If a payment is still outstanding more than sixty (60) days after its due date, DarbTech may instruct a debt recovery company. All legal costs are payable by the client."),
        ("retenue", "Withholding tax", "Some countries apply withholding tax to invoices. Any such withholding is paid by the client to the tax authorities; the full invoice amount remains due to DarbTech."),
        ("obligations", "Obligations", "DarbTech undertakes to deliver quality services within the agreed timeframes. Its obligations are best-efforts obligations, not obligations of result. DarbTech cannot be joined as a third party to any claim brought against the client by an end consumer."),
        ("reclamations", "Claims", "To be admissible, any claim must be sent by recorded delivery to DarbTech’s registered office within 8 days of delivery of the goods or services."),
        ("droit", "Governing law", "All our contractual relations are governed exclusively by Moroccan law."),
    ]
    items = items_fr if c.lang == "fr" else items_en
    s = [(sid, t, f"<p>{txt}</p>") for sid, t, txt in items]
    s.insert(0, ("entite", c.t("Entité contractante", "Contracting entity"),
                 f'<p>{c.t("Les présentes conditions générales de vente sont celles de DarbTech SARL.", "These standard terms of sale are those of DarbTech SARL.")}</p>'
                 f'<p class="note">{c.t("[Entité contractante à confirmer : DarbTech Labs SAS (France) ou DarbTech SARL (Maroc).]", "[Contracting entity to be confirmed: DarbTech Labs SAS (France) or DarbTech SARL (Morocco).]")}</p>'))
    body = legal_layout(c, trail, c.t("Conditions générales de vente", "Standard terms of sale"), c.t("Les conditions qui s’appliquent à nos prestations.", "The terms that apply to our services."), s)
    return dict(title=c.t("Conditions générales de vente | DarbTech", "Standard terms of sale | DarbTech"),
                desc=c.t("Conditions générales de vente de DarbTech : paiement à 21 jours ouvrés, recouvrement, retenue à la source, obligations de moyens, réclamations et droit applicable.",
                         "DarbTech standard terms of sale: payment within 21 working days, debt recovery, withholding tax, best-efforts obligations, claims and governing law."),
                body=body, trail=trail)


# ---------------------------------------------------------------------------
# 404
# ---------------------------------------------------------------------------
def page_404(c):
    links = [("odoo", c.t("Services Odoo", "Odoo services")), ("cases", c.t("Références", "Case studies")),
             ("team", c.t("L’équipe", "Team")), ("careers", c.t("Carrières", "Careers"))]
    quick = "".join(f'<li class="tag tag--dark"><a href="{c.href(p)}" style="color:inherit;text-decoration:none">{t}</a></li>' for p, t in links)
    body = f'''<section class="hero notfound">{hero_bg(canvas=True)}
<div class="container notfound__inner">
<p class="notfound__code" aria-hidden="true">404</p>
<h1 style="font-size:var(--fs-h2)">{c.t("Cette page s’est égarée", "This page got lost")}</h1>
<p class="lead" style="color:var(--on-dark-muted)">{c.t("Le lien est peut-être ancien : notre site a été entièrement repensé. Voici de quoi retrouver votre chemin.", "The link may be outdated: our website has been completely redesigned. Here is how to find your way.")}</p>
<div class="hero__ctas">{btn(c.href("home"), c.t("Retour à l’accueil", "Back to home"), "primary")}{btn(c.href("contact"), c.t("Nous contacter", "Contact us"), "ghost", arrow=False)}</div>
<ul class="tags" style="justify-content:center">{quick}</ul>
</div></section>'''
    return dict(title=c.t("Page introuvable | DarbTech", "Page not found | DarbTech"),
                desc=c.t("Cette page n’existe pas ou a été déplacée. Retrouvez les services Odoo de DarbTech, Odoo Gold Partner.",
                         "This page does not exist or has moved. Find DarbTech’s Odoo services, Odoo Gold Partner."),
                body=body, trail=None, noindex=True)
