"""Landing decision journey must agree with the backend plan catalog.

Run with DIQTO_BACKEND_ROOT when using a landing-only sparse worktree.
No API, database, purchase or production traffic is used.
"""
import ast
import importlib.util
import os
from pathlib import Path
import re
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
BACKEND = Path(os.environ.get('DIQTO_BACKEND_ROOT', str(ROOT.parent / 'batiboss')))
PAGES = ('index.html', 'fonctionnalites.html', 'guides/logiciel-devis-facture-artisan.html')


class CommercialOfferTruth(unittest.TestCase):
    def test_public_choice_agrees_with_backend_and_native_purchase_path(self):
        module = ast.parse((BACKEND / 'saas_billing.py').read_text())
        catalog = next(ast.literal_eval(node.value) for node in module.body
                       if isinstance(node, ast.AnnAssign)
                       and isinstance(node.target, ast.Name)
                       and node.target.id == 'PLAN_CATALOG')
        plans = {plan['id']: plan for plan in catalog}
        self.assertEqual(plans['free']['limits']['documents_per_month'], 3)
        self.assertEqual(plans['essential']['price_eur_month'], 9)
        self.assertEqual(plans['vocal_pro']['price_eur_month'], 19)
        self.assertIsNone(plans['essential']['limits']['documents_per_month'])
        for plan in (plans['essential'], plans['vocal_pro']):
            self.assertTrue(plan['price_tax_included'])
            self.assertEqual(plan['price_reference_country'], 'FR')
        for relative in PAGES:
            with self.subTest(page=relative):
                text = (ROOT / relative).read_text()
                self.assertRegex(text, r'3 documents par mois, brouillons compris')
                self.assertNotRegex(text.lower(), r'brouillons illimités|footer supprimé|sans footer|3 vocaux courts|1 entreprise et 1 utilisateur|3 documents finalisés')
                self.assertIn('Abonnement Diqto', text)
                self.assertIn('Apple', text)
                self.assertTrue(re.search(r'renouvellent mensuellement|renouvellent chaque mois|mensuels à renouvellement automatique', text), relative + ': monthly renewal must be explicit')
                self.assertIn('résili', text)
                self.assertIn('/plombier.html#exemple-devis-plombier', text)
                self.assertIn('https://apps.apple.com/fr/app/diqto/id6761616034', text)
                self.assertIn('data-growth-placement="hero"', text)
                self.assertEqual(len(re.findall(r'<h1\b', text)), 1)
                for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
                    import json
                    json.loads(block)
        app = BACKEND.parent / 'diqto-app'
        self.assertIn("label: 'Abonnement Diqto'", (app / 'app/(tabs)/profile.tsx').read_text())
        self.assertIn('Apple affiche le prix local définitif', (app / 'app/upgrade.tsx').read_text())

    def test_guide_regeneration_does_not_erase_decision_content(self):
        spec = importlib.util.spec_from_file_location('commercial_test_generator', ROOT / 'generate_seo_hubs.py')
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)
        with tempfile.TemporaryDirectory() as directory:
            generator.ROOT = Path(directory)
            guide = next(item for item in generator.GUIDES if item['slug'] == 'logiciel-devis-facture-artisan')
            generator.generate_guide(guide)
            relative = Path('guides/logiciel-devis-facture-artisan.html')
            self.assertEqual((ROOT / relative).read_bytes(), (Path(directory) / relative).read_bytes())


if __name__ == '__main__':
    unittest.main()
