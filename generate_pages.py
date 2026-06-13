#!/usr/bin/env python3
"""
Génère les pages métier SEO statiques pour diqto.fr/metiers/
Lit les configs depuis ../batiboss/config/metiers/*.json
Écrit dans metiers/{trade_id}.html
"""

import json
import os
import glob
from pathlib import Path
from urllib.parse import quote

SCRIPT_DIR = Path(__file__).parent
METIERS_CONFIG_DIR = SCRIPT_DIR / ".." / "batiboss" / "config" / "metiers"
OUTPUT_DIR = SCRIPT_DIR / "metiers"

# ── Category metadata ──────────────────────────────────────────────
CATEGORIES = {
    "batiment": {"label": "Bâtiment & Travaux", "order": 1},
    "sante": {"label": "Santé & Bien-être", "order": 2},
    "enseignement": {"label": "Enseignement & Coaching", "order": 3},
    "juridique_finance": {"label": "Juridique & Finance", "order": 4},
    "services": {"label": "Services & Créatifs", "order": 5},
    "beaute": {"label": "Beauté", "order": 5},
    "automobile": {"label": "Automobile", "order": 5},
    "evenementiel": {"label": "Événementiel", "order": 5},
    "restauration": {"label": "Restauration", "order": 5},
    "autre": {"label": "Autres métiers", "order": 6},
}

# ── Profile-specific content ───────────────────────────────────────
PROFILE_DATA = {
    "devis": {
        "doc_word": "devis",
        "doc_word_plural": "devis",
        "pain_point": "Vous faites vos devis sur papier entre deux chantiers ? Vous perdez du temps à recopier les mêmes lignes ?",
        "step1": "Dictez votre devis par message vocal ou texte",
        "step3": "Preparez le partage client, la signature et le paiement sous controle humain",
    },
    "abonnement": {
        "doc_word": "factures",
        "doc_word_plural": "factures et cotisations",
        "pain_point": "Vous courez après les cotisations de vos élèves ? Vous passez des heures à faire vos factures manuellement ?",
        "step1": "Ajoutez vos élèves et leurs forfaits",
        "step3": "Facturez tout le monde en 1 clic à la fin du mois",
    },
    "honoraires": {
        "doc_word": "notes d'honoraires",
        "doc_word_plural": "notes d'honoraires",
        "pain_point": "Vos notes d'honoraires vous prennent plus de temps que vos consultations ? La paperasse administrative vous freine ?",
        "step1": "Dictez votre consultation par message vocal",
        "step3": "Vous verifiez la note, puis le partage et le paiement restent sous controle humain",
    },
}

