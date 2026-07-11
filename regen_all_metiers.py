#!/usr/bin/env python3
"""Regenerate ALL metier pages (metiers/ folder) — no WhatsApp, app-first."""

import json, os, glob
from html import escape
from pathlib import Path
from urllib.parse import quote

CONFIG_DIR = Path(__file__).parent / ".." / "batiboss" / "config" / "metiers"
OUTPUT_DIR = Path(__file__).parent / "metiers"

TOP_LEVEL_CANONICALS = {
    "carreleur": "carreleur.html",
    "coach_sportif": "coach-sportif.html",
    "electricien": "electricien.html",
    "kinesitherapeute": "kinesitherapeute.html",
    "menuisier": "menuisier.html",
    "osteopathe": "osteopathe.html",
    "peintre": "peintre.html",
    "photographe": "photographe.html",
    "plombier": "plombier.html",
}

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
        ("📄", "Brouillons PDF à relire", "Devis et factures prêts à relire avec mentions, numérotation et conditions."),
        ("💳", "Paiement cadré", "On vérifie le mode de règlement adapté avant d'activer un lien ou un process de paiement."),
        ("🔄", "Relances pilotées", "Diqto prépare les prochaines relances et garde le contexte client, sans envoi aveugle."),
        ("🧠", "Catalogue appris", "Vos prestations habituelles en 1 tap après quelques utilisations."),
        ("🏛️", "URSSAF", "Alertes cotisations, seuils TVA, livre des recettes."),
    ],
    "honoraires": [
        ("🎤", "Dictée notes de séance", "Dictez après chaque consultation. L'IA structure : motif, observations, plan de suivi."),
        ("🩺", "Fiche conseil patient IA", "Exercices et prévention personnalisés prêts à partager après validation humaine."),
        ("📋", "Briefing pré-séance", "Résumé IA avant chaque patient : historique, progression, points d'attention."),
        ("📄", "Notes d'honoraires", "Prêtes à relire avec TVA adaptée, mentions légales et numérotation."),
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

ICON_LABELS = {
    "🎤": "VOIX",
    "📄": "PDF",
    "💳": "PAY",
    "🔄": "REL",
    "🧠": "CAT",
    "🏛️": "TAX",
    "🩺": "SOIN",
    "📋": "PREP",
    "📈": "SUIVI",
    "🎓": "ELEVE",
    "💰": "FACT",
    "📊": "BIZ",
}


def icon_label(icon):
    return ICON_LABELS.get(icon, "DIQ")


def display_plural(label):
    clean = label.strip()
    lower = clean.lower()
    if lower in {"nettoyage"}:
        return "entreprises de nettoyage"
    if lower.endswith(("s", "x")):
        return clean
    return f"{clean}s"

TEMPLATE = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#0c0c0c">
<title>{title_attr}</title>
<link rel="icon" href="../favicon.png">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
<link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../site-shell.css">
<script defer src="../site-shell.js"></script>
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
:root {{ --bg:#0c0c0c; --primary:#25d366; --text:#f5f5f2; --dim:#a3aaa3; --card:#171b17; --border:rgba(255,255,255,.11); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html {{ scroll-behavior:smooth; }}
body {{ font-family:'Work Sans',sans-serif; background:var(--bg); color:var(--text); line-height:1.55; -webkit-font-smoothing:antialiased; }}
.container {{ max-width:800px; margin:0 auto; padding:0 24px; }}
.canonical-note {{ max-width:800px; margin:0 auto; padding:20px 24px 0; color:var(--dim); font-size:13px; text-align:center; }}
.canonical-note a {{ color:var(--primary); text-decoration:none; font-weight:700; }}
.hero {{ padding:88px 0 48px; text-align:center; background:radial-gradient(circle at 78% 28%,rgba(37,211,102,.14),transparent 30%); }}
.hero h1 {{ font-size:clamp(38px,7vw,66px); font-weight:800; line-height:1.02; letter-spacing:-.05em; margin-bottom:20px; }}
.hero h1 span {{ color:var(--primary); }}
.hero p {{ color:var(--dim); font-size:clamp(17px,2.4vw,21px); line-height:1.6; max-width:650px; margin:0 auto 32px; }}
.cta {{ display:inline-flex; align-items:center; justify-content:center; min-height:52px; background:var(--primary); color:#0c0c0c; padding:14px 24px; border-radius:999px; text-decoration:none; font-weight:700; }}
.features {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:14px; margin:52px 0; }}
.feat {{ background:var(--card); border:1px solid var(--border); border-radius:18px; padding:20px; }}
.feat .icon {{ display:inline-flex;align-items:center;justify-content:center;min-width:42px;height:24px;padding:0 8px;border-radius:999px;background:rgba(37,211,102,.12);color:var(--primary);font-size:11px;font-weight:800;letter-spacing:.8px;margin-bottom:10px; }}
.feat h3 {{ font-size:16px; font-weight:700; margin-bottom:6px; }}
.feat p {{ font-size:14px; color:var(--dim); line-height:1.55; }}
.final {{ text-align:center; padding:72px 0; border-top:1px solid var(--border); background:#121712; }}
.final h2 {{ font-size:clamp(28px,5vw,46px); font-weight:800; letter-spacing:-.04em; margin-bottom:12px; }}
.final p {{ color:var(--dim); margin-bottom:24px; font-size:15px; }}
footer {{ text-align:center; padding:32px 0; color:var(--dim); font-size:12px; border-top:1px solid var(--border); }}
footer p {{ display:flex; flex-wrap:wrap; justify-content:center; gap:14px; }}
footer a {{ color:var(--dim); text-decoration:none; }}
footer a:hover {{ color:var(--primary); }}
@media (max-width:600px) {{ .hero {{ padding:58px 0 38px; }} .features {{ grid-template-columns:1fr; }} .cta {{ width:100%; }} }}
</style>
</head>
<body>
<a class="global-skip-link" href="#contenu">Aller au contenu</a>
<header class="global-header" data-menu-open="false">
  <div class="global-nav">
    <a class="global-brand" href="/" aria-label="Diqto, accueil"><span class="global-brand-mark" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span><span class="global-brand-name">diq<em>to</em></span></a>
    <button class="global-menu-toggle" type="button" aria-expanded="false" aria-controls="navigation-principale">Menu</button>
    <nav class="global-menu" id="navigation-principale" aria-label="Navigation principale"><a href="/">Accueil</a><a href="/fonctionnalites.html">Fonctionnalités</a><a href="/docs.html">Bien démarrer</a><a href="/#tarifs">Tarifs</a><a class="global-cta" href="{diagnostic_href}">Commencer gratuit</a></nav>
  </div>
</header>
<main id="contenu">
{canonical_note}
<section class="hero"><div class="container">
  <h1>Diqto pour les <span>{label}</span></h1>
  <p>{desc}</p>
  <a href="{diagnostic_href}" class="cta">Créer mon premier brouillon gratuit →</a>
</div></section>
<div class="container"><div class="features">
{features_html}
</div></div>
<section class="final"><div class="container">
  <h2>Prêt à simplifier votre administratif ?</h2>
  <p>Essai gratuit avant tout paiement : choisissez votre métier, créez un brouillon, relisez avant partage.</p>
  <a href="{diagnostic_href}" class="cta">Commencer gratuit →</a>
</div></section>
</main>
<footer><div class="container">
  <p><span>© 2026 Diqto</span><a href="/">Accueil</a><a href="/fonctionnalites.html">Fonctionnalités</a><a href="/docs.html">Bien démarrer</a><a href="/cgu.html">CGU</a><a href="/confidentialite.html">Confidentialité</a><a href="mailto:support@diqto.fr">Support</a></p>
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
    display_label = display_plural(label)
    emoji = cfg.get("emoji", "💼")
    profile = cfg.get("profile", "devis")
    category = cfg.get("category", "autre")
    
    features = PROFILE_FEATURES.get(profile, PROFILE_FEATURES["devis"])
    
    doc_types = {"devis": "Devis et factures", "honoraires": "Notes d'honoraires et suivi", "abonnement": "Abonnements et facturation"}
    doc_type = doc_types.get(profile, "Devis & factures")
    
    title = f"Diqto pour les {display_label} — {doc_type} IA"
    seo_desc = (
        f"Diqto pour les {display_label.lower()} : {doc_type.lower()} depuis l'iPhone. "
        "Dictez, relisez, puis partagez sous contrôle humain."
    )
    desc = seo_desc
    canonical_path = TOP_LEVEL_CANONICALS.get(trade_id, f"metiers/{trade_id}.html")
    canonical_url = f"https://diqto.fr/{canonical_path}"
    canonical_note = ""
    if trade_id in TOP_LEVEL_CANONICALS:
        canonical_note = (
            f'<p class="canonical-note">Page principale : '
            f'<a href="/{canonical_path}">Diqto pour les {escape(display_label)}</a></p>'
        )
    og_image = "https://diqto.fr/og-image.png"
    schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": f"Diqto pour {display_label}",
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
            "description": "Essai gratuit avant offre payante",
            "priceCurrency": "EUR",
            "availability": "https://schema.org/PreOrder",
        },
    }
    
    keywords = f"devis {label.lower()}, facture {label.lower()}, application {label.lower()}, {label.lower()} IA"
    
    features_html = ""
    for icon, feature_title, fdesc in features:
        features_html += f'    <div class="feat"><div class="icon">{icon_label(icon)}</div><h3>{feature_title}</h3><p>{fdesc}</p></div>\n'
    diagnostic_href = f"../?source=seo_metier_{trade_id}&metier={quote(label, safe='')}#beta"
    
    html = TEMPLATE.format(
        emoji=escape(emoji), label=escape(display_label), label_lower=escape(display_label.lower()),
        doc_type=doc_type, doc_type_lower=doc_type.lower(),
        trade_id=trade_id, desc=escape(desc), keywords=keywords,
        title_attr=escape(title, quote=True),
        seo_desc_attr=escape(seo_desc, quote=True),
        keywords_attr=escape(keywords, quote=True),
        canonical_url=canonical_url,
        og_title_attr=escape(f"Diqto pour les {display_label}", quote=True),
        og_image=og_image,
        schema_json=json.dumps(schema, ensure_ascii=False, indent=2),
        features_html=features_html, diagnostic_href=diagnostic_href,
        canonical_note=canonical_note,
    )
    
    out_path = OUTPUT_DIR / f"{trade_id}.html"
    with open(out_path, 'w') as f:
        f.write(html)
    count += 1

print(f"OK {count} pages métier régénérées dans metiers/")
