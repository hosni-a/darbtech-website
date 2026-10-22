"""Home, Odoo hub, Odoo service sub-pages and Apps page."""
from lib import (esc, icon, btn, gold_chip, section_head, checklist, tags, faq, placeholder, hero_bg,
                 page_hero, hero_tile, cta_band, post_card, odoo_menu, OFFICES, BLOG_URL)
from pages_common import (APP_GROUPS, apps_cloud, method_steps, values_cards, gold_panel, stats_light,
                          logo_marquee, case_card, team_teaser, CASES)


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------
def orbit(c):
    rings = [
        ("1", [("crm", "target", "#0047BB", "CRM", "CRM"), ("sales", "tag", "#B84E0E", "Ventes", "Sales"),
               ("acc", "chart", "#B8862A", "Comptabilité", "Accounting")], 0),
        ("2", [("inv", "box", "#0F7F74", "Inventaire", "Inventory"), ("mrp", "factory", "#6E4BD8", "Fabrication", "Manufacturing"),
               ("pur", "cart", "#1F63E0", "Achats", "Purchase"), ("prj", "kanban", "#C2366F", "Projet", "Project")], 45),
        ("3", [("hr", "users", "#0047BB", "RH", "HR"), ("web", "monitor", "#0F7F74", "Site web", "Website"),
               ("hd", "headset", "#B84E0E", "Helpdesk", "Helpdesk"), ("cti", "phone", "#6E4BD8", "Ringover", "Ringover"),
               ("ai", "mic", "#B8862A", "Leexi.ai", "Leexi.ai")], 20),
    ]
    out = []
    for rid, items, offset in rings:
        step = 360 / len(items)
        chips = "".join(
            f'<span class="orbit__item" style="--a:{offset + i * step:.0f}deg"><span class="orbit__pin">'
            f'<span class="orbit__chip"><i style="--c:{col}">{icon(ic)}</i>{fr if c.lang == "fr" else en}</span></span></span>'
            for i, (k, ic, col, fr, en) in enumerate(items))
        out.append(f'<div class="orbit__ring orbit__ring--{rid}">{chips}</div>')
    core = (f'<div class="orbit__core"><div class="orbit__core-inner"><span class="orbit__core-top">DarbTech × Odoo</span>'
            f'<span class="orbit__core-title">Gold<br>Partner</span><span class="orbit__core-sub">{c.t("depuis le 22/09/2026", "since 22/09/2026")}</span></div></div>')
    label = c.t("Illustration : les applications Odoo que DarbTech intègre autour d’un même cœur",
                "Illustration: the Odoo apps DarbTech integrates around a single core")
    return f'<div class="orbit" role="img" aria-label="{label}">{"".join(reversed(out))}{core}</div>'


