(function initialisePrivacySafeGrowth() {
    'use strict';

    var endpoint = 'https://necessary-danila-diqto-7fbe88c8.koyeb.app'
        + '/api/public/growth-event';
    var body = document.body;
    if (!body || !window.fetch) return;

    function opaqueId(prefix) {
        var random = window.crypto && window.crypto.randomUUID
            ? window.crypto.randomUUID().replace(/-/g, '')
            : Math.random().toString(36).slice(2) + Date.now().toString(36);
        return prefix + '_' + random;
    }

    var sessionId;
    try {
        sessionId = window.sessionStorage.getItem('diqto_growth_session_v1');
        if (!sessionId) {
            sessionId = opaqueId('session');
            window.sessionStorage.setItem('diqto_growth_session_v1', sessionId);
        }
    } catch (_error) {
        sessionId = opaqueId('session');
    }

    var page = body.getAttribute('data-growth-page') || 'unknown';
    var source = body.getAttribute('data-growth-source') || 'unknown';

    function track(eventName, placement, status) {
        var payload = {
            event_id: opaqueId('event'),
            session_id: sessionId,
            event: eventName,
            page: page,
            placement: placement || 'unknown',
            source: source,
            status: status || 'unknown',
        };
        window.fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
            keepalive: true,
            credentials: 'omit',
        }).catch(function ignoreGrowthFailure() {});
    }

    window.diqtoGrowthTrack = track;
    track('landing_view', 'hero', 'viewed');

    document.addEventListener('click', function trackGrowthClick(event) {
        var target = event.target.closest('[data-growth-placement]');
        if (!target) return;
        var href = target.getAttribute('href') || '';
        var eventName = href.indexOf('apps.apple.com') !== -1
            ? 'appstore_outbound'
            : 'cta_click';
        track(eventName, target.getAttribute('data-growth-placement'), 'started');
    });

    document.querySelectorAll('form[data-growth-form]').forEach(function bindForm(form) {
        var started = false;
        form.addEventListener('focusin', function trackFirstFormInteraction() {
            if (started) return;
            started = true;
            track('intake_started', 'intake', 'started');
        });
    });
})();
