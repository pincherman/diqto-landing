const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = __dirname;
const home = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const privacy = fs.readFileSync(path.join(root, 'confidentialite.html'), 'utf8');

assert.match(home, /<form class="starter-intake" id="starter-intake" novalidate>/);
assert.match(home, /name="email"[^>]+required/);
assert.match(home, /name="trade"[^>]+required/);
assert.match(home, /name="first_need"[^>]+required/);
assert.match(home, /name="contact_consent"[^>]+required/);
assert.match(home, /name="website"[^>]+tabindex="-1"/);
assert.match(home, /name="source" type="hidden"/);
assert.match(home, /role="status" aria-live="polite"/);
assert.match(home, /fetch\('https:\/\/necessary-danila-diqto-7fbe88c8\.koyeb\.app\/api\/public\/starter-intake'/);
assert.match(home, /contact_consent: data\.get\('contact_consent'\) === 'on'/);
assert.doesNotMatch(home, /mailto:support@diqto\.fr\?subject=Acces/);
assert.doesNotMatch(home, /console\.(?:log|info|debug)\(/);
assert.match(privacy, /Demande d’accès Diqto/);
assert.match(privacy, /3 ans à compter du dernier contact/);

console.log('starter_intake_contract: OK');
