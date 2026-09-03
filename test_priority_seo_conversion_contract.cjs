const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');

const root = __dirname;
const appStore = 'https://apps.apple.com/fr/app/diqto/id6761616034';
const priorityPages = [
  {
    file: 'guides/logiciel-devis-facture-artisan.html',
    canonical: 'https://diqto.fr/guides/logiciel-devis-facture-artisan.html',
    title: 'Logiciel devis facture artisan sur iPhone',
    h1: "Un logiciel de devis et factures pour artisan, pensé pour l'iPhone",
    intent: ['Décrivez le chantier', 'Contrôlez le brouillon', "Finalisez quand c'est prêt"],
  },
  {
    file: 'guides/logiciel-facturation-micro-entrepreneur.html',
    canonical: 'https://diqto.fr/guides/logiciel-facturation-micro-entrepreneur.html',
    title: 'Logiciel facturation auto-entrepreneur et micro-entreprise',
    h1: 'Un logiciel de facturation pour auto-entrepreneur, sans usine à gaz',
    intent: ['Parlez ou écrivez', 'Relisez chaque champ', 'Retrouvez le client'],
  },
];

for (const page of priorityPages) {
  const html = fs.readFileSync(path.join(root, page.file), 'utf8');
  assert(html.includes(`<title>${page.title} — Diqto</title>`), `${page.file} title`);
  assert(html.includes(`<h1>${page.h1}</h1>`), `${page.file} h1`);
  assert(html.includes(`<link rel="canonical" href="${page.canonical}">`), `${page.file} canonical`);
  assert(html.includes('"dateModified": "2026-09-03"'), `${page.file} modified date`);
  assert(html.includes('data-growth-page="guides"'), `${page.file} guide analytics bucket`);
  assert(html.includes('data-growth-source="direct_or_organic"'), `${page.file} closed source`);
  assert(html.includes('../growth.js'), `${page.file} growth script`);
  assert(html.includes(`href="${appStore}" data-growth-placement="hero"`), `${page.file} hero CTA`);
  assert(html.includes(`href="${appStore}" data-growth-placement="final_cta"`), `${page.file} final CTA`);
  assert(html.includes('Free à 0&nbsp;€') || html.includes('<strong>Plan Free :</strong>'), `${page.file} free price`);
  assert(html.includes('9&nbsp;€ TTC par mois'), `${page.file} essential price`);
  assert(html.includes('19&nbsp;€ TTC par mois'), `${page.file} vocal pro price`);
  assert(html.includes("Le prix local affiché par Apple"), `${page.file} local price truth`);
  assert(html.includes("Aucun envoi n'est automatique") || html.includes('Rien ne part à la seule dictée'), `${page.file} human control`);
  for (const marker of page.intent) {
    assert(html.includes(marker), `${page.file} missing ${marker}`);
  }
}

const generatedGuides = [
  'logiciel-devis-facture-artisan.html',
  'logiciel-facturation-micro-entrepreneur.html',
  'facturation-electronique-micro-entreprise.html',
  'mentions-obligatoires-facture-micro-entrepreneur.html',
  'devis-artisan-mentions-obligatoires.html',
];
for (const name of generatedGuides) {
  const html = fs.readFileSync(path.join(root, 'guides', name), 'utf8');
  assert(html.includes('data-growth-page="guides"'), `${name} guide analytics bucket`);
  assert(html.includes('../growth.js'), `${name} growth script`);
  assert(html.includes('data-growth-placement="announcement"'), `${name} announcement CTA`);
  assert(html.includes('data-growth-placement="header"'), `${name} header CTA`);
  assert(html.includes('data-growth-placement="final_cta"'), `${name} final CTA`);
}

console.log('PASS priority SEO conversion contract');
