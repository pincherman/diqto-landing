#!/usr/bin/env python3
"""Generate and validate the diqto.fr static sitemap."""
from __future__ import annotations

import argparse
import difflib
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parent
SITEMAP_PATH = ROOT / "sitemap.xml"
BASE_URL = "https://diqto.fr"
CANONICAL_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.IGNORECASE)

CORE_ROOT_ORDER = {
    "index.html": 0,
    "fonctionnalites.html": 1,
    "docs.html": 2,
    "cgu.html": 3,
    "confidentialite.html": 4,
    "mentions-legales.html": 5,
}


def is_public_html(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if not rel.endswith(".html"):
        return False
    if "/_" in f"/{rel}":
        return False
    return True


def canonical_url(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = CANONICAL_RE.search(text)
    if match:
        return match.group(1).strip()

    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return f"{BASE_URL}/"
    return f"{BASE_URL}/{rel}"


def sitemap_priority(path: Path) -> tuple[str, str]:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "weekly", "1.0"
    if rel == "fonctionnalites.html":
        return "weekly", "0.8"
    if rel == "docs.html":
        return "weekly", "0.7"
    if rel in {"metiers.html", "guides.html"}:
        return "weekly", "0.8"
    if rel.startswith("guides/"):
        return "weekly", "0.8"
    if rel in {"cgu.html", "confidentialite.html", "mentions-legales.html"}:
        return "weekly", "0.3"
    if rel.startswith("metiers/"):
        return "monthly", "0.6"
    return "monthly", "0.8"


def sort_key(path: Path) -> tuple[int, str]:
    rel = path.relative_to(ROOT).as_posix()
    if rel in CORE_ROOT_ORDER:
        return CORE_ROOT_ORDER[rel], rel
    if "/" not in rel:
        return 10, rel
    if rel.startswith("metiers/"):
        return 20, rel
    return 30, rel


def collect_pages() -> list[Path]:
    return sorted((path for path in ROOT.rglob("*.html") if is_public_html(path)), key=sort_key)


def build_sitemap(lastmod: str) -> str:
    urls: list[str] = []
    seen: set[str] = set()
    for path in collect_pages():
        loc = canonical_url(path)
        if not loc.startswith(f"{BASE_URL}/"):
            raise ValueError(f"canonical outside {BASE_URL}: {path.relative_to(ROOT)} -> {loc}")
        if loc in seen:
            continue
        seen.add(loc)
        changefreq, priority = sitemap_priority(path)
        urls.append(
            "  <url>\n"
            f"    <loc>{escape(loc)}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            f"    <changefreq>{changefreq}</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            "  </url>"
        )

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )


def current_utc_date() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if sitemap.xml is stale.")
    parser.add_argument("--lastmod", default=current_utc_date())
    args = parser.parse_args()

    expected = build_sitemap(args.lastmod)
    if args.check:
        actual = SITEMAP_PATH.read_text(encoding="utf-8")
        if actual != expected:
            diff = difflib.unified_diff(
                actual.splitlines(),
                expected.splitlines(),
                fromfile=str(SITEMAP_PATH),
                tofile="generated sitemap",
                lineterm="",
            )
            print("\n".join(diff))
            return 1
        print(f"sitemap_check: OK pages={len(collect_pages())}")
        return 0

    SITEMAP_PATH.write_text(expected, encoding="utf-8")
    print(f"sitemap_generate: OK pages={len(collect_pages())} path={SITEMAP_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
