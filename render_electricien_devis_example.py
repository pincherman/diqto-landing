#!/usr/bin/env python3
"""Render the electrician fixture using the shared, network-blocked Diqto renderer."""

import argparse
from pathlib import Path

import electricien_devis_example
from render_plombier_devis_example import render

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    render(args.backend_root, args.output_root, electricien_devis_example)
