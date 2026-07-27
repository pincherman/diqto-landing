#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const root = __dirname;
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');
const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

const home = read('index.html');
const hub = read('facturation-electronique.html');
const annex = read('facturation-electronique-conditions.html');
const cgu = read('cgu.html');
const privacy = read('confidentialite.html');
const markdownAnnex = read('legal/ANNEXE_FACTURATION_ELECTRONIQUE.md');

for (const [name, source] of [
  ['home', home],
  ['hub', hub],
  ['annex', annex],
  ['cgu', cgu],
]) {
  assert(/B2Brouter/.test(source), `${name} must name the production partner`);
  assert(
    !/Diqto (est|devient) (une )?(PA|Plateforme Agréée)/i.test(source),
    `${name} must never present Diqto as the accredited platform`,
  );
}

assert(
  home.includes('DIQTO rejoint le programme Startups de B2Brouter')
    && home.includes('rien ne part sans validation explicite'),
  'homepage must expose the partnership and human-control boundary',
);
assert(
  hub.includes('B2Brouter assure le transport réglementaire en tant que Plateforme Agréée')
    && hub.includes("Un brouillon est d'abord préparé sans envoi"),
  'SEO hub must explain the exact operator and no-send draft sequence',
);
assert(
  annex.includes("L'acceptation générale des CGU ne vaut ni activation, ni mandat")
    && annex.includes("Aucune facture n'est transmise automatiquement")
    && annex.includes('confirmation humaine explicite'),
  'public annex must require separate acceptance and human confirmation',
);
assert(
  markdownAnnex.includes('mandat de facturation')
    && markdownAnnex.includes('empreinte du texte accepté')
    && markdownAnnex.includes('révocation'),
  'canonical annex must cover mandate separation, evidence and reversibility',
);
assert(
  cgu.includes('/facturation-electronique-conditions.html')
    && privacy.includes('B2Brouter Global, S.L.')
    && privacy.includes('Factures électroniques, statuts et archives réglementaires'),
  'CGU and privacy policy must link the annex and disclose regulatory processing',
);

console.log('PASS B2Brouter production partnership contract');
