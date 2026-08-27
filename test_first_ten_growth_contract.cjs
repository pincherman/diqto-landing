const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = __dirname;
const growth = fs.readFileSync(path.join(root, 'growth.js'), 'utf8');
const home = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const ec = fs.readFileSync(path.join(root, 'experts-comptables.html'), 'utf8');
const ecScript = fs.readFileSync(path.join(root, 'experts-comptables.js'), 'utf8');
const privacy = fs.readFileSync(path.join(root, 'confidentialite.html'), 'utf8');

for (const marker of [
    "sessionStorage.getItem('diqto_growth_session_v1')",
    "'diqto_growth_attribution_v1'",
    "credentials: 'omit'",
    "track('landing_view'",
    "'appstore_outbound'",
    "track('intake_started'",
    'linkedin_founder_launch: true',
    'new URLSearchParams(window.location.search)',
    "campaign: campaign",
    "content: content",
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
    'artisan_concierge',
    'facebook_reels',
    'instagram_reels',
    'linkedin_carousel',
    'linkedin_founder_comment',
    'linkedin_founder_launch',
    'linkedin_profile',
    'linkedin_video',
    'tiktok_video',
    'youtube_shorts',
]) {
    assert(growth.includes(`${source}: true`), `missing closed source ${source}`);
}
assert(!growth.includes("source = requestedSource || defaultSource"));

function executeGrowth(search, storedSession = {}) {
    const payloads = [];
    const body = {
        getAttribute(name) {
            return {
                'data-growth-page': 'home',
                'data-growth-source': 'direct_or_organic',
            }[name] || null;
        },
    };
    const context = {
        URLSearchParams,
        Math,
        Date,
        window: {
            fetch(_url, options) {
                payloads.push(JSON.parse(options.body));
                return Promise.resolve({ ok: true });
            },
            location: { search },
            crypto: { randomUUID: () => '01234567-89ab-cdef-0123-456789abcdef' },
            sessionStorage: {
                getItem: (key) => storedSession[key] || null,
                setItem: (key, value) => {
                    storedSession[key] = value;
                },
            },
        },
        document: {
            body,
            addEventListener: () => {},
            querySelectorAll: () => [],
        },
    };
    vm.runInNewContext(growth, context);
    return payloads;
}

const conciergePayloads = executeGrowth('?source=artisan_concierge');
assert.equal(conciergePayloads.length, 1);
assert.equal(conciergePayloads[0].event, 'landing_view');
assert.equal(conciergePayloads[0].source, 'artisan_concierge');
assert.equal(conciergePayloads[0].campaign, 'unknown');
assert.equal(conciergePayloads[0].content, 'unknown');
assert(!JSON.stringify(conciergePayloads[0]).includes('window.location'));

const fallbackPayloads = executeGrowth('?source=untrusted@example.test');
assert.equal(fallbackPayloads.length, 1);
assert.equal(fallbackPayloads[0].source, 'direct_or_organic');
assert(!JSON.stringify(fallbackPayloads[0]).includes('untrusted@example.test'));

for (const source of [
    'facebook_reels',
    'instagram_reels',
    'linkedin_video',
    'tiktok_video',
    'youtube_shorts',
]) {
    const payloads = executeGrowth(`?source=${source}`);
    assert.equal(payloads.length, 1);
    assert.equal(payloads[0].source, source);
}

const socialSession = {};
const socialQuery = [
    '?source=facebook_reels',
    'utm_source=facebook',
    'utm_medium=organic_social',
    'utm_campaign=deuxieme_journee_s1_btp',
    'utm_content=ep01_plombier_v2',
].join('&');
const socialPayloads = executeGrowth(socialQuery, socialSession);
assert.equal(socialPayloads[0].source, 'facebook_reels');
assert.equal(
    socialPayloads[0].campaign,
    'deuxieme_journee_s1_btp',
);
assert.equal(socialPayloads[0].content, 'ep01_plombier_v2');

const continuedPayloads = executeGrowth('', socialSession);
assert.equal(continuedPayloads[0].source, 'facebook_reels');
assert.equal(
    continuedPayloads[0].campaign,
    'deuxieme_journee_s1_btp',
);
assert.equal(continuedPayloads[0].content, 'ep01_plombier_v2');

const poisonedPayloads = executeGrowth(
    '?source=facebook_reels'
    + '&utm_source=facebook'
    + '&utm_medium=organic_social'
    + '&utm_campaign=private@example.test'
    + '&utm_content=client-phone-0600000000',
);
assert.equal(poisonedPayloads[0].source, 'facebook_reels');
assert.equal(poisonedPayloads[0].campaign, 'unknown');
assert.equal(poisonedPayloads[0].content, 'unknown');
assert(!JSON.stringify(poisonedPayloads[0]).includes('private@example.test'));
assert(!JSON.stringify(poisonedPayloads[0]).includes('0600000000'));

console.log('PASS first-ten privacy-safe growth contract');
