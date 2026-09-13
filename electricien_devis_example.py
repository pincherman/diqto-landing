"""Original electrician quote fixture: illustrative scope, never a compliance claim."""

from html import escape
from quote_example_common import CSS, euro, quote_totals, render_rows

TRADE = "electricien"
PDF_PATH = "assets/examples/devis-electricien-tableau-demonstration.pdf"
DOCUMENT_NUMBER = "DEMO-ELECTRICIEN-001"
PDF_TITLE = "DEMONSTRATION - Devis electricien fictif - aucune somme due"
LINES = (
    {"description": "Fourniture du coffret et des équipements du tableau", "quantity": 1, "unit_price": 360, "tva_rate": 20},
    {"description": "Pose et raccordement du tableau", "quantity": 1, "unit_price": 240, "tva_rate": 20},
    {"description": "Repérage des circuits existants", "quantity": 1, "unit_price": 90, "tva_rate": 20},
)
DICTATION = (
    "Prépare un devis pour le Client fictif : remplacement d’un tableau électrique. "
    "Fourniture du coffret et de ses équipements : 360 euros HT. "
    "Pose et raccordement : 240 euros HT. Repérage des circuits existants : 90 euros HT. "
    "Une unité par ligne. Pour ce calcul d’exemple uniquement, TVA à 20 %. "
    "Le matériel exact et le périmètre des travaux restent à vérifier."
)
EXTRA_NOTES = (
    "A verifier : references et quantites du materiel, circuits concernes, travaux inclus et exclus. "
    "Cet exemple ne certifie ni la securite ni la conformite d'une installation."
)


def render_example(app_store_url):
    total_ht, total_tva, total_ttc = quote_totals(LINES)
    return f'''<section class="quote-proof" id="exemple-devis-electricien" aria-labelledby="quote-proof-title">
    <p class="proof-label">Exemple de démonstration · données fictives</p>
    <h2 id="quote-proof-title">Un devis électricien pour remplacer un tableau</h2>
    <p>Le matériel, la pose et le repérage des circuits n’ont pas le même rôle dans votre devis. Cet exemple montre comment les distinguer et quels détails préciser avant de partager le document. Les montants sont illustratifs, pas des tarifs de marché.</p>
    <h3>1. Préparer les informations à dicter</h3>
    <blockquote>{escape(DICTATION)}</blockquote>
    <h3>2. Distinguer les fournitures et l’intervention</h3>
    <p>Client : <strong>Client fictif</strong>. Entreprise : <strong>Entreprise fictive - démonstration</strong>. Cas : remplacement d’un tableau électrique, périmètre à préciser.</p>
    <table>
      <caption>Trois lignes à relire - quantité 1 par poste dans cet exemple</caption>
      <thead><tr><th scope="col">Poste</th><th scope="col">Qté</th><th scope="col">Montant HT</th></tr></thead>
      <tbody>{render_rows(LINES)}</tbody>
      <tfoot>
        <tr><th scope="row" colspan="2">Total HT</th><td>{euro(total_ht)}</td></tr>
        <tr><th scope="row" colspan="2">TVA 20 % (hypothèse)</th><td>{euro(total_tva)}</td></tr>
        <tr><th scope="row" colspan="2">Total TTC</th><td>{euro(total_ttc)}</td></tr>
      </tfoot>
    </table>
    <p class="proof-note">La TVA à 20 % sert uniquement à montrer le calcul. Vérifiez le taux applicable à votre intervention avant de finaliser. Ce document ne certifie ni la sécurité ni la conformité d’une installation électrique.</p>
    <h3>3. Compléter ce que les trois lignes ne disent pas</h3>
    <ul>
      <li><strong>Matériel :</strong> indiquez les références, les quantités et les équipements réellement prévus. « Coffret et équipements » est un libellé de démonstration, pas une liste de fournitures complète.</li>
      <li><strong>Périmètre :</strong> précisez les circuits concernés et les travaux inclus ou exclus. Ne présentez pas le remplacement du tableau comme une rénovation complète de l’installation.</li>
      <li><strong>Avant partage :</strong> vérifiez les coordonnées, vos mentions d’entreprise, les conditions, les prix et la TVA. Si le diagnostic change le périmètre, corrigez le devis puis relisez son PDF.</li>
    </ul>
    <h3>4. Examiner le PDF généré par Diqto</h3>
    <a class="proof-download" href="/{PDF_PATH}" type="application/pdf">Consulter l’exemple de devis électricien en PDF</a>
    <p class="proof-note">Ce PDF a été généré par Diqto avec les données fictives préparées ci-dessus. La phrase de dictée est une aide : elle n’a pas été transcrite par l’IA pour produire ce PDF. L’exemple ne montre ni signature, ni envoi client, ni paiement ; aucune somme n’est due. Ce n’est ni une offre commerciale ni un modèle juridique complet.</p>
    <p><a href="/guides/logiciel-devis-facture-artisan.html">Comparer le parcours et les plans Diqto pour artisan</a> · <a href="/guides/devis-artisan-mentions-obligatoires.html">Consulter les points à vérifier sur un devis artisan</a></p>
    <h3>Préparer votre premier document</h3>
    <p><a href="/docs.html#premiere-dictee">Copiez une trame de dictée et suivez les étapes dans l’app</a>. Diqto Free : 3 documents par mois pour essayer. Dans le parcours actuel, les nouveaux brouillons enregistrés comptent dans ce quota. Aucun achat requis.</p>
    <p class="proof-note">Téléchargement gratuit sur iPhone, achats intégrés optionnels. <a href="/#tarifs">Consulter les formules et leurs limites</a>.</p>
    <a class="cta" href="{escape(app_store_url, quote=True)}" data-growth-placement="final_cta">Télécharger Diqto gratuitement →</a>
  </section>'''
