#!/usr/bin/env node

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = __dirname;
const read = (relative) => fs.readFileSync(path.join(root, relative), 'utf8');

const home = read('index.html');
const report = read(
    'reportage-premier-client-facturation-electronique.html',
);
const shell = read('site-shell.css');

for (const marker of [
    '--paper: #0c0c0c',
    '--card: #151a15',
    '--green: #25d366',
    'font-family: "Work Sans", sans-serif',
    'background: var(--card)',
    'outline: 3px solid var(--green)',
]) {
    assert.ok(
        report.includes(marker),
        `report missing Diqto brand marker: ${marker}`,
    );
}

for (const forbidden of [
    'Fraunces',
    'DM Mono',
    '--paper: #f5f0e5',
    '--orange:',
    '--yellow:',
]) {
    assert.ok(
        !report.includes(forbidden),
        `report must not recreate a parallel visual identity: ${forbidden}`,
    );
}

assert.ok(
    home.includes('--paper-light: #0c0c0c')
        && home.includes('--green: #25d366')
        && shell.includes('--site-shell-green: #25d366'),
    'homepage and shared shell must expose the canonical dark/green identity',
);

assert.ok(
    report.includes('<link rel="stylesheet" href="/site-shell.css">')
        && report.includes('<header class="global-header"')
        && report.includes('<a class="global-cta" href="/#beta">'),
    'report must retain the shared Diqto navigation and CTA',
);

console.log('PASS e-invoicing report brand consistency contract');
