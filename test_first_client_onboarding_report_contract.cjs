#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const root = __dirname;
const report = fs.readFileSync(
  path.join(root, 'reportage-premier-client-facturation-electronique.html'),
  'utf8',
);
const hub = fs.readFileSync(
  path.join(root, 'facturation-electronique.html'),
  'utf8',
);

const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

assert(
  report.includes('<article>')
    && report.includes('<nav class="story-index"')
    && report.includes('aria-label="Chapitres du reportage"')
    && report.includes('class="global-skip-link"'),
  'report must use semantic article, chapter navigation and skip link',
);

for (let step = 1; step <= 7; step += 1) {
  assert(
    report.includes(`id="chapitre-${step}" data-step="${step}"`),
    `report must expose chapter ${step}`,
  );
}

for (const marker of [
  'Consentement',
  'Mandat',
  'KYC / KYB',
  'DGFiP',
  'Annuaire',
  'Coordonnées bancaires',
  'Confirmer l’envoi réglementaire',
]) {
  assert(report.includes(marker), `report must expose gate: ${marker}`);
}

assert(
  report.includes('Aucune transmission avant validation humaine')
    && report.includes('aucune transmission automatique')
    && report.includes('B2Brouter · PA')
    && report.includes('Diqto reste la solution'),
  'report must preserve human confirmation and exact Diqto/B2Brouter roles',
);

assert(
  report.includes('Données 100 % fictives')
    && report.includes('ENTREPRISE FICTIVE')
    && report.includes('SIREN DE DÉMONSTRATION')
    && report.includes('IBAN masqué')
    && !report.includes('Philippe Incherman'),
  'report must be synthetic and must not expose personal data',
);

assert(
  report.includes('@media (max-width: 980px)')
    && report.includes('@media (max-width: 680px)')
    && report.includes('@media (prefers-reduced-motion: reduce)')
    && report.includes(':focus-visible'),
  'report must cover responsive, reduced-motion and keyboard focus states',
);

assert(
  report.includes('https://diqto.fr/reportage-premier-client-facturation-electronique.html')
    && report.includes('"@type": "Article"')
    && hub.includes('/reportage-premier-client-facturation-electronique.html'),
  'report must be canonical, structured and linked from the e-invoicing hub',
);

console.log('PASS first-client e-invoicing onboarding report contract');
