const assert = require('node:assert/strict');
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
    },
    {
        id: 'claire-osteopathe',
        destination: '/osteopathe.html',
    },
    {
        id: 'sarah-avocate',
        destination: '/metiers/avocat.html',
    },
    {
        id: 'jean-luc-karate',
        destination: '/metiers/prof_karate.html',
    },
];

assert.match(home, /id="histoires"/);
assert.match(home, /href="\/histoires\.html"/);
assert.match(siteShell, /ensureStoriesLink/);
assert.match(siteShell, /href = '\/histoires\.html'/);
assert.match(siteShell, /tagConsentlessConversionPaths/);
assert.match(siteShell, /seo_guides_hub_cta/);
assert.match(siteShell, /seo_stories_nav/);
assert.match(siteShell, /seo_stories_final_cta/);
assert.doesNotMatch(siteShell, /document\.cookie|localStorage|sessionStorage|sendBeacon|gtag|plausible/i);
assert.match(home, /if \(\(metier \|\| source\) && accessLink\)/);
assert.match(home, /if \(source\) body \+= 'Source : ' \+ source/);
assert.match(stories, /Histoires inspirées du quotidien/);
assert.match(stories, /personnages et situations sont fictifs/i);
assert.doesNotMatch(stories, /témoignage client/i);

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

    assert.match(stories, new RegExp(`src="/${videoRelative}"`));
    assert.match(stories, new RegExp(`poster="/${posterRelative}"`));
    assert.match(stories, new RegExp(`href="${story.destination}"`));
}

const videos = stories.match(/<video\b[^>]*>/g) || [];
assert.equal(videos.length, storyCases.length);
for (const video of videos) {
    assert.match(video, /controls/);
    assert.match(video, /preload="none"/);
    assert.doesNotMatch(video, /autoplay/);
}

assert.match(stories, /Rien ne part sans votre validation/);
assert.match(stories, /href="\/#beta"/);
assert.doesNotMatch(stories, /conforme|automatique(?:ment)? envoyé/i);

console.log('story_gallery_contract: OK');
