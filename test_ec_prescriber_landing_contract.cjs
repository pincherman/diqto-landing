#!/usr/bin/env node

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = __dirname;
const read = (relative) => fs.readFileSync(
    path.join(root, relative),
    'utf8',
);

const page = read('experts-comptables.html');
const styles = read('experts-comptables.css');
const script = read('experts-comptables.js');
const home = read('index.html');
const legacyEcPage = read('metiers/expert_comptable.html');
const kineAlias = read('metiers/kine.html');

for (const marker of [
    'Vos clients parlent métier.',
    'Diqto prépare l’information.',
    'Évaluer un client sur un cycle',
    'Voir la démo de l’espace EC',
    'Voir ce qui est déjà prouvé',
    '0 € pour le cabinet',
    'Aucun frais de siège ni abonnement cabinet',
    'Diqto Essential',
    '9 € TTC / mois',
    'Diqto Vocal Pro',
    '19 € TTC / mois',
    'Compatibilité vérifiée d’abord',
    'Simulation produit · 32 secondes',
    'Aucune connexion réelle à un cabinet n’est montrée',
    'Recenser et qualifier vos outils',
    'Un client, un cycle, quatre mesures',
    'Le cycle de facturation électronique a été testé en recette',
    'Leur usage dans l’organisation d’un cabinet reste à valider',
    'Aucune donnée réelle n’est ouverte dans la démonstration publique',
    'L’humain valide ce qui engage',
    'Un chemin vérifiable, pas un connecteur promis',
    'Ce qui est prouvé, ce qui reste à prouver',
    'Vérification du 25 juillet 2026',
    'À démontrer avec le premier cabinet',
    'Votre logiciel, votre GED et votre PA restent en place',
    'Nous qualifions le chemin avant tout pilote',
    'Vérifier la compatibilité d’un cas client',
]) {
    assert.ok(page.includes(marker), `EC prescriber page missing: ${marker}`);
}

for (const marker of [
    '<a href="/">Accueil</a>',
    '<a href="/fonctionnalites.html">Fonctionnalités</a>',
    '<a href="/histoires.html">Histoires</a>',
    '<a href="/metiers.html">Métiers</a>',
    '<a href="/guides.html">Guides</a>',
    '<a href="/experts-comptables.html" aria-current="page">',
    '<a href="/#tarifs">Tarifs</a>',
    '<a class="global-cta" href="https://apps.apple.com/fr/app/diqto/id6761616034" data-growth-placement="header">Télécharger l’app</a>',
]) {
    assert.ok(page.includes(marker), `canonical menu missing: ${marker}`);
}

assert.match(
    page,
    /global-announcement" href="https:\/\/apps\.apple\.com\/fr\/app\/diqto\/id6761616034"/,
);
assert.match(
    page,
    /<link rel="canonical" href="https:\/\/diqto\.fr\/experts-comptables\.html">/,
);
assert.match(page, /"@type": "ProfessionalAudience"/);
assert.match(page, /"@type": "FAQPage"/);
assert.match(page, /class="ec-freedom-film"/);
assert.match(page, /<video[\s\S]+muted[\s\S]+controls[\s\S]+preload="none"/);
assert.doesNotMatch(page, /<video[^>]+(?:autoplay|loop)/);
assert.match(page, /diqto-cabinet-cinematique-v9\.mp4/);
assert.match(page, /diqto-cabinet-cinematique-v9-fr\.vtt/);
assert.match(
    page,
    /href="\/histoires\/cabinet-expert-comptable\.html"[^>]*>[\s\S]*?Voir le film et sa transcription/,
);

assert.match(page, /<form id="ec-prescriber-intake" data-growth-form novalidate>/);
assert.match(page, /name="email"[\s\S]+required/);
assert.match(page, /name="tools"[\s\S]+required/);
assert.match(page, /name="client_problem"[\s\S]+required/);
assert.match(page, /name="partnership_offer" type="hidden" value=""/);
assert.doesNotMatch(page, /name="partnership_offer"[^>]+required/);
assert.match(page, /data-offer-choice="free_accountant_access"/);
assert.match(page, /data-offer-choice="one_client_pilot"/);
assert.match(
    page,
    /href="https:\/\/necessary-danila-diqto-7fbe88c8\.koyeb\.app\/ec\/v1"/,
);
assert.match(page, /name="source"[\s\S]+value="ec_prescripteur_pilot"/);
assert.match(page, /name="contact_consent"[\s\S]+required/);
assert.match(page, /name="website"[\s\S]+tabindex="-1"/);
assert.match(page, /role="status"[\s\S]+aria-live="polite"/);
assert.match(page, /Ne renseignez aucun nom ni donnée personnelle/);

assert.match(script, /\/api\/public\/starter-intake/);
assert.match(script, /contact_consent:[\s\S]+=== 'on'/);
assert.match(script, /first_need: buildFirstNeed\(data\)/);
assert.match(
    script,
    /source: String\(data\.get\('source'\) \|\| ''\)\.slice\(0, 120\)/,
);
assert.match(script, /Modèle envisagé/);
assert.match(script, /à qualifier après compatibilité/);
assert.match(script, /free_accountant_access: 'accès cabinet gratuit'/);
assert.match(script, /one_client_pilot: 'pilote sur un client volontaire'/);
assert.match(script, /data-offer-choice/);
assert.match(script, /result\.confirmation_email_sent/);
assert.doesNotMatch(script, /console\.(?:log|info|debug)\(/);

assert.match(
    home,
    /<title>Diqto — Devis et factures par la voix pour indépendants<\/title>/,
);
assert.match(home, /class="ec-entry-section"/);
assert.match(home, /Aidez un client de terrain à mieux alimenter vos outils/);
assert.match(home, /Vous évitez de tout ressaisir/);
assert.match(home, /"@type": "UnitPriceSpecification"/);

assert.ok(
    (page.match(/B2Brouter/g) || []).length <= 3,
    'PA partner must be explicit without becoming the main message',
);
for (const forbidden of [
    /Vos outils\. Vos PA\. Votre IA/i,
    /Diqto les fait travailler ensemble/i,
    /Connecter ses plateformes/i,
    /Cabinet Ambassadeur/i,
    /contre 5 clients actifs/i,
    /99\s*(?:€|EUR)/i,
    /notre PA\b/i,
    /gagnez \d+ ?%|économisez \d+|ROI garanti/i,
    /Diqto est une Plateforme Agréée|Diqto remplace votre PA/i,
    /connexion (?:déjà )?active avec (?:Claude|ChatGPT|Codex)/i,
]) {
    assert.doesNotMatch(page, forbidden, `forbidden EC claim found: ${forbidden}`);
}

for (const marker of [
    ':focus-visible',
    '@media (max-width: 980px)',
    '@media (max-width: 768px)',
    '@media (max-width: 680px)',
    '@media (max-width: 480px)',
    '@media (prefers-reduced-motion: reduce)',
]) {
    assert.ok(styles.includes(marker), `EC styles missing: ${marker}`);
}
assert.match(
    styles,
    /@media \(max-width: 980px\)[\s\S]*?\.ec-hero-copy\s*\{\s*grid-row: 1;[\s\S]*?\.ec-freedom-film\s*\{\s*grid-row: 2;/,
);

assert.ok(
    legacyEcPage.includes('/experts-comptables.html'),
    'legacy EC métier page must link to the prescriber page',
);
assert.match(
    kineAlias,
    /rel="canonical" href="https:\/\/diqto\.fr\/kinesitherapeute\.html"/,
);

console.log(
    'PASS EC prescriber landing: client problem first, bounded claims, '
    + 'fast media and compatibility-first intake',
);
