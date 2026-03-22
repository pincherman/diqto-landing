# Politique de Confidentialité

**Diqto — Application de facturation pour micro-entrepreneurs**

*Dernière mise à jour : 22 mars 2026*

La présente Politique de Confidentialité décrit la manière dont Diqto collecte, utilise, stocke et protège les données personnelles de ses Utilisateurs, conformément au Règlement (UE) 2016/679 (« RGPD ») et à la loi n°78-17 du 6 janvier 1978 modifiée (« Informatique et Libertés »).

---

## 1. Responsable de traitement

**Diqto**
Philippe Incherman
SIRET : *[À compléter]*
Adresse : *[À compléter]*
Email : support@diqto.fr

Contact délégué à la protection des données (DPO) : **support@diqto.fr**

---

## 2. Données collectées

### 2.1 Données fournies par l'Utilisateur

| Catégorie | Données | Finalité |
|-----------|---------|----------|
| **Identification** | Numéro de téléphone mobile | Création de compte, authentification par SMS |
| **Profil professionnel** | Nom, prénom, nom commercial, adresse, SIRET, activité | Personnalisation des documents, conformité légale |
| **Contact** | Adresse email (optionnel) | Communications, notifications, récupération de compte |
| **Facturation** | Informations clients de l'Utilisateur, montants, descriptions de prestations | Génération des devis, factures, notes d'honoraires |
| **Paiement** | Données de carte bancaire (traitées par Stripe, jamais stockées par Diqto) | Paiement des abonnements |

### 2.2 Données collectées automatiquement

| Catégorie | Données | Finalité |
|-----------|---------|----------|
| **Données techniques** | Adresse IP, type de navigateur, système d'exploitation | Sécurité, débogage, amélioration du Service |
| **Données d'usage** | Pages consultées, fonctionnalités utilisées, horodatage | Statistiques, amélioration du Service |
| **Documents créés** | Devis, factures, notes d'honoraires générés | Fourniture du Service, historique |
| **Conversations** | Échanges via l'interface WhatsApp | Fourniture du Service (traitement des instructions) |

### 2.3 Données non collectées

Diqto ne collecte pas de données sensibles au sens de l'article 9 du RGPD (origine ethnique, opinions politiques, données de santé, etc.).

---

## 3. Bases légales du traitement

| Traitement | Base légale (art. 6 RGPD) |
|------------|---------------------------|
| Création et gestion du compte | Exécution du contrat (art. 6.1.b) |
| Génération et stockage des documents | Exécution du contrat (art. 6.1.b) |
| Traitement des paiements | Exécution du contrat (art. 6.1.b) |
| Envoi de notifications de service | Exécution du contrat (art. 6.1.b) |
| Communications commerciales | Consentement (art. 6.1.a) |
| Statistiques et amélioration du Service | Intérêt légitime (art. 6.1.f) |
| Sécurité et prévention de la fraude | Intérêt légitime (art. 6.1.f) |
| Conservation des factures émises | Obligation légale (art. 6.1.c) — CGI, Code de commerce |

---

## 4. Sous-traitants et destinataires

Diqto fait appel aux sous-traitants suivants pour la fourniture du Service. Chaque sous-traitant est lié par un accord de traitement des données (DPA) conforme à l'article 28 du RGPD.

| Sous-traitant | Fonction | Localisation | Garanties |
|---------------|----------|--------------|-----------|
| **Koyeb** | Hébergement de l'application | 🇪🇺 Union Européenne | Hébergeur européen, données en UE |
| **Neon** | Base de données PostgreSQL | 🇪🇺 Union Européenne | Données chiffrées, hébergement UE |
| **Cloudflare (R2)** | Stockage de fichiers (PDFs) | 🇪🇺 Union Européenne | Chiffrement, réseau européen |
| **Stripe** | Traitement des paiements | 🇪🇺 / 🇺🇸 UE & États-Unis | Certifié PCI-DSS, clauses contractuelles types (CCT) |
| **Meta / WhatsApp** | Canal de messagerie | 🇪🇺 / 🇺🇸 UE & États-Unis | Clauses contractuelles types (CCT), chiffrement de bout en bout |
| **OpenAI** | Intelligence artificielle (assistance à la génération de documents) | 🇺🇸 États-Unis | Clauses contractuelles types (CCT), DPA en place, pas de réutilisation des données pour entraînement (API) |

Diqto ne vend, ne loue et ne partage jamais les données personnelles de ses Utilisateurs avec des tiers à des fins commerciales.

---

## 5. Transferts hors Union Européenne

Certains sous-traitants sont situés en dehors de l'Espace Économique Européen (EEE), principalement aux États-Unis :

- **OpenAI** (traitement IA) ;
- **Stripe** (paiement, partiellement) ;
- **Meta/WhatsApp** (messagerie, partiellement).

Ces transferts sont encadrés par :