# ── Smart accroche per category/profile ────────────────────────────
def get_accroche(metier_data):
    """Generate a specific SEO accroche for the métier."""
    name = metier_data.get("name", metier_data.get("label", ""))
    profile = metier_data.get("profile", "devis")
    category = metier_data.get("category", "autre")
    
    # Specific overrides for key métiers
    accroches = {
        "plombier": "Devis plomberie prêt à relire depuis votre téléphone",
        "electricien": "Devis électricité entre deux chantiers, sans paperasse",
        "peintre": "Devis peinture et ravalement prêt à relire",
        "macon": "Devis maçonnerie dicté depuis le chantier",
        "carreleur": "Devis carrelage et pose prêt à relire",
        "menuisier": "Devis menuiserie sur mesure depuis votre atelier",
        "couvreur": "Devis toiture prêt à relire depuis votre camionnette",
        "chauffagiste": "Devis chauffage et climatisation sans paperasse",
        "serrurier": "Devis serrurerie prêt à valider depuis votre téléphone",
        "paysagiste": "Devis entretien et aménagement paysager prêt à relire",
        "photographe": "Devis shooting photo professionnel depuis votre iPhone",
        "animateur": "Devis animation et DJ depuis votre iPhone",
        "coach_sportif": "Gérez vos clients et séances de coaching sans paperasse",
        "prof_karate": "Gérez vos élèves et cotisations sans paperasse",
        "prof_yoga": "Gérez vos élèves et abonnements yoga sans paperasse",
        "prof_danse": "Gérez vos élèves et inscriptions danse sans paperasse",
        "prof_musique": "Gérez vos élèves et cours de musique sans paperasse",
        "prof_langue": "Gérez vos élèves et facturation de cours sans paperasse",
        "prof_natation": "Gérez vos élèves et séances de natation sans paperasse",
        "moniteur_ski": "Préparez vos factures de cours de ski sans paperasse",
        "auto_ecole": "Gérez vos élèves et heures de conduite sans paperasse",
        "formateur": "Devis et factures formation professionnelle depuis votre iPhone",
        "osteopathe": "Notes d'honoraires ostéopathie depuis votre iPhone",
        "kine": "Notes d'honoraires kiné depuis votre iPhone",
        "kinesitherapeute": "Notes d'honoraires kinésithérapie depuis votre iPhone",
        "infirmier": "Facturation soins infirmiers depuis votre iPhone",
        "podologue": "Notes d'honoraires podologie depuis votre iPhone",
        "orthophoniste": "Notes d'honoraires orthophonie depuis votre iPhone",
        "psychologue": "Notes d'honoraires psychologue depuis votre iPhone",
        "sage_femme": "Facturation sage-femme depuis votre iPhone",
        "dieteticien": "Notes d'honoraires diététique depuis votre iPhone",
        "masseur": "Facturation massages et soins depuis votre iPhone",
        "sophrologue": "Notes d'honoraires sophrologie depuis votre iPhone",
        "veterinaire": "Facturation vétérinaire depuis votre iPhone",
        "avocat": "Notes d'honoraires et conventions depuis votre iPhone",
        "expert_comptable": "Lettres de mission et facturation depuis votre iPhone",
        "consultant": "Devis et factures consulting depuis votre iPhone",
        "architecte": "Devis et honoraires architecture depuis votre iPhone",
        "architecte_interieur": "Devis décoration et aménagement depuis votre iPhone",
        "coiffeur": "Devis et factures coiffure depuis votre iPhone",
        "estheticienne": "Devis et factures esthétique depuis votre iPhone",
        "tatoueur": "Devis tatouage depuis votre iPhone",
        "fleuriste": "Devis compositions florales depuis votre iPhone",
        "traiteur": "Devis traiteur et événementiel depuis votre iPhone",
        "nettoyage": "Devis nettoyage et entretien depuis votre iPhone",
        "garagiste": "Devis réparation auto depuis votre iPhone",
        "graphiste": "Devis graphisme et design depuis votre iPhone",
        "climatisation": "Devis climatisation et entretien depuis votre iPhone",
        "domotique": "Devis domotique et installation depuis votre iPhone",
        "ramoneur": "Devis ramonage depuis votre iPhone",
        "diagnostiqueur": "Devis diagnostics immobiliers depuis votre iPhone",
        "pisciniste": "Devis piscine et entretien depuis votre iPhone",
        "facade": "Devis ravalement de façade depuis votre iPhone",
        "platrier": "Devis plâtrerie et isolation depuis votre iPhone",
        "charpentier": "Devis charpente et ossature bois depuis votre iPhone",
        "terrassier": "Devis terrassement et VRD depuis votre iPhone",
    }
    
    metier_id = metier_data.get("metier", "")
    if metier_id in accroches:
        return accroches[metier_id]
    
    # Fallback by profile
    if profile == "abonnement":
        return f"Gérez vos élèves et factures de {name.lower()} sans paperasse"
    elif profile == "honoraires":
        return f"Notes d'honoraires {name.lower()} depuis votre iPhone"
    else:
        return f"Devis {name.lower()} prêt à relire depuis votre téléphone"


