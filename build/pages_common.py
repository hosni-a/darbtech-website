"""Reusable content sections shared by several pages (FR/EN copy inline via c.t)."""
from lib import (esc, icon, btn, gold_chip, section_head, checklist, tags, OFFICES, EMAIL, LINKEDIN)

# Odoo apps, grouped. (key, icon, colour, FR name, EN name, FR desc, EN desc, blog post id or None)
APP_GROUPS = [
    ("sales", "Ventes & relation client", "Sales & customer relationship", [
        ("crm", "target", "#0047BB", "CRM", "CRM", "Pistes, opportunités et prévisions commerciales dans un pipeline partagé.", "Leads, opportunities and sales forecasts in one shared pipeline.", None),
        ("sales", "tag", "#1F63E0", "Ventes", "Sales", "Devis, commandes et suivi client, reliés au stock et à la facturation.", "Quotes, orders and customer follow-up, linked to inventory and invoicing.", None),
        ("marketing", "megaphone", "#B84E0E", "Marketing automation", "Marketing automation", "Campagnes et messages ciblés, déclenchés selon le parcours client.", "Targeted campaigns and messages triggered along the customer journey.", None),
        ("ecommerce", "bag", "#6E4BD8", "eCommerce", "eCommerce", "Boutique en ligne branchée en direct sur vos produits et vos stocks.", "An online shop connected live to your products and stock.", None),
        ("website", "monitor", "#0F7F74", "Site web", "Website", "Site vitrine éditable, intégré au CRM pour capter les demandes.", "An editable website, wired to the CRM to capture enquiries.", None),
        ("pos", "card", "#C2366F", "Point de vente", "Point of Sale", "Encaissement en boutique, synchronisé avec les ventes et le stock.", "In-store checkout, synchronised with sales and stock.", None),
    ]),
    ("finance", "Finance", "Finance", [
        ("accounting", "chart", "#0047BB", "Comptabilité", "Accounting", "Écritures, rapprochements et reporting financier dans l’ERP.", "Entries, reconciliation and financial reporting inside the ERP.", None),
        ("invoicing", "receipt", "#B8862A", "Facturation", "Invoicing", "Factures et relances générées depuis les ventes et les projets.", "Invoices and reminders generated from sales and projects.", None),
    ]),
    ("ops", "Opérations", "Operations", [
        ("inventory", "box", "#0F7F74", "Inventaire", "Inventory", "Stocks, entrepôts et mouvements suivis en temps réel.", "Stock, warehouses and moves tracked in real time.", None),
        ("purchase", "cart", "#1F63E0", "Achats", "Purchase", "Demandes de prix et commandes fournisseurs reliées au stock.", "Requests for quotation and purchase orders tied to stock.", None),
        ("mrp", "factory", "#B84E0E", "Fabrication (MRP)", "Manufacturing (MRP)", "Nomenclatures, ordres de fabrication et planification de la production.", "Bills of materials, manufacturing orders and production planning.", "4"),
        ("planning", "calendar", "#6E4BD8", "Planning", "Planning", "Planification des équipes, de la production et des interventions.", "Scheduling for teams, production and field work.", None),
        ("project", "kanban", "#0047BB", "Projet", "Project", "Tâches, jalons et feuilles de temps pour piloter vos projets.", "Tasks, milestones and timesheets to run your projects.", None),
        ("helpdesk", "headset", "#C2366F", "Helpdesk", "Helpdesk", "Tickets clients centralisés, priorisés et suivis jusqu’à résolution.", "Customer tickets centralised, prioritised and tracked to resolution.", "1"),
    ]),
    ("hr", "Ressources humaines", "Human resources", [
        ("hr", "users", "#0047BB", "Employés (RH)", "Employees (HR)", "Dossiers salariés, organisation et absences au même endroit.", "Employee records, organisation and time off in one place.", None),
        ("payroll", "wallet", "#B8862A", "Paie", "Payroll", "Préparation de la paie à partir des données RH.", "Payroll preparation from your HR data.", None),
        ("recruitment", "user-plus", "#0F7F74", "Recrutement", "Recruitment", "Offres, candidatures et entretiens suivis dans un pipeline.", "Job posts, applications and interviews tracked in a pipeline.", None),
    ]),
    ("integrations", "Intégrations partenaires", "Partner integrations", [
        ("cti", "phone", "#1F63E0", "Téléphonie CTI (Ringover)", "CTI telephony (Ringover)", "Appels, SVI et statistiques téléphoniques reliés au CRM.", "Calls, IVR and call analytics connected to the CRM.", "3"),
        ("leexi", "mic", "#6E4BD8", "IA de réunion (Leexi.ai)", "Meeting AI (Leexi.ai)", "Comptes rendus et actions générés par l’IA, remontés dans Odoo.", "AI-generated summaries and action items, pushed into Odoo.", None),
    ]),
]