- Les **Clauses Contractuelles Types** (CCT) adoptées par la Commission européenne (décision d'exécution 2021/914) ;
- Le **Data Privacy Framework** (DPF) UE-États-Unis, le cas échéant ;
- Des **mesures techniques complémentaires** (chiffrement en transit et au repos, minimisation des données transmises).

L'Utilisateur peut obtenir une copie des garanties mises en place en contactant support@diqto.fr.

---

## 6. Durée de conservation

| Données | Durée de conservation |
|---------|----------------------|
| Données de compte (profil, téléphone) | Durée de vie du compte + 3 ans après suppression |
| Documents commerciaux (factures, devis) | 10 ans à compter de la clôture de l'exercice (obligation légale — art. L.123-22 du Code de commerce) |
| Données de paiement | Durée de la relation commerciale + 13 mois (CB) pour gestion des contestations |
| Conversations WhatsApp | 12 mois glissants, puis anonymisation |
| Données techniques (logs) | 12 mois |
| Données de prospection | 3 ans à compter du dernier contact |

À l'expiration de ces durées, les données sont supprimées ou anonymisées de manière irréversible.

---

## 7. Sécurité des données

Diqto met en œuvre les mesures techniques et organisationnelles appropriées pour protéger les données personnelles contre tout accès non autorisé, altération, divulgation ou destruction, notamment :

- Chiffrement des données en transit (TLS/HTTPS) et au repos ;
- Authentification sécurisée par code SMS (OTP) ;
- Accès aux données limité au strict nécessaire (principe du moindre privilège) ;
- Sauvegardes régulières et chiffrées ;
- Surveillance et journalisation des accès ;
- Mises à jour de sécurité régulières.

---

## 8. Droits des personnes

Conformément au RGPD (articles 15 à 22) et à la loi Informatique et Libertés, l'Utilisateur dispose des droits suivants sur ses données personnelles :

| Droit | Description |
|-------|-------------|
| **Accès** (art. 15) | Obtenir confirmation du traitement et une copie de ses données |
| **Rectification** (art. 16) | Corriger des données inexactes ou incomplètes |
| **Effacement** (art. 17) | Demander la suppression de ses données (« droit à l'oubli »), sous réserve des obligations légales de conservation |
| **Limitation** (art. 18) | Demander la limitation du traitement dans certains cas |
| **Portabilité** (art. 20) | Recevoir ses données dans un format structuré, couramment utilisé et lisible par machine |
| **Opposition** (art. 21) | S'opposer au traitement fondé sur l'intérêt légitime, y compris le profilage |
| **Retrait du consentement** | Retirer son consentement à tout moment (sans affecter la licéité du traitement antérieur) |

### Comment exercer vos droits

Par email à : **support@diqto.fr**

Diqto s'engage à répondre dans un délai d'**un mois** à compter de la réception de la demande. Ce délai peut être prolongé de deux mois en cas de complexité ou de nombre élevé de demandes.

Une pièce d'identité pourra être demandée en cas de doute raisonnable sur l'identité du demandeur.

### Réclamation

En cas de difficulté, l'Utilisateur peut introduire une réclamation auprès de la **Commission Nationale de l'Informatique et des Libertés (CNIL)** :

- Site : [www.cnil.fr](https://www.cnil.fr)
- Adresse : 3 Place de Fontenoy, TSA 80715, 75334 Paris Cedex 07

---

## 9. Cookies et traceurs

### 9.1 Application web (diqto.fr)

Diqto utilise des cookies et technologies similaires dans les catégories suivantes :

| Type | Finalité | Consentement requis |
|------|----------|---------------------|
| **Cookies strictement nécessaires** | Fonctionnement du Service (session, authentification) | Non (exemptés) |
| **Cookies analytiques** | Mesure d'audience, amélioration du Service | Oui |
| **Cookies de préférence** | Mémorisation des choix de l'Utilisateur | Oui |

L'Utilisateur peut gérer ses préférences de cookies via le bandeau de consentement affiché lors de sa première visite, ou à tout moment via les paramètres du Service.

### 9.2 Interface WhatsApp

L'interface WhatsApp ne dépose pas de cookies. Les données de conversation sont traitées conformément à la section 4 (Meta/WhatsApp) et à la politique de confidentialité de Meta.

---

## 10. Mineurs

Le Service est destiné aux professionnels et n'est pas conçu pour les mineurs de moins de 16 ans. Diqto ne collecte pas sciemment de données de mineurs. Si Diqto découvre avoir collecté des données d'un mineur, celles-ci seront supprimées dans les meilleurs délais.

---

## 11. Modifications de la Politique

Diqto se réserve le droit de modifier la présente Politique de Confidentialité. En cas de modification substantielle, les Utilisateurs en seront informés par notification via le Service ou par email/SMS, au moins 30 jours avant l'entrée en vigueur.

La date de dernière mise à jour est indiquée en haut du présent document.

---

## 12. Contact

Pour toute question relative à la protection de vos données personnelles :

📧 **DPO / Contact** : support@diqto.fr
🌐 **Site** : [diqto.fr](https://diqto.fr)
