#!/usr/bin/env python3
"""Regenerate the 10 metier landing pages with updated messaging (no WhatsApp, app-first)."""

import json
from html import escape
from urllib.parse import quote

METIERS = [
    {
        "id": "osteopathe", "emoji": "🦴", "label": "Ostéopathes",
        "title_doc": "Notes d'honoraires & fiches conseil IA",
        "desc": "Le copilote IA pour ostéopathes : dictez vos notes de séance, générez vos notes d'honoraires, préparez des fiches conseil personnalisées. Tout depuis votre iPhone.",
        "keywords": "ostéopathe facturation, note honoraires ostéo, application ostéopathe, fiche conseil patient, gestion cabinet ostéo",
        "pain": "Vos notes de séance s'accumulent sur papier ? Vos patients n'ont aucun suivi entre deux consultations ? La facturation vous prend plus de temps que les soins ?",
        "features": [
            ("🎤", "Dictée notes de séance", "Dictez en langage naturel après chaque consultation. L'IA structure : motif, techniques, observations, douleur, plan de suivi."),
            ("🩺", "Fiche conseil patient IA", "Après chaque séance, une fiche personnalisée avec exercices et prévention — prête à partager au patient."),
            ("📋", "Briefing pré-séance", "Avant chaque patient, un résumé IA : historique, dernière séance, progression, points d'attention. Zéro préparation."),
            ("📄", "Notes d'honoraires PDF", "Prêtes à relire avec mentions, numérotation et TVA adaptée."),
            ("💳", "Paiement cadré", "On vérifie le mode de règlement adapté avant d'activer un lien ou un process de paiement."),
            ("📈", "Suivi longitudinal", "Évolution de la douleur séance après séance. Tendances et progrès en un coup d'œil."),
        ],
        "example": "Consultation Emma Laurent, douleur lombaire chronique, techniques tissulaires sur le psoas, amélioration mobilité, score douleur 7/10, revoir dans 2 semaines.",
    },
    {
        "id": "kinesitherapeute", "emoji": "💆", "label": "Kinésithérapeutes",
        "title_doc": "Facturation & suivi patient IA",
        "desc": "Diqto pour kinés : dictez vos bilans, préparez vos notes d'honoraires, suivez la progression de vos patients avec l'IA.",
        "keywords": "kiné facturation, application kinésithérapeute, bilan kiné IA, suivi patient kiné",
        "pain": "Entre les bilans, les factures et le suivi des patients, vous passez plus de temps en administratif qu'en rééducation ?",
        "features": [
            ("🎤", "Dictée bilan & notes", "Dictez vos bilans et notes de séance. Diqto prépare un brouillon structuré."),
            ("🩺", "Fiche conseil patient", "Exercices personnalisés envoyés au patient après chaque séance."),
            ("📄", "Facturation prête à relire", "Notes d'honoraires, tiers payant et TVA adaptée sous validation humaine."),
            ("💳", "Paiement cadré", "On qualifie le mode de règlement adapté avant d'activer un lien de paiement."),
            ("📈", "Suivi progression", "Évolution fonctionnelle séance après séance."),
            ("🏛️", "URSSAF & comptabilité", "Alertes cotisations, livre des recettes, export FEC."),
        ],
        "example": "Bilan kiné M. Dupont, entorse cheville gauche J+15, mobilité 80%, renforcement proprioceptif, 10 séances prescrites.",
    },
    {
        "id": "plombier", "emoji": "🔧", "label": "Plombiers",
        "title_doc": "Devis & factures IA",
        "desc": "Diqto pour plombiers : dictez le chantier, relisez le brouillon de devis, puis partagez sous contrôle humain. Paiement et relance restent cadrés avant activation.",
        "keywords": "devis plombier, facture plombier, application plombier, diagnostic métier plombier",
        "pain": "Vous faites vos devis sur papier entre deux interventions ? Vous perdez du temps à recopier les mêmes lignes ?",
        "features": [
            ("🎤", "Dictez votre devis", "Entre deux interventions, dictez. L'IA structure : main d'œuvre, fournitures, TVA."),
            ("📸", "Photo → brouillon IA", "Photographiez le chantier. Diqto prépare un brouillon à relire avec prestations, fournitures et TVA."),
            ("📄", "Brouillons PDF conformes", "Devis et factures prêts à relire avec mentions légales, numérotation et conditions."),
            ("💳", "Paiement cadré", "On vérifie le mode de règlement adapté avant d'activer un lien ou un process de paiement."),
            ("🔄", "Relances pilotées", "Diqto prépare les prochaines relances et garde le contexte client, sans envoi aveugle."),
            ("🏛️", "URSSAF", "Alertes cotisations, seuil TVA, livre des recettes."),
        ],
        "example": "Devis pour Mme Martin, remplacement chauffe-eau 200L, fourniture 450€, pose 250€, dépose ancien 80€.",
    },
    {
        "id": "electricien", "emoji": "⚡", "label": "Électriciens",
        "title_doc": "Devis & factures IA",
        "desc": "Diqto pour électriciens : devis et factures depuis l'iPhone. Dictez, relisez, puis partagez sous contrôle humain.",
        "keywords": "devis électricien, facture électricien, application électricien",
        "pain": "Les devis prennent plus de temps que les interventions ?",
        "features": [
            ("🎤", "Dictez", "Dictez votre devis en langage naturel. L'IA structure tout."),
            ("📸", "Photo → brouillon", "Photographiez le tableau électrique. Diqto prépare un brouillon à relire."),
            ("📄", "PDF conformes", "Devis et factures prêts à relire avec mentions, numérotation et conditions."),
            ("💳", "Paiement cadré", "On vérifie le mode de règlement adapté avant activation."),
            ("🔄", "Relances", "Préparées à J+7, J+15, J+30, avec contexte client."),
            ("🧠", "Catalogue appris", "Vos prestations habituelles en 1 tap."),
        ],
        "example": "Devis installation tableau électrique 3 rangées, mise aux normes NF C 15-100, 12 points lumineux.",
    },
    {
        "id": "photographe", "emoji": "📸", "label": "Photographes",
        "title_doc": "Devis & factures IA",
        "desc": "Diqto pour photographes : devis shooting, factures et relances préparés à relire depuis l'iPhone.",
        "keywords": "devis photographe, facture photographe, application photographe freelance",
        "pain": "Vos devis de shooting prennent autant de temps que le shooting lui-même ?",
        "features": [
            ("🎤", "Dictez", "Dictez vos devis et factures en langage naturel."),
            ("📄", "PDF pro", "Devis shooting avec prestations détaillées."),
            ("💳", "Paiement cadré", "Acompte et solde restent qualifiés avant activation du paiement."),
            ("🔄", "Relances", "Préparées avec contexte pour les retards de paiement."),
            ("🧠", "Catalogue", "Vos formules shooting en 1 tap."),
            ("✍️", "Signature cadrée", "Devis préparé pour signature après validation humaine."),
        ],
        "example": "Devis shooting mariage 8h, prestation 1200€, album 30 pages 350€, tirages 150€.",
    },
    {
        "id": "coach-sportif", "emoji": "🥋", "label": "Coachs sportifs",
        "title_doc": "Abonnements & facturation IA",
        "desc": "Diqto pour coachs : gérez vos élèves, formules d'abonnement et facturation batch préparée sous contrôle humain.",
        "keywords": "facturation coach sportif, gestion élèves coach, abonnement cours sport",
        "pain": "Vous courez après les cotisations de vos élèves ? La gestion administrative freine votre activité ?",
        "features": [
            ("🎓", "Gestion élèves", "Formules, inscriptions, suivi. Tout en un endroit."),
            ("💰", "Facturation batch", "Préparez vos factures élèves en lot à la fin du mois."),
            ("🔄", "Relances pilotées", "Diqto prépare les relances avec contexte, sans envoi aveugle."),
            ("📊", "Coach IA Business", "Suggestions pricing, rétention élèves, saisonnalité."),
            ("💳", "Paiement cadré", "On qualifie le mode de règlement adapté avant activation."),
            ("🏛️", "URSSAF", "Alertes et estimations cotisations."),
        ],
        "example": "Emma Laurent, formule mensuelle yoga 45€, cours collectif mardi et jeudi.",
    },
    {
        "id": "peintre", "emoji": "🎨", "label": "Peintres en bâtiment",
        "title_doc": "Devis & factures IA",
        "desc": "Diqto pour peintres : devis chantier par la voix, factures prêtes à relire, relances pilotées.",
        "keywords": "devis peintre, facture peintre bâtiment, application peintre",
        "pain": "Chiffrer un chantier vous prend plus de temps que le peindre ?",
        "features": [
            ("🎤", "Dictez", "Dictez votre devis sur le chantier."),
            ("📄", "PDF conformes", "Devis détaillés : main d'œuvre + fournitures + TVA."),
            ("💳", "Paiement cadré", "Acompte et solde restent qualifiés avant activation du paiement."),
            ("🔄", "Relances", "Préparées à J+7, J+15, J+30, avec contexte client."),
            ("🧠", "Catalogue", "Vos prestations habituelles en 1 tap."),
            ("🏛️", "URSSAF", "Alertes seuils et cotisations."),
        ],
        "example": "Devis peinture salon 35m², 2 couches acrylique mat, préparation murs, fournitures incluses.",
    },
    {
        "id": "menuisier", "emoji": "🪵", "label": "Menuisiers",
        "title_doc": "Devis & factures IA",
        "desc": "Diqto pour menuisiers : devis sur mesure par la voix, PDF prêts à relire, paiement cadré avant activation.",
        "keywords": "devis menuisier, facture menuisier, application menuisier",
        "pain": "Les devis sur mesure vous prennent des heures ?",
        "features": [
            ("🎤", "Dictez", "Dictez vos devis en langage naturel."),
            ("📄", "PDF pro", "Devis détaillés avec main d'œuvre et fournitures."),
            ("💳", "Paiement cadré", "On vérifie le mode de règlement adapté avant activation."),
            ("🔄", "Relances", "Préparées avec contexte client."),
            ("🧠", "Catalogue", "Vos réalisations habituelles en 1 tap."),
            ("✍️", "Signature cadrée", "Devis préparé pour signature après validation humaine."),
        ],
        "example": "Devis bibliothèque sur mesure chêne massif, 2m40 × 3m, 6 étagères, finition vernis mat.",
    },
    {
        "id": "professeur-yoga", "emoji": "🧘", "label": "Professeurs de yoga",
        "title_doc": "Abonnements & facturation IA",
        "desc": "Diqto pour profs de yoga : gérez vos élèves, abonnements et facturation préparée. Concentrez-vous sur l'enseignement.",
        "keywords": "facturation yoga, gestion élèves yoga, abonnement cours yoga",
        "pain": "La gestion de vos élèves et abonnements vous prend plus de temps que vos cours ?",
        "features": [
            ("🎓", "Élèves & formules", "Inscriptions, formules mensuel/trimestriel/annuel."),
            ("💰", "Facturation batch", "Préparez les factures élèves en lot sous contrôle humain."),
            ("🔄", "Relances", "Paiements en retard préparés avec contexte avant action."),
            ("📊", "Insights IA", "Suggestions pricing et rétention."),
            ("💳", "Paiement cadré", "On qualifie le mode de règlement adapté avant activation."),
            ("🏛️", "URSSAF", "Cotisations et seuils."),
        ],
        "example": "Chloé Martin, formule trimestrielle yoga vinyasa, 2 cours par semaine, 120€/trimestre.",
    },
    {
        "id": "carreleur", "emoji": "🏗️", "label": "Carreleurs",
        "title_doc": "Devis & factures IA",
        "desc": "Diqto pour carreleurs : devis chantier par la voix ou la photo, factures prêtes à relire, paiement cadré avant activation.",
        "keywords": "devis carreleur, facture carreleur, application carreleur",
        "pain": "Chiffrer un chantier entre deux poses vous ralentit ?",
        "features": [
            ("🎤", "Dictez", "Dictez votre devis sur le chantier."),
            ("📸", "Photo → brouillon", "Photographiez la pièce. Diqto prépare un brouillon à relire."),
            ("📄", "PDF conformes", "Main d'œuvre + fournitures + TVA."),
            ("💳", "Paiement cadré", "On vérifie le mode de règlement adapté avant activation."),
            ("🔄", "Relances", "Préparées avec contexte client."),
            ("🧠", "Catalogue", "Vos prestations en 1 tap."),
        ],
        "example": "Devis pose carrelage 60×60 salle de bain 12m², fourniture joints, préparation sol, dépose ancien.",
    },
]

