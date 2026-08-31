const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const root = __dirname;
const read = (relativePath) => fs.readFileSync(path.join(root, relativePath), 'utf8');

const campaigns = [
  {
    id: 'plombier',
    page: 'plombier.html',
    canonical: 'https://diqto.fr/plombier.html',
    media: 'assets/campaign/diqto-plombier-devis-paiement.mp4',
    poster: 'assets/campaign/diqto-plombier-devis-paiement-poster.jpg',
    captions: 'assets/campaign/diqto-plombier-devis-paiement-fr.vtt',
    sha256: '56a881f132c1f014a8573245a0008b8d132b548779f9077aca35f8edf6c4e16b',
  },
  {
    id: 'electricien',
    page: 'electricien.html',
    canonical: 'https://diqto.fr/electricien.html',
    media: 'assets/campaign/diqto-electricien-diagnostic-paiement.mp4',
    poster: 'assets/campaign/diqto-electricien-diagnostic-paiement-poster.jpg',
    captions: 'assets/campaign/diqto-electricien-diagnostic-paiement-fr.vtt',
    sha256: '117ebdaf79ab0c03b8dc2d5a5b136a309b5e0ab63634c8d31d7f33832c19e2aa',
  },
  {
    id: 'couvreur',
    page: 'metiers/couvreur.html',
    canonical: 'https://diqto.fr/metiers/couvreur.html',
    media: 'assets/campaign/diqto-couvreur-inspection-paiement.mp4',
    poster: 'assets/campaign/diqto-couvreur-inspection-paiement-poster.jpg',
    captions: 'assets/campaign/diqto-couvreur-inspection-paiement-fr.vtt',
    sha256: 'cfa86319c041210e21f04170337b1d54f32bc309bd35dd140c2f822857caf0c5',
  },
  {
    id: 'macon',
    page: 'metiers/macon.html',
    canonical: 'https://diqto.fr/metiers/macon.html',
    media: 'assets/campaign/diqto-macon-devis-paiement.mp4',
    poster: 'assets/campaign/diqto-macon-devis-paiement-poster.jpg',
    captions: 'assets/campaign/diqto-macon-devis-paiement-fr.vtt',
    sha256: 'c524916bf97b2f1557bb24818c9713abc008210dd027931e1eedd2d3598f3ead',
  },
];

test('each canonical métier page exposes one prominent, accessible campaign video', () => {
  for (const campaign of campaigns) {
    const html = read(campaign.page);
    const videoBlocks = html.match(new RegExp(`data-campaign-video="${campaign.id}"`, 'g')) || [];
    assert.equal(videoBlocks.length, 1, campaign.page);
    assert.match(html, /<meta name="robots" content="index,follow,max-image-preview:large,max-video-preview:-1">/);
    assert.ok(html.includes(`<source src="/${campaign.media}" type="video/mp4">`));
    assert.ok(html.includes(`<track kind="captions" src="/${campaign.captions}"`));
    assert.ok(html.includes(`poster="/${campaign.poster}"`));
    assert.match(html, /<details class="campaign-video-transcript">/);

    const match = html.match(/<script type="application\/ld\+json" data-schema="campaign-video">\s*([\s\S]*?)\s*<\/script>/);
    assert.ok(match, `missing VideoObject in ${campaign.page}`);
    const schema = JSON.parse(match[1]);
    assert.equal(schema['@type'], 'VideoObject');
    assert.equal(schema.url, campaign.canonical);
    assert.equal(schema.mainEntityOfPage, campaign.canonical);
    assert.equal(schema.contentUrl, `https://diqto.fr/${campaign.media}`);
    assert.equal(schema.thumbnailUrl[0], `https://diqto.fr/${campaign.poster}`);
    assert.equal(schema.duration, 'PT40S');
    assert.ok(schema.transcript.length > 500);
  }
});

test('published assets are exact masters with stable posters and French captions', () => {
  for (const campaign of campaigns) {
    const media = fs.readFileSync(path.join(root, campaign.media));
    assert.equal(crypto.createHash('sha256').update(media).digest('hex'), campaign.sha256);
    assert.ok(fs.statSync(path.join(root, campaign.poster)).size > 20_000);
    const captions = read(campaign.captions);
    assert.ok(captions.startsWith('WEBVTT\n\n'));
    assert.equal((captions.match(/ --> /g) || []).length, 10);
  }
});

test('video sitemap contains the five stories and four canonical campaign pages', () => {
  const sitemap = read('video-sitemap.xml');
  assert.equal((sitemap.match(/<video:video>/g) || []).length, 9);
  for (const campaign of campaigns) {
    assert.ok(sitemap.includes(`<loc>${campaign.canonical}</loc>`));
    assert.ok(sitemap.includes(`<video:content_loc>https://diqto.fr/${campaign.media}</video:content_loc>`));
  }
});

test('canonical consolidation and internal links do not create competing métier URLs', () => {
  const yogaAlias = read('metiers/prof_yoga.html');
  assert.ok(yogaAlias.includes('<link rel="canonical" href="https://diqto.fr/professeur-yoga.html">'));

  const sitemap = read('sitemap.xml');
  assert.ok(sitemap.includes('<loc>https://diqto.fr/professeur-yoga.html</loc>'));
  assert.ok(!sitemap.includes('<loc>https://diqto.fr/metiers/prof_yoga.html</loc>'));

  const trades = read('metiers.html');
  assert.equal((trades.match(/href="\/kinesitherapeute\.html"/g) || []).length, 1);
  assert.ok(trades.includes('href="/metiers/couvreur.html"'));
  assert.ok(trades.includes('href="/metiers/macon.html"'));
});

test('brand identity and truthful lastmod values are aligned with the campaign', () => {
  const home = read('index.html');
  assert.ok(home.includes('https://www.tiktok.com/@diqto.fr'));
  assert.ok(!home.includes('@philippeincherma5'));

  const sitemap = read('sitemap.xml');
  for (const campaign of campaigns) {
    const entry = `<loc>${campaign.canonical}</loc>\n    <lastmod>2026-08-31</lastmod>`;
    assert.ok(sitemap.includes(entry), campaign.page);
  }
  assert.ok(sitemap.includes('<loc>https://diqto.fr/mentions-legales.html</loc>\n    <lastmod>2026-08-20</lastmod>'));
});
