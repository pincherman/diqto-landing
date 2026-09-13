"""Shared presentation and arithmetic for explicitly synthetic public quotes."""

from decimal import Decimal, ROUND_HALF_UP
from html import escape

CSS = """
.quote-proof { margin:40px 0; border:1px solid rgba(37,211,102,.26); border-radius:18px; padding:24px; background:rgba(37,211,102,.06); }
.quote-proof h2 { font-size:clamp(24px,4vw,32px); line-height:1.2; margin:8px 0 16px; }
.quote-proof h3 { font-size:18px; margin:24px 0 10px; }
.quote-proof p, .quote-proof li { color:var(--dim); }
.quote-proof .proof-label { color:var(--primary); font-size:12px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; }
.quote-proof blockquote { padding:16px; border-left:3px solid var(--primary); background:var(--card); border-radius:0 12px 12px 0; }
.quote-proof table { width:100%; border-collapse:collapse; margin:16px 0; font-size:14px; }
.quote-proof caption { text-align:left; color:var(--dim); margin-bottom:10px; }
.quote-proof th, .quote-proof td { padding:10px 6px; border-bottom:1px solid var(--border); text-align:left; vertical-align:top; }
.quote-proof th[scope=row] { font-weight:500; }
.quote-proof th:last-child, .quote-proof td:last-child { text-align:right; white-space:nowrap; }
.quote-proof tfoot tr:last-child { color:var(--primary); font-weight:800; }
.quote-proof ul { padding-left:20px; margin:12px 0; }
.quote-proof li + li { margin-top:8px; }
.quote-proof .proof-note { font-size:13px; margin:12px 0; }
.quote-proof a:not(.cta) { color:var(--primary); text-underline-offset:3px; }
.quote-proof a:focus-visible { outline:3px solid var(--primary); outline-offset:5px; }
.quote-proof .proof-download { display:inline-block; font-weight:700; padding:12px 0; }
@media (max-width:400px) { .quote-proof { padding:16px; } .quote-proof th, .quote-proof td { padding:8px 3px; font-size:12px; } }
"""


def quote_totals(lines):
    """Mirror monetary line rounding without importing the application or storage."""
    cent = Decimal("0.01")
    ht = Decimal("0")
    tax = Decimal("0")
    for line in lines:
        amount = (Decimal(str(line["quantity"])) * Decimal(str(line["unit_price"]))).quantize(cent, rounding=ROUND_HALF_UP)
        ht += amount
        tax += (amount * Decimal(str(line["tva_rate"])) / Decimal("100")).quantize(cent, rounding=ROUND_HALF_UP)
    return ht, tax, ht + tax


def euro(amount):
    rounded = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{rounded:.2f}".replace(".", ",") + " €"


def render_rows(lines):
    return "\n".join(
        f'<tr><th scope="row">{escape(line["description"])}</th><td>{escape(str(line["quantity"]))}</td><td>{euro(Decimal(str(line["quantity"])) * Decimal(str(line["unit_price"])))}</td></tr>'
        for line in lines
    )
