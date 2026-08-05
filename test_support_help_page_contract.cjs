const fs = require('fs');
const path = require('path');

const root = __dirname;
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');
const help = read('aide.html');
const home = read('index.html');
const docs = read('docs.html');
const sitemap = read('sitemap.xml');

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

for (const marker of [
  '<html lang="fr">',
  'href="#contenu"',
  'id="contenu"',
  '"@type": "FAQPage"',
  'Profil → Abonnement',
  'Restaurer mes achats',
  '9 € TTC/mois en France',
  '19 € TTC/mois en France',
  'https://support.apple.com/fr-fr/108096',
  'https://support.apple.com/fr-fr/118428',
  'https://support.apple.com/fr-fr/118223',
  'https://reportaproblem.apple.com/',
  'Ce que le support ne vous demandera jamais',
  'mailto:support@diqto.fr?subject=Aide%20Diqto',
]) {
  assert(help.includes(marker), `help page missing ${marker}`);
}

assert(home.includes('href="/aide.html">Aide et support</a>'), 'home footer must expose public help');
assert(docs.includes('href="/aide.html">Aide</a>'), 'getting-started footer must expose public help');
assert(sitemap.includes('<loc>https://diqto.fr/aide.html</loc>'), 'sitemap must expose public help');

for (const forbidden of [
  /essential[^\n<]{0,20}HT/i,
  /vocal pro[^\n<]{0,20}HT/i,
  /90\s*€|190\s*€/i,
  /abonnement annuel/i,
  /stripe/i,
  /envoyez[^.<]{0,50}(code|mot de passe|carte bancaire|identifiant Apple)/i,
  /remboursement manuel/i,
  /envoi automatique/i,
]) {
  assert(!forbidden.test(help), `help page contains forbidden support claim ${forbidden}`);
}

console.log('PASS public support help page contract');
