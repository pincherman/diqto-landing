"""Canonical, explicitly synthetic quote example for the plumber landing page."""

from html import escape
from quote_example_common import CSS, render_rows

TRADE = "plombier"
PDF_TITLE = "DEMONSTRATION - Devis plombier fictif - aucune somme due"
EXTRA_NOTES = ""

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




def render_example(app_store_url):
    rows = render_rows(LINES)
    return f'''<section class="quote-proof" id="exemple-devis-plombier" aria-labelledby="quote-proof-title">
    <p class="proof-label">Exemple de démonstration · données fictives</p>
    <h2 id="quote-proof-title">Un devis de chauffe-eau, de la dictée au PDF à relire</h2>
    <p>Voici les informations à dicter, les lignes à vérifier et un PDF consultable sans installer l’app. Les montants servent à illustrer le parcours : ce ne sont pas des tarifs de marché.</p>
    <h3>1. Décrire les travaux et les montants</h3>
    <blockquote>{escape(DICTATION)}</blockquote>
    <h3>2. Relire le brouillon structuré</h3>
    <p>Client : <strong>Client fictif</strong>. Entreprise : <strong>Entreprise fictive - démonstration</strong>. Chantier : remplacement d’un chauffe-eau de 200 litres.</p>
    <table>
      <caption>Exemple de lignes à vérifier - quantité 1 par prestation</caption>
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
    <p class="proof-note">PDF généré par Diqto à partir de données de démonstration préparées. La phrase ci-dessus illustre une dictée : elle n’a pas été transcrite par l’IA pour produire cet exemple. Ce document fictif n’est ni une offre commerciale ni un modèle juridique complet.</p>
    <ul>
      <li><strong>Avant le partage :</strong> corrigez les coordonnées, le matériel exact, les quantités, les prix et la TVA. Renseignez vos mentions d’entreprise, assurances et conditions adaptées.</li>
      <li><strong>Si le chantier change :</strong> ajustez les lignes et vérifiez de nouveau le total et le PDF avant de partager la version corrigée.</li>
      <li><strong>Après le chantier :</strong> reprenez le devis pour préparer la facture dans Diqto, avec les éventuels changements à relire. Cet exemple ne montre ni envoi client, ni acceptation, ni paiement.</li>
    </ul>
    <p><a href="/guides/devis-artisan-mentions-obligatoires.html">Voir les points à vérifier sur un devis artisan</a></p>
    <h3>Essayer avec votre propre chantier</h3>
    <p>Diqto Free : 3 documents par mois pour essayer. Dans le parcours actuel, les nouveaux brouillons enregistrés comptent dans ce quota. Aucun achat requis. <a href="/docs.html#premiere-dictee">Préparez votre première dictée avec une trame à copier</a>.</p>
    <p class="proof-note">Téléchargement gratuit sur iPhone, achats intégrés optionnels. <a href="/#tarifs">Consulter les formules et leurs limites</a>.</p>
    <a class="cta" href="{escape(app_store_url, quote=True)}" data-growth-placement="final_cta">Télécharger Diqto gratuitement →</a>
  </section>'''
