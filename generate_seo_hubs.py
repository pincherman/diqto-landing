#!/usr/bin/env python3
"""Generate people-first SEO hubs and guides for diqto.fr."""
from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent
CONFIG_ROOT = ROOT.parent / "batiboss" / "config" / "metiers"
BASE_URL = "https://diqto.fr"
UPDATED = "2026-07-11"

CATEGORY_LABELS = {
    "batiment": "Bâtiment et travaux",
    "sante": "Santé et bien-être",
    "enseignement": "Enseignement et coaching",
    "juridique_finance": "Conseil, droit et expertise",
    "services": "Services et création",
    "creatif": "Création et événementiel",
    "beaute": "Beauté et soins",
    "automobile": "Automobile",
    "evenementiel": "Événementiel",
    "restauration": "Restauration",
    "autre": "Autres activités indépendantes",
}

TOP_LEVEL = {
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

GUIDES = [
    {
        "slug": "logiciel-devis-facture-artisan",
        "title": "Logiciel de devis et factures pour artisan : choisir sans alourdir ses journées",
        "description": "Les critères concrets pour choisir un logiciel de devis et factures d'artisan : usage chantier, brouillons, clients, prix, contrôle et limites.",
        "eyebrow": "Guide pratique · Artisans",
        "lead": "Le bon outil n'est pas celui qui affiche le plus de boutons. C'est celui qui vous évite de refaire au bureau ce que vous saviez déjà sur le chantier.",
        "body": """
<section class="seo-section"><h2>Commencez par la contrainte réelle</h2>
<p>Pour un artisan, le devis n'est pas qu'un calcul. Il faut retrouver le client, se rappeler les travaux, reprendre les quantités, vérifier le matériel, appliquer le bon taux de TVA et garder une trace. Si le logiciel exige de tout ressaisir le soir, il déplace la paperasse sans la réduire.</p>
<div class="seo-note"><p><strong>Le test le plus utile :</strong> prenez une intervention terminée aujourd'hui. Pouvez-vous préparer un brouillon fiable depuis votre téléphone, le corriger et le garder pour demain sans rien envoyer par erreur&nbsp;?</p></div></section>
<section class="seo-section"><h2>Les sept critères qui comptent sur le terrain</h2><ol>
<li><strong>Un démarrage rapide :</strong> voix, texte ou photo selon le métier, sans formation préalable.</li>
<li><strong>Un brouillon modifiable :</strong> prestations, quantités, prix et coordonnées doivent rester sous votre contrôle.</li>
<li><strong>Un historique client :</strong> retrouver les devis, factures et prochaines actions au même endroit.</li>
<li><strong>Un catalogue réutilisable :</strong> vos prestations habituelles reviennent sans les recréer à chaque chantier.</li>
<li><strong>Un passage devis vers facture :</strong> éviter la double saisie une fois le travail accepté.</li>
<li><strong>Des prix lisibles :</strong> abonnement, limites du plan gratuit et options annoncés avant l'achat.</li>
<li><strong>Une sortie simple :</strong> vos données et documents doivent rester exportables.</li>
</ol></section>
<section class="seo-section"><h2>Tableur, logiciel générique ou outil pensé chantier&nbsp;?</h2>
<div class="seo-table-wrap"><table class="seo-table"><thead><tr><th>Approche</th><th>Utile quand</th><th>Limite fréquente</th></tr></thead><tbody>
<tr><td>Papier ou tableur</td><td>Très peu de documents, habitudes stables</td><td>Ressaisie, numérotation et suivi client manuels</td></tr>
<tr><td>Logiciel généraliste</td><td>Gestion structurée depuis un ordinateur</td><td>Parcours parfois trop lourd sur téléphone</td></tr>
<tr><td>Outil mobile métier</td><td>Travail sur site, informations encore fraîches</td><td>Il faut vérifier que le brouillon reste éditable et que le métier est vraiment pris en charge</td></tr>
</tbody></table></div></section>
<section class="seo-section"><h2>Ce que Diqto apporte, et ce qu'il ne promet pas</h2>
<p>Diqto part de la voix, du texte et, pour sept métiers chantier, d'une photo afin de préparer une estimation modifiable. L'objectif est d'éviter la page blanche et de garder le fil client. Une analyse photo ne constitue jamais un prix ferme ni un devis envoyé automatiquement.</p>
<p>La fonction photo est actuellement limitée aux plombiers, électriciens, peintres, maçons, menuisiers, carreleurs et chauffagistes. Pour les autres métiers, la dictée et le texte restent les entrées principales.</p></section>
""",
        "related": [
            ("/plombier.html", "Diqto pour plombiers"),
            ("/electricien.html", "Diqto pour électriciens"),
            ("/metiers/chauffagiste.html", "Diqto pour chauffagistes"),
        ],
        "sources": [],
    },
    {
        "slug": "logiciel-facturation-micro-entrepreneur",
        "title": "Logiciel de facturation pour micro-entrepreneur : le choisir selon votre vraie activité",
        "description": "Comment choisir un logiciel de facturation pour micro-entrepreneur sans payer pour une usine à gaz : documents, clients, TVA, mobile et contrôle.",
        "eyebrow": "Guide pratique · Micro-entreprise",
        "lead": "Un micro-entrepreneur n'a pas besoin d'un mini-ERP. Il a besoin de documents justes, d'un suivi clair et de moins de tâches reportées au soir.",
        "body": """
<section class="seo-section"><h2>Le volume de documents ne dit pas tout</h2>
<p>Deux indépendants qui émettent dix factures par mois peuvent avoir des besoins opposés. L'un reprend toujours les mêmes prestations. L'autre travaille sur devis, facture des acomptes et doit relancer plusieurs clients. Le bon choix part donc de votre parcours réel, pas d'une liste de fonctionnalités.</p></section>
<section class="seo-section"><h2>La checklist avant de choisir</h2><ul>
<li><strong>Documents :</strong> devis, factures, avoirs ou notes d'honoraires selon votre activité.</li>
<li><strong>Mentions et numérotation :</strong> les champs doivent être visibles et contrôlables avant finalisation.</li>
<li><strong>TVA :</strong> votre régime et les changements futurs doivent pouvoir être configurés proprement.</li>
<li><strong>Clients :</strong> coordonnées, historique et documents associés doivent être faciles à retrouver.</li>
<li><strong>Mobile :</strong> si vous travaillez hors bureau, testez le parcours complet sur votre téléphone.</li>
<li><strong>Export :</strong> vérifiez comment récupérer vos documents et transmettre les éléments utiles à votre comptable.</li>
</ul>
<div class="seo-note"><p>Les mentions obligatoires varient selon le destinataire et la situation. Le site officiel Entreprendre.Service-Public.fr tient une liste de référence. Un logiciel aide à préparer le document, mais vous restez responsable de sa vérification.</p></div></section>
<section class="seo-section"><h2>Gratuit ou payant&nbsp;: regardez les limites, pas seulement le prix</h2>
<p>Un plan gratuit peut suffire pour tester votre parcours et produire quelques documents. Vérifiez ce qui est limité&nbsp;: documents finalisés, envois, exports, utilisateurs, pied de page ou durée des fonctions vocales. Chez Diqto, Free permet les clients et brouillons illimités, avec trois documents finalisés, exportés ou envoyés par mois.</p>
<p>Essential est affiché à 9&nbsp;€ TTC par mois en France et Vocal Pro à 19&nbsp;€ TTC. Dans l'app iPhone, le prix local présenté par Apple avant l'achat fait foi.</p></section>
<section class="seo-section"><h2>Quand la voix devient réellement utile</h2>
<p>La dictée a de la valeur quand elle récupère des informations que vous auriez sinon dû retaper&nbsp;: client, prestation, montant connu, détail à vérifier et prochaine action. Elle n'a pas de valeur si le résultat part sans relecture ou si vous devez corriger tout le document.</p>
<p>Le test Diqto est volontairement simple&nbsp;: choisissez une tâche réelle, parlez comme à un collègue, puis jugez le brouillon obtenu. Rien n'est partagé simplement parce que vous avez dicté.</p></section>
""",
        "related": [
            ("/fonctionnalites.html", "Voir les fonctionnalités Diqto"),
            ("/docs.html", "Préparer votre premier brouillon"),
            ("/guides/facturation-electronique-micro-entreprise.html", "Comprendre la facture électronique"),
        ],
        "sources": [
            ("https://entreprendre.service-public.fr/vosdroits/F31808", "Entreprendre.Service-Public.fr — mentions obligatoires sur une facture"),
        ],
    },
    {
        "slug": "facturation-electronique-micro-entreprise",
        "title": "Facturation électronique et micro-entreprise : ce qui change en 2026 et 2027",
        "description": "Calendrier officiel de la facturation électronique pour micro-entreprises : réception en 2026, émission en 2027, PDF, plateforme agréée et préparation.",
        "eyebrow": "Guide vérifié · Facturation électronique",
        "lead": "Deux dates, une confusion fréquente : recevoir devient obligatoire pour toutes les entreprises en 2026, tandis que les micro-entreprises ont jusqu'en 2027 pour émettre.",
        "body": """
<section class="seo-section"><h2>Les deux dates à retenir</h2>
<div class="seo-grid"><article class="seo-card"><h3>1er septembre 2026</h3><p>Toutes les entreprises, quelle que soit leur taille, doivent pouvoir recevoir des factures électroniques.</p></article><article class="seo-card"><h3>1er septembre 2027</h3><p>Les PME et micro-entreprises doivent émettre leurs factures électroniques et transmettre les données concernées.</p></article><article class="seo-card"><h3>Dès maintenant</h3><p>Vérifiez votre situation, vos clients B2B/B2C et la façon dont votre outil se raccordera à une plateforme agréée.</p></article></div>
<p class="seo-meta">Sources officielles vérifiées le 11 juillet 2026.</p></section>
<section class="seo-section"><h2>Un PDF envoyé par email n'est pas la facture électronique de la réforme</h2>
<p>Le ministère de l'Économie précise qu'une facture électronique doit respecter un format normé, porter les données obligatoires dans des champs dédiés et transiter par une plateforme agréée. Un PDF ordinaire joint à un email ne suffit donc pas pour ce parcours réglementaire.</p>
<div class="seo-note"><p><strong>Point de vigilance :</strong> méfiez-vous des logiciels qui utilisent le mot «&nbsp;conforme&nbsp;» sans expliquer le rôle de la plateforme agréée, le calendrier et le périmètre réellement opérationnel.</p></div></section>
<section class="seo-section"><h2>Comment vous préparer sans tout changer aujourd'hui</h2><ol>
<li>Identifiez les factures reçues et émises entre entreprises françaises.</li>
<li>Vérifiez que vos coordonnées légales, SIREN, régime de TVA et clients sont propres.</li>
<li>Demandez à votre outil quel partenaire plateforme agréée portera la transmission.</li>
<li>Distinguez vos factures B2B, vos ventes aux particuliers et les éventuelles données de paiement.</li>
<li>Gardez une validation humaine avant toute transmission réelle.</li>
</ol></section>
<section class="seo-section"><h2>La position de Diqto</h2>
<p>Diqto reste une solution de préparation et de suivi. Diqto ne se présente pas comme une plateforme agréée. Le parcours réglementaire doit passer par un partenaire agréé, avec vérification de l'annuaire destinataire et confirmation humaine avant envoi.</p>
<p>Cette intégration est en cours de préparation. Tant que le parcours de production n'est pas validé de bout en bout, un email ou un PDF Diqto ne doit pas être présenté comme une transmission réglementaire.</p></section>
""",
        "related": [
            ("/guides/logiciel-facturation-micro-entrepreneur.html", "Choisir son logiciel de facturation"),
            ("/fonctionnalites.html", "Ce que Diqto prépare aujourd'hui"),
            ("/cgu.html", "Consulter le cadre d'utilisation"),
        ],
        "sources": [
            ("https://www.economie.gouv.fr/tout-savoir-sur-la-facturation-electronique-pour-les-entreprises", "Ministère de l'Économie — calendrier et définition"),
            ("https://www.impots.gouv.fr/professionnel/questions/partir-de-quand-suis-je-concerne-par-la-reforme-de-la-facturation", "impots.gouv.fr — dates selon la taille de l'entreprise"),
            ("https://www.impots.gouv.fr/facturation-electronique-et-plateformes-agreees", "impots.gouv.fr — rôle des plateformes agréées"),
        ],
    },
    {
        "slug": "mentions-obligatoires-facture-micro-entrepreneur",
        "title": "Mentions obligatoires sur une facture de micro-entrepreneur : la checklist 2026",
        "description": "La checklist vérifiée des mentions d'une facture de micro-entrepreneur en 2026 : identité, numérotation, TVA, paiement et cas particuliers.",
        "eyebrow": "Guide vérifié · Factures",
        "lead": "Une facture correcte ne se résume pas à un nom, un prix et un total. Voici les champs à contrôler avant de finaliser votre document.",
        "body": """
<section class="seo-section"><h2>Les informations de base à vérifier</h2>
<p>La liste exacte dépend de votre activité, de votre régime de TVA, du client et de l'opération. Le socle comprend généralement la date d'émission, un numéro unique suivant une séquence chronologique continue, l'identité du vendeur et celle du client, la date de la vente ou de la prestation, ainsi que le détail des produits ou services.</p>
<div class="seo-table-wrap"><table class="seo-table"><thead><tr><th>Bloc</th><th>Points à contrôler</th></tr></thead><tbody>
<tr><td>Émetteur</td><td>Nom ou dénomination, adresse, numéro Siren, forme juridique si elle s'applique et coordonnées d'immatriculation utiles.</td></tr>
<tr><td>Client</td><td>Nom ou dénomination et adresse de facturation ; adresse de livraison si elle est différente et requise.</td></tr>
<tr><td>Document</td><td>Date, numéro unique, date de prestation ou de livraison et numéro de bon de commande s'il a été établi par l'acheteur.</td></tr>
<tr><td>Détail</td><td>Désignation, quantité, prix unitaire hors taxe, taux de TVA applicable ou mention d'exonération, réductions et totaux.</td></tr>
<tr><td>Paiement</td><td>Date ou délai de règlement, conditions d'escompte, pénalités de retard et indemnité forfaitaire de 40&nbsp;€ lorsqu'elle s'applique entre professionnels.</td></tr>
</tbody></table></div></section>
<section class="seo-section"><h2>Micro-entreprise sans TVA : la mention ne se devine pas</h2>
<p>Si vous bénéficiez de la franchise en base de TVA, la facture doit porter la mention prévue par le code général des impôts&nbsp;: «&nbsp;TVA non applicable, art. 293 B du CGI&nbsp;». Si votre situation change ou si une opération suit un régime particulier, ne réutilisez pas automatiquement une ancienne facture sans vérifier le traitement.</p>
<div class="seo-note"><p><strong>À retenir :</strong> «&nbsp;micro-entrepreneur&nbsp;» ne signifie pas toujours «&nbsp;sans TVA&nbsp;». C'est votre régime applicable à la date de l'opération qui commande la facture.</p></div></section>
<section class="seo-section"><h2>Ce que la réforme ajoute progressivement</h2>
<p>Le ministère de l'Économie indique que la réforme de la facturation électronique ajoute notamment le Siren du client, l'adresse de livraison quand elle diffère de l'adresse de facturation, la nature des opérations — biens, services ou les deux — et, le cas échéant, la mention de l'option pour le paiement de la TVA d'après les débits.</p>
<p>Ces champs ne transforment pas un PDF envoyé par email en facture électronique réglementaire. La transmission concernée devra passer par une plateforme agréée selon le calendrier officiel.</p></section>
<section class="seo-section"><h2>Le contrôle simple avant de finaliser</h2><ol>
<li>Vérifiez le client et la date de l'opération.</li>
<li>Contrôlez la continuité de la numérotation.</li>
<li>Relisez chaque quantité, prix, taux ou mention de TVA.</li>
<li>Vérifiez les conditions de règlement adaptées au client.</li>
<li>Conservez la facture selon vos obligations comptables et fiscales.</li>
</ol>
<p>Diqto prépare un brouillon éditable et garde le contexte client. La finalisation reste une action humaine&nbsp;: aucun guide générique ne remplace la vérification de votre situation ou le conseil d'un professionnel.</p></section>
""",
        "related": [
            ("/guides/logiciel-facturation-micro-entrepreneur.html", "Choisir son logiciel de facturation"),
            ("/guides/facturation-electronique-micro-entreprise.html", "Comprendre la réforme 2026–2027"),
            ("/fonctionnalites.html", "Voir les fonctions de préparation Diqto"),
        ],
        "sources": [
            ("https://www.economie.gouv.fr/entreprises/gerer-son-entreprise-au-quotidien/gerer-sa-comptabilite-et-ses-demarches/mentions-obligatoires-dune-facture-tout-savoir", "Ministère de l'Économie — mentions obligatoires d'une facture"),
            ("https://entreprendre.service-public.fr/vosdroits/F31808", "Entreprendre.Service-Public.fr — facturation et cas particuliers"),
        ],
    },
    {
        "slug": "devis-artisan-mentions-obligatoires",
        "title": "Devis artisan : mentions obligatoires et points à vérifier avant signature",
        "description": "Ce qu'un artisan doit vérifier sur un devis : identité, détail des travaux, prix, déplacement, durée de validité, signature et cas obligatoires.",
        "eyebrow": "Guide vérifié · Devis artisan",
        "lead": "Un devis protège le client et l'artisan seulement s'il décrit clairement ce qui sera fait, à quel prix et dans quelles conditions.",
        "body": """
<section class="seo-section"><h2>Quand le devis devient obligatoire</h2>
<p>La règle dépend de la prestation. La DGCCRF rappelle qu'un professionnel doit informer le consommateur sur le prix avant la conclusion du contrat et qu'un devis détaillé est obligatoire pour plusieurs activités, notamment de nombreux travaux de dépannage, réparation et entretien dans le bâtiment.</p>
<p>Plomberie, électricité, maçonnerie, menuiserie, serrurerie, couverture, peinture, plâtrerie, revêtements de sols ou génie climatique font partie des activités explicitement citées. D'autres règles particulières existent pour les services à la personne, le déménagement, l'optique, les prestations funéraires et d'autres secteurs.</p></section>
<section class="seo-section"><h2>La checklist d'un devis lisible</h2><ul>
<li><strong>Les parties :</strong> identité et coordonnées du professionnel et du client.</li>
<li><strong>Le document :</strong> date d'établissement et durée de validité de l'offre.</li>
<li><strong>La prestation :</strong> description précise, quantités et prix unitaires.</li>
<li><strong>Le chantier :</strong> taux horaire de main-d'œuvre et frais de déplacement lorsqu'ils existent.</li>
<li><strong>Les montants :</strong> total hors taxe, taux et montant de TVA, total TTC ou mention adaptée au régime.</li>
<li><strong>Le prix du devis :</strong> caractère gratuit ou payant lorsque cette information est pertinente.</li>
<li><strong>L'engagement :</strong> signature du professionnel et espace d'acceptation du client selon le parcours.</li>
</ul>
<div class="seo-note"><p><strong>Attention :</strong> le contenu varie selon la prestation et les textes qui l'encadrent. Cette checklist est un socle de contrôle, pas une liste universelle suffisante pour tous les métiers.</p></div></section>
<section class="seo-section"><h2>Un devis accepté engage</h2>
<p>La DGCCRF décrit le devis comme une offre de contrat. Une fois accepté, il engage les parties sur le périmètre et le prix prévus. Une description vague, une option non distinguée ou un déplacement oublié peut donc devenir un désaccord concret.</p>
<p>Avant signature, relisez les exclusions, les délais, les conditions de paiement, l'acompte éventuel et les règles applicables si le contrat est conclu à distance ou hors établissement.</p></section>
<section class="seo-section"><h2>Préparer vite sans envoyer trop vite</h2>
<p>Sur le terrain, le bon réflexe est de capturer les informations pendant qu'elles sont fraîches&nbsp;: travaux observés, quantités, accès, matériel et réserves. Diqto peut en faire un brouillon modifiable depuis la voix, le texte et, pour sept métiers chantier, une photo.</p>
<p>Le brouillon n'est ni un prix ferme ni un devis accepté. Vous corrigez les lignes, contrôlez les montants et choisissez vous-même quand finaliser ou partager le document.</p></section>
""",
        "related": [
            ("/guides/logiciel-devis-facture-artisan.html", "Choisir un logiciel utile sur chantier"),
            ("/metiers.html", "Trouver votre parcours métier"),
            ("/fonctionnalites.html", "Voir ce que Diqto prépare"),
        ],
        "sources": [
            ("https://www.economie.gouv.fr/dgccrf/les-fiches-pratiques/devis", "DGCCRF — obligations, cas et contenu d'un devis"),
        ],
    },
]

PRIORITY_PATHS = [
    ("/guides/facturation-electronique-micro-entreprise.html", "Facturation électronique micro-entreprise"),
    ("/guides/logiciel-facturation-micro-entrepreneur.html", "Logiciel de facturation micro-entrepreneur"),
    ("/guides/logiciel-devis-facture-artisan.html", "Logiciel devis et factures artisan"),
    ("/guides/mentions-obligatoires-facture-micro-entrepreneur.html", "Mentions obligatoires facture micro-entrepreneur"),
    ("/guides/devis-artisan-mentions-obligatoires.html", "Mentions obligatoires devis artisan"),
    ("/histoires.html", "Histoires de terrain"),
    ("/metiers.html", "Tous les métiers"),
    ("/plombier.html", "Plombier"),
    ("/electricien.html", "Électricien"),
    ("/osteopathe.html", "Ostéopathe"),
    ("/coach-sportif.html", "Coach sportif"),
    ("/metiers/avocat.html", "Avocat"),
    ("/metiers/prof_karate.html", "Professeur de karaté"),
    ("/fonctionnalites.html", "Fonctionnalités"),
    ("/docs.html", "Bien démarrer"),
]


def shell(active: str = "") -> str:
    items = [
        ("/", "Accueil", "home"),
        ("/fonctionnalites.html", "Fonctionnalités", "features"),
        ("/metiers.html", "Métiers", "trades"),
        ("/guides.html", "Guides", "guides"),
        ("/#tarifs", "Tarifs", "pricing"),
    ]
    links = "".join(
        f'<a href="{href}"{(" aria-current=\"page\"" if key == active else "")}>{label}</a>'
        for href, label, key in items
    )
    return f'''<a class="global-skip-link" href="#contenu">Aller au contenu</a>
<a class="global-announcement" href="/guides/facturation-electronique-micro-entreprise.html"><strong>Facturation électronique</strong><span>Ce qui change en 2026 et 2027 <span aria-hidden="true">→</span></span></a>
<header class="global-header" data-menu-open="false"><div class="global-nav">
  <a class="global-brand" href="/" aria-label="Diqto, accueil"><span class="global-brand-mark" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span><span class="global-brand-name">diq<em>to</em></span></a>
  <button class="global-menu-toggle" type="button" aria-expanded="false" aria-controls="navigation-principale">Menu</button>
  <nav class="global-menu" id="navigation-principale" aria-label="Navigation principale">{links}<a class="global-cta" href="/#beta">Commencer gratuit</a></nav>
</div></header>'''


def footer() -> str:
    return '''<footer class="seo-footer"><div class="seo-container"><nav aria-label="Navigation de pied de page">
<span>© 2026 Diqto</span><a href="/">Accueil</a><a href="/fonctionnalites.html">Fonctionnalités</a><a href="/metiers.html">Métiers</a><a href="/guides.html">Guides</a><a href="/docs.html">Bien démarrer</a><a href="/cgu.html">CGU</a><a href="/confidentialite.html">Confidentialité</a><a href="mailto:support@diqto.fr">Support</a>
</nav></div></footer>'''


def schemas(page_type: str, title: str, description: str, url: str, parent: str, items=None, sources=None) -> str:
    parent_url = f"{BASE_URL}/{parent.lower()}.html"
    breadcrumb_items = [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{BASE_URL}/"},
    ]
    if url != parent_url:
        breadcrumb_items.append({"@type": "ListItem", "position": 2, "name": parent, "item": parent_url})
    breadcrumb_items.append({"@type": "ListItem", "position": len(breadcrumb_items) + 1, "name": title, "item": url})
    breadcrumb = {
        "@type": "BreadcrumbList",
        "itemListElement": breadcrumb_items,
    }
    page = {"@type": page_type, "headline": title, "name": title, "description": description, "url": url, "inLanguage": "fr-FR"}
    if page_type == "Article":
        page.update({"datePublished": UPDATED, "dateModified": UPDATED, "author": {"@type": "Organization", "name": "DIQTO"}, "publisher": {"@type": "Organization", "name": "DIQTO", "url": f"{BASE_URL}/"}})
        if sources:
            page["citation"] = [url for url, _ in sources]
    if items:
        page["mainEntity"] = {"@type": "ItemList", "itemListElement": items}
    graph = {"@context": "https://schema.org", "@graph": [page, breadcrumb]}
    return json.dumps(graph, ensure_ascii=False, indent=2)


def page_head(title: str, description: str, url: str, schema: str, og_type: str = "website", asset_prefix: str = "") -> str:
    escaped_title = html.escape(title, quote=True)
    escaped_description = html.escape(description, quote=True)
    return f'''<!DOCTYPE html><html lang="fr"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="theme-color" content="#0c0c0c">
<title>{escaped_title} — Diqto</title><meta name="description" content="{escaped_description}"><meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}"><link rel="icon" type="image/png" sizes="64x64" href="/favicon.png"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{asset_prefix}site-shell.css"><link rel="stylesheet" href="{asset_prefix}seo-pages.css"><script defer src="{asset_prefix}site-shell.js"></script>
<meta property="og:type" content="{og_type}"><meta property="og:url" content="{url}"><meta property="og:title" content="{escaped_title}"><meta property="og:site_name" content="Diqto"><meta property="og:description" content="{escaped_description}"><meta property="og:image" content="{BASE_URL}/og-image.png"><meta property="og:locale" content="fr_FR">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escaped_title}"><meta name="twitter:description" content="{escaped_description}"><meta name="twitter:image" content="{BASE_URL}/og-image.png">
<script type="application/ld+json">{schema}</script></head><body>'''


def related_section(related) -> str:
    cards = "".join(f'<article class="seo-card"><h3>{html.escape(label)}</h3><p><a href="{href}">Consulter cette page</a></p></article>' for href, label in related)
    return f'<section class="seo-section"><h2>Continuer avec un cas concret</h2><div class="seo-grid">{cards}</div></section>'


def source_section(sources) -> str:
    if not sources:
        return ""
    links = "".join(f'<li><a href="{href}" rel="noopener">{html.escape(label)}</a></li>' for href, label in sources)
    return f'<aside class="seo-sources"><h2>Sources officielles</h2><ul>{links}</ul></aside>'


def priority_paths_section() -> str:
    links = "".join(f'<a href="{href}">{html.escape(label)}</a>' for href, label in PRIORITY_PATHS)
    return f'''<section class="seo-category seo-priority-paths" aria-labelledby="parcours-prioritaires"><h2 id="parcours-prioritaires">Parcours à explorer en priorité</h2><p>Ces pages relient les guides, les métiers les plus parlants et les premières actions utiles avant de tester Diqto.</p><div class="seo-link-grid">{links}</div></section>'''


def generate_guide(guide: dict) -> None:
    url = f"{BASE_URL}/guides/{guide['slug']}.html"
    schema = schemas("Article", guide["title"], guide["description"], url, "Guides", sources=guide["sources"])
    content = page_head(guide["title"], guide["description"], url, schema, "article", "../")
    content += shell("guides")
    content += f'''<main id="contenu"><div class="seo-container"><nav class="seo-breadcrumbs" aria-label="Fil d'Ariane"><a href="/">Accueil</a><span>›</span><a href="/guides.html">Guides</a><span>›</span>Guide</nav></div>
<header class="seo-hero"><div class="seo-container"><p class="seo-eyebrow">{guide['eyebrow']}</p><h1>{guide['title']}</h1><p class="seo-lead">{guide['lead']}</p><p class="seo-meta">Publié et vérifié le 11 juillet 2026 · Lecture 6 minutes</p></div></header>
<div class="seo-container seo-main">{guide['body']}{source_section(guide['sources'])}{related_section(guide['related'])}
<section class="seo-cta"><h2>Testez Diqto sur une tâche réelle.</h2><p>Un devis, une facture ou une note à finir aujourd'hui. Vous jugerez le brouillon, pas une promesse marketing.</p><div class="seo-actions"><a class="seo-button" href="/?source=seo_guide_{guide['slug']}#beta">Créer mon premier brouillon gratuit</a><a class="seo-button secondary" href="/fonctionnalites.html">Voir les fonctionnalités</a></div></section></div></main>'''
    content += footer() + "</body></html>"
    out = ROOT / "guides" / f"{guide['slug']}.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(content, encoding="utf-8")


def load_trades():
    groups = {key: [] for key in CATEGORY_LABELS}
    for path in sorted(CONFIG_ROOT.glob("*.json")):
        if path.stem.startswith("_"):
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        label = data.get("label", path.stem.replace("_", " ").title())
        category = data.get("category", "autre")
        href = "/" + TOP_LEVEL.get(path.stem, f"metiers/{path.stem}.html")
        groups.setdefault(category, []).append((label, href))
    return groups


def generate_trades_hub() -> None:
    groups = load_trades()
    flat = [(label, href) for values in groups.values() for label, href in values]
    items = [{"@type": "ListItem", "position": index + 1, "name": label, "url": f"{BASE_URL}{href}"} for index, (label, href) in enumerate(flat)]
    title = "Métiers accompagnés par Diqto"
    description = "Découvrez les parcours Diqto par métier : artisans, professions libérales, enseignants, consultants et activités de service."
    url = f"{BASE_URL}/metiers.html"
    schema = schemas("CollectionPage", title, description, url, "Métiers", items=items)
    content = page_head(title, description, url, schema) + shell("trades")
    content += '''<main id="contenu"><header class="seo-hero"><div class="seo-container"><p class="seo-eyebrow">Votre activité, vos mots</p><h1>Diqto part de votre métier.</h1><p class="seo-lead">Le moteur reste commun. Les documents, le vocabulaire et les raccourcis s'adaptent à votre activité sans promettre la même fonction à tout le monde.</p></div></header><div class="seo-container seo-main">'''
    for category, category_label in CATEGORY_LABELS.items():
        links = groups.get(category, [])
        if not links:
            continue
        link_html = "".join(f'<a href="{href}">{html.escape(label)}</a>' for label, href in sorted(links))
        content += f'<section class="seo-category"><h2>{category_label}</h2><div class="seo-link-grid">{link_html}</div></section>'
    content += '''<section class="seo-cta"><h2>Votre métier n'apparaît pas&nbsp;?</h2><p>Commencez par décrire votre activité et le premier document que vous voulez préparer. Nous vérifierons le parcours réellement adapté.</p><div class="seo-actions"><a class="seo-button" href="/#beta">Demander mon accès gratuit</a><a class="seo-button secondary" href="/guides.html">Consulter les guides</a></div></section></div></main>'''
    content += footer() + "</body></html>"
    (ROOT / "metiers.html").write_text(content, encoding="utf-8")


def generate_guides_hub() -> None:
    title = "Guides pratiques pour indépendants"
    description = "Des guides Diqto concrets et sourcés sur les devis, la facturation des micro-entreprises et la réforme de la facture électronique."
    url = f"{BASE_URL}/guides.html"
    items = [{"@type": "ListItem", "position": index + 1, "name": guide["title"], "url": f"{BASE_URL}/guides/{guide['slug']}.html"} for index, guide in enumerate(GUIDES)]
    schema = schemas("CollectionPage", title, description, url, "Guides", items=items)
    cards = "".join(f'''<article class="seo-card"><h2>{guide['title']}</h2><p>{guide['description']}</p><p><a href="/guides/{guide['slug']}.html">Lire le guide</a></p></article>''' for guide in GUIDES)
    content = page_head(title, description, url, schema) + shell("guides")
    content += f'''<main id="contenu"><header class="seo-hero"><div class="seo-container"><p class="seo-eyebrow">Comprendre avant de choisir</p><h1>Des repères clairs pour décider sereinement.</h1><p class="seo-lead">Chaque guide part d'une décision réelle d'indépendant, cite les sources officielles quand le sujet est réglementaire et distingue clairement ce que Diqto fait déjà.</p></div></header><div class="seo-container seo-main"><div class="seo-grid">{cards}</div>{priority_paths_section()}<section class="seo-cta"><h2>Vous préférez tester plutôt que lire&nbsp;?</h2><p>Prenez la tâche administrative qui vous attend aujourd'hui et regardez si Diqto vous évite une ressaisie.</p><div class="seo-actions"><a class="seo-button" href="/#beta">Créer mon premier brouillon gratuit</a><a class="seo-button secondary" href="/metiers.html">Trouver mon métier</a></div></section></div></main>'''
    content += footer() + "</body></html>"
    (ROOT / "guides.html").write_text(content, encoding="utf-8")


def main() -> None:
    generate_trades_hub()
    generate_guides_hub()
    for guide in GUIDES:
        generate_guide(guide)
    print(f"seo_hubs_generate: OK guides={len(GUIDES)} trades={sum(len(v) for v in load_trades().values())}")


if __name__ == "__main__":
    main()