def page_home(c):
    d = c.data
    posts = [d["posts"][pid][c.lang] for pid in ("73", "72", "69")]
    team = d["team"][c.lang]

    hero = f'''<section class="hero hero--home">{hero_bg(canvas=True)}
<div class="container">
<div class="hero__inner">
<div class="hero__content">
{gold_chip(c)}
<h1 class="hero__title" data-split>{c.t('Votre partenaire <span class="accent accent--gold">Odoo Gold</span>, de l’analyse au go‑live',
                                       'Your <span class="accent accent--gold">Odoo Gold</span> partner, from analysis to go‑live')}</h1>
<p class="hero__lead">{c.t("Implémentation, migration et développement Odoo pour les PME et les ETI. 21 experts certifiés, entre Paris et Rabat, qui accompagnent leurs clients depuis 2015.",
                           "Odoo implementation, migration and development for SMEs and mid-market companies. 21 certified experts in Paris and Rabat, helping clients since 2015.")}</p>
<div class="hero__ctas">
{btn(c.href("contact"), c.t("Parler à un expert", "Talk to an expert"), "primary", magnetic=True)}
{btn(c.href("odoo"), c.t("Découvrir nos services Odoo", "Explore our Odoo services"), "ghost", arrow=False)}
</div>
<ul class="hero__proof">
<li>{icon("check")}{c.t("Partenaire Odoo depuis 2015", "Odoo partner since 2015")}</li>
<li>{icon("check")}{c.t("Consultants 100 % certifiés", "100% certified consultants")}</li>
<li>{icon("check")}{c.t("Paris · Rabat", "Paris · Rabat")}</li>
</ul>
</div>
<div class="hero__visual" data-reveal="scale">{orbit(c)}</div>
</div>
</div>
<div class="hero-stats"><div class="container">
<ul class="stats">
<li class="stat"><span class="stat__num" data-count="2015" data-from="2000">2015</span><span class="stat__label">{c.t("Partenaire Odoo depuis", "Odoo partner since")}</span></li>
<li class="stat"><span class="stat__num"><span data-count="21">21</span></span><span class="stat__label">{c.t("experts à Paris et Rabat", "experts in Paris and Rabat")}</span></li>
<li class="stat"><span class="stat__num"><span data-count="100">100</span><small>%</small></span><span class="stat__label">{c.t("consultants certifiés Odoo", "Odoo-certified consultants")}</span></li>
<li class="stat"><span class="stat__num">V8<small>→</small></span><span class="stat__label">{c.t("jusqu’aux dernières versions", "to the latest releases")}</span></li>
</ul></div></div>
</section>'''

    m = {pid: (ic, t, desc) for pid, ic, t, desc in odoo_menu(c)}
    flow = "".join(f'<li><span>0{i}</span>{t}</li>' for i, t in enumerate([
        c.t("Analyse", "Analysis"), c.t("Adaptation", "Alignment"), c.t("Implémentation", "Implementation"),
        c.t("Formation", "Training"), c.t("Maintenance", "Maintenance")], start=1))
    services = f'''<section class="section" aria-labelledby="svc-title">
<div class="container">
<div class="section-head section-head--split" data-reveal>
<div style="display:grid;gap:18px">{'<span class="eyebrow">' + c.t("Expertise Odoo", "Odoo expertise") + '</span>'}<h2 id="svc-title">{c.t('Tout Odoo, <span class="accent accent--blue">sous un même toit</span>', 'Everything Odoo, <span class="accent accent--blue">under one roof</span>')}</h2></div>
<p class="lead">{c.t("Du cadrage à la maintenance, une seule équipe pilote votre projet. Nos consultants comprennent vos métiers, nos développeurs adaptent Odoo quand le standard ne suffit plus.",
                     "From scoping to maintenance, one team runs your project. Our consultants understand your business; our developers extend Odoo when the standard is not enough.")}</p>
</div>
<div class="bento">
<a class="card card--feature" href="{c.href("odoo_impl")}" data-reveal style="--i:0">
<span class="card__icon">{icon("layers")}</span>
<h3 class="card__title">{m["odoo_impl"][1]}</h3>
<p class="card__text" style="max-width:46ch">{c.t("Nous déployons Odoo autour de vos processus : étude de l’existant, paramétrage du standard, modules spécifiques, formation puis suivi.",
                                                  "We roll out Odoo around your processes: current-state review, standard configuration, custom modules, training and follow-up.")}</p>
<ul class="mini-flow">{flow}</ul>
<div class="card__visual card__visual--bars" aria-hidden="true"><span style="--h:30%;--c:#8DB5FF"></span><span style="--h:48%;--c:#4C8DFF"></span><span style="--h:66%;--c:#0047BB"></span><span style="--h:82%;--c:#D86018"></span><span style="--h:100%;--c:#D9A93E"></span></div>
<span class="card__foot"><span class="card__more">{c.t("Voir l’implémentation", "See implementation")}{icon("arrow-right")}</span></span>
</a>
<a class="card card--accent" href="{c.href("odoo_migration")}" data-reveal style="--i:1">
<span class="card__icon">{icon("migrate")}</span>
<h3 class="card__title">{m["odoo_migration"][1]}</h3>
<p class="card__text">{c.t("Nous accompagnons les clients Odoo d’une version à l’autre depuis la V8, modules spécifiques compris.", "We have taken Odoo clients from one version to the next since V8, custom modules included.")}</p>
<span class="card__foot"><span class="mono" style="font-size:1.6rem;color:#fff;letter-spacing:-.02em">V8 → V<span style="color:var(--gold-300)">n</span></span><span class="card__more">{icon("arrow-right")}<span class="visually-hidden">{m["odoo_migration"][1]}</span></span></span>
</a>
<a class="card" href="{c.href("odoo_custom")}" data-reveal style="--i:0">
<span class="card__icon card__icon--orange">{icon("code")}</span>
<h3 class="card__title">{m["odoo_custom"][1]}</h3>
<p class="card__text">{c.t("Modules Python, rapports et automatisations quand votre métier sort du standard.", "Python modules, reports and automations when your business goes beyond the standard.")}</p>
<span class="card__foot"><span class="card__more">{c.t("En savoir plus", "Learn more")}{icon("arrow-right")}</span></span>
</a>
<a class="card" href="{c.href("odoo_integrations")}" data-reveal style="--i:1">
<span class="card__icon">{icon("plug")}</span>
<h3 class="card__title">{m["odoo_integrations"][1]}</h3>
<p class="card__text">{c.t("Téléphonie Ringover, IA de réunion Leexi.ai et connexion à vos logiciels métiers.", "Ringover telephony, Leexi.ai meeting AI and connections to your business software.")}</p>
<span class="card__foot"><span class="card__more">{c.t("En savoir plus", "Learn more")}{icon("arrow-right")}</span></span>
</a>
<a class="card" href="{c.href("odoo_support")}" data-reveal style="--i:2">
<span class="card__icon card__icon--gold">{icon("lifebuoy")}</span>
<h3 class="card__title">{m["odoo_support"][1]}</h3>
<p class="card__text">{c.t("Formation de chaque équipe, maintenance et évolutions après le go-live.", "Training for every team, then maintenance and enhancements after go-live.")}</p>
<span class="card__foot"><span class="card__more">{c.t("En savoir plus", "Learn more")}{icon("arrow-right")}</span></span>
</a>
<a class="card card--wide" href="{c.href("odoo_apps")}" data-reveal>
<span class="card__icon card__icon--dark">{icon("grid")}</span>
<div><h3 class="card__title">{c.t("Toutes les applications Odoo, reliées entre elles", "Every Odoo app, working together")}</h3>
<p class="card__text" style="margin-top:6px">{c.t("CRM et ERP dans une seule plateforme : fini les silos d’information.", "CRM and ERP in a single platform: no more information silos.")}</p>
<div style="margin-top:16px">{apps_cloud(c, ["crm", "sales", "accounting", "inventory", "purchase", "mrp", "project", "helpdesk", "hr", "website"])}</div></div>
<span class="card__more">{c.t("Voir les applications", "See the apps")}{icon("arrow-right")}</span>
</a>
</div>
</div></section>'''

    method = f'''<section class="section section--paper" aria-labelledby="method-title">
<div class="container"><div class="method">
<div class="method__intro" data-reveal>
<span class="eyebrow">{c.t("Méthode", "Approach")}</span>
<h2 id="method-title">{c.t('Cinq étapes, <span class="accent accent--blue">éprouvées depuis 2015</span>', 'Five steps, <span class="accent accent--blue">proven since 2015</span>')}</h2>
<p class="lead">{c.t("Nous vous accompagnons pendant toute la mise en place de l’outil, puis bien après. Chaque étape est menée en cycles Agile courts, avec un suivi partagé.",
                     "We stay with you throughout the roll-out, and well beyond. Every step runs in short Agile cycles with shared tracking.")}</p>
{tags(["Agile-Scrum", "DevOps", c.t("Transparence", "Transparency"), c.t("Engagement", "Commitment")], "blue")}
<a class="link-arrow" href="{c.href("method")}">{c.t("Découvrir notre méthode", "Discover our approach")}{icon("arrow-right")}</a>
</div>
{method_steps(c)}
</div></div></section>'''

    cases = f'''<section class="section" aria-labelledby="cases-title">
<div class="container">
<div class="section-head section-head--split" data-reveal>
<div style="display:grid;gap:18px"><span class="eyebrow">{c.t("Références", "Case studies")}</span>
<h2 id="cases-title">{c.t('Des processus métier, <span class="accent accent--blue">enfin digitalisés</span>', 'Business processes, <span class="accent accent--blue">finally digital</span>')}</h2></div>
<p class="lead">{c.t("Deux projets menés en Pays de Savoie, dans deux métiers très différents : le paysage et l’événementiel.", "Two projects in the Pays de Savoie region, in two very different trades: landscaping and events.")}</p>
</div>
<div class="grid grid--2">{case_card(c, "puthod", 0)}{case_card(c, "cameleon", 1)}</div>
<div style="margin-top:18px">{placeholder(c)}</div>
<p style="margin-top:28px"><a class="link-arrow" href="{c.href("cases")}">{c.t("Toutes nos références", "All case studies")}{icon("arrow-right")}</a></p>
</div></section>'''

    team_sec = f'''<section class="section section--dark" aria-labelledby="team-title">
<div class="bg-grid"></div>
<div class="container" style="position:relative">
<div class="section-head section-head--split" data-reveal>
<div style="display:grid;gap:18px"><span class="eyebrow">{c.t("Pourquoi DarbTech", "Why DarbTech")}</span>
<h2 id="team-title">{c.t('Une équipe intégrée, <span class="accent accent--gold">entre Paris et Rabat</span>', 'One integrated team, <span class="accent accent--gold">across Paris and Rabat</span>')}</h2></div>
<p class="lead">{c.t("Le conseil au plus près de vos équipes en France, des ingénieurs ERP et développeurs certifiés à Rabat : la proximité d’un intégrateur, la capacité d’un centre de compétences nearshore.",
                     "Consulting close to your teams in France, certified ERP engineers and developers in Rabat: the closeness of an integrator with the capacity of a nearshore competence centre.")}</p>
</div>
{values_cards(c, dark=True)}
<div class="card" data-reveal style="margin-top:18px;flex-direction:row;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:20px">
<div style="display:flex;align-items:center;gap:18px;flex-wrap:wrap">{team_teaser(c, team)}
<p style="color:#fff;font-weight:500">{c.t("21 experts, tous certifiés Odoo", "21 experts, all Odoo-certified")}<br><span style="color:var(--on-dark-muted);font-weight:400;font-size:.92rem">{c.t("Direction, conseil, ingénierie ERP, développement et QA", "Leadership, consulting, ERP engineering, development and QA")}</span></p></div>
<div style="display:flex;gap:10px;flex-wrap:wrap">{btn(c.href("team"), c.t("Rencontrer l’équipe", "Meet the team"), "ghost")}{btn(c.href("careers"), c.t("Nous rejoindre", "Join us"), "ghost", arrow=False)}</div>
</div>
</div></section>'''

    blog = f'''<section class="section" aria-labelledby="blog-title">
<div class="container">
<div class="section-head section-head--split" data-reveal>
<div style="display:grid;gap:18px"><span class="eyebrow">Blog</span>
<h2 id="blog-title">{c.t("Derniers articles", "Latest articles")}</h2></div>
<p class="lead">{c.t("Odoo, IA et gestion d’entreprise : les analyses de nos consultants.", "Odoo, AI and business management: insights from our consultants.")}</p>
</div>
<div class="grid grid--3">{"".join(post_card(c, p, i) for i, p in enumerate(posts))}</div>
<p style="margin-top:28px"><a class="link-arrow" href="{BLOG_URL[c.lang]}">{c.t("Tous les articles", "All articles")}{icon("arrow-up-right")}</a></p>
</div></section>'''

    body = hero + logo_marquee(c) + services + gold_panel(c) + method + cases + team_sec + blog + cta_band(c)
    return dict(
        title=c.t("DarbTech | Intégrateur Odoo Gold Partner à Paris et Rabat",
                  "DarbTech | Odoo Gold Partner in Paris and Rabat"),
        desc=c.t("DarbTech, Odoo Gold Partner depuis le 22/09/2026 et partenaire Odoo depuis 2015 : implémentation, migration et développement Odoo pour PME et ETI, depuis Paris et Rabat.",
                 "DarbTech, Odoo Gold Partner since 22/09/2026 and Odoo partner since 2015: Odoo implementation, migration and development for SMEs and mid-market companies, from Paris and Rabat."),
        body=body, trail=None)


