#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const landingRoot = __dirname;
const forbiddenNumber = ['523', '4942'].join('');
const forbiddenClaim = ['Marque', 'déposée', 'INPI'].join(' ');

const landingFiles = fs.readdirSync(landingRoot)
  .filter((name) => name.endsWith('.html') || name.endsWith('.py'))
  .map((name) => path.join(landingRoot, name));

const publicSources = landingFiles;
const violations = [];

for (const file of publicSources) {
  const source = fs.readFileSync(file, 'utf8');
  if (source.includes(forbiddenNumber) || source.includes(forbiddenClaim)) {
    violations.push(path.relative(landingRoot, file));
  }
}

if (violations.length > 0) {
  throw new Error(`Statut INPI refusé encore présenté comme actif: ${violations.join(', ')}`);
}

console.log(`PASS INPI public claim consistency (${publicSources.length} sources)`);
