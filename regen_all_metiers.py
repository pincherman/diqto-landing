#!/usr/bin/env python3
"""Regenerate ALL metier pages (metiers/ folder) — no WhatsApp, app-first."""

import json, os, glob
from pathlib import Path

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
        ("📄", "PDF conformes", "Devis et factures professionnels avec mentions légales automatiques."),
        ("💳", "Paiement CB", "Vos clients paient par carte directement depuis la facture."),
        ("🔄", "Relances auto", "J+7, J+15, J+30. Vos impayés se règlent automatiquement."),
        ("🧠", "Catalogue appris", "Vos prestations habituelles en 1 tap après quelques utilisations."),
        ("🏛️", "URSSAF", "Alertes cotisations, seuils TVA, livre des recettes."),
    ],
    "honoraires": [
        ("🎤", "Dictée notes de séance", "Dictez après chaque consultation. L'IA structure : motif, observations, plan de suivi."),
        ("🩺", "Fiche conseil patient IA", "Exercices et prévention personnalisés envoyés au patient par email."),
        ("📋", "Briefing pré-séance", "Résumé IA avant chaque patient : historique, progression, points d'attention."),
        ("📄", "Notes d'honoraires", "Conformes, TVA adaptée, mentions légales. En 3 secondes."),
        ("💳", "Paiement CB", "Vos patients paient par carte depuis leur téléphone."),
        ("📈", "Suivi longitudinal", "Progression patient séance après séance."),
    ],
    "abonnement": [
        ("🎓", "Gestion élèves", "Formules, inscriptions, suivi. Tout en un endroit."),
        ("💰", "Facturation batch", "Facturez tous vos élèves en 1 tap à la fin du mois."),
        ("🔄", "Relances auto", "Les retards de paiement se gèrent tout seuls."),
        ("📊", "Coach IA Business", "Suggestions pricing, rétention, saisonnalité."),
        ("💳", "Paiement CB", "Vos élèves paient par carte."),
        ("🏛️", "URSSAF", "Alertes et estimations cotisations."),
    ],
}

TEMPLATE = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{emoji} Diqto pour les {label} — {doc_type} IA</title>
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
<link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<meta name="description" content="Diqto pour les {label_lower} : {doc_type_lower} par la voix et l'IA. Dictez, l'IA comprend votre métier. Disponible sur iOS.">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="https://diqto.fr/metiers/{trade_id}.html">
<meta property="og:title" content="{emoji} Diqto pour les {label}">
<meta property="og:description" content="Diqto pour les {label_lower} : {doc_type_lower} par la voix et l'IA.">
<meta property="og:url" content="https://diqto.fr/metiers/{trade_id}.html">
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
<nav><a href="/">← diqto.fr</a><a href="mailto:support@diqto.fr?subject=Accès%20beta%20Diqto%20{label}">Demander l'accès</a></nav>
<section class="hero"><div class="container">
  <h1>{emoji} Diqto pour les <span>{label}</span></h1>
  <p>{desc}</p>
  <a href="mailto:support@diqto.fr?subject=Accès%20beta%20Diqto%20{label}" class="cta">Demander l'accès beta →</a>
</div></section>
<div class="container">
  <div class="features">
{features_html}
  </div>
</div>
<section class="final"><div class="container">
  <h2>Prêt à simplifier votre administratif ?</h2>
  <p>Disponible sur iOS. Gratuit pour commencer.</p>
  <a href="mailto:support@diqto.fr?subject=Accès%20beta%20Diqto%20{label}" class="cta">Demander l'accès beta →</a>
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
    label = cfg.get("label", trade_id.replace("_", " ").title())
    emoji = cfg.get("emoji", "💼")
    profile = cfg.get("profile", "devis")
    category = cfg.get("category", "autre")
    
    features = PROFILE_FEATURES.get(profile, PROFILE_FEATURES["devis"])
    
    doc_types = {"devis": "Devis & factures", "honoraires": "Notes d'honoraires & suivi", "abonnement": "Abonnements & facturation"}
    doc_type = doc_types.get(profile, "Devis & factures")
    
    desc = f"Diqto pour les {label.lower()} : {doc_type.lower()} par la voix et l'IA. Dictez, l'IA comprend votre métier et génère vos documents en quelques secondes."
    
    keywords = f"devis {label.lower()}, facture {label.lower()}, application {label.lower()}, {label.lower()} IA"
    
    features_html = ""
    for icon, title, fdesc in features:
        features_html += f'    <div class="feat"><div class="icon">{icon}</div><h3>{title}</h3><p>{fdesc}</p></div>\n'
    
    html = TEMPLATE.format(
        emoji=emoji, label=label, label_lower=label.lower(),
        doc_type=doc_type, doc_type_lower=doc_type.lower(),
        trade_id=trade_id, desc=desc, keywords=keywords,
        features_html=features_html,
    )
    
    out_path = OUTPUT_DIR / f"{trade_id}.html"
    with open(out_path, 'w') as f:
        f.write(html)
    count += 1

print(f"✅ {count} pages métier régénérées dans metiers/")
