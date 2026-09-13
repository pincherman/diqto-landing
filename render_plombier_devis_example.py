#!/usr/bin/env python3
"""Render the public fixture with Diqto's genuine PDF engine, offline only.

Usage: python3 render_plombier_devis_example.py --backend-root ../batiboss
No database, IA transcription, cloud upload, client send or real identity.
"""

import argparse
import hashlib
import json
from pathlib import Path
import socket
import sys
from types import SimpleNamespace
from unittest.mock import patch

from plombier_devis_example import DOCUMENT_NUMBER, LINES, PDF_PATH


def render(backend_root, output_root):
    def refuse_network(*_args, **_kwargs):
        raise RuntimeError("Public demo generation must not access the network")

    output = output_root / PDF_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(backend_root.resolve()))
    with patch.object(socket.socket, "connect", refuse_network), patch.object(socket, "create_connection", refuse_network):
        import pdf_generator

        def save_local(pdf, _filename, _doc_type):
            pdf.set_title("DEMONSTRATION - Devis plombier fictif - aucune somme due")
            pdf.set_author("Diqto - demonstration fictive")
            pdf.output(str(output))
            return str(output), None

        document = SimpleNamespace(
            doc_type="devis", client_name="CLIENT FICTIF - DEMONSTRATION",
            client_address="", client_email="", client_phone="",
            created_at="2026-09-13T00:00:00Z", prestations=[dict(line) for line in LINES],
            tva_rate=20, payment_terms="Demonstration fictive : aucune somme due.",
            notes=("DEMONSTRATION FICTIVE - Ne pas signer ni utiliser comme offre. "
                   "Donnees preparees, sans transcription IA. Prix illustratifs, pas des tarifs de marche. "
                   "TVA 20 % : hypothese de calcul, pas un conseil fiscal. "
                   "Identites fictives. Mentions d'entreprise, assurances et conditions reelles non renseignees. "
                   "Exemple non contractuel, pas un modele juridique complet."),
        )
        company = {"nom_entreprise": "ENTREPRISE FICTIVE - DEMONSTRATION", "metier": "plombier", "tva_applicable": True, "tva": 20}
        with patch.object(pdf_generator, "save_pdf_persistent", save_local):
            pdf_generator.generate_pdf(document, company, doc_type="devis", doc_number=DOCUMENT_NUMBER)

    proof = {
        "kind": "synthetic_pdf_renderer_example", "renderer": "pdf_generator.generate_pdf",
        "pdf_path": PDF_PATH, "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "bytes": output.stat().st_size, "document_number": DOCUMENT_NUMBER,
        "total_ht": 780, "total_tva": 156, "total_ttc": 936,
        "ai_transcription_tested": False, "production_called": False,
        "database_called": False, "cloud_upload": False, "client_send": False,
    }
    output.with_suffix(".json").write_text(json.dumps(proof, indent=2) + "\n")
    print(json.dumps(proof, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    render(args.backend_root, args.output_root)
