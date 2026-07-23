#!/usr/bin/env node

const assert = require('assert');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const root = __dirname;
const guideHref = '/facturation-electronique.html';
const read = (relative) => fs.readFileSync(path.join(root, relative), 'utf8');

function pngMetadata(relative) {
  const data = fs.readFileSync(path.join(root, relative));
  assert.strictEqual(
    data.subarray(1, 4).toString('ascii'),
    'PNG',
    `${relative}: PNG signature missing`,
  );
  return {
    width: data.readUInt32BE(16),
    height: data.readUInt32BE(20),
    sha256: crypto.createHash('sha256').update(data).digest('hex'),
  };
}

const favicon = pngMetadata('favicon.png');
assert.deepStrictEqual(
  [favicon.width, favicon.height],
  [64, 64],
  'favicon must be a square 64 px brand asset',
);
assert.strictEqual(
  favicon.sha256,
  '720716bd64c04ee5f59f6002b322f22d6fdb58b4b28609fe850aaa0542746aaf',
  'favicon must match the canonical Diqto voice-mark export',
);

const appleTouchIcon = pngMetadata('apple-touch-icon.png');
assert.deepStrictEqual(
  [appleTouchIcon.width, appleTouchIcon.height],
  [180, 180],
  'apple touch icon must be 180 px',
);
assert.strictEqual(
  appleTouchIcon.sha256,
  '0bcbc43b9a5c226286754e798ac24a046b16e8dd28bf47c5a05f9f601a186ff1',
  'apple touch icon must match the canonical Diqto voice-mark export',
);

const home = read('index.html');
assert(
  home.includes(
    'rel="icon" type="image/svg+xml" sizes="any" href="/favicon-diqto-voice.svg"',
  ),
  'home must declare the stable versioned voice-mark favicon URL',
);
assert(
  !home.includes('rel="icon" type="image/png" sizes="64x64" href="/favicon.png"'),
  'home must not keep the legacy cached favicon URL as its canonical icon',
);

const voiceFavicon = read('favicon-diqto-voice.svg');
assert(
  voiceFavicon.includes('viewBox="0 0 64 64"'),
  'versioned favicon must expose a square 64 px viewBox',
);
assert(
  voiceFavicon.includes('fill="#25d366"'),
  'versioned favicon must use the canonical Diqto green',
);
assert.strictEqual(
  (voiceFavicon.match(/<rect /g) || []).length,
  5,
  'versioned favicon must expose the five-bar Diqto voice mark',
);
assert(
  home.includes(`class="global-announcement" href="${guideHref}"`),
  'home must expose a crawlable e-invoicing announcement',
);
assert(
  home.includes('<strong>Facturation électronique</strong>'),
  'home must name the e-invoicing topic explicitly',
);
assert(!home.includes('Réforme 2026–2027'), 'home must not hide the topic behind a vague label');

const guides = read('guides.html');
assert(
  guides.includes('Des repères clairs pour décider sereinement.'),
  'guide hub must use positive, reader-first microcopy',
);
assert(!guides.includes('remplissage SEO'), 'guide hub must not talk about SEO to readers');
assert(
  guides.includes(`class="global-announcement" href="${guideHref}"`),
  'guide hub must expose the static e-invoicing announcement',
);

const shell = read('site-shell.js');
assert(
  shell.includes(`announcement.href = '${guideHref}'`),
  'shared shell must add the announcement to legacy public pages',
);
assert(
  shell.includes("document.querySelector('.global-announcement')"),
  'shared shell must avoid duplicate announcements',
);

const guide = read('facturation-electronique.html');
for (const marker of [
  "Diqto n'est pas une Plateforme Agréée",
  "L'intégration Diqto est en cours de qualification",
  'Un PDF envoyé par email est-il une facture électronique ?',
]) {
  assert(guide.includes(marker), `e-invoicing guide missing safety marker: ${marker}`);
}
assert(!/Diqto (?:est|sera) conforme/i.test(guide), 'guide must not claim Diqto compliance');

console.log(
  'search_discovery_polish_contract: OK favicon=versioned-voice announcement=global guide=no-claim',
);
