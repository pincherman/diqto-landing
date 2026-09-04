(function initialiseEcPrescriberIntake() {
    var form = document.getElementById('ec-prescriber-intake');
    if (!form) return;

    var intakeStatus = document.getElementById('ec-form-status');
    var qualificationStatus = document.getElementById(
        'ec-qualification-status',
    );
    var qualificationButton = document.getElementById('ec-qualify-stack');
    var qualificationResult = document.getElementById(
        'ec-qualification-result',
    );
    var qualificationTitle = document.getElementById(
        'ec-qualification-title',
    );
    var qualificationDecision = document.getElementById(
        'ec-qualification-decision',
    );
    var qualificationSteps = document.getElementById(
        'ec-qualification-steps',
    );
    var qualificationPartner = document.getElementById(
        'ec-qualification-partner',
    );
    var qualificationNext = document.getElementById(
        'ec-qualification-next',
    );
    var qualificationSummary = form.querySelector(
        'input[name="qualification_summary"]',
    );
    var contactStage = document.getElementById('ec-contact-stage');
    var submit = form.querySelector('button[type="submit"]');
    var offerLinks = document.querySelectorAll('[data-offer-choice]');
    var apiRoot = 'https://necessary-danila-diqto-7fbe88c8.koyeb.app';
    var qualificationEndpoint = apiRoot
        + '/api/public/ec-stack-qualification';
    var intakeEndpoint = apiRoot + '/api/public/starter-intake';
    var paLabels = {
        chosen: 'PA déjà choisie',
        selection_in_progress: 'PA en cours d’évaluation',
        not_chosen: 'aucune PA choisie',
        unknown: 'statut PA à identifier',
    };
    var softwareLabels = {
        api_documented: 'API documentée',
        structured_export: 'export structuré',
        manual_only: 'manipulation manuelle uniquement',
        unknown: 'sortie à identifier',
    };
    var gedLabels = {
        integrated: 'dépôt intégré',
        api_documented: 'API documentée',
        structured_export: 'échange structuré',
        manual_only: 'dépôt manuel uniquement',
        none: 'aucune GED',
        unknown: 'accès GED à identifier',
    };
    var clientTypeLabels = {
        artisan: 'artisan',
        profession_liberale: 'profession libérale',
        commerce: 'commerce',
        services: 'entreprise de services',
        association: 'association',
        other: 'autre catégorie',
    };
    var issueLabels = {
        late_documents: 'pièces reçues trop tard',
        manual_reentry: 'ressaisie manuelle',
        duplicate_deposit: 'dépôts en double',
        status_tracking: 'suivi des pièces difficile',
        other: 'autre difficulté',
    };

    function clearStatus(target) {
        target.className = 'ec-form-status';
        target.textContent = '';
    }

    function hideQualification() {
        qualificationSummary.value = '';
        qualificationResult.hidden = true;
        contactStage.disabled = true;
        contactStage.hidden = true;
        clearStatus(qualificationStatus);
    }

    function buildQualificationPayload(data) {
        return {
            software_access: data.get('software_access'),
            document_management_access: data.get(
                'document_management_access',
            ),
            pa_status: data.get('pa_status'),
            client_type: data.get('client_type'),
            workflow_issue: data.get('workflow_issue'),
            country_code: 'FR',
        };
    }

    function renderQualification(assessment) {
        qualificationTitle.textContent = assessment.headline;
        qualificationDecision.textContent = assessment.decision;
        qualificationSteps.textContent = '';
        assessment.steps.forEach(function appendStep(step) {
            var item = document.createElement('li');
            var label = document.createElement('strong');
            var state = document.createElement('span');
            label.textContent = step.label;
            state.textContent = step.status === 'to_identify'
                ? 'À identifier'
                : 'À vérifier';
            item.append(label, state);
            qualificationSteps.appendChild(item);
        });
        var partnerNote = assessment.pa_route.partner_note;
        qualificationPartner.hidden = !partnerNote;
        qualificationPartner.textContent = partnerNote || '';
        qualificationNext.textContent = assessment.pilot_gate.next_step;
        qualificationSummary.value = assessment.intake_summary;
        qualificationResult.hidden = false;
        contactStage.disabled = false;
        contactStage.hidden = false;
        qualificationResult.focus();
    }

    function buildFirstNeed(data) {
        var offer = String(data.get('partnership_offer') || '').trim();
        var offerLabels = {
            free_accountant_access: 'accès cabinet gratuit',
            one_client_pilot: 'pilote sur un client volontaire',
        };
        var parts = [
            'Modèle envisagé : '
                + (offerLabels[offer] || 'à qualifier après compatibilité'),
            'Sortie logiciel : '
                + (softwareLabels[data.get('software_access')] || 'à qualifier'),
            'GED : '
                + (gedLabels[data.get('document_management_access')]
                    || 'à qualifier'),
            'PA : ' + (paLabels[data.get('pa_status')] || 'à qualifier'),
            'Type de client : '
                + (clientTypeLabels[data.get('client_type')] || 'à qualifier'),
            'Difficulté : '
                + (issueLabels[data.get('workflow_issue')] || 'à qualifier'),
            String(data.get('qualification_summary') || '').trim(),
        ];
        return parts.filter(Boolean).join(' | ').slice(0, 500);
    }

    offerLinks.forEach(function bindOfferChoice(link) {
        link.addEventListener('click', function chooseOffer() {
            var value = link.getAttribute('data-offer-choice');
            var offerInput = form.querySelector(
                'input[name="partnership_offer"]',
            );
            if (offerInput) offerInput.value = value;
        });
    });

    form.querySelectorAll('#ec-qualification-stage select').forEach(
        function bindQualificationInvalidation(input) {
            input.addEventListener('input', hideQualification);
            input.addEventListener('change', hideQualification);
        },
    );

    qualificationButton.addEventListener(
        'click',
        async function qualifyStack() {
            hideQualification();
            clearStatus(intakeStatus);
            if (!form.reportValidity()) return;

            qualificationButton.disabled = true;
            qualificationStatus.textContent = 'Qualification du chemin…';

            try {
                var data = new FormData(form);
                var response = await fetch(qualificationEndpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(buildQualificationPayload(data)),
                });
                if (!response.ok) {
                    if (response.status === 422) throw new Error('invalid_category');
                    throw new Error('qualification_failed');
                }
                var result = await response.json();
                if (result.assessment.status !== 'qualification_required') {
                    throw new Error('invalid_qualification_contract');
                }

                renderQualification(result.assessment);
                qualificationStatus.className = 'ec-form-status success';
                qualificationStatus.textContent =
                    'Pré-diagnostic terminé. Aucun email n’a été demandé.';
                if (window.diqtoGrowthTrack) {
                    window.diqtoGrowthTrack(
                        'ec_stack_qualified',
                        'ec_preflight',
                        result.assessment.pa_route.status,
                    );
                }
            } catch (error) {
                qualificationStatus.className = 'ec-form-status error';
                qualificationStatus.textContent = error.message
                    === 'invalid_category'
                    ? 'Choisissez une catégorie pour chaque étape, puis réessayez.'
                    : 'Le pré-diagnostic est indisponible. Aucune donnée n’a été enregistrée.';
            } finally {
                qualificationButton.disabled = false;
            }
        },
    );

    form.addEventListener('submit', async function submitEcPilot(event) {
        event.preventDefault();
        clearStatus(intakeStatus);
        if (!qualificationSummary.value) {
            intakeStatus.className = 'ec-form-status error';
            intakeStatus.textContent =
                'Qualifiez d’abord le chemin avant de demander un cadrage.';
            qualificationButton.focus();
            return;
        }
        if (!form.reportValidity()) return;

        submit.disabled = true;
        intakeStatus.textContent = 'Envoi de votre demande de cadrage…';

        try {
            var data = new FormData(form);
            var response = await fetch(intakeEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: data.get('email'),
                    trade: data.get('trade'),
                    first_need: buildFirstNeed(data),
                    source: String(data.get('source') || '').slice(0, 120),
                    contact_consent:
                        data.get('contact_consent') === 'on',
                    website: data.get('website') || '',
                }),
            });

            if (!response.ok) throw new Error('request_failed');
            var result = await response.json();

            intakeStatus.className = 'ec-form-status success';
            intakeStatus.textContent = result.confirmation_email_sent
                ? 'Demande reçue. Un email de confirmation vient de vous '
                    + 'être envoyé.'
                : 'Demande reçue. L’email de confirmation n’a pas pu partir, '
                    + 'mais votre demande est bien enregistrée.';
            form.reset();
            qualificationSummary.value = '';
            qualificationResult.hidden = true;
            contactStage.disabled = true;
            contactStage.hidden = true;
            clearStatus(qualificationStatus);
            if (window.diqtoGrowthTrack) {
                window.diqtoGrowthTrack(
                    'intake_submitted',
                    'intake',
                    'submitted',
                );
            }
        } catch (_error) {
            intakeStatus.className = 'ec-form-status error';
            intakeStatus.textContent =
                'La demande n’a pas pu être envoyée. Réessayez ou écrivez '
                + 'à support@diqto.fr.';
        } finally {
            submit.disabled = false;
        }
    });
})();
