(function initialiseStarterPrompts() {
  'use strict';
  var panel = document.getElementById('premiere-dictee');
  if (!panel || panel.dataset.copyReady) return;
  panel.dataset.copyReady = 'true';
  panel.addEventListener('click', async function copyPrompt(event) {
    var button = event.target.closest('button[data-copy-prompt]');
    if (!button || !panel.contains(button)) return;
    var prompt = document.getElementById(button.dataset.copyPrompt);
    var status = panel.querySelector('[role="status"]');
    if (!prompt || !panel.contains(prompt) || !status) return;
    try {
      if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error('unavailable');
      await navigator.clipboard.writeText(prompt.textContent.trim());
      status.textContent = 'Trame copiée. Remplacez les éléments entre crochets avant de la dicter dans Diqto.';
    } catch (_) {
      status.textContent = 'La copie automatique est indisponible. Vous pouvez sélectionner et copier le texte affiché ci-dessus.';
    }
  });
}());
