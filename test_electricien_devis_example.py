"""Electrician fixture -> HTML -> genuine PDF -> local journey, without network."""
import hashlib
import json
from pathlib import Path
import re
import os
import tempfile
import unittest
from unittest.mock import patch

import fitz

from electricien_devis_example import DOCUMENT_NUMBER, LINES, PDF_PATH
from quote_example_common import euro, quote_totals, render_rows
from test_plombier_devis_example import TableRows

ROOT = Path(__file__).resolve().parent


class ElectricianExampleContract(unittest.TestCase):
    def test_original_example_is_consistent_with_rendered_pdf_and_destinations(self):
        html = (ROOT / 'electricien.html').read_text()
        table = TableRows()
        table.feed(html)
        self.assertEqual(html.count('id="exemple-devis-electricien"'), 1)
        self.assertNotIn('exemple-devis-plombier', html)
        self.assertNotIn('mise aux normes NF C 15-100', html)
        self.assertIn('ne certifie ni la sécurité ni la conformité', html)
        self.assertIn('elle n’a pas été transcrite par l’IA', html)
        self.assertIn('les nouveaux brouillons enregistrés comptent dans ce quota', html)
        self.assertNotIn('brouillons illimités', html)
        self.assertIn('<link rel="canonical" href="https://diqto.fr/electricien.html">', html)
        with fitz.open(ROOT / PDF_PATH) as pdf:
            self.assertEqual(len(pdf), 1)
            text = re.sub(r'\s+', ' ', pdf[0].get_text())
        self.assertIn(DOCUMENT_NUMBER, text)
        for line in LINES:
            self.assertIn([line['description'], str(line['quantity']), euro(line['quantity'] * line['unit_price'])], table.rows)
            self.assertIn(line['description'], text)
            self.assertIn(f"{line['unit_price']:.2f} EUR", text)
        self.assertEqual(tuple(map(float, quote_totals(LINES))), (690, 138, 828))
        for label, amount in zip(('Total HT', 'TVA (20%)', 'TOTAL TTC'), (690, 138, 828)):
            self.assertIn(f'{label} {amount}.00 EUR', text)
        for marker in ('DEMONSTRATION FICTIVE', 'aucune somme due', 'sans transcription IA', 'references et quantites du materiel', 'circuits concernes', 'ne certifie ni la securite ni la conformite'):
            self.assertIn(marker, text)
        self.assertNotIn('SIRET', text)
        for href in ('/docs.html#premiere-dictee', '/guides/logiciel-devis-facture-artisan.html', '/' + PDF_PATH):
            self.assertIn(f'href="{href}"', html)
            file, _, fragment = href.partition('#')
            target = ROOT / file.lstrip('/')
            self.assertTrue(target.is_file(), href)
            if fragment:
                self.assertIn(f'id="{fragment}"', target.read_text())
        self.assertIn('data-growth-placement="final_cta"', html)
        proof = json.loads((ROOT / PDF_PATH).with_suffix('.json').read_text())
        self.assertEqual(proof['sha256'], hashlib.sha256((ROOT / PDF_PATH).read_bytes()).hexdigest())
        self.assertEqual(proof['total_ttc'], 828)
        self.assertEqual(proof['renderer'], 'pdf_generator.generate_pdf')
        for key in ('ai_transcription_tested', 'production_called', 'database_called', 'cloud_upload', 'client_send'):
            self.assertIs(proof[key], False)

    def test_shared_renderer_preserves_default_plumber_document(self):
        from render_plombier_devis_example import render
        from plombier_devis_example import PDF_PATH as PLUMBER_PDF
        backend = Path(os.environ.get('DIQTO_BACKEND_ROOT', str(ROOT.parent / 'batiboss')))
        with tempfile.TemporaryDirectory() as temporary, patch('builtins.print'):
            render(backend, Path(temporary))
            with fitz.open(Path(temporary) / PLUMBER_PDF) as fresh, fitz.open(ROOT / PLUMBER_PDF) as baseline:
                self.assertEqual(len(fresh), len(baseline))
                normalize = lambda doc: re.sub(r'\s+', ' ', ''.join(page.get_text() for page in doc)).strip()
                self.assertEqual(normalize(fresh), normalize(baseline))

    def test_shared_quote_rows_do_not_confuse_unit_and_line_total(self):
        # A reusable row must multiply quantity and escape the proposed label.
        lines = ({'description': '<test & matériel>', 'quantity': 3, 'unit_price': '12.35', 'tva_rate': 20},)
        self.assertEqual(tuple(map(str, quote_totals(lines))), ('37.05', '7.41', '44.46'))
        html = render_rows(lines)
        self.assertIn('&lt;test &amp; matériel&gt;', html)
        self.assertIn('<td>3</td><td>37,05 €</td>', html)
        # A half-cent must not display a different HT amount from the totals.
        half_cent = ({'description': 'Poste de démonstration', 'quantity': 3, 'unit_price': '12.355', 'tva_rate': 20},)
        self.assertEqual(tuple(map(str, quote_totals(half_cent))), ('37.07', '7.41', '44.48'))
        self.assertIn('<td>3</td><td>37,07 €</td>', render_rows(half_cent))


if __name__ == '__main__':
    unittest.main()