def all_apps():
    for g in APP_GROUPS:
        for a in g[3]:
            yield a


def app_chip(c, key):
    for a in all_apps():
        if a[0] == key:
            return f'<li class="app-chip"><i style="--c:{a[2]}">{icon(a[1])}</i>{a[3] if c.lang == "fr" else a[4]}</li>'
    raise KeyError(key)


def apps_cloud(c, keys):
    return '<ul class="apps-cloud">' + "".join(app_chip(c, k) for k in keys) + "</ul>"


# ---------------------------------------------------------------------------
def method_steps(c, detailed=False):
    steps = [
        ("search",
         c.t("Étude et analyse", "Study and analysis"),
         c.t("Nous étudions votre activité et vos procédures, service par service, ainsi que les échanges entre services et avec vos logiciels métiers.",
             "We study your business and procedures, department by department, including how departments work together and with your existing business software."),
         c.t("Analyse de l’existant, cartographie des flux, interconnexions à prévoir",
             "Current-state review, process map, integrations to plan")),
        ("sliders",
         c.t("Adaptation des processus", "Process alignment"),
         c.t("Nous ajustons vos procédures à la logique de l’ERP pour tirer parti du standard Odoo, sans perdre ce qui fait votre spécificité.",
             "We align your procedures with the ERP’s logic to get the most from standard Odoo, without losing what makes you different."),
         c.t("Processus cibles, choix standard ou spécifique", "Target processes, standard vs custom decisions")),
        ("layers",
         c.t("Implémentation", "Implementation"),
         c.t("Nous paramétrons les modules standards et développons les modules spécifiques qui ajustent l’outil à vos méthodes de travail.",
             "We configure the standard apps and build the custom modules that fit the tool to the way you work."),
         c.t("Paramétrage, modules spécifiques, tests", "Configuration, custom modules, testing")),
        ("graduation",
         c.t("Formation et accompagnement", "Training and support"),
         c.t("Nous formons et accompagnons chaque équipe, de la prise en main jusqu’à l’usage quotidien.",
             "We train and support every team, from first steps to everyday use."),
         c.t("Formation par métier, accompagnement au démarrage", "Role-based training, go-live support")),
        ("wrench",
         c.t("Maintenance et évolutions", "Maintenance and evolution"),
         c.t("Nous maintenons votre Odoo pour qu’il suive vos nouvelles activités et vos nouvelles façons de travailler.",
             "We maintain your Odoo so it keeps up with new activities and new ways of working."),
         c.t("Maintenance, évolutions, montées de version", "Maintenance, enhancements, version upgrades")),
    ]
    items = []
    for n, (ic, title, text, deliv) in enumerate(steps, start=1):
        d = ""
        if detailed:
            d = '<ul class="step__deliv">' + "".join(f'<li class="tag tag--blue">{esc(x.strip()[:1].upper() + x.strip()[1:])}</li>' for x in deliv.split(",")) + "</ul>"
        items.append(f'<li class="step" data-reveal style="--i:{n % 2}"><span class="step__dot">0{n}</span>'
                     f'<div class="step__body"><h3 class="step__title">{title}</h3><p class="step__text">{text}</p>{d}</div></li>')
    return f'<ol class="steps" data-steps><span class="steps__line" aria-hidden="true"><span></span></span>{"".join(items)}</ol>'


