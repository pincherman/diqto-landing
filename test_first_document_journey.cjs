const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const read = file => fs.readFileSync(path.join(__dirname, file), 'utf8');
const docs = read('docs.html');
const appRoot = path.join(__dirname, '../diqto-app');
const create = fs.readFileSync(path.join(appRoot, 'app/meeting/new.tsx'), 'utf8');
const form = fs.readFileSync(path.join(appRoot, 'src/components/DocForm.tsx'), 'utf8');
const profile = fs.readFileSync(path.join(appRoot, 'app/(tabs)/profile.tsx'), 'utf8');

for (const label of ['Parler', 'Manuel', 'Document à générer']) {
  assert(create.includes(label), `native path missing ${label}`);
  assert(docs.includes(label), `public guide missing ${label}`);
}
assert(form.includes('Relire le brouillon') && docs.includes('Relire le brouillon'));
assert(profile.includes('Abonnement Diqto') && profile.includes('Voir les offres'));
assert(docs.includes('Abonnement Diqto &gt; Voir les offres'));
for (const id of ['premiere-dictee', 'trame-devis', 'trame-honoraires', 'trame-cours']) {
  assert.equal((docs.match(new RegExp(`id="${id}"`, 'g')) || []).length, 1);
}
for (const kind of ['devis', 'honoraires', 'cours']) {
  assert(docs.includes(`data-copy-prompt="prompt-${kind}"`));
  assert(docs.includes(`id="prompt-${kind}"`));
}
assert(docs.includes('<noscript>') && docs.includes('role="status"'));
assert(docs.includes('nouveau brouillon enregistré compte dans le quota'));
assert(!docs.includes('brouillons illimités') && !docs.includes('footer supprimé'));
const script = read('starter-prompts.js');
assert(!/fetch\(|XMLHttpRequest|localStorage|sessionStorage|innerHTML\s*=/.test(script), 'prompt copy must remain local and text-only');
assert(script.includes('clipboard.writeText') && script.includes('copie automatique est indisponible'));
for (const file of ['guides.html', 'metiers.html', 'plombier.html']) {
  assert(read(file).includes('/docs.html#'), `${file} must connect to first-value help`);
}
for (const file of fs.readdirSync(path.join(__dirname, 'guides'))) {
  if (file.endsWith('.html')) assert(!read('guides/'+file).includes('Consulter cette page'), file);
}
console.log('PASS first document journey: native labels, 3 document families, local-only prompts and discovery links');
