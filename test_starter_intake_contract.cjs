const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = __dirname;
const home = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const accountant = fs.readFileSync(
    path.join(root, 'experts-comptables.html'),
    'utf8',
);
const accountantScript = fs.readFileSync(
    path.join(root, 'experts-comptables.js'),
    'utf8',
);
const privacy = fs.readFileSync(
    path.join(root, 'confidentialite.html'),
    'utf8',
);

assert.doesNotMatch(home, /id="starter-intake"|data-growth-form/);
assert.doesNotMatch(home, /starterIntakeSubmit|starterIntakePrefill/);
assert.doesNotMatch(home, /Demander mon accès|#beta/i);
assert.match(
    home,
    /href="https:\/\/apps\.apple\.com\/fr\/app\/diqto\/id6761616034"/,
);
assert.match(accountant, /id="ec-prescriber-intake" data-growth-form/);
assert.match(accountant, /name="email"[^>]+required/);
assert.match(accountant, /name="contact_consent"[^>]+required/);
assert.match(
    accountantScript,
    /\/api\/public\/starter-intake/,
);
assert.doesNotMatch(accountantScript, /console\.(?:log|info|debug)\(/);
assert.match(privacy, /Demande d’accès Diqto/);
assert.match(privacy, /3 ans à compter du dernier contact/);

console.log('starter_intake_contract: OK public install direct, EC intake kept');