# ---------------------------------------------------------------------------
# Odoo hub
# ---------------------------------------------------------------------------
def page_odoo(c):
    benefits = [
        ("layers", c.t("Intégration complète", "Fully integrated"), c.t("CRM et ERP réunis dans une seule plateforme : fini les silos d’information.", "CRM and ERP in one platform, so information silos disappear.")),
        ("globe", c.t("Accessible en ligne", "Online access"), c.t("Un outil web : vos données et votre gestion, depuis n’importe où.", "A web tool: your data and your business, from anywhere.")),
        ("monitor", c.t("Interface intuitive", "Intuitive interface"), c.t("Une prise en main rapide qui réduit le temps de formation.", "Quick to learn, which shortens training time.")),
        ("plug", c.t("Interopérable", "Interoperable"), c.t("Odoo se connecte aux logiciels métiers déjà en place.", "Odoo connects to the business software you already use.")),
        ("clock", c.t("Rapide à déployer", "Fast to deploy"), c.t("Déploiement rapide et modules adaptables à vos besoins précis.", "Quick roll-out, with modules you can adapt to your exact needs.")),
        ("code", c.t("Open source", "Open source"), c.t("Le code source des modules est ouvert : transparence et personnalisation totales.", "Module source code is open, for full transparency and customisation.")),
        ("repeat", c.t("Communauté et mises à jour", "Community and updates"), c.t("Une communauté mondiale active et des versions régulières.", "An active global community and regular releases.")),
    ]
    ben = "".join(f'<article class="card" data-reveal style="--i:{i % 4}"><span class="card__icon">{icon(ic)}</span><h3 class="card__title">{t}</h3><p class="card__text">{d}</p></article>'
                  for i, (ic, t, d) in enumerate(benefits))
    ben += (f'<a class="card card--accent" href="{c.href("contact")}" data-reveal style="--i:3"><span class="card__icon">{icon("sparkle")}</span>'
            f'<h3 class="card__title">{c.t("Et un partenaire Gold pour le déployer", "And a Gold partner to roll it out")}</h3>'
            f'<span class="card__foot"><span class="card__more">{c.t("Parler à un expert", "Talk to an expert")}{icon("arrow-right")}</span></span></a>')

    svc = "".join(f'<a class="card" href="{c.href(pid)}" data-reveal style="--i:{i % 3}"><span class="card__icon">{icon(ic)}</span>'
                  f'<h3 class="card__title">{t}</h3><p class="card__text">{d}</p><span class="card__foot"><span class="card__more">{c.t("En savoir plus", "Learn more")}{icon("arrow-right")}</span></span></a>'
                  for i, (pid, ic, t, d) in enumerate(odoo_menu(c)))

    body = page_hero(
        c, [("Odoo", None)], c.t("Services Odoo", "Odoo services"),
        c.t('Intégrateur Odoo <span class="accent accent--gold">Gold Partner</span>, à Paris et à Rabat',
            'Odoo <span class="accent accent--gold">Gold Partner</span> integrator, in Paris and Rabat'),
        c.t("Partenaire Odoo depuis 2015 et Gold depuis le 22 septembre 2026, nous accompagnons PME et ETI sur tout le cycle de vie d’Odoo : implémentation, migration, développement, intégrations, formation et support.",
            "An Odoo partner since 2015 and Gold since 22 September 2026, we support SMEs and mid-market companies across the whole Odoo lifecycle: implementation, migration, development, integrations, training and support."),
        btn(c.href("contact"), c.t("Parler à un expert", "Talk to an expert"), "primary", magnetic=True)
        + btn(c.href("odoo_apps"), c.t("Voir les applications", "See the apps"), "ghost", arrow=False),
        aside=hero_tile("grid"), chip=True)
    body += f'''<section class="section" aria-labelledby="svc-title"><div class="container">
{section_head(c.t("Nos services", "Our services"), c.t("Un accompagnement Odoo de bout en bout", "End-to-end Odoo services"), c.t("Six expertises, une seule équipe, des consultants et des développeurs tous certifiés Odoo.", "Six areas of expertise, one team, and every consultant and developer Odoo-certified."))}
<div class="grid grid--3">{svc}</div>
</div></section>'''
    body += gold_panel(c)
    body += f'''<section class="section section--paper" aria-labelledby="why-odoo"><div class="container">
{section_head(c.t("Pourquoi Odoo", "Why Odoo"), c.t('Une plateforme complète, <span class="accent accent--blue">flexible et évolutive</span>', 'A complete platform, <span class="accent accent--blue">flexible and scalable</span>'), c.t("Choisir Odoo, c’est plus qu’adopter un logiciel de gestion : c’est s’appuyer sur une suite intégrée, soutenue par une communauté mondiale, pour gagner en croissance et en efficacité.", "Choosing Odoo is more than adopting management software: it means relying on an integrated suite, backed by a global community, to drive growth and efficiency."), extra_cls="", )}
<div class="grid grid--4">{ben}</div>
</div></section>'''
    body += f'''<section class="section" aria-labelledby="why-dt"><div class="container">
<div class="split"><div class="split__text" data-reveal>
<span class="eyebrow">{c.t("Pourquoi DarbTech", "Why DarbTech")}</span>
<h2 id="why-dt">{c.t("Plus de dix ans d’Odoo, de la V8 à aujourd’hui", "Over ten years of Odoo, from V8 to today")}</h2>
<p class="lead">{c.t("Nous avons vu évoluer cet ERP, pensé pour les TPE, les PME et les groupes, et nous y avons pris part. Notre valeur ajoutée :", "Odoo is built for small businesses, SMEs and groups. We have watched it grow and played our part in it. What we bring:")}</p>
{checklist([c.t("Une expertise éprouvée par des années de projets variés.", "Expertise proven over years of varied projects."),
            c.t("La capacité à conseiller et à mettre en œuvre des solutions adaptées, quel que soit votre secteur.", "The ability to advise on and deliver the right solution, whatever your sector."),
            c.t("Une approche centrée sur l’efficacité, l’innovation et la satisfaction client.", "An approach focused on efficiency, innovation and client satisfaction."),
            c.t("Les éditions Community et Enterprise.", "Both Community and Enterprise editions.")])}
</div>
<div data-reveal="scale">{stats_light(c)}</div></div>
</div></section>'''
    body += f'''<section class="section section--paper" aria-labelledby="cases-title"><div class="container">
{section_head(c.t("Références", "Case studies"), c.t("Odoo en production chez nos clients", "Odoo in production at our clients"))}
<div class="grid grid--2">{case_card(c, "puthod", 0)}{case_card(c, "cameleon", 1)}</div>
</div></section>'''
    body += f'''<section class="section" aria-labelledby="faq-title"><div class="container container--narrow">
{section_head("FAQ", c.t("Questions fréquentes", "Frequently asked questions"), level=2)}
{faq([
        (c.t("Que signifie « Odoo Gold Partner » ?", "What does “Odoo Gold Partner” mean?"),
         c.t("Gold est un niveau du programme partenaires d’Odoo. DarbTech l’a obtenu le 22 septembre 2026, après plus de dix ans comme partenaire Odoo (depuis 2015).",
             "Gold is a level in Odoo’s partner programme. DarbTech reached it on 22 September 2026, after more than ten years as an Odoo partner (since 2015).")),
        (c.t("Sur quelles versions d’Odoo intervenez-vous ?", "Which Odoo versions do you work with?"),
         c.t("De la V8 aux dernières versions, en édition Community comme en Enterprise.", "From V8 to the latest releases, on both the Community and Enterprise editions.")),
        (c.t("Vos consultants sont-ils certifiés ?", "Are your consultants certified?"),
         c.t("Oui. Tous nos consultants et développeurs sont certifiés Odoo. Certains ont aussi des certifications ISTQB, SAFe, CSPO, Lean Six Sigma ou Ringover.", "Yes. All our consultants and developers are Odoo-certified. Some also hold ISTQB, SAFe, CSPO, Lean Six Sigma or Ringover certifications.")),
        (c.t("Où sont basées vos équipes ?", "Where are your teams based?"),
         c.t("À Paris (DarbTech Labs) et à Rabat (DarbTech). Nous travaillons avec des entreprises francophones et anglophones.", "In Paris (DarbTech Labs) and Rabat (DarbTech). We work with French- and English-speaking companies.")),
    ])}
</div></section>'''
    body += cta_band(c)
    return dict(
        title=c.t("Intégrateur Odoo Gold Partner Paris & Rabat | DarbTech", "Odoo Gold Partner integrator, Paris & Rabat | DarbTech"),
        desc=c.t("Services Odoo de bout en bout par un Odoo Gold Partner : implémentation, migration, développement sur mesure, intégrations, support et formation. Consultants 100 % certifiés.",
                 "End-to-end Odoo services from an Odoo Gold Partner: implementation, migration, custom development, integrations, support and training. 100% certified consultants."),
        body=body, trail=[("Odoo", None)])


