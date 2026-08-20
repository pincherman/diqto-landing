(function initialiseEcPrescriberIntake() {
    var form = document.getElementById('ec-prescriber-intake');
    if (!form) return;

    var status = document.getElementById('ec-form-status');
    var submit = form.querySelector('button[type="submit"]');
    var offerLinks = document.querySelectorAll('[data-offer-choice]');
    var endpoint =
        'https://necessary-danila-diqto-7fbe88c8.koyeb.app'
        + '/api/public/starter-intake';

    function buildFirstNeed(data) {
        var tools = String(data.get('tools') || '').trim();
        var clientProblem = String(data.get('client_problem') || '').trim();
        var offer = String(data.get('partnership_offer') || '').trim();
        var offerLabel = offer || 'à qualifier après compatibilité';
        return [
            'Modèle envisagé : ' + offerLabel,
            'Outils du cabinet : ' + tools,
            'Cas client : ' + clientProblem,
        ].join(' | ').slice(0, 500);
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

    form.addEventListener('submit', async function submitEcPilot(event) {
        event.preventDefault();
        status.className = 'ec-form-status';
        if (!form.reportValidity()) return;

        submit.disabled = true;
        status.textContent = 'Envoi de votre demande pilote…';

        try {
            var data = new FormData(form);
            var response = await fetch(endpoint, {
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

            status.className = 'ec-form-status success';
            status.textContent = result.confirmation_email_sent
                ? 'Demande reçue. Un email de confirmation vient de vous '
                    + 'être envoyé.'
                : 'Demande reçue. L’email de confirmation n’a pas pu partir, '
                    + 'mais votre demande est bien enregistrée.';
            form.reset();
            if (window.diqtoGrowthTrack) {
                window.diqtoGrowthTrack(
                    'intake_submitted',
                    'intake',
                    'submitted',
                );
            }
        } catch (error) {
            status.className = 'ec-form-status error';
            status.textContent =
                'La demande n’a pas pu être envoyée. Réessayez ou écrivez '
                + 'à support@diqto.fr.';
        } finally {
            submit.disabled = false;
        }
    });
})();
