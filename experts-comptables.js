(function initialiseEcPrescriberIntake() {
    var form = document.getElementById('ec-prescriber-intake');
    if (!form) return;

    var status = document.getElementById('ec-form-status');
    var submit = form.querySelector('button[type="submit"]');
    var endpoint =
        'https://necessary-danila-diqto-7fbe88c8.koyeb.app'
        + '/api/public/starter-intake';

    function buildFirstNeed(data) {
        var tools = String(data.get('tools') || '').trim();
        var clientProblem = String(data.get('client_problem') || '').trim();
        return (
            'Outils du cabinet : ' + tools
            + ' | Client pilote : ' + clientProblem
        ).slice(0, 500);
    }

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
                    source: data.get('source'),
                    contact_consent:
                        data.get('contact_consent') === 'on',
                    website: data.get('website') || '',
                }),
            });

            if (!response.ok) throw new Error('request_failed');

            status.className = 'ec-form-status success';
            status.textContent =
                'Demande reçue. Nous étudierons d’abord vos outils et la '
                + 'situation que vous souhaitez simplifier.';
            form.reset();
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
