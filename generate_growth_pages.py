#!/usr/bin/env python3
"""Embed the closed website route contract without runtime config requests."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTRACT = ROOT / 'config/public_website_pages.json'
TARGET = ROOT / 'growth.js'


def generate() -> str:
    contract = json.loads(CONTRACT.read_text())
    routes = {}
    keys = set()
    for page in contract['pages']:
        key = page['key']
        if not re.fullmatch(r'[a-z][a-z0-9_]{0,95}', key) or key in keys:
            raise ValueError('invalid or duplicate closed page key')
        keys.add(key)
        for route in [page['path'], *page['aliases']]:
            if not route.startswith('/') or '?' in route or '#' in route or route in routes:
                raise ValueError('invalid or duplicate route')
            routes[route] = key
    block = '// BEGIN GENERATED WEBSITE PAGES\n    var websitePages = ' + json.dumps(routes, sort_keys=True, indent=4) + ';\n    // END GENERATED WEBSITE PAGES'
    source, count = re.subn(r'// BEGIN GENERATED WEBSITE PAGES.*?// END GENERATED WEBSITE PAGES', lambda _: block, TARGET.read_text(), flags=re.S)
    if count != 1:
        raise ValueError('expected exactly one generated route block')
    return source


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    output = generate()
    if args.check:
        if output != TARGET.read_text():
            raise SystemExit('FAIL: generated website routes are stale')
        print('PASS: closed website route generation')
    else:
        TARGET.write_text(output)
        print('WROTE: closed website routes')
