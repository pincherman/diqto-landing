(function initialiseSiteShell() {
  var header = document.querySelector('.global-header');
  var toggle = document.querySelector('.global-menu-toggle');
  var menu = document.querySelector('.global-menu');

  if (!header || !toggle || !menu) return;

  function ensureStoriesLink() {
    if (menu.querySelector('a[href="/histoires.html"]')) return;

    var storiesLink = document.createElement('a');
    storiesLink.href = '/histoires.html';
    storiesLink.textContent = 'Histoires';
    if (window.location.pathname === '/histoires.html') {
      storiesLink.setAttribute('aria-current', 'page');
    }

    var featuresLink = menu.querySelector('a[href="/fonctionnalites.html"]');
    if (featuresLink) {
      featuresLink.insertAdjacentElement('afterend', storiesLink);
      return;
    }
    menu.prepend(storiesLink);
  }

  ensureStoriesLink();

  function setMenu(open) {
    header.dataset.menuOpen = String(open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.textContent = open ? 'Fermer' : 'Menu';
  }

  toggle.addEventListener('click', function toggleMenu() {
    setMenu(header.dataset.menuOpen !== 'true');
  });

  menu.addEventListener('click', function closeAfterNavigation(event) {
    if (event.target.closest('a')) setMenu(false);
  });

  document.addEventListener('keydown', function closeOnEscape(event) {
    if (event.key === 'Escape' && header.dataset.menuOpen === 'true') {
      setMenu(false);
      toggle.focus();
    }
  });

  document.addEventListener('click', function closeOutside(event) {
    if (header.dataset.menuOpen === 'true' && !header.contains(event.target)) {
      setMenu(false);
    }
  });
})();