def get_features_html(metier_data):
    """Generate feature list HTML based on métier features."""
    features = metier_data.get("features", {})
    profile = metier_data.get("profile", "devis")
    items = []
    
    feature_labels = {
        "photo_devis": ("PHOTO", "Photo → brouillon IA", "Prenez en photo le chantier, Diqto propose un brouillon de devis a valider"),
        "signature": ("SIGN", "Signature électronique", "Votre client signe sur son téléphone"),
        "payment_link": ("PAY", "Paiement cadré", "Le mode de règlement est qualifié avant toute activation de lien ou process de paiement"),
        "import_devis": ("IMP", "Import devis", "Importez vos devis existants et transformez-les en factures"),
        "import_contacts": ("CRM", "Import contacts", "Importez vos clients en photo ou fichier"),
        "export_comptable": ("CSV", "Export comptable", "Export CSV + PDF pour votre comptable en 1 clic"),
        "eleves": ("ELEVE", "Gestion des élèves", "Ajoutez, suivez et facturez vos élèves facilement"),
        "batch_facture": ("BATCH", "Facturation batch", "Facturez tous vos élèves en 1 clic"),
        "catalogue": ("CAT", "Catalogue de prestations", "Vos prestations habituelles mémorisées et réutilisables"),
        "relances": ("REL", "Relances préparées", "Rappels préparés avec contexte, sans envoi automatique"),
        "saison": ("SAISON", "Gestion de saison", "Nouvelle saison, nouveaux tarifs en quelques secondes"),
        "convention_honoraires": ("CONV", "Convention d'honoraires", "Générez vos conventions professionnelles"),
        "note_debours": ("FRAIS", "Notes de débours", "Suivez et refacturez vos frais avancés"),
        "facturation_recurrente": ("RECUR", "Facturation récurrente cadrée", "Abonnements et forfaits préparés avant validation humaine"),
        "briefing": ("BRIEF", "Briefing chantier", "Résumé du projet pour votre équipe"),
        "lettre_mission": ("MISSION", "Lettre de mission", "Générez vos lettres de mission conformes"),
    }
    
    for feat_key, feat_info in feature_labels.items():
        if features.get(feat_key):
            emoji, title, desc = feat_info
            items.append(f'<div class="metier-feature"><span class="mf-icon">{emoji}</span><div><strong>{title}</strong><br><span class="mf-desc">{desc}</span></div></div>')
    
    # Always add security
    items.append('<div class="metier-feature"><span class="mf-icon">SEC</span><div><strong>Sécurité</strong><br><span class="mf-desc">Documents contrôlés, données protégées, partage sous validation humaine</span></div></div>')
    
    return "\n        ".join(items)


def get_preparation_conversation(metier_data):
    """Generate a preparation mockup from exemples_prestations."""
    prestations = metier_data.get("exemples_prestations", [])
    name = metier_data.get("name", metier_data.get("label", ""))
    profile = metier_data.get("profile", "devis")
    
    if not prestations:
        return ""
    
    presta = prestations[0]
    desc = presta.get("description", "Prestation")
    price = presta.get("unit_price", 100)
    unit = presta.get("unit", "forfait")
    
    if profile == "abonnement":
        user_msg = f'"Prépare une facture pour Marc Durand, {desc.lower()} {price}€"'
        bot_msg = f"Brouillon de facture préparé\n{desc} — {price}€\nÀ relire avant partage"
    elif profile == "honoraires":
        user_msg = f'"Prépare une note d\'honoraires pour M. Dupont, {desc.lower()} {price}€"'
        bot_msg = f"Note d'honoraires préparée\n{desc} — {price}€\nÀ relire avant partage"
    else:
        user_msg = f'"Prépare un devis pour Mme Martin, {desc.lower()} {price}€"'
        bot_msg = f"Brouillon de devis préparé\n{desc} — {price}€\nÀ relire avant partage"
    
    return f"""<div class="wa-msg wa-user">{user_msg}</div>
        <div class="wa-msg wa-bot">{bot_msg}</div>
        <div class="wa-msg wa-bot">Partage manuel · Signature · Paiement cadré</div>"""


