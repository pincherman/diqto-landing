const assert = require('node:assert/strict');
const childProcess = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');

const root = __dirname;
const appStoreUrl = 'https://apps.apple.com/fr/app/diqto/id6761616034';
const trackedHtml = childProcess
    .execFileSync('git', ['ls-files', '*.html'], {
        cwd: root,
        encoding: 'utf8',
    })
    .trim()
    .split('\n')
    .filter(Boolean)
    .filter((relativePath) => !relativePath.startsWith('prototypes/'));

assert.ok(trackedHtml.length >= 100, 'public HTML corpus unexpectedly shrank');

let globalCtaPageCount = 0;
for (const relativePath of trackedHtml) {
    const html = fs.readFileSync(path.join(root, relativePath), 'utf8');
    assert.doesNotMatch(
        html,
        /#beta|Demander mon accès|Commencer gratuit|TestFlight|expo\.dev/i,
        `${relativePath} exposes a stale pre-launch path`,
    );
    assert.doesNotMatch(
        html,
        /https:\/\/apps\.apple\.com\/[^"']*\/id(?!6761616034)\d+/i,
        `${relativePath} points to another App Store id`,
    );

    const globalCtas = html.match(/<a\b[^>]*class="[^"]*global-cta[^"]*"[^>]*>/g) || [];
    if (!globalCtas.length) continue;
    globalCtaPageCount += 1;
    for (const cta of globalCtas) {
        assert.match(
            cta,
            new RegExp(`href="${appStoreUrl}"`),
            `${relativePath} global CTA must open the official App Store page`,
        );
    }
}

assert.ok(globalCtaPageCount >= 100, 'App Store CTA coverage unexpectedly shrank');

const home = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const shell = fs.readFileSync(path.join(root, 'site-shell.js'), 'utf8');
const releaseConfig = fs.readFileSync(
    path.join(root, 'release_config.py'),
    'utf8',
);

for (const marker of [
    'Diqto 1.0 est disponible',
    'Disponible maintenant sur l’App Store France',
    `"downloadUrl": "${appStoreUrl}"`,
    '"softwareVersion": "1.0"',
    '"datePublished": "2026-08-20"',
    'https://schema.org/InStock',
]) {
    assert.ok(home.includes(marker), `home launch marker missing: ${marker}`);
}

assert.ok(shell.includes(appStoreUrl), 'site shell must own the launch banner URL');
assert.ok(releaseConfig.includes('APP_STORE_ID = "6761616034"'));
assert.ok(releaseConfig.includes('APP_VERSION = "1.0"'));
assert.ok(releaseConfig.includes('IOS_MINIMUM_VERSION = "15.1"'));
assert.ok(releaseConfig.includes('PUBLIC_RELEASE_DATE = "2026-08-20"'));

console.log(
    `public_appstore_launch_contract: OK html=${trackedHtml.length} cta_pages=${globalCtaPageCount}`,
);