# ---------------------------------------------------------------------------
# Odoo service sub-pages (shared template)
# ---------------------------------------------------------------------------
def mock_code(lines):
    rows = "".join(f'<span class="mock-code__line" style="--w:{w}%;--c:{col}"></span>' for w, col in lines)
    return (f'<div class="mock-window" aria-hidden="true"><div class="mock-window__bar"><i></i><i></i><i></i></div>'
            f'<div class="mock-code">{rows}</div></div>')


def service_page(c, pid, conf):
    trail = [("Odoo", "odoo"), (conf["crumb"], None)]
    body = page_hero(c, trail, conf["eyebrow"], conf["h1"], conf["lead"],
                     btn(c.href("contact"), c.t("Parler à un expert", "Talk to an expert"), "primary", magnetic=True)
                     + btn(c.href("odoo"), c.t("Tous les services Odoo", "All Odoo services"), "ghost", arrow=False),
                     aside=hero_tile(conf["icon"]), chip=True)
    # For whom + scope
    body += f'''<section class="section" aria-labelledby="for-title"><div class="container">
<div class="split"><div class="split__text" data-reveal>
<span class="eyebrow">{c.t("Pour qui", "Who it is for")}</span>
<h2 id="for-title">{conf["for_title"]}</h2>
{checklist(conf["for"])}
</div>
<div data-reveal="scale">{conf.get("visual", "")}</div>
</div></div></section>'''
    scope = "".join(f'<article class="card" data-reveal style="--i:{i % 3}"><span class="card__icon{v}">{icon(ic)}</span><h3 class="card__title">{t}</h3><p class="card__text">{d}</p></article>'
                    for i, (ic, t, d, v) in enumerate([(s[0], s[1], s[2], s[3] if len(s) > 3 else "") for s in conf["scope"]]))
    body += f'''<section class="section section--paper" aria-labelledby="scope-title"><div class="container">
{section_head(c.t("Périmètre", "Scope"), conf["scope_title"], conf.get("scope_lead"))}
<div class="grid grid--3">{scope}</div>
</div></section>'''
    if conf.get("extra"):
        body += conf["extra"]
    # Steps
    steps_html = conf.get("steps_html") or method_steps(c, detailed=True)
    body += f'''<section class="section" aria-labelledby="steps-title"><div class="container"><div class="method">
<div class="method__intro" data-reveal><span class="eyebrow">{c.t("Déroulé", "How it works")}</span>
<h2 id="steps-title">{conf["steps_title"]}</h2><p class="lead">{conf["steps_lead"]}</p>
<a class="link-arrow" href="{c.href("method")}">{c.t("Notre méthode en détail", "Our approach in detail")}{icon("arrow-right")}</a></div>
{steps_html}</div></div></section>'''
    # Apps + case
    case_html = "".join(case_card(c, k, i) for i, k in enumerate(conf.get("cases", [])))
    body += f'''<section class="section section--paper" aria-labelledby="rel-title"><div class="container">
{section_head(c.t("En pratique", "In practice"), c.t("Applications et références liées", "Related apps and case studies"))}
<div data-reveal>{apps_cloud(c, conf["apps"])}</div>
{('<div class="grid grid--2" style="margin-top:32px">' + case_html + '</div>') if case_html else ''}
</div></section>'''
    body += f'''<section class="section" aria-labelledby="faq-title"><div class="container container--narrow">
{section_head("FAQ", c.t("Questions fréquentes", "Frequently asked questions"))}
{faq(conf["faq"])}
</div></section>'''
    body += cta_band(c)
    return dict(title=conf["title"], desc=conf["desc"], body=body, trail=trail)


def page_odoo_impl(c):
    pipeline = f'''<div class="mock-board" aria-hidden="true">
<div class="mock-board__col"><span class="mock-board__h">{c.t("Analyse", "Analysis")}</span><span class="mock-board__card"></span><span class="mock-board__card mock-board__card--s"></span></div>
<div class="mock-board__col"><span class="mock-board__h">{c.t("Paramétrage", "Configuration")}</span><span class="mock-board__card mock-board__card--b"></span><span class="mock-board__card"></span><span class="mock-board__card mock-board__card--s"></span></div>
<div class="mock-board__col"><span class="mock-board__h">{c.t("Recette", "Testing")}</span><span class="mock-board__card mock-board__card--o"></span></div>
<div class="mock-board__col"><span class="mock-board__h">Go-live</span><span class="mock-board__card mock-board__card--g"></span></div>
</div>'''
    return service_page(c, "odoo_impl", dict(
        crumb=c.t("Implémentation", "Implementation"), icon="layers",
        eyebrow=c.t("Implémentation Odoo", "Odoo implementation"),
        h1=c.t('Déployer Odoo, <span class="accent accent--gold">de l’analyse au go-live</span>', 'Rolling out Odoo, <span class="accent accent--gold">from analysis to go-live</span>'),
        lead=c.t("Nous mettons en place Odoo pour qu’il épouse vos processus : étude de l’existant, paramétrage du standard, modules spécifiques, formation, puis suivi après la mise en production.",
                 "We set Odoo up to fit your processes: current-state review, standard configuration, custom modules, training, then follow-up after go-live."),
        for_title=c.t("Vous voulez une seule plateforme pour piloter l’entreprise", "You want one platform to run the business"),
        **{"for": [c.t("Vos informations sont dispersées entre tableurs, papier et logiciels isolés.", "Your information is scattered across spreadsheets, paper and stand-alone tools."),
                   c.t("Vous voulez réunir CRM et ERP dans un même outil.", "You want CRM and ERP in a single tool."),
                   c.t("Vos équipes, parfois mobiles ou multi-sites, ont besoin d’un accès en ligne partout.", "Your teams, sometimes mobile or multi-site, need online access from anywhere."),
                   c.t("Vous cherchez un ERP rapide à déployer et adaptable à vos méthodes.", "You need an ERP that is quick to deploy and adapts to your methods.")]},
        visual=pipeline,
        scope_title=c.t("Ce que nous prenons en charge", "What we take care of"),
        scope=[("search", c.t("Étude de l’existant", "Current-state review"), c.t("Procédures, flux entre services et interconnexions avec vos logiciels métiers.", "Procedures, flows between departments and links with your business software.")),
               ("sliders", c.t("Adaptation des processus", "Process alignment"), c.t("Vos procédures alignées sur la logique de l’ERP, sans perdre vos spécificités.", "Your procedures aligned with the ERP’s logic, without losing what is specific to you.")),
               ("layers", c.t("Paramétrage du standard", "Standard configuration"), c.t("Configuration des applications Odoo dont vous avez besoin.", "Configuration of the Odoo apps you need.")),
               ("code", c.t("Modules spécifiques", "Custom modules"), c.t("Développements sur mesure quand votre métier l’exige.", "Bespoke development where your business requires it."), " card__icon--orange"),
               ("graduation", c.t("Formation des équipes", "Team training"), c.t("Chaque équipe formée, de la prise en main à l’usage quotidien.", "Every team trained, from first steps to daily use.")),
               ("wrench", c.t("Maintenance", "Maintenance"), c.t("Un outil qui suit vos nouvelles activités et vos nouvelles méthodes.", "A tool that keeps up with new activities and new methods."), " card__icon--gold")],
        steps_title=c.t("Cinq étapes, du cadrage à la maintenance", "Five steps, from scoping to maintenance"),
        steps_lead=c.t("Chaque étape est menée en sprints courts : vous validez au fil de l’eau, sans effet tunnel.", "Each step runs in short sprints: you validate as we go, with no black box."),
        apps=["crm", "sales", "accounting", "invoicing", "inventory", "purchase", "mrp", "project"],
        cases=["puthod", "cameleon"],
        faq=[(c.t("Faut-il adapter nos processus à Odoo ?", "Do we have to change our processes to fit Odoo?"),
              c.t("Nous cherchons le bon équilibre : aligner vos procédures sur la logique de l’ERP quand c’est pertinent, et développer des modules spécifiques quand votre métier l’exige.", "We look for the right balance: align your procedures with the ERP’s logic where it makes sense, and build custom modules where your business requires it.")),
             (c.t("Community ou Enterprise ?", "Community or Enterprise?"),
              c.t("Nous intervenons sur les deux éditions et vous aidons à choisir en fonction de vos besoins.", "We work with both editions and help you choose based on your needs.")),
             (c.t("Qui forme nos équipes ?", "Who trains our teams?"),
              c.t("Nos consultants, tous certifiés Odoo, forment et accompagnent chaque équipe jusqu’à l’usage quotidien.", "Our consultants, all Odoo-certified, train and support each team through to daily use."))],
        title=c.t("Implémentation Odoo : de l’analyse au go-live | DarbTech", "Odoo implementation, from analysis to go-live | DarbTech"),
        desc=c.t("Implémentation Odoo par un Gold Partner : étude de l’existant, paramétrage, modules spécifiques, formation et maintenance. Méthode Agile en 5 étapes, Paris et Rabat.",
                 "Odoo implementation by a Gold Partner: current-state review, configuration, custom modules, training and maintenance. A 5-step Agile method, from Paris and Rabat.")))


