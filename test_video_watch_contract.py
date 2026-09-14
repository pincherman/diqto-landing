"""Watch discovery contract: sitemap -> page -> schema -> media -> navigation."""
import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent
BASE = "https://diqto.fr"
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9",
      "v": "http://www.google.com/schemas/sitemap-video/1.1"}


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.schemas = []
        self.schema_text = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.schema_text = ""

    def handle_data(self, data):
        if self.schema_text is not None:
            self.schema_text += data

    def handle_endtag(self, tag):
        if tag == "script" and self.schema_text is not None:
            data = json.loads(self.schema_text)
            self.schemas.extend(data.get("@graph", [data]))
            self.schema_text = None

    def elements(self, tag):
        return [attrs for name, attrs in self.tags if name == tag]


class VideoWatchContract(unittest.TestCase):
    def test_all_video_entries_are_unique_watch_pages_with_matching_assets(self):
        sitemap = ElementTree.parse(ROOT / "video-sitemap.xml")
        main_sitemap = (ROOT / "sitemap.xml").read_text()
        hub = (ROOT / "histoires.html").read_text()
        seen_pages, seen_media = set(), set()
        for entry in sitemap.findall("s:url", NS):
            url = entry.findtext("s:loc", namespaces=NS)
            with self.subTest(url=url):
                self.assertTrue(url.startswith(BASE + "/histoires/"))
                self.assertNotIn(url, seen_pages)
                seen_pages.add(url)
                relative = urlparse(url).path
                text = (ROOT / relative.lstrip("/")).read_text()
                page = Page(text)
                canonical = [a["href"] for a in page.elements("link") if a.get("rel") == "canonical"]
                self.assertEqual(canonical, [url])
                self.assertIn(f"<loc>{url}</loc>", main_sitemap)
                self.assertIn(f'href="{relative}"', hub)
                self.assertNotIn("noindex", text)
                self.assertEqual(len(page.elements("h1")), 1)
                videos = page.elements("video")
                self.assertEqual(len(videos), 1)
                self.assertIn("controls", videos[0])
                self.assertNotIn("autoplay", videos[0])
                self.assertEqual(len(page.elements("source")), 1)
                source = page.elements("source")[0]["src"]
                poster = videos[0]["poster"]
                captions = page.elements("track")
                self.assertEqual(len(captions), 1)
                self.assertEqual(captions[0]["srclang"], "fr")
                for asset in (source, poster, captions[0]["src"]):
                    self.assertTrue((ROOT / asset.lstrip("/")).is_file(), asset)
                self.assertNotIn(source, seen_media)
                seen_media.add(source)
                schema = [s for s in page.schemas if s.get("@type") == "VideoObject"]
                self.assertEqual(len(schema), 1)
                schema = schema[0]
                self.assertEqual(schema["url"], url)
                self.assertEqual(schema["mainEntityOfPage"], url)
                self.assertEqual(schema["contentUrl"], BASE + source)
                self.assertEqual(schema["thumbnailUrl"], [BASE + poster])
                self.assertEqual(entry.findtext("v:video/v:content_loc", namespaces=NS), BASE + source)
                self.assertEqual(entry.findtext("v:video/v:thumbnail_loc", namespaces=NS), BASE + poster)
                duration = entry.findtext("v:video/v:duration", namespaces=NS)
                self.assertEqual(schema["duration"], f"PT{duration}S")
                # Explanatory copy cannot push the only player below a long hero.
                self.assertLess(text.index("<video "), text.index('class="watch-lead"'))
                self.assertLess(text.index("<video "), text.index('class="watch-disclosure"'))
                self.assertIn('href="/histoires.html"', text)
                self.assertIn("Voir le parcours", text)
        self.assertEqual(len(seen_pages), 9)

    def test_non_watch_pages_are_indexable_and_link_to_real_watch_pages(self):
        for path in ROOT.rglob("*.html"):
            relative = path.relative_to(ROOT)
            if relative.parts[0] in {"histoires", "tmp", "prototypes"}:
                continue
            page = Page(path.read_text())
            with self.subTest(page=str(relative)):
                self.assertEqual(page.elements("video"), [])
                self.assertFalse(any(s.get("@type") == "VideoObject" for s in page.schemas))
                for a in page.elements("a"):
                    href = a.get("href", "")
                    if href.startswith("/histoires/"):
                        self.assertTrue((ROOT / href.lstrip("/")).is_file(), href)


if __name__ == "__main__":
    unittest.main()
