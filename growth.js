(function initialisePrivacySafeGrowth() {
    'use strict';

    var endpoint = 'https://necessary-danila-diqto-7fbe88c8.koyeb.app'
        + '/api/public/growth-event';
    var body = document.body;
    if (!body || !window.fetch) return;
    if (window.__diqtoGrowthInitialized) return;

    // BEGIN GENERATED WEBSITE PAGES
    var websitePages = {
    "/": "home",
    "/aide.html": "page_aide",
    "/carreleur.html": "metier_carreleur",
    "/cgu.html": "page_cgu",
    "/coach-sportif.html": "metier_coach_sportif",
    "/confidentialite.html": "page_confidentialite",
    "/docs.html": "page_docs",
    "/electricien.html": "metier_electricien",
    "/experts-comptables.html": "experts_comptables",
    "/facturation-electronique-conditions.html": "page_facturation_electronique_conditions",
    "/facturation-electronique.html": "page_facturation_electronique",
    "/fonctionnalites.html": "page_fonctionnalites",
    "/guides.html": "guides_index",
    "/guides/devis-artisan-mentions-obligatoires.html": "guide_devis_artisan_mentions_obligatoires",
    "/guides/facturation-electronique-micro-entreprise.html": "guide_facturation_electronique_micro_entreprise",
    "/guides/logiciel-devis-facture-artisan.html": "guide_logiciel_devis_facture_artisan",
    "/guides/logiciel-facturation-micro-entrepreneur.html": "guide_logiciel_facturation_micro_entrepreneur",
    "/guides/mentions-obligatoires-facture-micro-entrepreneur.html": "guide_mentions_obligatoires_facture_micro_entrepreneur",
    "/guides/pdf-email-facture-electronique.html": "guide_pdf_email_facture_electronique",
    "/histoires.html": "story_histoires",
    "/histoires/cabinet-expert-comptable.html": "story_cabinet_expert_comptable",
    "/histoires/claire-osteopathe.html": "story_claire_osteopathe",
    "/histoires/jean-luc-karate.html": "story_jean_luc_karate",
    "/histoires/marc-artisan.html": "story_marc_artisan",
    "/histoires/sarah-avocate.html": "story_sarah_avocate",
    "/index.html": "home",
    "/kinesitherapeute.html": "metier_kinesitherapeute",
    "/mentions-legales.html": "page_mentions_legales",
    "/menuisier.html": "metier_menuisier",
    "/metiers.html": "metiers_index",
    "/metiers/accastilleur.html": "metier_accastilleur",
    "/metiers/acupuncteur.html": "metier_acupuncteur",
    "/metiers/animateur.html": "metier_animateur",
    "/metiers/architecte.html": "metier_architecte",
    "/metiers/architecte_interieur.html": "metier_architecte_interieur",
    "/metiers/art_therapeute.html": "metier_art_therapeute",
    "/metiers/auto_ecole.html": "metier_auto_ecole",
    "/metiers/avocat.html": "metier_avocat",
    "/metiers/carreleur.html": "metier_carreleur",
    "/metiers/charpentier.html": "metier_charpentier",
    "/metiers/chauffagiste.html": "metier_chauffagiste",
    "/metiers/chiropracteur.html": "metier_chiropracteur",
    "/metiers/climatisation.html": "metier_climatisation",
    "/metiers/coach_sportif.html": "metier_coach_sportif",
    "/metiers/coiffeur.html": "metier_coiffeur",
    "/metiers/consultant.html": "metier_consultant",
    "/metiers/couvreur.html": "metier_couvreur",
    "/metiers/diagnostiqueur.html": "metier_diagnostiqueur",
    "/metiers/dieteticien.html": "metier_dieteticien",
    "/metiers/dog_groomer.html": "metier_dog_groomer",
    "/metiers/domotique.html": "metier_domotique",
    "/metiers/electricien.html": "metier_electricien",
    "/metiers/ergotherapeute.html": "metier_ergotherapeute",
    "/metiers/estheticienne.html": "metier_estheticienne",
    "/metiers/expert_comptable.html": "metier_expert_comptable",
    "/metiers/facade.html": "metier_facade",
    "/metiers/fleuriste.html": "metier_fleuriste",
    "/metiers/formateur.html": "metier_formateur",
    "/metiers/garagiste.html": "metier_garagiste",
    "/metiers/graphiste.html": "metier_graphiste",
    "/metiers/hypnotherapeute.html": "metier_hypnotherapeute",
    "/metiers/infirmier.html": "metier_infirmier",
    "/metiers/kine.html": "metier_kinesitherapeute",
    "/metiers/kinesiologue.html": "metier_kinesiologue",
    "/metiers/kinesitherapeute.html": "metier_kinesitherapeute",
    "/metiers/macon.html": "metier_macon",
    "/metiers/masseur.html": "metier_masseur",
    "/metiers/medecine_chinoise.html": "metier_medecine_chinoise",
    "/metiers/menuisier.html": "metier_menuisier",
    "/metiers/moniteur_ski.html": "metier_moniteur_ski",
    "/metiers/musicotherapeute.html": "metier_musicotherapeute",
    "/metiers/naturopathe.html": "metier_naturopathe",
    "/metiers/nettoyage.html": "metier_nettoyage",
    "/metiers/orthophoniste.html": "metier_orthophoniste",
    "/metiers/osteopathe.html": "metier_osteopathe",
    "/metiers/paysagiste.html": "metier_paysagiste",
    "/metiers/peintre.html": "metier_peintre",
    "/metiers/pet_sitter.html": "metier_pet_sitter",
    "/metiers/photographe.html": "metier_photographe",
    "/metiers/pisciniste.html": "metier_pisciniste",
    "/metiers/platrier.html": "metier_platrier",
    "/metiers/plombier.html": "metier_plombier",
    "/metiers/podologue.html": "metier_podologue",
    "/metiers/prof_danse.html": "metier_prof_danse",
    "/metiers/prof_karate.html": "metier_prof_karate",
    "/metiers/prof_langue.html": "metier_prof_langue",
    "/metiers/prof_musique.html": "metier_prof_musique",
    "/metiers/prof_natation.html": "metier_prof_natation",
    "/metiers/prof_yoga.html": "metier_professeur_yoga",
    "/metiers/psychologue.html": "metier_psychologue",
    "/metiers/ramoneur.html": "metier_ramoneur",
    "/metiers/reflexologue.html": "metier_reflexologue",
    "/metiers/sage_femme.html": "metier_sage_femme",
    "/metiers/serrurier.html": "metier_serrurier",
    "/metiers/sophrologue.html": "metier_sophrologue",
    "/metiers/tatoueur.html": "metier_tatoueur",
    "/metiers/terrassier.html": "metier_terrassier",
    "/metiers/traiteur.html": "metier_traiteur",
    "/metiers/veterinaire.html": "metier_veterinaire",
    "/osteopathe.html": "metier_osteopathe",
    "/peintre.html": "metier_peintre",
    "/photographe.html": "metier_photographe",
    "/plombier.html": "metier_plombier",
    "/professeur-yoga.html": "metier_professeur_yoga",
    "/reportage-premier-client-facturation-electronique.html": "page_reportage_premier_client_facturation_electronique"
};
    // END GENERATED WEBSITE PAGES
    var location = window.location;
    if (!location || !['diqto.fr', 'www.diqto.fr'].includes(location.hostname)) return;
    var page = websitePages[location.pathname];
    if (!page) return;
    window.__diqtoGrowthInitialized = true;

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

    var defaultSource = page === 'experts_comptables'
        ? 'expert_accountant' : 'direct_or_organic';
    var campaignSources = {
        artisan_concierge: true,
        facebook_post: true,
        facebook_reels: true,
        instagram_post: true,
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
        facebook_post: 'facebook',
        facebook_reels: 'facebook',
        instagram_post: 'instagram',
        instagram_reels: 'instagram',
        linkedin_video: 'linkedin',
        tiktok_video: 'tiktok',
        youtube_shorts: 'youtube',
    };
    var campaigns = {
        deuxieme_journee_s1_btp: true,
        preuve_produit_s1: true,
    };
    var campaignContents = {
        dictee_prete_v1: 'preuve_produit_s1',
        documents_controle_v1: 'preuve_produit_s1',
        ep01_plombier_v2: 'deuxieme_journee_s1_btp',
        ep02_electricien_v3: 'deuxieme_journee_s1_btp',
        ep03_couvreur_v1: 'deuxieme_journee_s1_btp',
        ep04_macon_v2: 'deuxieme_journee_s1_btp',
    };
    var source = defaultSource;
    var campaign = 'unknown';
    var content = 'unknown';

    function member(map, value) {
        return typeof value === 'string'
            && Object.prototype.hasOwnProperty.call(map, value);
    }

    function closedAttribution(candidate) {
        var candidateSource = member(campaignSources, candidate.source)
            ? candidate.source
            : defaultSource;
        var hasCompleteSocialCampaign = Boolean(
            socialCampaignSources[candidateSource]
            && candidate.utmSource === socialCampaignSources[candidateSource]
            && candidate.medium === 'organic_social'
            && member(campaigns, candidate.campaign)
            && member(campaignContents, candidate.content)
            && campaignContents[candidate.content] === candidate.campaign
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

    var placements = {
        announcement: true, header: true, hero: true, expert_entry: true,
        pricing: true, final_cta: true, intake: true, unknown: true,
    };
    var placementAliases = {
        final: 'final_cta', 'intent-evening': 'hero',
        hero_ec_demo: 'hero', offer_ec_demo: 'expert_entry',
    };
    var publicEvents = {
        landing_view: true, cta_click: true, appstore_outbound: true,
        intake_started: true, intake_submitted: true,
    };
    var publicStatuses = {
        viewed: true, started: true, submitted: true, unknown: true,
    };
    function closedPlacement(value) {
        var normalized = member(placementAliases, value) ? placementAliases[value] : value;
        return member(placements, normalized) ? normalized : 'unknown';
    }
    function track(eventName, placement, status) {
        if (!member(publicEvents, eventName)) return;
        var payload = {
            event_id: opaqueId('event'),
            session_id: sessionId,
            event: eventName,
            page: page,
            placement: closedPlacement(placement),
            source: source,
            campaign: campaign,
            content: content,
            status: member(publicStatuses, status) ? status : 'unknown',
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
        if (!event.target || typeof event.target.closest !== 'function') return;
        var target = event.target.closest('a[href], [data-growth-placement]');
        if (!target) return;
        var href = target.getAttribute('href') || '';
        var isAppStore = false;
        try {
            var destination = new URL(href, location.origin);
            isAppStore = destination.protocol === 'https:'
                && destination.hostname === 'apps.apple.com'
                && /\/id6761616034\/?$/.test(destination.pathname);
        } catch (_error) {}
        var placement = target.getAttribute('data-growth-placement');
        if (!isAppStore && !placement) return;
        if (!placement && target.closest('.global-announcement')) placement = 'announcement';
        if (!placement && target.closest('.global-header')) placement = 'header';
        if (!placement && target.closest('footer')) placement = 'final_cta';
        track(isAppStore ? 'appstore_outbound' : 'cta_click', placement, 'started');
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