def values_cards(c, dark=False):
    vals = [
        ("repeat", "Agile-Scrum",
         c.t("Des cycles courts qui vous gardent impliqué à chaque étape et alignent le projet sur vos vrais besoins.",
             "Short cycles keep you involved at every step and keep the project aligned with your real needs.")),
        ("infinity", "DevOps",
         c.t("Des procédés industrialisés, de l’automatisation au déploiement continu, dans une logique d’amélioration continue.",
             "Industrialised delivery, from automation to continuous deployment, with continuous improvement built in.")),
        ("eye", c.t("Transparence", "Transparency"),
         c.t("Des outils de suivi partagés qui donnent une vision claire des actions engagées et des coûts associés.",
             "Shared tracking tools give you a clear view of the work in progress and the related costs.")),
        ("target", c.t("Engagement", "Commitment"),
         c.t("Tout projet connaît des aléas. Nous les anticipons pour dé-risquer le projet et le mener à bien, à vos côtés.",
             "Every project meets obstacles. We anticipate them to de-risk delivery and see it through, alongside you.")),
    ]
    return '<div class="grid grid--4">' + "".join(
        f'<article class="card card--hover" data-reveal style="--i:{i}"><span class="card__icon{" card__icon--gold" if i == 3 else ""}">{icon(ic)}</span>'
        f'<h3 class="card__title">{t}</h3><p class="card__text">{d}</p></article>'
        for i, (ic, t, d) in enumerate(vals)) + "</div>"


def gold_panel(c):
    facts = [
        c.t("Partenaire Odoo depuis 2015, de la V8 aux dernières versions, en Community comme en Enterprise",
            "Odoo partner since 2015, from V8 to the latest releases, on both Community and Enterprise"),
        c.t("100 % de nos consultants et développeurs certifiés Odoo", "100% of our consultants and developers are Odoo-certified"),
        c.t("Une équipe intégrée de 21 personnes entre Paris et Rabat", "One integrated team of 21 people across Paris and Rabat"),
        c.t("Partenaire officiel de Ringover et partenaire de Leexi.ai, pour aller au-delà de l’ERP", "Official Ringover partner and Leexi.ai partner, to go beyond the ERP"),
    ]
    fl = "".join(f'<li>{icon("check")}<span>{f}</span></li>' for f in facts)
    return f'''<section class="section gold-section on-dark" aria-labelledby="gold-title">
<div class="bg-grid"></div>
<div class="container"><div class="gold-panel" data-reveal="scale"><div class="gold-panel__inner">
<div class="gold-panel__body">
{gold_chip(c)}
<h2 id="gold-title">{c.t('Odoo Gold Partner <span class="accent accent--gold">depuis le 22 septembre 2026</span>', 'Odoo Gold Partner <span class="accent accent--gold">since 22 September 2026</span>')}</h2>
<p class="lead">{c.t("Le niveau Gold est attribué par Odoo à ses partenaires. Il s’inscrit dans plus de dix ans d’accompagnement de PME et d’ETI sur Odoo. Pour vous, c’est l’assurance d’une équipe expérimentée, certifiée et engagée dans la durée.",
                     "Gold is a partner level awarded by Odoo. It builds on more than ten years of helping SMEs and mid-market companies with Odoo. For you, it means an experienced, certified team that is in it for the long run.")}</p>
<ul class="gold-facts">{fl}</ul>
<a class="link-arrow" href="{c.href("odoo")}">{c.t("Nos services Odoo", "Our Odoo services")}{icon("arrow-right")}</a>
</div>
<div class="gold-date">
<span class="gold-date__label">{c.t("Parcours partenaire", "Partner journey")}</span>
<ol class="mini-timeline">
<li><time datetime="2015">2015</time><strong>{c.t("Partenaire Odoo certifié", "Certified Odoo partner")}</strong><span>{c.t("Premiers projets Odoo, dès la V8", "First Odoo projects, from V8")}</span></li>
<li class="is-gold"><time datetime="2026-09-22">22.09.2026</time><strong>Odoo Gold Partner</strong><span>{c.t("Un nouveau niveau de partenariat avec Odoo", "A new partnership level with Odoo")}</span></li>
<li><time datetime="2026-10">{c.t("Aujourd’hui", "Today")}</time><strong>{c.t("21 experts certifiés Odoo", "21 Odoo-certified experts")}</strong><span>{c.t("Conseil, intégration et développement, à Paris et à Rabat", "Consulting, implementation and development, in Paris and Rabat")}</span></li>
</ol>
</div>
</div></div></div></section>'''