def get_related_metiers(metier_id, all_metiers):
    """Get 3-4 related métiers from the same category."""
    current = all_metiers.get(metier_id, {})
    category = current.get("category", "autre")
    
    related = []
    for mid, mdata in all_metiers.items():
        if mid != metier_id and mdata.get("category") == category:
            related.append(mid)
    
    # If not enough in same category, add from others
    if len(related) < 3:
        for mid, mdata in all_metiers.items():
            if mid != metier_id and mid not in related:
                related.append(mid)
            if len(related) >= 4:
                break
    
    return related[:4]


def get_seo_description(metier_data):
    """Generate SEO meta description."""
    name = metier_data.get("name", "")
    profile = metier_data.get("profile", "devis")
    
    if profile == "abonnement":
        return f"Diqto pour les {name.lower()}s : préparez élèves, cotisations et factures depuis l'iPhone, avec validation humaine."
    elif profile == "honoraires":
        return f"Diqto pour les {name.lower()}s : notes d'honoraires et factures depuis l'iPhone. Dictez, relisez, puis partagez sous contrôle humain."
    else:
        return f"Diqto pour les {name.lower()}s : devis et factures depuis l'iPhone. Dictez, relisez, puis partagez sous contrôle humain."


def get_narrative_story(metier_data):
    """Generate a short narrative story for the métier, like the main landing page quotidien section."""
    name = metier_data.get("name", metier_data.get("label", ""))
    profile = metier_data.get("profile", "devis")
    
    stories = {
        "devis": {
            "scene": f"Mardi 8h. Le client appelle.",
            "dialogue1": "« Vous pouvez me faire un devis ? »",
            "context": f"Tu es en intervention. Les mains occupées.",
            "dialogue2": "« Je vous envoie ça ce soir. »",
            "consequence": "Ce soir, tu es crevé. Le devis attendra demain.",
            "punchline": "Demain, le client a signé chez un autre.",
            "resolution": f"Et si ton brouillon de devis {name.lower()} était déjà prêt à relire ?",
        },
        "abonnement": {
            "scene": "Fin du mois. Les cotisations.",
            "dialogue1": "« Faut que je fasse les factures de tous mes élèves. »",
            "context": "Tu ouvres un tableur. Tu copies-colles. Tu recommences.",
            "dialogue2": "« Plus que 23 à faire... »",
            "consequence": "2 heures plus tard, tu as facturé. Mais ta soirée est foutue.",
            "punchline": "Et le mois prochain, rebelote.",
            "resolution": "Et si un message vocal suffisait pour tout facturer ?",
        },
        "honoraires": {
            "scene": "Entre deux consultations. La paperasse.",
            "dialogue1": "« Il faut que je fasse ma note d'honoraires. »",
            "context": "Tu ouvres Word. Tu cherches le dernier modèle. Tu corriges les montants.",
            "dialogue2": "« Je ferai ça ce soir. »",
            "consequence": "Ce soir, tu as 3 autres notes en retard.",
            "punchline": "Et ton comptable qui relance.",
            "resolution": "Et si ta note était prête à relire sans repartir de zéro ?",
        },
    }
    
    s = stories.get(profile, stories["devis"])
    story_html = f"""<p>{s['scene']}</p>
    <p class="dialogue">{s['dialogue1']}</p>
    <p>&nbsp;</p>
    <p>{s['context']}</p>
    <p class="dialogue">{s['dialogue2']}</p>
    <p>&nbsp;</p>
    <p>{s['consequence']}</p>
    <p class="emphasis">{s['punchline']}</p>"""
    return story_html, s['resolution']


