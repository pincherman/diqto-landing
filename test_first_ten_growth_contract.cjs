const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');

const root = __dirname;
const growth = fs.readFileSync(path.join(root, 'growth.js'), 'utf8');
const home = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const ec = fs.readFileSync(path.join(root, 'experts-comptables.html'), 'utf8');
const ecScript = fs.readFileSync(path.join(root, 'experts-comptables.js'), 'utf8');
const privacy = fs.readFileSync(path.join(root, 'confidentialite.html'), 'utf8');

for (const marker of [
    "sessionStorage.getItem('diqto_growth_session_v1')",
    "credentials: 'omit'",
    "track('landing_view'",
    "'appstore_outbound'",
    "track('intake_started'",
    'linkedin_founder_launch: true',
    "new URLSearchParams(\n            window.location.search\n        ).get('source')",
]) {
    assert(growth.includes(marker), `growth rail missing ${marker}`);
}

for (const forbidden of [
    'document.cookie',
    'localStorage',
    'document.referrer',
    'navigator.userAgent',
    'window.location.href',
]) {
    assert(!growth.includes(forbidden), `growth rail must not collect ${forbidden}`);
}

assert(home.includes('data-growth-page="home"'));
assert(home.includes('data-growth-source="direct_or_organic"'));
assert(home.includes('data-growth-placement="announcement"'));
assert(home.includes('data-growth-placement="hero"'));
assert(home.includes('data-growth-placement="final"'));
assert(home.includes('https://apps.apple.com/fr/app/diqto/id6761616034'));
assert(!home.includes('id="starter-intake" data-growth-form'));
assert(!home.includes("window.diqtoGrowthTrack('intake_submitted'"));
assert(ec.includes('data-growth-page="experts_comptables"'));
assert(ec.includes('data-growth-source="expert_accountant"'));
assert(ec.includes('id="ec-prescriber-intake" data-growth-form'));
assert(ecScript.includes("'intake_submitted'"));
assert(privacy.includes("ne dépose aucun cookie de mesure d'audience"));
assert(privacy.includes('90 jours maximum pour les événements de parcours sans cookie'));
assert(privacy.includes('<strong>Sentry</strong>'));
assert(!privacy.includes('bandeau de consentement présent sur le site'));

for (const source of [
    'linkedin_carousel',
    'linkedin_founder_comment',
    'linkedin_founder_launch',
    'linkedin_profile',
    'linkedin_video',
]) {
    assert(growth.includes(`${source}: true`), `missing closed source ${source}`);
}
assert(!growth.includes("source = requestedSource || defaultSource"));

console.log('PASS first-ten privacy-safe growth contract');
