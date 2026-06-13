#!/usr/bin/env python3
"""Regenerate ALL metier pages (metiers/ folder) — no WhatsApp, app-first."""

import json, os, glob
from html import escape
from pathlib import Path
from urllib.parse import quote

CONFIG_DIR = Path(__file__).parent / ".." / "batiboss" / "config" / "metiers"
OUTPUT_DIR = Path(__file__).parent / "metiers"

CATEGORY_LABELS = {
    "batiment": "Bâtiment & Travaux",
    "sante": "Santé & Bien-être", 
    "enseignement": "Enseignement & Coaching",
    "juridique_finance": "Conseil & Expertise",
    "services": "Services & Créatifs",
    "beaute": "Beauté & Bien-être",
    "automobile": "Automobile",
    "evenementiel": "Événementiel",
    "restauration": "Restauration",
    "autre": "Autres métiers",
}

PROFILE_FEATURES = {
    "devis": [
        ("🎤", "Dictez votre devis", "Dictez en langage naturel, l'IA structure tout : prestations, quantités, prix, TVA."),
        ("📄", "PDF conformes", "Devis et factures prêts à relire avec mentions, numérotation et conditions."),
        ("💳", "Paiement cadré", "On vérifie le mode de règlement adapté avant d'activer un lien ou un process de paiement."),
        ("🔄", "Relances pilotées", "Diqto prépare les prochaines relances et garde le contexte client, sans envoi aveugle."),
        ("🧠", "Catalogue appris", "Vos prestations habituelles en 1 tap après quelques utilisations."),
        ("🏛️", "URSSAF", "Alertes cotisations, seuils TVA, livre des recettes."),
    ],
    "honoraires": [
        ("🎤", "Dictée notes de séance", "Dictez après chaque consultation. L'IA structure : motif, observations, plan de suivi."),
        ("🩺", "Fiche conseil patient IA", "Exercices et prévention personnalisés envoyés au patient par email."),
        ("📋", "Briefing pré-séance", "Résumé IA avant chaque patient : historique, progression, points d'attention."),
        ("📄", "Notes d'honoraires", "Conformes, TVA adaptée, mentions légales. En 3 secondes."),
        ("💳", "Paiement cadré", "On qualifie le mode de règlement adapté avant d'activer un lien de paiement."),
        ("📈", "Suivi longitudinal", "Progression patient séance après séance."),
    ],
    "abonnement": [
        ("🎓", "Gestion élèves", "Formules, inscriptions, suivi. Tout en un endroit."),
        ("💰", "Facturation batch", "Facturez tous vos élèves en 1 tap à la fin du mois."),
        ("🔄", "Relances pilotées", "Diqto prépare les relances avec contexte, sans envoi aveugle."),
        ("📊", "Coach IA Business", "Suggestions pricing, rétention, saisonnalité."),
        ("💳", "Paiement cadré", "On qualifie le mode de règlement adapté avant activation."),
        ("🏛️", "URSSAF", "Alertes et estimations cotisations."),
    ],
}