def generate_page(metier_id, metier_data, all_metiers):
    """Generate a full narrative HTML page for a métier."""
    name = metier_data.get("name", metier_data.get("label", metier_id))
    profile = metier_data.get("profile", "devis")
    profile_data = PROFILE_DATA.get(profile, PROFILE_DATA["devis"])
    doc_word = profile_data["doc_word"]
    accroche = get_accroche(metier_data)
    seo_desc = get_seo_description(metier_data)
    features_html = get_features_html(metier_data)
    prep_convo = get_preparation_conversation(metier_data)
    narrative_html, narrative_resolution = get_narrative_story(metier_data)
    related = get_related_metiers(metier_id, all_metiers)
    
    # Related links
    related_links = []
    for rid in related:
        rdata = all_metiers.get(rid, {})
        rname = rdata.get("name", rdata.get("label", rid))
        related_links.append(f'<a href="{rid}.html" class="metier-tag">{rname}</a>')
    related_html = "\n          ".join(related_links)
    
    # Example prestation for the example section
    prestations = metier_data.get("exemples_prestations", [])
    exemple_title = prestations[0]["description"] if prestations else "Prestation type"
    
    # Mentions légales
    mentions = metier_data.get("mentions_legales", [])
    mentions_html = ""
    if mentions:
        clean_mentions = [m for m in mentions if "{" not in m]
        if clean_mentions:
            mentions_html = '<div class="legal-mentions"><strong>Mentions légales auto-intégrées :</strong> ' + " · ".join(clean_mentions) + '</div>'
    
    # Keywords
    name_lower = name.lower()
    keywords = f"devis {name_lower}, facture {name_lower}, application {name_lower}, assistant iPhone {name_lower}, facturation {name_lower}"
    
    # Title based on profile
    if profile == "honoraires":
        title = f"Diqto pour les {name}s — Notes d'honoraires sur iPhone"
    elif profile == "abonnement":
        title = f"Diqto pour les {name}s — Gestion élèves et facturation sur iPhone"
    else:
        title = f"Diqto pour les {name}s — Devis et factures sur iPhone"
    
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 38'><rect width='48' height='38' rx='19' ry='19' fill='%2325d366'/><circle cx='15' cy='19' r='3' fill='white' opacity='.7'/><circle cx='24' cy='19' r='3' fill='white' opacity='.7'/><circle cx='33' cy='19' r='3' fill='white' opacity='.7'/></svg>">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Outfit:wght@700;800&family=Work+Sans:wght@800&display=swap" rel="stylesheet">
<meta name="description" content="{seo_desc}">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="https://diqto.fr/metiers/{metier_id}.html">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://diqto.fr/metiers/{metier_id}.html">
<meta property="og:title" content="Diqto — L'assistant devis pour les {name}s">
<meta property="og:description" content="{seo_desc}">
<meta property="og:image" content="https://diqto.fr/og-image.png">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Diqto">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Diqto pour les {name}s">
<meta name="twitter:description" content="{seo_desc}">

<!-- Schema.org -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Diqto pour {name}",
  "url": "https://diqto.fr/metiers/{metier_id}.html",
  "description": "{seo_desc}",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "iOS",
  "offers": {{
    "@type": "Offer",
    "price": "",
    "priceCurrency": "EUR",
    "description": "Essai gratuit avant offre payante"
  }}
}}
</script>

