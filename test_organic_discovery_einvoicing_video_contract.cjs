#!/usr/bin/env node

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = __dirname;
const read = (relative) => fs.readFileSync(path.join(root, relative), 'utf8');
const storySlugs = [
    'marc-artisan',
    'claire-osteopathe',
    'sarah-avocate',
    'jean-luc-karate',
];

const hub = read('facturation-electronique.html');
for (const marker of [
    '1er septembre 2026',
    '1er septembre 2027',
    "Diqto n'est pas une Plateforme Agréée",
    "L'intégration Diqto est en cours de qualification",
    'Un PDF envoyé par email est-il une facture électronique ?',
    'https://www.impots.gouv.fr/facturation-electronique-et-plateformes-agreees',
]) {
    assert.ok(hub.includes(marker), `hub missing marker: ${marker}`);
}
assert.doesNotMatch(
    hub,
    /Diqto (?:est|sera) (?:conforme|une Plateforme Agréée)/i,
    'hub must not claim unproven compliance or PA status',
);
assert.match(hub, /"@type": "FAQPage"/);
assert.match(hub, /rel="canonical" href="https:\/\/diqto\.fr\/facturation-electronique\.html"/);

const robots = read('robots.txt');
assert.match(robots, /Sitemap: https:\/\/diqto\.fr\/video-sitemap\.xml/);

const videoSitemap = read('video-sitemap.xml');
assert.match(
    videoSitemap,
    /xmlns:video="http:\/\/www\.google\.com\/schemas\/sitemap-video\/1\.1"/,
);

for (const slug of storySlugs) {
    const relative = `histoires/${slug}.html`;
    const page = read(relative);
    assert.match(page, new RegExp(`https://diqto.fr/histoires/${slug}\\.html`));
    assert.match(page, /"@type": "VideoObject"/);
    assert.match(
        page,
        new RegExp(`https://diqto.fr/assets/stories/${slug}\\.mp4`),
    );
    assert.match(
        page,
        new RegExp(`https://diqto.fr/assets/stories/${slug}-poster\\.jpg`),
    );
    assert.match(page, new RegExp(`/assets/stories/${slug}-fr\\.vtt`));
    assert.match(page, /<video controls preload="metadata" playsinline/);
    assert.match(page, /Transcription de la vidéo/);
    assert.match(page, /Personnage et situation fictifs/);
    assert.doesNotMatch(page, /autoplay/);

    const captions = read(`assets/stories/${slug}-fr.vtt`);
    assert.ok(captions.startsWith('WEBVTT\n'));
    assert.doesNotMatch(captions, /\bDicto\b/);

    assert.match(
        videoSitemap,
        new RegExp(`<loc>https://diqto.fr/histoires/${slug}\\.html</loc>`),
    );
    assert.match(
        videoSitemap,
        new RegExp(
            `<video:content_loc>https://diqto.fr/assets/stories/${slug}\\.mp4</video:content_loc>`,
        ),
    );
}

assert.equal(
    (videoSitemap.match(/<video:video>/g) || []).length,
    storySlugs.length,
);
assert.equal(
    (videoSitemap.match(/<video:thumbnail_loc>/g) || []).length,
    storySlugs.length,
);

console.log('organic_discovery_einvoicing_video_contract: OK');