def simple_steps(items):
    out = []
    for n, (title, text) in enumerate(items, start=1):
        out.append(f'<li class="step" data-reveal><span class="step__dot">0{n}</span><div class="step__body"><h3 class="step__title">{title}</h3><p class="step__text">{text}</p></div></li>')
    return f'<ol class="steps" data-steps><span class="steps__line" aria-hidden="true"><span></span></span>{"".join(out)}</ol>'


def page_odoo_migration(c):
    versions = '<div class="mock-versions" aria-hidden="true">' + "".join(
        f'<span class="mock-versions__v{" is-gold" if i == 6 else ""}">{v}</span>' for i, v in enumerate(["V8", "V10", "V12", "V14", "V16", "V17", c.t("Dernière", "Latest")])) + "</div>"
    return service_page(c, "odoo_migration", dict(
        crumb="Migration", icon="migrate",
        eyebrow=c.t("Migration Odoo", "Odoo migration"),
        h1=c.t('Migrer Odoo vers la dernière version, <span class="accent accent--gold">sans rupture</span>', 'Upgrade Odoo to the latest version, <span class="accent accent--gold">without disruption</span>'),
        lead=c.t("Depuis la V8, nous accompagnons nos clients d’une version d’Odoo à l’autre. Nous analysons votre base, adaptons vos modules spécifiques et sécurisons la bascule par des tests.",
                 "Since V8, we have helped our clients move from one Odoo version to the next. We analyse your database, adapt your custom modules and secure the switch-over with testing."),
        for_title=c.t("Votre Odoo a pris de l’âge", "Your Odoo is showing its age"),
        **{"for": [c.t("Vous êtes sur une ancienne version d’Odoo et passez à côté des nouveautés.", "You run an older Odoo version and miss out on new features."),
                   c.t("Vos modules spécifiques freinent les montées de version.", "Your custom modules hold back upgrades."),
                   c.t("Vous hésitez entre Community et Enterprise pour la suite.", "You are weighing Community against Enterprise for the future."),
                   c.t("Vous voulez une bascule maîtrisée, sans interrompre l’activité.", "You want a controlled switch-over that does not stop the business.")]},
        visual=versions,
        scope_title=c.t("Une migration préparée, testée et accompagnée", "A migration that is prepared, tested and supported"),
        scope=[("search", c.t("Audit de l’existant", "Current-state audit"), c.t("Version, modules installés, développements spécifiques et volume de données.", "Version, installed apps, custom developments and data volume.")),
               ("code", c.t("Adaptation des modules", "Module adaptation"), c.t("Chaque module spécifique est adapté, remplacé par le standard ou retiré.", "Each custom module is ported, replaced by standard features or retired."), " card__icon--orange"),
               ("database", c.t("Migration des données", "Data migration"), c.t("Reprise de l’historique et contrôles de cohérence.", "History carried over, with consistency checks.")),
               ("shield", c.t("Tests et recette", "Testing and acceptance"), c.t("Tests fonctionnels et de non-régression, avec notre ingénieur QA certifié ISTQB.", "Functional and regression testing, with our ISTQB-certified QA engineer.")),
               ("graduation", c.t("Prise en main des nouveautés", "New-feature onboarding"), c.t("Vos équipes formées à ce qui change dans la nouvelle version.", "Your teams trained on what changes in the new version.")),
               ("lifebuoy", c.t("Bascule accompagnée", "Supported switch-over"), c.t("Mise en production planifiée et suivi après la migration.", "Planned go-live and follow-up after the migration."), " card__icon--gold")],
        steps_title=c.t("Une migration en cinq temps", "A migration in five stages"),
        steps_lead=c.t("Le même cadre Agile que nos projets d’implémentation, appliqué à votre montée de version.", "The same Agile framework as our implementation projects, applied to your upgrade."),
        steps_html=simple_steps([
            (c.t("Audit", "Audit"), c.t("État des lieux technique et fonctionnel de votre Odoo.", "Technical and functional review of your Odoo.")),
            (c.t("Plan de migration", "Migration plan"), c.t("Choix de la version cible, de l’édition et du sort de chaque module spécifique.", "Choice of target version, edition and what to do with each custom module.")),
            (c.t("Adaptation", "Adaptation"), c.t("Portage des modules et migration des données sur un environnement de test.", "Modules ported and data migrated on a test environment.")),
            (c.t("Tests et recette", "Testing and acceptance"), c.t("Tests de non-régression, puis validation avec vos utilisateurs clés.", "Regression testing, then sign-off with your key users.")),
            (c.t("Bascule et suivi", "Switch-over and follow-up"), c.t("Mise en production planifiée, formation aux nouveautés et suivi.", "Planned go-live, training on what is new, and follow-up."))]),
        apps=["accounting", "sales", "inventory", "crm", "mrp", "hr"],
        cases=[],
        faq=[(c.t("Depuis quelles versions migrez-vous ?", "Which versions do you migrate from?"),
              c.t("Nous connaissons Odoo depuis la V8 et accompagnons nos clients jusqu’aux dernières versions, en Community comme en Enterprise.", "We have worked with Odoo since V8 and take clients through to the latest releases, on Community and Enterprise alike.")),
             (c.t("Nos développements spécifiques seront-ils conservés ?", "Will our custom developments be kept?"),
              c.t("Chaque module est étudié : adapté à la nouvelle version, remplacé par une fonction standard devenue disponible, ou retiré s’il n’est plus utile.", "Each module is reviewed: ported to the new version, replaced by a standard feature that now exists, or retired if no longer needed.")),
             (c.t("Comment limitez-vous les risques ?", "How do you limit the risks?"),
              c.t("Par une migration à blanc sur un environnement de test, des tests fonctionnels et de non-régression, puis une recette avec vos utilisateurs avant la bascule.", "With a dry run on a test environment, functional and regression testing, then user acceptance before the switch-over."))],
        title=c.t("Migration Odoo vers la dernière version | DarbTech", "Odoo migration to the latest version | DarbTech"),
        desc=c.t("Migration Odoo de la V8 aux dernières versions, Community ou Enterprise : audit, adaptation des modules spécifiques, migration des données et tests. Par un Odoo Gold Partner.",
                 "Odoo migration from V8 to the latest releases, Community or Enterprise: audit, custom module porting, data migration and testing. By an Odoo Gold Partner.")))