TEMPLATE = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_attr}</title>
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
<link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<meta name="description" content="{seo_desc_attr}">
<meta name="keywords" content="{keywords_attr}">
<link rel="canonical" href="{canonical_url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical_url}">
<meta property="og:title" content="{og_title_attr}">
<meta property="og:description" content="{seo_desc_attr}">
<meta property="og:image" content="{og_image}">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Diqto">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title_attr}">
<meta name="twitter:description" content="{seo_desc_attr}">
<meta name="twitter:image" content="{og_image}">
<script type="application/ld+json">
{schema_json}
</script>
<style>
:root {{ --bg:#0C0C0C; --primary:#6366F1; --green:#22C55E; --text:#fff; --dim:#9CA3AF; --card:#1A1A2E; --border:#2A2A3E; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'Work Sans',sans-serif; background:var(--bg); color:var(--text); }}
.container {{ max-width:800px; margin:0 auto; padding:0 24px; }}
nav {{ padding:20px 24px; max-width:800px; margin:0 auto; display:flex; justify-content:space-between; align-items:center; }}
nav a {{ color:var(--primary); text-decoration:none; font-weight:600; font-size:14px; }}
.hero {{ padding:80px 0 40px; text-align:center; }}
.hero h1 {{ font-size:clamp(26px,5vw,38px); font-weight:800; line-height:1.2; margin-bottom:16px; }}
.hero h1 span {{ color:var(--primary); }}
.hero p {{ color:var(--dim); font-size:16px; line-height:1.6; max-width:560px; margin:0 auto 32px; }}
.cta {{ display:inline-block; background:var(--primary); color:#fff; padding:14px 32px; border-radius:12px; text-decoration:none; font-weight:700; }}
.features {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px; margin:40px 0; }}
.feat {{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:16px; }}
.feat .icon {{ font-size:24px; margin-bottom:6px; }}
.feat h3 {{ font-size:15px; font-weight:700; margin-bottom:4px; }}
.feat p {{ font-size:13px; color:var(--dim); line-height:1.5; }}
.final {{ text-align:center; padding:60px 0; }}
.final h2 {{ font-size:24px; font-weight:800; margin-bottom:12px; }}
.final p {{ color:var(--dim); margin-bottom:24px; font-size:15px; }}
footer {{ text-align:center; padding:32px 0; color:var(--dim); font-size:12px; border-top:1px solid var(--border); }}
footer a {{ color:var(--primary); text-decoration:none; }}
</style>
</head>
<body>
<nav><a href="/">← diqto.fr</a><a href="{diagnostic_href}">Diagnostic Diqto</a></nav>
<section class="hero"><div class="container">
  <h1>{emoji} Diqto pour les <span>{label}</span></h1>
  <p>{desc}</p>
  <a href="{diagnostic_href}" class="cta">Lancer mon diagnostic Diqto →</a>
</div></section>
<div class="container">
  <div class="features">
{features_html}
  </div>
</div>
<section class="final"><div class="container">
  <h2>Prêt à simplifier votre administratif ?</h2>
  <p>Diagnostic court avant tout paiement : métier, documents, clients, contraintes légales.</p>
  <a href="{diagnostic_href}" class="cta">Demander mon diagnostic Diqto →</a>
</div></section>
<footer><div class="container">
  <p>© 2026 Diqto · <a href="/">diqto.fr</a> · <a href="mailto:support@diqto.fr">support@diqto.fr</a></p>
</div></footer>
</body>
</html>'''

count = 0
for config_file in sorted(glob.glob(str(CONFIG_DIR / "*.json"))):
    try:
        with open(config_file) as f:
            cfg = json.load(f)
    except:
        continue
    
    trade_id = Path(config_file).stem
    if trade_id.startswith("_"):
        continue

    label = cfg.get("label", trade_id.replace("_", " ").title())
    emoji = cfg.get("emoji", "💼")
    profile = cfg.get("profile", "devis")
    category = cfg.get("category", "autre")
    
    features = PROFILE_FEATURES.get(profile, PROFILE_FEATURES["devis"])
    
    doc_types = {"devis": "Devis & factures", "honoraires": "Notes d'honoraires & suivi", "abonnement": "Abonnements & facturation"}
    doc_type = doc_types.get(profile, "Devis & factures")
    
    title = f"{emoji} Diqto pour les {label} — {doc_type} IA"
    seo_desc = (
        f"Diqto pour les {label.lower()} : {doc_type.lower()} depuis l'iPhone. "
        "Dictez, relisez, puis partagez sous contrôle humain."
    )
    desc = seo_desc
    canonical_url = f"https://diqto.fr/metiers/{trade_id}.html"
    og_image = "https://diqto.fr/og-image.png"
    schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": f"Diqto pour {label}",
        "url": canonical_url,
        "description": seo_desc,
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
    
    keywords = f"devis {label.lower()}, facture {label.lower()}, application {label.lower()}, {label.lower()} IA"
    
    features_html = ""
    for icon, feature_title, fdesc in features:
        features_html += f'    <div class="feat"><div class="icon">{icon}</div><h3>{feature_title}</h3><p>{fdesc}</p></div>\n'
    diagnostic_href = f"../?source=seo_metier_{trade_id}&metier={quote(label, safe='')}#beta"
    
    html = TEMPLATE.format(
        emoji=escape(emoji), label=escape(label), label_lower=escape(label.lower()),
        doc_type=doc_type, doc_type_lower=doc_type.lower(),
        trade_id=trade_id, desc=escape(desc), keywords=keywords,
        title_attr=escape(title, quote=True),
        seo_desc_attr=escape(seo_desc, quote=True),
        keywords_attr=escape(keywords, quote=True),
        canonical_url=canonical_url,
        og_title_attr=escape(f"{emoji} Diqto pour les {label}", quote=True),
        og_image=og_image,
        schema_json=json.dumps(schema, ensure_ascii=False, indent=2),
        features_html=features_html, diagnostic_href=diagnostic_href,
    )
    
    out_path = OUTPUT_DIR / f"{trade_id}.html"
    with open(out_path, 'w') as f:
        f.write(html)
    count += 1

print(f"✅ {count} pages métier régénérées dans metiers/")
