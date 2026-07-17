(function initialiseSiteShell() {
  var header = document.querySelector('.global-header');
  var toggle = document.querySelector('.global-menu-toggle');
  var menu = document.querySelector('.global-menu');

  if (!header || !toggle || !menu) return;

  function ensureEInvoicingAnnouncement() {
    if (document.querySelector('.global-announcement')) return;

    var announcement = document.createElement('a');
    announcement.className = 'global-announcement';
    announcement.href = '/guides/facturation-electronique-micro-entreprise.html';
    announcement.innerHTML = '<strong>Facturation électronique</strong>'
      + '<span>Ce qui change en 2026 et 2027 '
      + '<span aria-hidden="true">→</span></span>';
    header.insertAdjacentElement('beforebegin', announcement);
  }

  ensureEInvoicingAnnouncement();

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

  function setBetaSource(link, source) {
    if (!link || link.getAttribute('href') !== '/#beta') return;
    link.setAttribute('href', '/?source=' + encodeURIComponent(source) + '#beta');
  }

  function tagConsentlessConversionPaths() {
    var path = window.location.pathname;

    if (path === '/guides.html') {
      Array.prototype.forEach.call(
        document.querySelectorAll('a[href="/#beta"]'),
        function tagGuideCta(link) {
          setBetaSource(link, 'seo_guides_hub_cta');
        }
      );
      return;
    }

    if (path !== '/histoires.html') return;

    setBetaSource(menu.querySelector('.global-cta'), 'seo_stories_nav');

    Array.prototype.forEach.call(
      document.querySelectorAll('.story-card a[href="/#beta"]'),
      function tagStoryCta(link) {
        var storyCard = link.closest('.story-card');
        if (!storyCard || !storyCard.id) return;
        setBetaSource(link, 'seo_story_' + storyCard.id.replace(/-/g, '_'));
      }
    );

    setBetaSource(
      document.querySelector('.story-final a[href="/#beta"]'),
      'seo_stories_final_cta'
    );
  }

  tagConsentlessConversionPaths();

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
