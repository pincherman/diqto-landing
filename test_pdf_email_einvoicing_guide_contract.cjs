#!/usr/bin/env node

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = __dirname;
const read = (relative) => fs.readFileSync(path.join(root, relative), 'utf8');
const relative = 'guides/pdf-email-facture-electronique.html';
const page = read(relative);
const guides = read('guides.html');
const hub = read('facturation-electronique.html');
const sitemap = read('sitemap.xml');
const schemas = [...page.matchAll(
    /<script type="application\/ld\+json">([\s\S]*?)<\/script>/g,
)].map((match) => JSON.parse(match[1]));

for (const marker of [
    '<h1>Un PDF par email n\'est pas la facture électronique de la réforme.</h1>',
    'Un PDF ordinaire envoyé par email ne suffit pas',
    'UBL, CII ou un format mixte',
    'Factur-X',
    'plateforme agréée',
    'Diqto n\'est pas présenté comme une plateforme agréée',
    'https://www.impots.gouv.fr/professionnel/je-decouvre-la-facturation-electronique',
    'https://www.impots.gouv.fr/facturation-electronique-et-plateformes-agreees',
    'https://www.economie.gouv.fr/tout-savoir-sur-la-facturation-electronique-pour-les-entreprises',
    'source=seo_guide_pdf_email_facture_electronique',
    '"@type": "Article"',
    '"@type": "FAQPage"',
]) {
    assert.ok(page.includes(marker), `${relative}: missing ${marker}`);
}

assert.match(
    page,
    /rel="canonical" href="https:\/\/diqto\.fr\/guides\/pdf-email-facture-electronique\.html"/,
);
assert.equal(schemas.length, 1, 'the guide must expose one valid JSON-LD graph');
assert.ok(
    schemas[0]['@graph'].some((entry) => entry['@type'] === 'Article'),
    'the JSON-LD graph must expose the article',
);
assert.ok(
    schemas[0]['@graph'].some((entry) => entry['@type'] === 'FAQPage'),
    'the JSON-LD graph must expose the visible FAQ',
);
assert.doesNotMatch(
    page,
    /Diqto (?:est|sera) (?:conforme|une Plateforme Agréée)/i,
    'the guide must not claim unproven compliance or PA status',
);
assert.ok(
    guides.includes('href="/guides/pdf-email-facture-electronique.html"'),
    'guides hub must link the new guide',
);
assert.ok(
    hub.includes('href="/guides/pdf-email-facture-electronique.html"'),
    'e-invoicing hub must link the new guide',
);
assert.ok(
    hub.includes('"dateModified": "2026-09-02"'),
    'the changed e-invoicing hub must expose its fresh modification date',
);
assert.ok(
    sitemap.includes('<loc>https://diqto.fr/guides/pdf-email-facture-electronique.html</loc>'),
    'sitemap must include the new guide',
);

console.log('pdf_email_einvoicing_guide_contract: OK');
