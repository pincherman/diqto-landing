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
    'Votre client le plus difficile n’a pas besoin d’un',
    'Le dernier kilomètre, enfin structuré.',
    'Votre PA reste en place',
    'Aucun cockpit cabinet obligatoire',
    'Tester avec 1 client',
    'Un cycle suffit pour savoir',
    'Minutes cabinet',
    'Doubles dépôts',
    'Objets acceptés sans ressaisie',
]) {
    assert.ok(page.includes(marker), `EC prescriber page missing: ${marker}`);
}

assert.match(
    page,
    /<link rel="canonical" href="https:\/\/diqto\.fr\/experts-comptables\.html">/,
);
assert.match(page, /"@type": "ProfessionalAudience"/);
assert.match(page, /"@type": "FAQPage"/);

assert.match(page, /<form id="ec-prescriber-intake" novalidate>/);
assert.match(page, /name="email"[\s\S]+required/);
assert.match(page, /name="stack"[\s\S]+required/);
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
assert.doesNotMatch(script, /console\.(?:log|info|debug)\(/);

assert.ok(
    (page.match(/B2Brouter/g) || []).length <= 1,
    'provider plumbing must remain secondary',
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
    'PASS EC prescriber landing: problem measurable, stack retained, '
    + 'accessible pilot intake',
);
