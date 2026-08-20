(function initialiseSiteShell() {
  var appStoreUrl = 'https://apps.apple.com/fr/app/diqto/id6761616034';
  var header = document.querySelector('.global-header');
  var toggle = document.querySelector('.global-menu-toggle');
  var menu = document.querySelector('.global-menu');

  if (!header || !toggle || !menu) return;

  function ensureAppStoreAnnouncement() {
    if (document.querySelector('.global-announcement')) return;

    var announcement = document.createElement('a');
    announcement.className = 'global-announcement';
    announcement.href = appStoreUrl;
    announcement.innerHTML = '<strong>Diqto 1.0 est disponible</strong>'
      + '<span>Télécharger sur l’App Store France '
      + '<span aria-hidden="true">→</span></span>';
    header.insertAdjacentElement('beforebegin', announcement);
  }

  ensureAppStoreAnnouncement();

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

  function ensureAccountantLink() {
    var existingLink = menu.querySelector(
      'a[href="/experts-comptables.html"]'
    );
    var accountantLink = existingLink || document.createElement('a');

    accountantLink.href = '/experts-comptables.html';
    accountantLink.textContent = 'Experts-comptables';
    if (window.location.pathname === '/experts-comptables.html') {
      accountantLink.setAttribute('aria-current', 'page');
    } else {
      accountantLink.removeAttribute('aria-current');
    }

    if (existingLink) return;

    var pricingLink = menu.querySelector(
      'a[href="/#tarifs"], a[href="#tarifs"]'
    );
    if (pricingLink) {
      pricingLink.insertAdjacentElement('beforebegin', accountantLink);
      return;
    }
    var ctaLink = menu.querySelector('.global-cta');
    if (ctaLink) {
      ctaLink.insertAdjacentElement('beforebegin', accountantLink);
      return;
    }
    menu.append(accountantLink);
  }

  ensureAccountantLink();

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
