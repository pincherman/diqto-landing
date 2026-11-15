# M20 : inventaire public GitHub Pages

Lecture : 15/11/2026, via web.run. Skill forge-software-delivery lu. Sources publiques officielles uniquement. Aucun accès/écriture dépôt, publication, contact externe ou contrôle de preuve Philippe.

## Périmètre

Entrée du mandat, non preuve de déploiement : décision Claude du 15 novembre 2026 d'héberger la politique de retrait sous diqto.fr/mitonna/, via GitHub Pages et diqto-landing. DNS, dépôt, compte, contrat, page publiée et trafic applicatif non inspectés.

## Sources canoniques, toutes lues le 15/11/2026

- S1 : What is GitHub Pages?, About / Data collection / custom domain.
  https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
- S2 : GitHub General Privacy Statement, date d'effet affichée 27 avril 2026 ; Automatically / Your Privacy Rights / International data transfers / Security and Retention.
  https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement
- S3 : GitHub Subprocessors, introduction et tableau.
  https://docs.github.com/en/site-policy/privacy-policies/github-subprocessors
- S4 : GitHub Data Protection Agreement, version affichée October 2025 ; §§3, 7, 8, 9.
  https://github.com/customer-terms/github-data-protection-agreement
- S5 : Fastly, étude client GitHub, passages Pages.
  https://www.fastly.com/customers/github
- S6 : GitHub Terms of Service, M.2 Upon Cancellation.
  https://docs.github.com/en/site-policy/github-terms/github-terms-of-service

S4 est le lien suivi depuis S2. L'ancien chemin docs.github.com/en/site-policy/privacy-policies/github-data-protection-agreement redirige vers l'index : ne pas le citer comme DPA. Les PDF historiques 2022 trouvés ne fondent pas cet inventaire.

## GET métier et traces réseau

Pages héberge des fichiers statiques depuis un dépôt, avec domaine personnalisé possible. GitHub indique explicitement enregistrer et conserver l'IP du visiteur pour la sécurité, même sans connexion à GitHub. [S1]

Le GET prévu sans recettes, profil, compte ou contenu métier Mitonna est un objectif du mandat, pas un comportement vérifié. Il ne signifie pas absence de données personnelles : S2 décrit généralement IP, appareil/session, horodatage, référent et pages consultées. La liste générale n'établit pas tous les champs reçus ou enregistrés à chaque visite Pages. [S1, S2]

En-têtes exacts User-Agent/Referer, cookies, paramètres URL, scripts tiers, ouverture WebView/navigateur et éventuel canal de demande de retrait : non vérifiés. Ne pas annoncer « aucune collecte » ni affirmer la journalisation systématique de chaque en-tête.

## Durées et sauvegardes

Durée exacte des IP/journaux de sécurité Pages : NON PRÉCISÉE par S1/S2. S2 donne des critères généraux : activité du compte, nécessité contractuelle/légale et litiges. Cela ne chiffre pas la rétention d'une visite anonyme. [S1, S2]

S6 prévoit, sous réserves légales, suppression du profil complet et du contenu des dépôts dans les 90 jours après annulation/résiliation ; certaines informations peuvent subsister dans des sauvegardes chiffrées. Ce délai ne concerne pas explicitement les IP Pages. Aucun délai d'expiration de ces sauvegardes, fréquence ou localisation n'y est précisé. Ne pas transformer ces 90 jours en durée IP/cache/sauvegarde Pages. [S6]

S4 §8 prévoit restitution ou suppression en fin de service quand GitHub est sous-traitant, avec suppression des copies selon sa politique, sauf interdiction légale ; aucun délai chiffré dans ce paragraphe. [S4]

## CDN et régions

S3 liste Fastly et Cloudflare pour la diffusion de contenu, avec « United States » comme lieu de traitement. Sa portée annoncée concerne les clients Enterprise et les services régis par le DPA. Ce tableau n'est pas un inventaire propre à diqto.fr. Il ne prouve ni Cloudflare actif sur cette cible, ni tous les points CDN uniquement américains. [S3]

