const fs = require('fs');
const path = require('path');

const files = ['confidentialite.html', 'legal/PRIVACY.md'];
const requiredDisclosures = [
  'OpenAI',
  'Anthropic',
  'Deepgram',
  'Continuer sans IA',
  'Réglages → Données',
];

for (const file of files) {
  const content = fs.readFileSync(path.join(__dirname, file), 'utf8');
  for (const disclosure of requiredDisclosures) {
    if (!content.includes(disclosure)) {
      throw new Error(`${file}: missing Apple AI-consent disclosure: ${disclosure}`);
    }
  }
}

console.log('PASS Apple AI-consent privacy contract');
