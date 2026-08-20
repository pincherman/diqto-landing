const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const root = __dirname;
const home = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const stories = fs.readFileSync(path.join(root, 'histoires.html'), 'utf8');
const siteShell = fs.readFileSync(path.join(root, 'site-shell.js'), 'utf8');

const storyCases = [
    {
        id: 'marc-artisan',
        destination: '/plombier.html',
        watch: '/histoires/marc-artisan.html',
        sha256: '398970df27ee00a17403a60e0813f6c817d3781d734d1f74035a0ab97e27c550',
    },
    {
        id: 'claire-osteopathe',
        destination: '/osteopathe.html',
        watch: '/histoires/claire-osteopathe.html',
    },
    {
        id: 'sarah-avocate',
        destination: '/metiers/avocat.html',
        watch: '/histoires/sarah-avocate.html',
    },
    {
        id: 'jean-luc-karate',
        destination: '/metiers/prof_karate.html',
        watch: '/histoires/jean-luc-karate.html',
    },
];

assert.match(home, /id="histoires"/);
assert.match(home, /href="\/histoires\.html"/);
assert.match(siteShell, /ensureStoriesLink/);
assert.match(siteShell, /href = '\/histoires\.html'/);
assert.match(siteShell, /ensureAppStoreAnnouncement/);
assert.match(
    siteShell,
    /https:\/\/apps\.apple\.com\/fr\/app\/diqto\/id6761616034/,
);
assert.doesNotMatch(siteShell, /document\.cookie|localStorage|sessionStorage|sendBeacon|gtag|plausible/i);
assert.doesNotMatch(home, /starterIntake|#beta/);
assert.match(stories, /Histoires inspirées du quotidien/);
assert.match(stories, /personnages et situations sont fictifs/i);
assert.doesNotMatch(stories, /témoignage client/i);
assert.match(stories, /id="cabinet-expert-comptable"/);
assert.match(
    stories,
    /href="\/histoires\/cabinet-expert-comptable\.html"/,
);
assert.match(stories, /href="\/experts-comptables\.html"/);
assert.match(
    stories,
    /src="\/assets\/ec\/diqto-cabinet-cinematique-v9-poster\.jpg"/,
);
assert.match(stories, /toute connexion réelle reste à cadrer et autoriser/i);

for (const story of storyCases) {
    const videoRelative = `assets/stories/${story.id}.mp4`;
    const posterRelative = `assets/stories/${story.id}-poster.jpg`;
    const videoPath = path.join(root, videoRelative);
    const posterPath = path.join(root, posterRelative);

    assert.ok(fs.existsSync(videoPath), `${videoRelative} is missing`);
    assert.ok(fs.existsSync(posterPath), `${posterRelative} is missing`);
    assert.ok(
        fs.statSync(videoPath).size <= 3 * 1024 * 1024,
        `${videoRelative} exceeds the 3 MB web budget`,
    );
    assert.ok(
        fs.statSync(posterPath).size <= 150 * 1024,
        `${posterRelative} exceeds the 150 KB poster budget`,
    );
    if (story.sha256) {
        const digest = crypto
            .createHash('sha256')
            .update(fs.readFileSync(videoPath))
            .digest('hex');
        assert.equal(digest, story.sha256, `${videoRelative} provenance drifted`);
    }

    assert.match(stories, new RegExp(`src="/${videoRelative}"`));
    assert.match(stories, new RegExp(`poster="/${posterRelative}"`));
    assert.match(stories, new RegExp(`href="${story.destination}"`));
    assert.match(stories, new RegExp(`href="${story.watch}"`));
    assert.match(home, new RegExp(`href="${story.watch}"`));
}

const videos = stories.match(/<video\b[^>]*>/g) || [];
assert.equal(videos.length, storyCases.length);
for (const video of videos) {
    assert.match(video, /controls/);
    assert.match(video, /preload="none"/);
    assert.doesNotMatch(video, /autoplay/);
}

assert.match(stories, /Rien ne part sans votre validation/);
assert.match(
    stories,
    /href="https:\/\/apps\.apple\.com\/fr\/app\/diqto\/id6761616034"/,
);
assert.doesNotMatch(stories, /#beta|Demander mon accès/i);
assert.doesNotMatch(stories, /conforme|automatique(?:ment)? envoyé/i);

console.log('story_gallery_contract: OK');