L'étude officielle Fastly décrit un CDN/cache devant Pages et les domaines personnalisés. Son contenu utile non daté et ses chiffres anciens en limitent la portée : relation documentée, pas preuve du routage actuel ou exclusif de diqto.fr/mitonna/. TTL du cache non établi. [S5]

S2 décrit des traitements dans plusieurs pays, dont les États-Unis ; S4 §7 prévoit des transferts internationaux avec DPF et/ou clauses contractuelles types selon le cas. Aucune résidence France/UE démontrée. Régions effectives d'origine, journaux, sauvegardes et point CDN : NON ÉTABLIES pour cette cible. [S2, S4]

## Rôle et droits selon la finalité

S4 §3.A/B distingue GitHub sous-traitant pour les instructions client de fourniture/maintenance ; sous-traitant ultérieur si le client est lui-même sous-traitant. §3.C le décrit responsable indépendant pour ses finalités propres, dont compte/facturation, obligations légales, anti-abus/protection et statistiques agrégées internes. [S4]

Interprétation conditionnelle : la sécurité Pages annoncée par S1 est compatible avec la finalité anti-abus propre de S4, sans qualification explicite de chaque journal IP Pages. Ne pas présenter GitHub comme toujours sous-traitant, ni toujours responsable. Contrat effectif, plan, incorporation du DPA et qualité juridique DIQTO/Mitonna : NON VÉRIFIÉS. Texte public ne vaut pas preuve contractuelle ou avis juridique. [S1, S4]

Pour GitHub responsable : S2 prévoit selon la situation accès, rectification, effacement/limitation, opposition, portabilité, retrait du consentement pertinent ; demandes via privacy@github.com, DPO dpo@github.com, réclamation auprès de l'autorité compétente. Vérification d'identité et conservation légale possibles. [S2]

Pour GitHub sous-traitant : §3.G renvoie les demandes au client responsable avec assistance GitHub. Effacement d'un compte Mitonna ne prouve pas purge immédiate des journaux GitHub ; canal Mitonna et capacité de purge restent à établir. [S4]

## Conclusion

Documenter séparément GET sans données métier et traces réseau, IP de sécurité, durées spécifiques non publiées et droits selon finalité. Ne promettre ni rétention chiffrée IP, résidence UE, purge des sauvegardes ni rôle juridique exclusif. Base documentaire seulement, pas recette réseau, conformité certifiée ou preuve Philippe.

## Raccordement au candidat M17 de cette PR

Contrôle source local au pin app `c5b6d32de2b51d3775de49606253281105f788dd` : le transport utilise le GET fixe `https://diqto.fr/mitonna/retraits-recettes.json`, sans corps ni identifiant applicatif ajouté, avec Accept application/json ; cookies, cache et stockage de credentials désactivés, redirections refusées. Contrôle de source et HTTP en boucle locale uniquement : pas une capture du trafic du binaire distribué. L’IP et les en-têtes réseau peuvent rester visibles ; aucune absence d’IP n’est affirmée. Les neuf tests locaux déjà verts ne sont pas rejoués pour cet ajout documentaire.

Le JSON N=0 signifie zéro recette retirée, pas une séquence distante zéro : schéma 1, séquence 1, lot catalogue exact, sept clés strictes, aucun champ personnel. Il reste figé pour revue : émission le 15 novembre 2026 à 13:42:12 UTC, expiration le 16 novembre 2026 à 13:42:12 UTC. Actualiser la politique avant publication selon le producteur et les gardes monotones existants si cette fenêtre n’est plus valable ; ne pas prolonger silencieusement la durée ni réinitialiser des retraits déjà connus. Aucun changement de signature, d’admission ou de fail-closed.

Les limites des sources publiques ci-dessus sont explicites et non bloquantes pour ajouter cet inventaire documentaire à la PR. Elles ne valent ni attestation juridique, ni preuve de configuration effective, ni nouvelle preuve ou autorisation de Philippe. L’intégration du candidat n’autorise aucune fusion ni publication.
