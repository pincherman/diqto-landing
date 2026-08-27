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
    var defaultSource = body.getAttribute('data-growth-source') || 'unknown';
    var campaignSources = {
        artisan_concierge: true,
        facebook_reels: true,
        instagram_reels: true,
        linkedin_carousel: true,
        linkedin_founder_comment: true,
        linkedin_founder_launch: true,
        linkedin_profile: true,
        linkedin_video: true,
        tiktok_video: true,
        youtube_shorts: true,
    };
    var socialCampaignSources = {
        facebook_reels: 'facebook',
        instagram_reels: 'instagram',
        linkedin_video: 'linkedin',
        tiktok_video: 'tiktok',
        youtube_shorts: 'youtube',
    };
    var campaigns = {
        deuxieme_journee_s1_btp: true,
    };
    var campaignContents = {
        ep01_plombier_v2: true,
        ep02_electricien_v3: true,
        ep03_couvreur_v1: true,
        ep04_macon_v2: true,
    };
    var source = defaultSource;
    var campaign = 'unknown';
    var content = 'unknown';

    function closedAttribution(candidate) {
        var candidateSource = campaignSources[candidate.source]
            ? candidate.source
            : defaultSource;
        var hasCompleteSocialCampaign = Boolean(
            socialCampaignSources[candidateSource]
            && candidate.utmSource === socialCampaignSources[candidateSource]
            && candidate.medium === 'organic_social'
            && campaigns[candidate.campaign]
            && campaignContents[candidate.content]
        );
        return {
            source: candidateSource,
            campaign: hasCompleteSocialCampaign
                ? candidate.campaign
                : 'unknown',
            content: hasCompleteSocialCampaign
                ? candidate.content
                : 'unknown',
        };
    }

    try {
        var params = new URLSearchParams(window.location.search);
        var hasRequestedAttribution = [
            'source', 'utm_source', 'utm_medium',
            'utm_campaign', 'utm_content',
        ].some(function hasParam(name) {
            return params.has(name);
        });
        var attribution;
        if (hasRequestedAttribution) {
            attribution = closedAttribution({
                source: params.get('source'),
                utmSource: params.get('utm_source'),
                medium: params.get('utm_medium'),
                campaign: params.get('utm_campaign'),
                content: params.get('utm_content'),
            });
            window.sessionStorage.setItem(
                'diqto_growth_attribution_v1',
                JSON.stringify(attribution)
            );
        } else {
            var storedAttribution = JSON.parse(
                window.sessionStorage.getItem(
                    'diqto_growth_attribution_v1'
                ) || '{}'
            );
            attribution = closedAttribution({
                source: storedAttribution.source,
                utmSource: socialCampaignSources[storedAttribution.source],
                medium: storedAttribution.campaign
                    ? 'organic_social'
                    : '',
                campaign: storedAttribution.campaign,
                content: storedAttribution.content,
            });
        }
        source = attribution.source;
        campaign = attribution.campaign;
        content = attribution.content;
    } catch (_error) {
        source = defaultSource;
        campaign = 'unknown';
        content = 'unknown';
    }

    function track(eventName, placement, status) {
        var payload = {
            event_id: opaqueId('event'),
            session_id: sessionId,
            event: eventName,
            page: page,
            placement: placement || 'unknown',
            source: source,
            campaign: campaign,
            content: content,
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
