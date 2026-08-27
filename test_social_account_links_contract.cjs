const assert = require('node:assert/strict');
const childProcess = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');

const root = __dirname;
const home = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const publicHtml = childProcess
    .execFileSync('git', ['ls-files', '*.html'], {
        cwd: root,
        encoding: 'utf8',
    })
    .trim()
    .split('\n')
    .filter(Boolean)
    .map((relativePath) => fs.readFileSync(path.join(root, relativePath), 'utf8'))
    .join('\n');

const verifiedSocialProfiles = [
    ['LinkedIn', 'https://www.linkedin.com/company/diqto/'],
    ['Instagram', 'https://www.instagram.com/diqto.app/'],
    ['Facebook', 'https://www.facebook.com/profile.php?id=61593797400849'],
    ['TikTok', 'https://www.tiktok.com/@philippeincherma5'],
    ['YouTube', 'https://www.youtube.com/@diqtoapp'],
];

for (const [network, url] of verifiedSocialProfiles) {
    const escapedUrl = url.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    assert.match(
        home,
        new RegExp(`href="${escapedUrl}"[^>]*target="_blank"[^>]*rel="noopener noreferrer"[^>]*>${network}<\\/a>`),
        `home must expose the verified public Diqto ${network} profile safely`,
    );
    assert.match(
        home,
        new RegExp(`"${escapedUrl}"`),
        `organization structured data must expose the verified Diqto ${network} profile`,
    );
}

assert.doesNotMatch(
    publicHtml,
    /(?:facebook\.com\/(?:login|reg)|instagram\.com\/accounts\/(?:login|emailsignup)|tiktok\.com\/(?:login|signup)|accounts\.google\.com)/i,
    'public site must never expose signup, login or account-creation placeholders',
);

console.log('PASS verified public social account links contract');
