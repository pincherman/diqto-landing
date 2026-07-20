#!/usr/bin/env node

const assert = require('assert');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const root = __dirname;
const guideHref = '/guides/facturation-electronique-micro-entreprise.html';
const read = (relative) => fs.readFileSync(path.join(root, relative), 'utf8');
const publicExtensions = new Set(['.html', '.js', '.md', '.py']);

function walkPublicFiles(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === '.git' || entry.name === 'assets') return [];
      return walkPublicFiles(fullPath);
    }
    return publicExtensions.has(path.extname(entry.name)) ? [fullPath] : [];
  });
}

const forbiddenEInvoicingClaims = [
  /Envoyer maintenant/i,
  /Envoi demand[ée]/i,
  /Envoyer depuis Diqto/i,
  /transmission r[ée]glementaire est op[ée]r[ée]e/i,
  /Diqto (?:est|sera|devient) (?:une )?plateforme agr[ée][ée]e/i,
  /Diqto (?:transmet|envoie) (?:vos )?(?:factures|donn[ée]es) (?:fiscales? )?(?:aux imp[ôo]ts|[àa] l'administration)/i,
];

const claimViolations = [];
for (const file of walkPublicFiles(root)) {
  const content = fs.readFileSync(file, 'utf8');
  for (const claim of forbiddenEInvoicingClaims) {
    if (claim.test(content)) {
      claimViolations.push(`${path.relative(root, file)} matches ${claim}`);
    }
  }
}
assert.deepStrictEqual(
  claimViolations,
  [],
  `public landing must not imply active e-invoicing send/PA role:\n${claimViolations.join('\n')}`,
);

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
  home.includes('rel="icon" type="image/png" sizes="64x64" href="/favicon.png"'),
  'home must declare the stable 64 px favicon URL',
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

const guide = read('guides/facturation-electronique-micro-entreprise.html');
for (const marker of [
  'Diqto ne se présente pas comme une plateforme agréée',
  'confirmation humaine avant envoi',
  "un email ou un PDF Diqto ne doit pas être présenté comme une transmission réglementaire",
]) {
  assert(guide.includes(marker), `e-invoicing guide missing safety marker: ${marker}`);
}
assert(!/Diqto (?:est|sera) conforme/i.test(guide), 'guide must not claim Diqto compliance');

console.log('search_discovery_polish_contract: OK favicon=64 announcement=global guide=no-claim');