<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--green:#25D366;--green-dark:#1ebe59;--blue:#2563EB;--dark:#1e293b;--gray:#f8fafc;--text:#334155;--text-light:#64748b;--white:#fff}}
body{{font-family:'DM Sans','Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:var(--text);line-height:1.6}}
h1,h2,h3,h4,h5,h6{{font-family:'Outfit','DM Sans',sans-serif}}

/* LOGO DIQTO #65 */
@keyframes dotPulse{{0%,100%{{opacity:.3;transform:scale(.8)}}50%{{opacity:1;transform:scale(1)}}}}
.logo-diqto{{display:inline-flex;align-items:center;gap:12px;text-decoration:none}}
.logo-diqto .bubble{{width:48px;height:38px;background:#25d366;border-radius:19px 19px 19px 4px;display:flex;align-items:center;justify-content:center;gap:5px;box-shadow:0 4px 16px rgba(37,211,102,.25)}}
.logo-diqto .bubble i{{display:block;width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,.7);animation:dotPulse 1.4s ease infinite}}
.logo-diqto .bubble i:nth-child(2){{animation-delay:.2s}}
.logo-diqto .bubble i:nth-child(3){{animation-delay:.4s}}
.logo-diqto .text{{font-family:'Work Sans',sans-serif;font-size:34px;font-weight:800;color:#fff;letter-spacing:-1.5px}}
.logo-diqto .text em{{font-style:normal;color:#25d366}}
.logo-diqto.logo-light .text{{color:#111}}
.logo-diqto.logo-sm{{transform:scale(.6);transform-origin:left center}}

/* NAV */
nav{{position:fixed;top:0;left:0;right:0;background:rgba(255,255,255,.92);backdrop-filter:blur(12px);z-index:100;padding:16px 32px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(0,0,0,.06)}}
nav .logo-diqto{{transform:scale(.55);transform-origin:left center}}
nav a.nav-cta{{background:var(--green);color:var(--white);padding:11px 26px;border-radius:50px;text-decoration:none;font-weight:600;font-size:.9em;transition:transform .2s;display:inline-flex;align-items:center;gap:6px;box-shadow:0 2px 12px rgba(37,211,102,.2)}}
nav a.nav-cta:hover{{transform:translateY(-1px);box-shadow:0 4px 20px rgba(37,211,102,.35)}}

/* HERO */
.hero{{min-height:70vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:140px 24px 80px;text-align:center;background:var(--white)}}
.hero h1{{font-family:'Work Sans',sans-serif;font-size:clamp(2rem,5vw,3rem);font-weight:800;color:var(--dark);letter-spacing:-1px;line-height:1.15;margin-bottom:20px}}
.hero .subtitle{{font-size:clamp(1em,2.5vw,1.2em);color:var(--text-light);max-width:560px;margin:0 auto 40px;line-height:1.6}}
.btn-wa{{display:inline-flex;align-items:center;gap:10px;background:var(--green);color:var(--white);padding:18px 44px;border-radius:50px;text-decoration:none;font-size:1.15em;font-weight:700;transition:transform .2s,box-shadow .2s;box-shadow:0 4px 24px rgba(37,211,102,.3)}}
.btn-wa:hover{{transform:translateY(-2px);box-shadow:0 8px 32px rgba(37,211,102,.4)}}

/* STORY / NARRATIVE */
.story-section{{padding:100px 24px;background:var(--gray);text-align:center}}
.story-section h2{{font-family:'Work Sans',sans-serif;font-size:clamp(1.3em,3vw,1.8em);font-weight:700;color:var(--dark);margin-bottom:48px;letter-spacing:-.5px}}
.story{{max-width:520px;margin:0 auto;font-size:clamp(1rem,2vw,1.1rem);line-height:2;color:var(--text-light)}}
.story p{{margin-bottom:8px}}
.story .dialogue{{color:var(--dark);font-style:italic;font-weight:500}}
.story .emphasis{{color:var(--dark);font-weight:600}}
.story-separator{{width:48px;height:2px;background:var(--green);margin:40px auto;border-radius:2px}}
.story-punchline{{font-family:'Work Sans',sans-serif;font-size:clamp(1.2em,3vw,1.6em);font-weight:700;color:var(--dark);letter-spacing:-.5px;text-align:center;margin-top:40px}}

/* SECTIONS */
.section{{padding:80px 24px;max-width:800px;margin:0 auto}}
.section-alt{{background:var(--gray)}}
.section-dark{{background:var(--dark);color:var(--white)}}
h2{{font-family:'Work Sans',sans-serif;font-size:clamp(1.4em,3vw,1.8em);font-weight:700;color:var(--dark);margin-bottom:24px;text-align:center;letter-spacing:-.5px}}
.section-dark h2{{color:var(--white)}}

/* STEPS */
.steps-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:30px;margin-top:30px}}
.step{{text-align:center;padding:20px}}
.step .num{{display:inline-block;background:var(--green);color:var(--white);width:36px;height:36px;border-radius:50%;font-size:1em;font-weight:700;line-height:36px;margin-bottom:10px}}
.step p{{color:var(--text-light);font-size:.9em}}

/* FEATURES */
.metier-features{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-top:24px}}
.metier-feature{{display:flex;gap:12px;align-items:flex-start;background:var(--white);padding:16px;border-radius:12px}}
.section-alt .metier-feature{{background:var(--gray);border:1px solid #e2e8f0}}
.mf-icon{{display:inline-flex;align-items:center;justify-content:center;min-width:42px;height:24px;padding:0 8px;border-radius:999px;background:rgba(37,211,102,.12);color:#15803d;font-size:11px;font-weight:800;letter-spacing:.7px;flex-shrink:0}}
.mf-desc{{color:var(--text-light);font-size:.85em}}

/* WHATSAPP MOCKUP */
.wa-mockup{{background:#e5ddd5;border-radius:16px;padding:20px;max-width:400px;margin:20px auto 0}}
.wa-msg{{background:var(--white);border-radius:8px;padding:10px 14px;margin-bottom:8px;font-size:.9em;max-width:85%;white-space:pre-line}}
.wa-user{{background:#dcf8c6;margin-left:auto}}
.wa-bot{{background:var(--white)}}

/* RELATED */
.related-tags{{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:16px}}
.metier-tag{{display:inline-flex;align-items:center;gap:4px;background:var(--gray);padding:10px 20px;border-radius:25px;text-decoration:none;font-size:.9em;color:var(--text);font-weight:500;transition:all .2s;border:1px solid transparent}}
.metier-tag:hover{{border-color:var(--green);background:rgba(37,211,102,.06)}}

/* LEGAL MENTIONS */
.legal-mentions{{background:#fef3c7;border-radius:8px;padding:12px 16px;margin-top:16px;font-size:.85em;color:#92400e}}

/* CTA */
.cta-section{{padding:80px 24px;text-align:center;background:var(--dark);color:var(--white)}}
.cta-section h2{{color:var(--white);margin-bottom:12px}}
.cta-sub{{color:rgba(255,255,255,.6);font-size:1em;margin-bottom:30px}}

/* FOOTER */
footer{{padding:40px 24px 30px;background:#0f172a;color:rgba(255,255,255,.4);font-size:.85em;text-align:center}}
footer a{{color:rgba(255,255,255,.5);text-decoration:none}}
footer a:hover{{color:rgba(255,255,255,.7)}}
footer .links{{display:flex;justify-content:center;gap:20px;flex-wrap:wrap;margin-top:12px}}

/* RESPONSIVE */
@media(max-width:768px){{
  .hero{{padding:110px 20px 60px}}
  .btn-wa{{padding:16px 32px;font-size:1.05em}}
  .steps-grid{{grid-template-columns:1fr;gap:16px}}
  .metier-features{{grid-template-columns:1fr}}
  .section{{padding:40px 20px}}
}}
</style>
</head>
<body>

<!-- NAV -->
<nav>
  <a href="/" class="logo-diqto logo-light">
    <span class="bubble"><i></i><i></i><i></i></span>
    <span class="text">diq<em>to</em></span>
  </a>
  <a href="../?source=seo_metier_{metier_id}&metier={quote(name, safe='')}#beta" class="nav-cta">
    Commencer gratuit
  </a>
</nav>

<!-- HERO -->
<section class="hero">
  <h1>{accroche}</h1>
  <p class="subtitle">Tu t'es mis à ton compte pour faire ce que tu aimes.<br><strong>Pas pour faire de l'administratif.</strong></p>
  <a href="../?source=seo_metier_{metier_id}&metier={quote(name, safe='')}#beta" class="btn-wa">
    Créer mon premier brouillon gratuit
  </a>
</section>

<!-- LE QUOTIDIEN (narrative) -->
<section class="story-section">
  <h2>Le scénario que tu connais par cœur</h2>
  <div class="story">
    {narrative_html}
  </div>
  <div class="story-separator"></div>
  <p class="story-punchline">{narrative_resolution}</p>
</section>

<!-- SOLUTION -->
<section class="section section-alt" style="max-width:100%;padding:80px 24px">
  <div style="max-width:800px;margin:0 auto">
    <h2>En 2026, l'IA prépare tes {doc_word} avant validation.</h2>
    <div class="steps-grid">
      <div class="step">
        <span class="num">1</span>
        <p>{profile_data['step1']}</p>
      </div>
      <div class="step">
        <span class="num">2</span>
        <p>Diqto prépare un brouillon PDF professionnel à relire</p>
      </div>
      <div class="step">
        <span class="num">3</span>
        <p>{profile_data['step3']}</p>
      </div>
    </div>
  </div>
</section>

<!-- EXEMPLE PREPARATION -->
<section class="section" style="text-align:center">
  <h2>Exemple : {exemple_title}</h2>
  <div class="wa-mockup">
    {prep_convo}
  </div>
</section>

<!-- FEATURES -->
<section class="section section-alt" style="max-width:100%;padding:80px 24px">
  <div style="max-width:800px;margin:0 auto">
    <h2>Et ça ne s'arrête pas là.</h2>
    <div class="metier-features">
      {features_html}
    </div>
    {mentions_html}
  </div>
</section>

<!-- CTA FINAL -->
<section class="cta-section">
  <h2>Ton prochain {profile_data['doc_word']} part d'un brouillon clair.<br>Pas d'une page blanche.</h2>
  <a href="../?source=seo_metier_{metier_id}&metier={quote(name, safe='')}#beta" class="btn-wa" style="margin:24px 0">
    Commencer gratuit
  </a>
  <p class="cta-sub">Essai gratuit avant tout paiement.<br>Premier brouillon uniquement après validation humaine.</p>
</section>

<!-- AUTRES MÉTIERS -->
<section class="section" style="text-align:center">
  <h2>Découvrez aussi</h2>
  <div class="related-tags">
    {related_html}
  </div>
</section>

<!-- FOOTER -->
<footer>
  <p>© 2026 Diqto — Vous dictez, on facture.</p>
  <div class="links">
    <a href="/">Accueil</a>
    <a href="mailto:contact@diqto.fr">Contact</a>
    <a href="/cgu.html">CGU</a>
    <a href="/confidentialite.html">Confidentialité</a>
  </div>
</footer>

</body>
</html>"""
    return html


def load_all_metiers():
    """Load all métier configs."""
    metiers = {}
    for filepath in sorted(glob.glob(str(METIERS_CONFIG_DIR / "*.json"))):
        filename = os.path.basename(filepath)
        if filename.startswith("_"):
            continue
        metier_id = filename.replace(".json", "")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["metier"] = metier_id
            metiers[metier_id] = data
        except Exception as e:
            print(f"  WARN Erreur {filename}: {e}")
    return metiers


def main():
    print("Génération des pages métier SEO...")
    
    # Create output dir
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load all métiers
    metiers = load_all_metiers()
    print(f"{len(metiers)} métiers chargés")
    
    # Generate pages
    count = 0
    for metier_id, metier_data in metiers.items():
        html = generate_page(metier_id, metier_data, metiers)
        output_path = OUTPUT_DIR / f"{metier_id}.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        name = metier_data.get("name", metier_data.get("label", metier_id))
        print(f"  OK {name} -> metiers/{metier_id}.html")
        count += 1
    
    print(f"\nOK {count} pages générées dans {OUTPUT_DIR}/")
    print("Relancez ce script à tout moment pour régénérer toutes les pages.")


if __name__ == "__main__":
    main()