def page_odoo_custom(c):
    code = mock_code([(42, "#8DB5FF"), (68, "#E9C46A"), (55, "#A3AEC7"), (30, "#FFB27F"), (74, "#A3AEC7"), (48, "#8DB5FF"), (62, "#A3AEC7"), (36, "#E9C46A")])
    return service_page(c, "odoo_custom", dict(
        crumb=c.t("Développement sur mesure", "Custom development"), icon="code",
        eyebrow=c.t("Développement Odoo", "Odoo development"),
        h1=c.t('Des modules Odoo sur mesure, <span class="accent accent--gold">quand le standard ne suffit pas</span>', 'Custom Odoo modules, <span class="accent accent--gold">when standard is not enough</span>'),
        lead=c.t("Modules spécifiques, rapports, automatisations et API : nos développeurs Python, tous certifiés Odoo, adaptent l’outil à vos méthodes de travail.",
                 "Custom modules, reports, automations and APIs: our Python developers, all Odoo-certified, fit the tool to the way you work."),
        for_title=c.t("Votre métier a ses particularités", "Your business has its own way of working"),
        **{"for": [c.t("Une partie de vos processus n’existe pas dans le standard Odoo.", "Part of your process does not exist in standard Odoo."),
                   c.t("Vous avez besoin de rapports et d’exports prêts pour la comptabilité ou la direction.", "You need reports and exports ready for finance or management."),
                   c.t("Vous voulez automatiser des tâches répétitives et sources d’erreurs.", "You want to automate repetitive, error-prone tasks."),
                   c.t("Vous souhaitez intégrer de l’IA ou des API dans vos flux Odoo.", "You want to bring AI or APIs into your Odoo flows.")]},
        visual=code,
        scope_title=c.t("Ce que nous développons", "What we build"),
        scope=[("code", c.t("Modules spécifiques", "Custom modules"), c.t("Des modules Python qui collent à vos processus métier.", "Python modules shaped around your business processes."), " card__icon--orange"),
               ("file", c.t("Rapports et exports", "Reports and exports"), c.t("Modèles de rapports directement exploitables par vos services.", "Report templates your departments can use straight away.")),
               ("flow", c.t("Automatisations", "Automations"), c.t("Des tâches répétitives automatisées pour fiabiliser vos processus.", "Repetitive tasks automated to make processes more reliable.")),
               ("plug", c.t("API Odoo", "Odoo APIs"), c.t("Fonctionnalités avancées et échanges de données via les API d’Odoo.", "Advanced features and data exchange through Odoo’s APIs.")),
               ("sparkle", c.t("Intégration d’IA", "AI integration"), c.t("Des cas d’usage IA ciblés, intégrés à vos flux Odoo.", "Targeted AI use cases, built into your Odoo flows."), " card__icon--gold"),
               ("shield", c.t("Qualité logicielle", "Software quality"), c.t("Tests menés par un ingénieur QA certifié ISTQB et Odoo.", "Testing led by an ISTQB- and Odoo-certified QA engineer."))],
        steps_title=c.t("Du besoin au module en production", "From requirement to module in production"),
        steps_lead=c.t("Nous privilégions toujours le standard, puis développons ce qui fait votre différence, en sprints Agile.", "We always start from the standard, then build what sets you apart, in Agile sprints."),
        steps_html=simple_steps([
            (c.t("Expression du besoin", "Requirements"), c.t("Nous comprenons le processus métier à couvrir et vérifions ce que le standard sait déjà faire.", "We map the business process and check what the standard already covers.")),
            (c.t("Conception", "Design"), c.t("Spécifications courtes et validées avec vous avant le développement.", "Short specifications, signed off with you before development.")),
            (c.t("Développement en sprints", "Development in sprints"), c.t("Livraisons régulières, démonstrations et ajustements.", "Regular deliveries, demos and adjustments.")),
            (c.t("Tests et recette", "Testing and acceptance"), c.t("Tests fonctionnels et de non-régression, puis validation par vos utilisateurs.", "Functional and regression testing, then user sign-off.")),
            (c.t("Mise en production et maintenance", "Go-live and maintenance"), c.t("Déploiement, documentation et évolutions dans la durée.", "Deployment, documentation and long-term enhancements."))]),
        apps=["crm", "sales", "invoicing", "project", "planning", "mrp"],
        cases=["puthod", "cameleon"],
        faq=[(c.t("Les modules spécifiques compliquent-ils les montées de version ?", "Do custom modules make upgrades harder?"),
              c.t("Nous partons du standard et concevons les développements pour qu’ils restent maintenables, ce qui facilite les migrations futures.", "We start from the standard and design developments to stay maintainable, which keeps future migrations simpler.")),
             (c.t("Avec quelles technologies travaillez-vous ?", "Which technologies do you use?"),
              c.t("Python et le framework Odoo pour les modules, JavaScript pour les interfaces, et les API d’Odoo pour les échanges avec d’autres systèmes.", "Python and the Odoo framework for modules, JavaScript for interfaces, and Odoo’s APIs for exchanges with other systems.")),
             (c.t("Qui teste les développements ?", "Who tests the developments?"),
              c.t("Notre ingénieur QA, certifié ISTQB et Odoo, conçoit et exécute les plans de test avec l’équipe de développement.", "Our QA engineer, ISTQB- and Odoo-certified, designs and runs test plans with the development team."))],
        title=c.t("Développement Odoo sur mesure | DarbTech", "Custom Odoo development | DarbTech"),
        desc=c.t("Développement de modules Odoo spécifiques, rapports, automatisations, API et IA par des développeurs Python certifiés Odoo. DarbTech, Odoo Gold Partner.",
                 "Custom Odoo modules, reports, automations, APIs and AI, built by Odoo-certified Python developers. DarbTech, Odoo Gold Partner.")))


