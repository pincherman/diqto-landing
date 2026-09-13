"""Canonical, explicitly synthetic quote example for the plumber landing page."""

from html import escape

PDF_PATH = "assets/examples/devis-plombier-chauffe-eau-demonstration.pdf"
DOCUMENT_NUMBER = "DEMO-PLOMBIER-001"
LINES = (
    {"description": "Fourniture chauffe-eau 200 L", "quantity": 1, "unit_price": 450, "tva_rate": 20},
    {"description": "Pose du chauffe-eau", "quantity": 1, "unit_price": 250, "tva_rate": 20},
    {"description": "Depose de l'ancien chauffe-eau", "quantity": 1, "unit_price": 80, "tva_rate": 20},
)
DICTATION = (
    "Devis pour le Client fictif : remplacement d’un chauffe-eau de 200 litres. "
    "Fourniture : 450 euros hors taxes, pose : 250 euros hors taxes, "
    "dépose de l’ancien : 80 euros hors taxes. Une unité pour chaque ligne. "
    "Pour cet exemple uniquement, TVA à 20 %."
)

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


def render_example(app_store_url):
    rows = "\n".join(
        f'<tr><th scope="row">{escape(line["description"])}</th><td>1</td><td>{line["unit_price"]},00 €</td></tr>'
        for line in LINES
    )
    return f'''<section class="quote-proof" id="exemple-devis-plombier" aria-labelledby="quote-proof-title">
    <p class="proof-label">Exemple de démonstration · données fictives</p>
    <h2 id="quote-proof-title">Un devis de chauffe-eau, de la dictée au PDF à relire</h2>
    <p>Voici les informations à dicter, les lignes à vérifier et un PDF consultable sans installer l’app. Les montants servent à illustrer le parcours : ce ne sont pas des tarifs de marché.</p>
    <h3>1. Décrire les travaux et les montants</h3>
    <blockquote>{escape(DICTATION)}</blockquote>
    <h3>2. Relire le brouillon structuré</h3>
    <p>Client : <strong>Client fictif</strong>. Entreprise : <strong>Entreprise fictive — démonstration</strong>. Chantier : remplacement d’un chauffe-eau de 200 litres.</p>
    <table>
      <caption>Exemple de lignes à vérifier — quantité 1 par prestation</caption>
      <thead><tr><th scope="col">Prestation</th><th scope="col">Qté</th><th scope="col">Montant HT</th></tr></thead>
      <tbody>{rows}</tbody>
      <tfoot>
        <tr><th scope="row" colspan="2">Total HT</th><td>780,00 €</td></tr>
        <tr><th scope="row" colspan="2">TVA 20 % (hypothèse)</th><td>156,00 €</td></tr>
        <tr><th scope="row" colspan="2">Total TTC</th><td>936,00 €</td></tr>
      </tfoot>
    </table>
    <p class="proof-note">Le taux de 20 % est une hypothèse de calcul, pas un conseil fiscal. Le taux applicable à votre chantier dépend de sa situation et doit être vérifié avant partage.</p>
    <h3>3. Contrôler le PDF avant de le partager</h3>
    <a class="proof-download" href="/{PDF_PATH}" type="application/pdf">Consulter l’exemple de devis plombier en PDF</a>
    <p class="proof-note">PDF produit par le moteur PDF de Diqto à partir de données de démonstration préparées. La phrase ci-dessus illustre une dictée : elle n’a pas été transcrite par l’IA pour produire cet exemple. Ce document fictif n’est ni une offre commerciale ni un modèle juridique complet.</p>
    <ul>
      <li><strong>Avant le partage :</strong> corrigez les coordonnées, le matériel exact, les quantités, les prix et la TVA. Renseignez vos mentions d’entreprise, assurances et conditions adaptées.</li>
      <li><strong>Si le chantier change :</strong> ajustez les lignes et vérifiez de nouveau le total et le PDF avant de partager la version corrigée.</li>
      <li><strong>Après le chantier :</strong> reprenez le devis pour préparer la facture dans Diqto, avec les éventuels changements à relire. Cet exemple ne montre ni envoi client, ni acceptation, ni paiement.</li>
    </ul>
    <p><a href="/guides/devis-artisan-mentions-obligatoires.html">Voir les points à vérifier sur un devis artisan</a></p>
    <h3>Essayer avec votre propre chantier</h3>
    <p>Diqto Free : clients et brouillons illimités, 3 documents finalisés, exportés ou envoyés par mois, 3 vocaux courts par mois jusqu’à 1 minute. PDF avec footer Diqto ; 1 entreprise et 1 utilisateur. Aucun achat requis.</p>
    <p class="proof-note">Téléchargement gratuit sur iPhone, achats intégrés optionnels. <a href="/#tarifs">Consulter les formules et leurs limites</a>.</p>
    <a class="cta" href="{escape(app_store_url, quote=True)}" data-growth-placement="plombier-example">Télécharger Diqto gratuitement →</a>
  </section>'''
