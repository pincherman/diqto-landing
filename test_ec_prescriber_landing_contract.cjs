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
const legacyEcPage = read('metiers/expert_comptable.html');

for (const marker of [
    'Quand le métier se vit sur le terrain',
    'Vos outils font leur travail.',
    'Une PA partenaire si nécessaire',
    'La PA partenaire de Diqto',
    'B2Brouter, sa Plateforme Agréée',
    'Ce qui est prouvé, ce qui reste à prouver',
    'Preuves disponibles aujourd’hui',
    'Vérification du 25 juillet 2026',
    'Les six notifications associées à ce',
    'À démontrer avec le premier cabinet',
    'Le temps réellement économisé',
    'Tester avec 1 client',
    'Une première preuve, à petite échelle',
]) {
    assert.ok(page.includes(marker), `EC prescriber page missing: ${marker}`);
}

const canonicalMenuMarkers = [
    '<a href="/">Accueil</a>',
    '<a href="/fonctionnalites.html">Fonctionnalités</a>',
    '<a href="/histoires.html">Histoires</a>',
    '<a href="/metiers.html">Métiers</a>',
    '<a href="/guides.html">Guides</a>',
    '<a href="/experts-comptables.html" aria-current="page">',
    '<a href="/#tarifs">Tarifs</a>',
    '<a class="global-cta" href="/#beta">Commencer gratuit</a>',
];
for (const marker of canonicalMenuMarkers) {
    assert.ok(page.includes(marker), `canonical menu missing: ${marker}`);
}
assert.match(
    page,
    /global-announcement" href="\/facturation-electronique\.html"/,
);

assert.match(
    page,
    /<link rel="canonical" href="https:\/\/diqto\.fr\/experts-comptables\.html">/,
);
assert.match(page, /"@type": "ProfessionalAudience"/);
assert.match(page, /"@type": "FAQPage"/);

assert.match(page, /<form id="ec-prescriber-intake" novalidate>/);
assert.match(page, /name="email"[\s\S]+required/);
assert.match(page, /name="tools"[\s\S]+required/);
assert.match(page, /name="client_problem"[\s\S]+required/);
assert.match(
    page,
    /name="source"[\s\S]+value="ec_prescripteur_pilot"/,
);
assert.match(page, /name="contact_consent"[\s\S]+required/);
assert.match(page, /name="website"[\s\S]+tabindex="-1"/);
assert.match(page, /role="status"[\s\S]+aria-live="polite"/);
assert.match(page, /Ne renseignez aucun nom ni donnée personnelle/);

assert.match(
    script,
    /\/api\/public\/starter-intake/,
);
assert.match(script, /contact_consent:[\s\S]+=== 'on'/);
assert.match(script, /first_need: buildFirstNeed\(data\)/);
assert.match(script, /source: data\.get\('source'\)/);
assert.match(script, /Outils du cabinet/);
assert.match(script, /result\.confirmation_email_sent/);
assert.match(script, /Un email de confirmation vient de vous/);
assert.match(script, /mais votre demande est bien enregistrée/);
assert.doesNotMatch(script, /console\.(?:log|info|debug)\(/);

assert.ok(
    (page.match(/B2Brouter/g) || []).length <= 3,
    'PA partner must be explicit without becoming the main message',
);
assert.doesNotMatch(
    page,
    /gagnez \d+ ?%|économisez \d+|ROI garanti|migration offerte/i,
    'page must not invent a gain or migration promise',
);
assert.doesNotMatch(
    page,
    /Diqto est une Plateforme Agréée|Diqto remplace votre PA/i,
    'page must not make a PA claim',
);
assert.doesNotMatch(
    page,
    /\bstack\b|\bcockpit\b|\brail\b|\bbaseline\b|\bobjets\b/i,
    'page must speak the language of an accountant, not internal jargon',
);

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

assert.ok(
    legacyEcPage.includes('/experts-comptables.html'),
    'legacy EC métier page must link to the prescriber page',
);

console.log(
    'PASS EC prescriber landing: refined accountant language, two PA paths, '
    + 'honest proof and accessible pilot intake',
);