def page_odoo_integrations(c):
    d = c.data
    cti_post = d["posts"]["3"][c.lang]
    partners = f'''<section class="section" aria-labelledby="partners-title"><div class="container">
{section_head(c.t("Partenaires", "Partners"), c.t("Deux partenariats au service de votre Odoo", "Two partnerships for your Odoo"))}
<div class="grid grid--2">
<article class="card" data-reveal>
<div class="partner__logo"><img src="{c.asset("img/partners/ringover.png")}" alt="Ringover" loading="lazy" width="64" height="64"></div>
<h3 class="card__title">{c.t("Ringover : la téléphonie cloud reliée au CRM", "Ringover: cloud telephony connected to the CRM")}</h3>
<p class="card__text">{c.t("Partenaire officiel de Ringover, leader de la téléphonie cloud d’entreprise, nous améliorons l’expérience client et l’efficacité de vos équipes.", "As an official partner of Ringover, a leader in business cloud telephony, we improve customer experience and team efficiency.")}</p>
{checklist([c.t("CTI : couplage téléphonie-informatique avec votre CRM", "CTI: computer-telephony integration with your CRM"),
            c.t("SVI : un accueil et une orientation des appels entrants plus efficaces", "IVR: better greeting and routing of inbound calls"),
            c.t("Statistiques avancées sur l’activité téléphonique", "Advanced call analytics"),
            c.t("Outils collaboratifs intégrés pour une communication unifiée", "Built-in collaboration tools for unified communication")])}
</article>
<article class="card" data-reveal style="--i:1">
<div class="partner__logo"><img src="{c.asset("img/partners/leexi.webp")}" alt="Leexi.ai" loading="lazy" width="120" height="63"></div>
<h3 class="card__title">{c.t("Leexi.ai : l’IA de réunion, synchronisée avec Odoo", "Leexi.ai: meeting AI, synced with Odoo")}</h3>
<p class="card__text">{c.t("Leexi ne se contente pas de transcrire : il structure l’intelligence de vos réunions et la fait remonter dans votre CRM.", "Leexi does more than transcribe: it structures what is said in your meetings and feeds it into your CRM.")}</p>
{checklist([c.t("Comptes rendus, actions à mener et points clés générés par l’IA", "AI-generated summaries, action items and key points"),
            c.t("Intégration native avec Odoo : les informations remontent dans le CRM", "Native Odoo integration: insights flow into the CRM"),
            c.t("Google Meet, Microsoft Teams, Zoom ou en présentiel", "Google Meet, Microsoft Teams, Zoom or in person"),
            c.t("Conforme au RGPD et certifié ISO 27001", "GDPR-compliant and ISO 27001-certified")])}
</article>
</div>
<p style="margin-top:24px" data-reveal><a class="link-arrow" href="{cti_post["url"]}">{c.t("À lire : intégration CTI avec Odoo", "Read: CTI integration with Odoo")}{icon("arrow-up-right")}</a></p>
</div></section>'''
    nodes = f'''<div class="mock-hub" aria-hidden="true"><span class="mock-hub__core">Odoo</span>
<span class="mock-hub__n" style="--a:0deg">Ringover</span><span class="mock-hub__n" style="--a:72deg">Leexi.ai</span>
<span class="mock-hub__n" style="--a:144deg">API</span><span class="mock-hub__n" style="--a:216deg">{c.t("Web services", "Web services")}</span>
<span class="mock-hub__n" style="--a:288deg">{c.t("Logiciels métiers", "Business apps")}</span></div>'''
    return service_page(c, "odoo_integrations", dict(
        crumb=c.t("Intégrations", "Integrations"), icon="plug",
        eyebrow=c.t("Intégrations Odoo", "Odoo integrations"),
        h1=c.t('Connecter Odoo à vos outils : <span class="accent accent--gold">téléphonie, IA et logiciels métiers</span>', 'Connect Odoo to your tools: <span class="accent accent--gold">telephony, AI and business software</span>'),
        lead=c.t("Odoo s’intègre facilement aux logiciels déjà en place. Partenaires de Ringover et de Leexi.ai, nous relions votre ERP à la téléphonie cloud, à l’IA de réunion et à vos applications métiers.",
                 "Odoo integrates easily with the software you already use. As Ringover and Leexi.ai partners, we connect your ERP to cloud telephony, meeting AI and your business applications."),
        for_title=c.t("Vos outils ne se parlent pas encore", "Your tools don’t talk to each other yet"),
        **{"for": [c.t("Vos appels clients ne laissent aucune trace dans le CRM.", "Customer calls leave no trace in the CRM."),
                   c.t("Les comptes rendus de réunion se perdent dans les boîtes mail.", "Meeting notes get lost in inboxes."),
                   c.t("Vos logiciels métiers obligent à ressaisir les mêmes données.", "Your business software forces you to re-key the same data."),
                   c.t("Vous voulez une vision unifiée de la relation client.", "You want a single view of the customer relationship.")]},
        visual=nodes,
        scope_title=c.t("Ce que nous connectons", "What we connect"),
        scope=[("phone", c.t("Téléphonie cloud", "Cloud telephony"), c.t("Ringover : CTI, SVI, statistiques et outils collaboratifs.", "Ringover: CTI, IVR, analytics and collaboration tools.")),
               ("mic", c.t("IA de réunion", "Meeting AI"), c.t("Leexi.ai : comptes rendus et actions synchronisés avec Odoo.", "Leexi.ai: summaries and actions synced with Odoo."), " card__icon--gold"),
               ("server", c.t("Web services", "Web services"), c.t("Développement et exploitation des web services de vos projets.", "Building and running the web services your projects need.")),
               ("plug", c.t("API Odoo", "Odoo APIs"), c.t("Échanges de données entre Odoo et vos applications.", "Data exchange between Odoo and your applications.")),
               ("flow", c.t("Logiciels métiers", "Business software"), c.t("Interconnexion avec les outils spécifiques à votre secteur.", "Connections with your industry-specific tools."), " card__icon--orange"),
               ("shield", c.t("Données maîtrisées", "Data under control"), c.t("Des partenaires choisis pour leur conformité, comme Leexi (RGPD, ISO 27001).", "Partners chosen for compliance, such as Leexi (GDPR, ISO 27001)."))],
        extra=partners,
        steps_title=c.t("Une intégration en cinq étapes", "An integration in five steps"),
        steps_lead=c.t("Nous cartographions les échanges de données avant d’écrire la moindre ligne de code.", "We map data flows before writing a single line of code."),
        steps_html=simple_steps([
            (c.t("Cartographie", "Mapping"), c.t("Outils en place, données échangées et sens des flux.", "Existing tools, data exchanged and flow direction.")),
            (c.t("Choix de la solution", "Solution choice"), c.t("Connecteur partenaire, API Odoo ou développement spécifique.", "Partner connector, Odoo API or custom development.")),
            (c.t("Mise en place", "Build"), c.t("Paramétrage ou développement de l’intégration.", "Integration configured or developed.")),
            (c.t("Tests", "Testing"), c.t("Contrôle des flux de bout en bout avec vos équipes.", "End-to-end flow checks with your teams.")),
            (c.t("Suivi", "Follow-up"), c.t("Supervision et évolutions selon vos nouveaux besoins.", "Monitoring and changes as your needs evolve."))]),
        apps=["cti", "leexi", "crm", "helpdesk", "website", "ecommerce"],
        cases=["cameleon"],
        faq=[(c.t("Faut-il changer d’opérateur pour Ringover ?", "Do we need to change carrier for Ringover?"),
              c.t("Nous étudions votre installation actuelle et vous conseillons sur la meilleure façon de déployer Ringover avec Odoo.", "We review your current setup and advise on the best way to roll out Ringover with Odoo.")),
             (c.t("Leexi fonctionne-t-il en réunion physique ?", "Does Leexi work for in-person meetings?"),
              c.t("Oui : Leexi capture les échanges sur Google Meet, Microsoft Teams, Zoom, et aussi en présentiel.", "Yes: Leexi captures conversations on Google Meet, Microsoft Teams, Zoom, and in person too.")),
             (c.t("Pouvez-vous connecter un logiciel métier spécifique ?", "Can you connect an industry-specific tool?"),
              c.t("Oui, via les API d’Odoo ou des web services dédiés, après une étude des données à échanger.", "Yes, through Odoo’s APIs or dedicated web services, after reviewing the data to exchange."))],
        title=c.t("Intégrations Odoo : Ringover, Leexi.ai, API | DarbTech", "Odoo integrations: Ringover, Leexi.ai, APIs | DarbTech"),
        desc=c.t("Connectez Odoo à la téléphonie Ringover, à l’IA de réunion Leexi.ai et à vos logiciels métiers. DarbTech, partenaire Ringover et Leexi, Odoo Gold Partner.",
                 "Connect Odoo to Ringover telephony, Leexi.ai meeting AI and your business software. DarbTech, Ringover and Leexi partner and Odoo Gold Partner.")))


