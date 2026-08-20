#!/usr/bin/env node

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = __dirname;
const read = (relative) => fs.readFileSync(path.join(root, relative), 'utf8');
const count = (source, marker) => source.split(marker).length - 1;

const home = read('index.html');
const hub = read('facturation-electronique.html');
const report = read('reportage-premier-client-facturation-electronique.html');
const guide = read('guides/facturation-electronique-micro-entreprise.html');
const annex = read('facturation-electronique-conditions.html');
const shell = read('site-shell.js');

for (const marker of [
    'Diqto 1.0 est disponible',
    'Télécharger sur l’App Store France',
    'Votre facturation électronique, dans le même outil.',
    'Préparez, recevez, envoyez et suivez vos factures électroniques depuis Diqto.',
]) {
    assert.ok(home.includes(marker), `homepage missing customer-value marker: ${marker}`);
}

const homeDescription = home.match(
    /<meta name="description" content="([^"]+)">/,
);
assert.ok(homeDescription, 'homepage must expose a meta description');
assert.doesNotMatch(
    homeDescription[1],
    /B2Brouter|Plateforme Agréée|transport réglementaire/i,
    'homepage metadata must sell Diqto outcomes, not provider plumbing',
);

for (const marker of [
    'La facturation électronique, simplement dans Diqto.',
    'Ce que Diqto fait pour vous',
    'Préparer sans ressaisir',
    'Envoyer au bon moment',
    "Suivre jusqu'au règlement",
]) {
    assert.ok(hub.includes(marker), `hub missing customer-value marker: ${marker}`);
}
assert.doesNotMatch(
    hub,
    /Diqto n'est pas une Plateforme Agréée|Diqto ne devient pas une PA/,
    'the marketing hub must not lead with defensive legal negation',
);
assert.ok(
    count(hub, 'B2Brouter') <= 4,
    'the marketing hub must keep the partner disclosure discreet',
);

for (const marker of [
    'Camille active sa <em>facturation électronique</em> dans Diqto.',
    'Recevoir · envoyer · suivre',
    'Tout se passe dans Diqto',
    'Activée, prête, et toujours simple.',
]) {
    assert.ok(report.includes(marker), `report missing outcome marker: ${marker}`);
}
assert.ok(
    count(report, 'B2Brouter') <= 2,
    'the report must not repeat the provider at every activation step',
);
assert.doesNotMatch(
    report,
    /chaque verrou|Transmission verrouillée|Zéro raccourci|Aucune transmission réelle/,
    'the report hero and narrative must not sell internal safeguards as the product',
);

assert.ok(
    guide.includes('Ce que Diqto simplifie')
        && guide.includes('Vous préparez, recevez, envoyez et suivez'),
    'the guide must explain the Diqto outcome positively',
);
assert.doesNotMatch(
    guide,
    /Cette intégration est en cours de préparation|méfiez-vous des logiciels/,
    'the guide must not retain stale or adversarial positioning',
);

assert.ok(
    home.includes('Service opéré avec B2Brouter, Plateforme Agréée partenaire de Diqto.')
        && annex.includes('B2Brouter Global, S.L.')
        && annex.includes("Diqto n'est pas une Plateforme Agréée"),
    'partner transparency must remain in secondary marketing and legal surfaces',
);
assert.ok(
    shell.includes('Diqto 1.0 est disponible')
        && shell.includes('Télécharger sur l’App Store France'),
    'the shared site announcement must carry the current launch state',
);

console.log('PASS e-invoicing customer-value-first contract');