def stats_light(c):
    return f'''<ul class="stats stats--light" data-reveal>
<li class="stat"><span class="stat__num" data-count="2015" data-from="2000">2015</span><span class="stat__label">{c.t("Partenaire Odoo depuis", "Odoo partner since")}</span></li>
<li class="stat"><span class="stat__num"><span data-count="21">21</span></span><span class="stat__label">{c.t("experts à Paris et Rabat", "experts in Paris and Rabat")}</span></li>
<li class="stat"><span class="stat__num"><span data-count="100">100</span><small>%</small></span><span class="stat__label">{c.t("consultants certifiés Odoo", "Odoo-certified consultants")}</span></li>
<li class="stat"><span class="stat__num">V8<small>→</small></span><span class="stat__label">{c.t("jusqu’aux dernières versions", "to the latest releases")}</span></li>
</ul>'''


CLIENTS = [
    ("netiwan GROUPE", "img/clients/netiwan.png"),
    ("CMT GROUP", "img/clients/cmt-group.png"),
    ("PUTHOD PÉPINIÈRES", "img/clients/puthod.png"),
    ("L’AMBASSADE DES LANGUES PARIS", "img/clients/ambassade-des-langues.png"),
    ("ACSP Conseil", "img/clients/acsp-conseil.png"),
    ("tionis", "img/clients/tionis.png"),
    ("CAMELEON", None),
]


def logo_tiles(c, hidden=False):
    out = []
    for name, img in CLIENTS:
        if img:
            alt = "" if hidden else esc(name)
            out.append(f'<li class="logo-tile"><img src="{c.asset(img)}" alt="{alt}" loading="lazy" decoding="async"></li>')
        else:
            out.append(f'<li class="logo-tile logo-tile--word"{"" if hidden else ""}>{esc(name)}</li>')
    return "".join(out)


def logo_marquee(c):
    return f'''<section class="logos" aria-labelledby="logos-title">
<div class="container"><h2 class="logos__label" id="logos-title">{c.t("Ils nous font confiance", "Trusted by")}</h2></div>
<div class="marquee"><div class="marquee__track"><ul class="marquee__group">{logo_tiles(c)}</ul><ul class="marquee__group" aria-hidden="true">{logo_tiles(c, hidden=True)}</ul></div></div>
</section>'''


