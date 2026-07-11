#!/usr/bin/env python3
"""Submit the public diqto.fr sitemap URLs to IndexNow."""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SITEMAP = ROOT / "sitemap.xml"
HOST = "diqto.fr"
KEY = "b9e5c1a04e2d7f638a6c0b1d49e7f253"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"


def sitemap_urls() -> list[str]:
    tree = ET.parse(SITEMAP)
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [node.text.strip() for node in tree.findall("sm:url/sm:loc", namespace) if node.text]
    if not urls or any(not url.startswith(f"https://{HOST}/") for url in urls):
        raise ValueError("sitemap contains no URL or an URL outside diqto.fr")
    return urls


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    urls = sitemap_urls()
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }
    if args.dry_run:
        print(f"indexnow_dry_run: OK urls={len(urls)} key_location={KEY_LOCATION}")
        return 0

    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            status = response.status
    except urllib.error.HTTPError as error:
        status = error.code
    if status not in {200, 202}:
        print(f"indexnow_submit: FAIL status={status}", file=sys.stderr)
        return 1
    print(f"indexnow_submit: OK status={status} urls={len(urls)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
