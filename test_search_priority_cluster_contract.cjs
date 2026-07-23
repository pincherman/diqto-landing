#!/usr/bin/env node

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = __dirname;
const read = (relative) => fs.readFileSync(
    path.join(root, relative),
    'utf8',
);

const informationPages = [
    'facturation-electronique.html',
    'guides/logiciel-devis-facture-artisan.html',
    'guides/logiciel-facturation-micro-entrepreneur.html',
    'guides/facturation-electronique-micro-entreprise.html',
    'guides/mentions-obligatoires-facture-micro-entrepreneur.html',
    'guides/devis-artisan-mentions-obligatoires.html',
];

const tradePages = [
    'plombier.html',
    'electricien.html',
    'peintre.html',
    'menuisier.html',
    'carreleur.html',
    'coach-sportif.html',
    'osteopathe.html',
    'photographe.html',
    'metiers/psychologue.html',
];

const priorityPages = [...informationPages, ...tradePages];
const sitemap = read('sitemap.xml');
const home = read('index.html');
const guides = read('guides.html');
const trades = read('metiers.html');

function canonicalPath(relative) {
    return `/${relative}`;
}

function incomingLinks(target) {
    return fs.readdirSync(root, { recursive: true })
        .filter((entry) => entry.endsWith('.html'))
        .filter((entry) => read(entry).includes(`href="${target}"`));
}

const titles = new Set();
const descriptions = new Set();

for (const relative of priorityPages) {
    const page = read(relative);
    const target = canonicalPath(relative);
    const title = page.match(/<title>([^<]+)<\/title>/)?.[1];
    const description = page.match(
        /<meta name="description" content="([^"]+)"/,
    )?.[1];

    assert.ok(title, `${relative}: missing title`);
    assert.ok(description, `${relative}: missing meta description`);
    assert.ok(!titles.has(title), `${relative}: duplicate title`);
    assert.ok(
        !descriptions.has(description),
        `${relative}: duplicate description`,
    );
    titles.add(title);
    descriptions.add(description);

    assert.match(
        page,
        /href="(?:\/|\.\.\/)\?source=[^"]+#beta"/,
        `${relative}: CTA source must reach consented intake`,
    );
    assert.ok(
        sitemap.includes(`<loc>https://diqto.fr${target}</loc>`),
        `${relative}: missing from sitemap`,
    );
    assert.doesNotMatch(
        page,
        /Diqto (?:est|sera) (?:conforme|une Plateforme Agréée)/i,
        `${relative}: unproven compliance claim`,
    );
}

for (const relative of informationPages) {
    assert.ok(
        guides.includes(`href="/${relative}"`),
        `${relative}: missing from guides hub`,
    );
}

for (const relative of tradePages) {
    assert.ok(
        trades.includes(`href="/${relative}"`),
        `${relative}: missing from priority trade navigation`,
    );
}

for (const relative of [
    'facturation-electronique.html',
    'guides/mentions-obligatoires-facture-micro-entrepreneur.html',
    'guides/devis-artisan-mentions-obligatoires.html',
    'metiers/psychologue.html',
]) {
    const count = incomingLinks(canonicalPath(relative)).length;
    assert.ok(count >= 2, `${relative}: only ${count} internal links`);
}

assert.ok(
    incomingLinks('/facturation-electronique.html').length >= 70,
    'canonical e-invoicing hub must be the cluster root',
);
assert.equal(
    (guides.match(/data-search-intent="guide-prioritaire"/g) || []).length,
    informationPages.length,
    'guides hub must expose all priority information intents',
);
assert.equal(
    (trades.match(/data-search-intent="metier-prioritaire"/g) || []).length,
    tradePages.length,
    'trades hub must expose all priority trade intents',
);
assert.ok(
    home.includes(
        'href="/guides/mentions-obligatoires-facture-micro-entrepreneur.html"',
    ),
    'home must expose the invoice checklist',
);
assert.ok(
    home.includes(
        'href="/guides/devis-artisan-mentions-obligatoires.html"',
    ),
    'home must expose the artisan quote checklist',
);
assert.match(
    guides,
    /"url": "https:\/\/diqto\.fr\/facturation-electronique\.html"/,
    'guide collection schema must include the canonical hub',
);
assert.match(
    home,
    /sourceInput\.value = source\.slice\(0, 120\)/,
    'home must preserve bounded source attribution',
);

console.log(
    'search_priority_cluster_contract: OK '
    + `priority=${priorityPages.length}`,
);