CASES = {
    "puthod": {
        "page": "case_puthod", "img": "img/cases/puthod.webp", "post": "18",
        "client": "PUTHOD Pépinières",
        "fr": {
            "sector": "Aménagement paysager", "region": "Pays de Savoie",
            "scope": "Odoo ERP · modules standards et spécifiques",
            "title": "PUTHOD : du papier à un outil unique dans Odoo",
            "short": "Des fiches papier ressaisies au bureau à un outil unique, partagé par le terrain et le back-office.",
            "lead": "Spécialiste de l’aménagement paysager en Pays de Savoie, PUTHOD voulait digitaliser ses processus métier et en finir avec les fiches remplies à la main puis ressaisies dans l’outil informatique.",
            "challenge": ["Plusieurs équipes mobiles remplissaient chaque jour des fiches papier.",
                          "Le back-office ressaisissait l’ensemble de ces fiches pour éditer les bilans de chantier.",
                          "Le risque d’oublier une information était très important."],
            "solution": ["Mise en place des modules standards d’Odoo.",
                         "Développement de modules spécifiques pour correspondre aux processus métier.",
                         "Regroupement de toutes les informations utiles d’un chantier végétal dans un outil unique, accessible à l’ensemble du personnel."],
            "outcome": "Résultat : un gain de productivité et d’efficacité, avec une information centralisée et partagée entre le terrain et le bureau.",
            "tags": ["ERP Odoo", "Modules spécifiques", "Équipes mobiles"],
        },
        "en": {
            "sector": "Landscaping", "region": "Pays de Savoie, France",
            "scope": "Odoo ERP · standard and custom modules",
            "title": "PUTHOD: from paper forms to a single tool in Odoo",
            "short": "From paper forms re-keyed at the office to one tool shared by field teams and the back office.",
            "lead": "PUTHOD, a landscaping specialist in the Pays de Savoie region, wanted to digitise its business processes and stop filling in forms by hand only to type them up again at the office.",
            "challenge": ["Several mobile teams filled in paper forms every day.",
                          "The back office re-keyed every form to produce site reports.",
                          "The risk of losing information along the way was high."],
            "solution": ["Roll-out of standard Odoo apps.",
                         "Custom modules built around the company’s business processes.",
                         "All the relevant information for each landscaping project gathered in a single tool, available to every employee."],
            "outcome": "The result: higher productivity and efficiency, with information centralised and shared between the field and the office.",
            "tags": ["Odoo ERP", "Custom modules", "Mobile teams"],
        },
    },
    "cameleon": {
        "page": "case_cameleon", "img": "img/cases/cameleon.webp", "post": "19",
        "client": "CAMELEON",
        "fr": {
            "sector": "Événementiel d’entreprise", "region": "Pays de Savoie",
            "scope": "Odoo CRM · fonctionnalités spécifiques · rapports",
            "title": "CAMELEON : un CRM Odoo pour des équipes commerciales multi-sites",
            "short": "Un suivi commercial uniformisé entre plusieurs sites, et des rapports prêts pour la comptabilité et la direction.",
            "lead": "CAMELEON crée des événements sur mesure pour les entreprises. Ses équipes commerciales, réparties sur plusieurs sites distants, avaient besoin d’un suivi plus rigoureux de leurs pistes et de leurs offres.",
            "challenge": ["Uniformiser les procédures d’ajout et de suivi des pistes et des opportunités.",
                          "Traiter les données commerciales pour établir les prévisionnels."],
            "solution": ["Mise en place du module CRM standard d’Odoo.",
                         "Développement de quelques fonctionnalités spécifiques pour l’ajout des pistes dans la base.",
                         "Mise en forme de modèles de rapports, pour un export directement exploitable par le service comptable et la direction."],
            "outcome": "Résultat : des procédures commerciales communes à tous les sites et des données directement exploitables par la comptabilité et la direction.",
            "tags": ["CRM Odoo", "Multi-sites", "Reporting"],
        },
        "en": {
            "sector": "Corporate events", "region": "Pays de Savoie, France",
            "scope": "Odoo CRM · custom features · reports",
            "title": "CAMELEON: an Odoo CRM for sales teams across several sites",
            "short": "Consistent sales follow-up across several sites, with reports ready for finance and management.",
            "lead": "CAMELEON designs tailor-made events for businesses. Its sales teams, spread across several remote sites, needed tighter tracking of their leads and quotes.",
            "challenge": ["Standardise how leads and opportunities are added and followed up.",
                          "Process sales data to build forecasts."],
            "solution": ["Roll-out of the standard Odoo CRM app.",
                         "A few custom features to add leads to the database.",
                         "Report templates designed so that exports can be used directly by the accounting team and management."],
            "outcome": "The result: the same sales procedures on every site, and data that finance and management can use straight away.",
            "tags": ["Odoo CRM", "Multi-site", "Reporting"],
        },
    },
}


def case_card(c, key, i=0, heading="h3"):
    cs = CASES[key]
    d = cs[c.lang]
    return (f'<a class="case-card" href="{c.href(cs["page"])}" data-reveal style="--i:{i}">'
            f'<div class="case-card__media"><img src="{c.asset(cs["img"])}" alt="" loading="lazy" decoding="async"></div>'
            f'<div class="case-card__body"><span class="case-card__client">{esc(cs["client"])} · {esc(d["sector"])}</span>'
            f'<{heading}>{esc(d["title"])}</{heading}><p>{esc(d["short"])}</p>{tags(d["tags"])}'
            f'<span class="link-arrow" style="color:#fff">{c.t("Lire l’étude de cas", "Read the case study")}{icon("arrow-right")}</span></div></a>')


def offices_cards(c):
    out = []
    for key, o in OFFICES.items():
        out.append(f'''<article class="office" data-reveal>
<div class="office__head"><span class="office__city">{o["city"][c.lang]}</span><span class="tag">{o["country"][c.lang]}</span></div>
<address>{o["entity"]}<br>{o["street"]}<br>{o["postcode"]} {o["locality"]}</address>
<a class="office__line" href="tel:{o["tel"]}">{icon("phone")}{o["phone"]}</a>
</article>''')
    return "".join(out)


def team_teaser(c, team, dark=True):
    imgs = "".join(f'<img src="{c.asset(m["photo"])}" alt="" loading="lazy" width="44" height="44">' for m in team[:7])
    more = len(team) - 7
    return (f'<div class="avatar-stack" aria-hidden="true">{imgs}<span class="avatar-stack__more">+{more}</span></div>')
