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

assert.match(
    home,
    /href="https:\/\/www\.linkedin\.com\/company\/diqto\/"[^>]*>LinkedIn<\/a>/,
    'home must expose the verified public Diqto LinkedIn Page',
);

assert.doesNotMatch(
    publicHtml,
    /(?:facebook\.com\/(?:login|reg)|instagram\.com\/accounts\/(?:login|emailsignup)|tiktok\.com\/(?:login|signup)|accounts\.google\.com)/i,
    'public site must never expose signup, login or account-creation placeholders',
);

console.log('PASS verified public social account links contract');
