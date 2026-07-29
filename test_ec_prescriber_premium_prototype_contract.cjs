const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const html = fs.readFileSync(
    path.join(__dirname, 'prototypes', 'ec-prescriber-pilot-v1.html'),
    'utf8',
);

for (const required of [
    'Démonstration privée · données synthétiques · aucune transmission',
    'Votre logiciel et votre Plateforme Agréée restent en place.',
    'Aucun envoi automatique',
    'Une décision utile',
    'Choix simulé. Rien n’a été envoyé.',
    'Pas de gain inventé',
    'prefers-reduced-motion',
    'aria-live="polite"',
    'meta name="robots" content="noindex,nofollow"',
]) {
    assert.ok(html.includes(required), `missing premium rail: ${required}`);
}

for (const forbidden of [
    'stack',
    'cockpit',
    'connecté automatiquement',
    '30 %',
    'gagnez 1 jour',
    'tableau de bord',
]) {
    assert.equal(
        html.toLowerCase().includes(forbidden.toLowerCase()),
        false,
        `forbidden claim or jargon found: ${forbidden}`,
    );
}

assert.equal(
    [...html.matchAll(/class="choice"/g)].length,
    2,
    'the proof must keep one decision with two explicit choices',
);

console.log('EC prescriber premium prototype contract: PASS');
