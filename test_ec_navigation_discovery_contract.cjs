#!/usr/bin/env node

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = __dirname;
const read = (relative) => fs.readFileSync(
  path.join(root, relative),
  'utf8',
);

const homepage = read('index.html');
const accountantPage = read('experts-comptables.html');
const shell = read('site-shell.js');
const shellStyles = read('site-shell.css');
const sitemap = read('sitemap.xml');

assert.match(
  homepage,
  /<a href="\/experts-comptables\.html">Experts-comptables<\/a>/,
  'homepage navigation must expose the accountant page without JavaScript',
);
assert.match(
  accountantPage,
  /<a href="\/experts-comptables\.html" aria-current="page">/,
  'accountant page must identify its active navigation item',
);
assert.match(
  sitemap,
  /<loc>https:\/\/diqto\.fr\/experts-comptables\.html<\/loc>/,
  'accountant page must stay in the canonical sitemap',
);
assert.match(shell, /function ensureAccountantLink\(\)/);
assert.match(shell, /accountantLink\.textContent = 'Experts-comptables'/);
assert.match(shell, /if \(existingLink\) return;/);
assert.match(
  shell,
  /pricingLink\.insertAdjacentElement\('beforebegin', accountantLink\)/,
  'shared shell must add the shortcut before pricing on legacy pages',
);
assert.match(
  shellStyles,
  /@media \(max-width: 1080px\)/,
  'global menu must switch before the added item can overflow',
);

for (const generator of [
  'regen_all_metiers.py',
  'regen_metier_pages.py',
  'generate_seo_hubs.py',
  'generate_story_video_discovery.py',
]) {
  assert.ok(
    read(generator).includes('/experts-comptables.html'),
    `${generator} must preserve the accountant shortcut`,
  );
}

const publicHtml = [];
function collectHtml(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    if ([
      '.git',
      'node_modules',
      'playwright-report',
      'test-results',
      'tmp',
    ].includes(entry.name)) continue;
    const absolute = path.join(directory, entry.name);
    if (entry.isDirectory()) collectHtml(absolute);
    if (entry.isFile() && entry.name.endsWith('.html')) {
      publicHtml.push(absolute);
    }
  }
}
collectHtml(root);

const pagesWithGlobalMenu = publicHtml.filter((absolute) => (
  fs.readFileSync(absolute, 'utf8').includes(
    '<nav class="global-menu"',
  )
));
assert.ok(pagesWithGlobalMenu.length >= 90);
for (const absolute of pagesWithGlobalMenu) {
  const page = fs.readFileSync(absolute, 'utf8');
  assert.ok(
    page.includes('site-shell.js'),
    `${path.relative(root, absolute)} must load the shared navigation shell`,
  );
}

console.log(
  `PASS EC discovery: static homepage link, shared navigation on `
  + `${pagesWithGlobalMenu.length} pages, sitemap and generators aligned`,
);