TEMPLATE = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_attr}</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 38'><rect width='48' height='38' rx='19' ry='19' fill='%236366f1'/><rect x='8' y='13' width='4' height='12' rx='2' fill='white' opacity='.8'/><rect x='15' y='8' width='4' height='22' rx='2' fill='white' opacity='.8'/><rect x='22' y='5' width='4' height='28' rx='2' fill='white' opacity='.8'/><rect x='29' y='10' width='4' height='18' rx='2' fill='white' opacity='.8'/><rect x='36' y='14' width='4' height='10' rx='2' fill='white' opacity='.8'/></svg>">
<link rel="apple-touch-icon" href="./apple-touch-icon.png">
<link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<meta name="description" content="{desc_attr}">
<meta name="keywords" content="{keywords_attr}">
<link rel="canonical" href="{canonical_url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical_url}">
<meta property="og:title" content="{og_title_attr}">
<meta property="og:description" content="{desc_attr}">
<meta property="og:image" content="{og_image}">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Diqto">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title_attr}">
<meta name="twitter:description" content="{desc_attr}">
<meta name="twitter:image" content="{og_image}">
<script type="application/ld+json">
{schema_json}
</script>
<style>
:root {{ --bg:#0C0C0C; --primary:#6366F1; --green:#22C55E; --text:#fff; --dim:#9CA3AF; --card:#1A1A2E; --border:#2A2A3E; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'Work Sans',sans-serif; background:var(--bg); color:var(--text); }}
.container {{ max-width:800px; margin:0 auto; padding:0 24px; }}
nav {{ padding:20px 0; display:flex; align-items:center; justify-content:space-between; max-width:800px; margin:0 auto; padding:20px 24px; }}
nav a {{ color:var(--primary); text-decoration:none; font-weight:600; }}
.hero {{ padding:80px 0 60px; text-align:center; }}
.hero h1 {{ font-size:clamp(28px,5vw,42px); font-weight:800; line-height:1.2; margin-bottom:16px; }}
.hero h1 span {{ color:var(--primary); }}
.hero p {{ color:var(--dim); font-size:17px; line-height:1.6; max-width:600px; margin:0 auto 32px; }}
.cta {{ display:inline-block; background:var(--primary); color:#fff; padding:14px 32px; border-radius:12px; text-decoration:none; font-weight:700; font-size:16px; }}
.cta:hover {{ opacity:.9; }}
.pain {{ background:var(--card); border:1px solid var(--border); border-radius:16px; padding:32px; margin:40px 0; text-align:center; font-size:18px; color:var(--dim); line-height:1.6; }}
.features {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:16px; margin:40px 0; }}
.feat {{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:20px; }}
.feat .icon {{ font-size:28px; margin-bottom:8px; }}
.feat h3 {{ font-size:16px; font-weight:700; margin-bottom:6px; }}
.feat p {{ font-size:14px; color:var(--dim); line-height:1.5; }}
.example {{ background:linear-gradient(135deg,rgba(99,102,241,0.1),rgba(139,92,246,0.1)); border:1px solid rgba(99,102,241,0.3); border-radius:12px; padding:24px; margin:40px 0; }}
.example h3 {{ font-size:14px; color:var(--primary); text-transform:uppercase; letter-spacing:1px; margin-bottom:12px; }}
.example p {{ font-size:15px; color:var(--dim); line-height:1.6; font-style:italic; }}
.final {{ text-align:center; padding:60px 0; }}
.final h2 {{ font-size:28px; font-weight:800; margin-bottom:12px; }}
.final p {{ color:var(--dim); margin-bottom:24px; }}
footer {{ text-align:center; padding:40px 0; color:var(--dim); font-size:13px; border-top:1px solid var(--border); }}
footer a {{ color:var(--primary); text-decoration:none; }}
</style>
</head>
<body>
<nav>
  <a href="/">← diqto.fr</a>
  <a href="{diagnostic_href}">Diagnostic Diqto</a>
</nav>
<section class="hero">
  <div class="container">
    <h1>{emoji} Diqto pour les <span>{label}</span></h1>
    <p>{desc}</p>
    <a href="{diagnostic_href}" class="cta">Lancer mon diagnostic Diqto →</a>
  </div>
</section>
<div class="container">
  <div class="pain">{pain}</div>
  <div class="features">
{features_html}
  </div>
  <div class="example">
    <h3>🎤 Exemple de dictée</h3>
    <p>"{example}"</p>
  </div>
</div>
<section class="final">
  <div class="container">
    <h2>Prêt à gagner du temps ?</h2>
    <p>Diagnostic court avant tout paiement : métier, documents, clients, contraintes légales.</p>
    <a href="{diagnostic_href}" class="cta">Demander mon diagnostic Diqto →</a>
  </div>
</section>
<footer>
  <div class="container">
    <p>© 2026 Diqto · <a href="/">diqto.fr</a> · <a href="mailto:support@diqto.fr">support@diqto.fr</a></p>
    <p style="margin-top:8px;">Marque déposée INPI N° 5234942</p>
  </div>
</footer>
</body>
</html>'''

for m in METIERS:
    features_html = ""
    for icon, feature_title, feature_desc in m["features"]:
        features_html += f'    <div class="feat"><div class="icon">{icon}</div><h3>{feature_title}</h3><p>{feature_desc}</p></div>\n'

    canonical_url = f"https://diqto.fr/{m['id']}.html"
    og_image = "https://diqto.fr/og-image.png"
    schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": f"Diqto pour {m['label']}",
        "url": canonical_url,
        "description": m["desc"],
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "iOS",
        "image": og_image,
        "inLanguage": "fr-FR",
        "publisher": {
            "@type": "Organization",
            "name": "Diqto",
            "url": "https://diqto.fr/",
        },
        "offers": {
            "@type": "Offer",
            "description": "Diagnostic avant offre commerciale",
            "priceCurrency": "EUR",
            "availability": "https://schema.org/PreOrder",
        },
    }
    
    html = TEMPLATE.format(
        emoji=escape(m["emoji"]),
        label=escape(m["label"]),
        title_doc=escape(m["title_doc"]),
        title_attr=escape(f"{m['emoji']} Diqto pour les {m['label']} — {m['title_doc']}", quote=True),
        desc=escape(m["desc"]),
        desc_attr=escape(m["desc"], quote=True),
        keywords_attr=escape(m["keywords"], quote=True),
        keywords=m["keywords"],
        id=m["id"],
        canonical_url=canonical_url,
        og_title_attr=escape(f"{m['emoji']} Diqto pour les {m['label']}", quote=True),
        og_image=og_image,
        schema_json=json.dumps(schema, ensure_ascii=False, indent=2),
        pain=escape(m["pain"]),
        features_html=features_html,
        example=escape(m["example"]),
        diagnostic_href=f"/?source=seo_top_{m['id']}&metier={quote(m['label'], safe='')}#beta",
    )
    
    with open(f'{m["id"]}.html', 'w') as f:
        f.write(html)
    print(f'✅ {m["id"]}.html')

print(f'\n✅ {len(METIERS)} pages régénérées')
