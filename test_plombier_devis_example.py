"""Cross-surface example contract: public HTML, real PDF and canonical generator.

Run: python3 -m unittest test_plombier_devis_example -v
Requires PyMuPDF (fitz), also used by the Diqto PDF regression suite.
"""

import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import fitz

from plombier_devis_example import DOCUMENT_NUMBER, LINES, PDF_PATH

ROOT = Path(__file__).resolve().parent


class TableRows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = None

    def handle_starttag(self, tag, _attrs):
        if tag == "tr":
            self.row = []

    def handle_data(self, text):
        if self.row is not None and text.strip():
            self.row.append(text.strip())

    def handle_endtag(self, tag):
        if tag == "tr":
            self.rows.append(self.row)
            self.row = None


class PublicExampleContract(unittest.TestCase):
    def test_html_pdf_and_fixture_agree_on_real_rendered_amounts(self):
        html = (ROOT / "plombier.html").read_text()
        table = TableRows()
        table.feed(html)
        self.assertEqual(len(LINES), 3)
        self.assertEqual(sum(line["unit_price"] * line["quantity"] for line in LINES), 780)
        with fitz.open(ROOT / PDF_PATH) as pdf:
            self.assertEqual(len(pdf), 1, "the useful example must fit one page")
            text = " ".join(page.get_text() for page in pdf)
        normalized = re.sub(r"\s+", " ", text)
        self.assertIn(DOCUMENT_NUMBER, normalized)
        for line in LINES:
            self.assertIn([line["description"], "1", f'{line["unit_price"]},00 €'], table.rows)
            self.assertIn(line["description"], normalized)
            self.assertIn(f'{line["unit_price"]}.00 EUR', normalized)
        for label, html_label, amount in (("Total HT", "Total HT", 780), ("TVA (20%)", "TVA 20 % (hypothèse)", 156), ("TOTAL TTC", "Total TTC", 936)):
            self.assertIn([html_label, f"{amount},00 €"], table.rows)
            self.assertIn(f"{label} {amount}.00 EUR", normalized)
        self.assertIn(f'href="/{PDF_PATH}"', html)
        self.assertIn("DEMONSTRATION FICTIVE", normalized)
        self.assertIn("CLIENT FICTIF", normalized)
        self.assertIn("aucune somme due", normalized)
        self.assertIn("pas un conseil fiscal", normalized)
        self.assertNotIn("SIRET", normalized)
        self.assertIn("elle n’a pas été transcrite par l’IA", html)
        self.assertIn("3 documents finalisés, exportés ou envoyés par mois", html)
        self.assertIn("3 vocaux courts par mois jusqu’à 1 minute", html)
        self.assertIn('href="https://apps.apple.com/fr/app/diqto/id6761616034" data-growth-placement="final_cta"', html)
        proof = json.loads((ROOT / PDF_PATH).with_suffix(".json").read_text())
        self.assertEqual(proof["sha256"], hashlib.sha256((ROOT / PDF_PATH).read_bytes()).hexdigest())
        self.assertEqual(proof["renderer"], "pdf_generator.generate_pdf")
        for key in ("ai_transcription_tested", "production_called", "database_called", "cloud_upload", "client_send"):
            self.assertIs(proof[key], False)

    def test_regeneration_preserves_example_without_changing_neighboring_pages(self):
        with tempfile.TemporaryDirectory(prefix="diqto-proof-regeneration-") as tmp:
            destination = Path(tmp)
            for name in ("regen_metier_pages.py", "release_config.py", "campaign_video_content.py", "plombier_devis_example.py"):
                shutil.copyfile(ROOT / name, destination / name)
            result = subprocess.run([sys.executable, "regen_metier_pages.py"], cwd=destination, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            generated = list(destination.glob("*.html"))
            self.assertEqual(len(generated), 10)
            for page in generated:
                self.assertEqual(page.read_text(), (ROOT / page.name).read_text(), page.name)
                if page.name != "plombier.html":
                    self.assertNotIn("quote-proof", page.read_text(), page.name)
            html = (destination / "plombier.html").read_text()
            self.assertEqual(html.count('id="exemple-devis-plombier"'), 1)
            self.assertIn('<h1>Diqto pour les <span>Plombiers</span></h1>', html)
            self.assertIn('<title>Diqto pour les Plombiers — Devis &amp; factures IA</title>', html)


if __name__ == "__main__":
    unittest.main()