def page_odoo_support(c):
    support_note = (f'<div class="note" data-reveal style="margin-top:24px">{c.t("[Offres de support à préciser : formules, volumes et délais d’intervention.]", "[Support plans to be specified: packages, volumes and response times.]")}</div>')
    timeline = f'''<div class="mock-support" aria-hidden="true">
<div class="mock-support__row"><span class="tag tag--blue">{c.t("Formation", "Training")}</span><span class="mock-support__bar" style="--w:70%"></span></div>
<div class="mock-support__row"><span class="tag">{c.t("Ticket", "Ticket")} #128</span><span class="mock-support__bar mock-support__bar--o" style="--w:45%"></span></div>
<div class="mock-support__row"><span class="tag tag--gold">{c.t("Évolution", "Enhancement")}</span><span class="mock-support__bar mock-support__bar--g" style="--w:85%"></span></div>
</div>'''
    return service_page(c, "odoo_support", dict(
        crumb=c.t("Support & formation", "Support & training"), icon="lifebuoy",
        eyebrow=c.t("Support et formation Odoo", "Odoo support and training"),
        h1=c.t('Former vos équipes et <span class="accent accent--gold">faire vivre votre Odoo</span>', 'Train your teams and <span class="accent accent--gold">keep your Odoo alive</span>'),
        lead=c.t("Après le go-live, nous restons à vos côtés : formation de chaque équipe, maintenance corrective et évolutive, et adaptation de l’outil à vos nouvelles activités.",
                 "After go-live, we stay with you: training for every team, corrective and evolutive maintenance, and adapting the tool to new activities."),
        for_title=c.t("Un ERP ne s’arrête pas au go-live", "An ERP does not stop at go-live"),
        **{"for": [c.t("De nouveaux collaborateurs doivent prendre en main Odoo.", "New staff need to get started with Odoo."),
                   c.t("Votre activité évolue et l’outil doit suivre.", "Your business changes and the tool has to keep up."),
                   c.t("Vous voulez un interlocuteur qui connaît votre configuration.", "You want a contact who knows your configuration."),
                   c.t("Vous cherchez de la visibilité sur les demandes en cours et leurs coûts.", "You want visibility on open requests and their cost.")]},
        visual=timeline,
        scope_title=c.t("Un accompagnement dans la durée", "Long-term support"),
        scope_lead=c.t("Les dernières étapes de notre méthode, prolongées aussi longtemps que vous en avez besoin.", "The final steps of our method, extended for as long as you need."),
        scope=[("graduation", c.t("Formation par métier", "Role-based training"), c.t("Des sessions adaptées à chaque équipe : ventes, finance, logistique, production, RH…", "Sessions tailored to each team: sales, finance, logistics, production, HR…")),
               ("users", c.t("Accompagnement au changement", "Change management"), c.t("Un suivi au démarrage pour que l’outil soit vraiment adopté.", "Go-live support so the tool is truly adopted.")),
               ("lifebuoy", c.t("Maintenance corrective", "Corrective maintenance"), c.t("Analyse et correction des anomalies.", "Analysis and fixing of issues."), " card__icon--orange"),
               ("wrench", c.t("Évolutions", "Enhancements"), c.t("L’outil adapté à vos nouvelles activités et méthodes.", "The tool adapted to new activities and methods.")),
               ("eye", c.t("Suivi transparent", "Transparent tracking"), c.t("Des outils de suivi partagés : actions engagées et coûts associés.", "Shared tracking tools: work in progress and related costs.")),
               ("migrate", c.t("Montées de version", "Version upgrades"), c.t("Le moment venu, une migration préparée et testée.", "When the time comes, a prepared and tested migration."), " card__icon--gold")],
        extra=f'<section class="section section--tight" style="padding-top:0;background:var(--paper)"><div class="container">{support_note}</div></section>',
        steps_title=c.t("Notre méthode, jusqu’au bout", "Our method, all the way"),
        steps_lead=c.t("Formation et maintenance sont les étapes 4 et 5 de notre méthode : elles durent aussi longtemps que votre projet.", "Training and maintenance are steps 4 and 5 of our method, and they last as long as your project does."),
        apps=["helpdesk", "project", "hr", "accounting", "inventory"],
        cases=[],
        faq=[(c.t("Pouvez-vous former de nouveaux arrivants après le projet ?", "Can you train new starters after the project?"),
              c.t("Oui, nous organisons des sessions adaptées au rôle de chaque personne, à tout moment.", "Yes, we run sessions tailored to each person’s role, at any time.")),
             (c.t("Comment suivez-vous nos demandes ?", "How do you track our requests?"),
              c.t("Avec des outils de suivi partagés, qui donnent une vision claire des actions en cours et des coûts associés.", "With shared tracking tools that give a clear view of work in progress and the related costs.")),
             (c.t("Quelles formules de support proposez-vous ?", "Which support plans do you offer?"),
              c.t("Les formules sont définies avec vous selon votre contexte. [Détail des offres à confirmer par DarbTech.]", "Plans are defined with you based on your context. [Plan details to be confirmed by DarbTech.]"))],
        title=c.t("Support et formation Odoo | DarbTech", "Odoo support and training | DarbTech"),
        desc=c.t("Formation Odoo par métier, maintenance corrective et évolutive, suivi transparent : DarbTech, Odoo Gold Partner, accompagne vos équipes après le go-live.",
                 "Role-based Odoo training, corrective and evolutive maintenance, and transparent tracking: DarbTech, Odoo Gold Partner, supports your teams after go-live.")))


# ---------------------------------------------------------------------------
# Apps
# ---------------------------------------------------------------------------
def page_odoo_apps(c):
    d = c.data
    groups = []
    for gi, (gkey, gfr, gen, apps) in enumerate(APP_GROUPS):
        cards = []
        for i, (key, ic, col, fr, en, dfr, den, post) in enumerate(apps):
            link = ""
            if post and post in d["posts"]:
                p = d["posts"][post][c.lang]
                link = f'<a class="link-arrow" href="{esc(p["url"])}">{c.t("Lire l’article", "Read the article")}{icon("arrow-up-right")}</a>'
            if key == "crm":
                link = f'<a class="link-arrow" href="{c.href("case_cameleon")}">{c.t("Voir le cas CAMELEON", "See the CAMELEON case")}{icon("arrow-right")}</a>'
            if key in ("leexi", "cti"):
                link = f'<a class="link-arrow" href="{c.href("odoo_integrations")}">{c.t("Voir les intégrations", "See integrations")}{icon("arrow-right")}</a>'
            cards.append(f'<article class="card app-card" data-reveal style="--i:{i % 3}"><span class="card__icon" style="--c:{col}">{icon(ic)}</span>'
                         f'<div><h3>{fr if c.lang == "fr" else en}</h3><p>{dfr if c.lang == "fr" else den}</p>{link}</div></article>')
        groups.append(f'<div class="app-group"><div class="app-group__head" data-reveal><h2>{gfr if c.lang == "fr" else gen}</h2>'
                      f'<span class="mono muted" style="font-size:.8rem">{len(apps):02d} apps</span></div>'
                      f'<div class="grid grid--3">{"".join(cards)}</div></div>')
    body = page_hero(c, [("Odoo", "odoo"), (c.t("Applications", "Apps"), None)], c.t("Applications Odoo", "Odoo apps"),
                     c.t('Les applications Odoo, <span class="accent accent--gold">reliées entre elles</span>', 'Odoo apps, <span class="accent accent--gold">working as one</span>'),
                     c.t("Odoo réunit CRM et ERP dans une seule plateforme. Voici le périmètre fonctionnel que couvrent nos projets et nos articles : de la vente à la paie, en passant par la production.",
                         "Odoo brings CRM and ERP together in one platform. Here is the functional scope our projects and articles cover: from sales to payroll, by way of manufacturing."),
                     btn(c.href("contact"), c.t("Parler de votre périmètre", "Discuss your scope"), "primary", magnetic=True),
                     aside=hero_tile("grid"), chip=True)
    body += f'''<section class="section" aria-label="{c.t("Applications par domaine", "Apps by area")}"><div class="container">
<p class="muted" data-reveal style="margin-bottom:40px;max-width:70ch">{c.t("Liste indicative, construite à partir de nos projets, de nos articles et de notre propre instance Odoo. Nous définissons avec vous les applications utiles à votre activité.", "An indicative list, based on our projects, our articles and our own Odoo instance. We define with you which apps your business actually needs.")}</p>
{"".join(groups)}
</div></section>'''
    body += cta_band(c, c.t('Quelles applications pour <span class="accent accent--gold">votre activité</span> ?', 'Which apps for <span class="accent accent--gold">your business</span>?'))
    return dict(
        title=c.t("Applications Odoo : CRM, ventes, stock, compta, MRP | DarbTech", "Odoo apps: CRM, sales, inventory, accounting, MRP | DarbTech"),
        desc=c.t("CRM, ventes, comptabilité, inventaire, achats, fabrication, projet, helpdesk, RH, paie, eCommerce : les applications Odoo que DarbTech intègre et relie entre elles.",
                 "CRM, sales, accounting, inventory, purchase, manufacturing, project, helpdesk, HR, payroll, eCommerce: the Odoo apps DarbTech implements and connects."),
        body=body, trail=[("Odoo", "odoo"), (c.t("Applications", "Apps"), None)])
