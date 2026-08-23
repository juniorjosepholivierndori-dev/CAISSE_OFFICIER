# Analyse du projet Caisse des officiers

## 1. Fonctionnement général

L'application est un projet Django de gestion d'une caisse pour les officiers.

```text
.env
  -> config/settings/dev.py
  -> manage.py
  -> config/urls.py
  -> connexion
  -> tableau de bord
  -> API membre
  -> PostgreSQL caisse_gmmg
```

La base actuellement utilisée est PostgreSQL, avec la base `caisse_gmmg`.

## 2. Fichiers principaux

### Racine

- `manage.py` : lance Django et ses commandes (`runserver`, `migrate`, `createsuperuser`).
- `requirements.txt` : liste les dépendances Python.
- `.env` : configuration locale et identifiants PostgreSQL. Ce fichier est sensible.
- `.env.example` : exemple de configuration.
- `db.sqlite3` : ancienne base SQLite locale ; probablement inutilisée lorsque PostgreSQL est actif.

### Configuration

- `config/urls.py` : routes principales du site.
- `config/settings/base.py` : configuration commune Django.
- `config/settings/dev.py` : configuration de développement et choix SQLite/PostgreSQL.
- `config/settings/prod.py` : configuration prévue pour la production.
- `config/asgi.py` : point d'entrée ASGI.
- `config/wsgi.py` : point d'entrée WSGI.
- `config/settings/__init__.py` : fichier technique du module Python.

## 3. Application accounts

- `apps/accounts/models.py` : définit l'utilisateur, le profil membre et l'adhérent.
- `apps/accounts/views.py` : traite la connexion.
- `apps/accounts/urls.py` : définit `/connexion/`.
- `apps/accounts/admin.py` : affiche les comptes dans l'administration.
- `templates/accounts/login.html` : formulaire de connexion.

## 4. Application dashboard

- `apps/dashboard/views.py` : affiche le tableau de bord et exige une connexion.
- `apps/dashboard/urls.py` : définit la route `/`.
- `templates/dashboard/member.html` : contient l'interface, les styles CSS et le JavaScript du tableau de bord.

Le tableau de bord affiche les informations renvoyées par l'API et la base PostgreSQL :

- profil du membre ;
- cotisations ;
- prêts ;
- remboursements ;
- notifications ;
- demandes en cours.

## 5. Application operations

- `apps/operations/models.py` : définit les opérations, opérations personnelles et notifications.
- `apps/operations/api.py` : fournit les données du membre et enregistre les demandes.
- `apps/operations/urls.py` : définit les routes de l'API.
- `apps/operations/admin.py` : permet de gérer les opérations dans l'administration.

Routes principales :

```text
GET  /api/member/dashboard/
POST /api/member/requests/
GET  /api/member/notifications/
```

## 6. Application referentiels

`apps/referentiels/models.py` contient les tables de référence :

- pays ;
- villes ;
- grades ;
- statuts ;
- unités ;
- services ;
- types de service ;
- établissements ;
- états.

`apps/referentiels/admin.py` permet leur gestion dans l'administration Django.

## 7. Application audit

- `apps/audit/models.py` : définit les journaux d'audit et les traces d'opérations.
- `apps/audit/admin.py` : permet de consulter ces journaux dans l'administration.

Les modèles existent, mais l'enregistrement automatique des actions n'est pas encore clairement implémenté.

## 8. Application core

`apps/core` est déclarée dans `INSTALLED_APPS`, mais ne contient actuellement aucune fonctionnalité visible :

- pas de modèle ;
- pas de vue ;
- pas d'URL ;
- pas de migration métier.

Elle peut être conservée pour de futures fonctions communes.

## 9. Migrations

Les migrations créent les tables PostgreSQL nécessaires, notamment :

- `accounts_user` ;
- `accounts_adherent` ;
- `accounts_memberprofile` ;
- `operations_operation` ;
- `operations_notification` ;
- `referentiels_grade` ;
- `referentiels_unite` ;
- `audit_log`.

Les migrations déjà appliquées ne doivent pas être supprimées.

## 10. Fichiers potentiellement inutilisés

### Ancienne base SQLite

```text
db.sqlite3
```

Elle peut être inutilisée si PostgreSQL est toujours actif. Ne la supprimez qu'après avoir confirmé que toutes les données utiles sont dans `caisse_gmmg`.

### Ancien logo JPEG

```text
static/images/WhatsApp Image 2026-08-13 at 13.44.26.jpeg
```

Le tableau de bord utilise maintenant le logo PNG :

```text
static/images/WhatsApp_Image_2026-08-13_at_13.44.26-removebg-preview.png
```

L'ancien JPEG est donc probablement inutilisé.

### Application core

`apps/core` est actuellement vide ou presque vide. Elle n'est pas nécessaire au fonctionnement actuel, mais peut être conservée pour une extension future.

### JWT et CORS

DRF, SimpleJWT et CORS sont configurés, mais les routes actuelles utilisent surtout l'authentification par session Django. Les fonctions JWT ne sont pas encore utilisées par l'interface actuelle.

## 11. Fonctionnalités encore incomplètes

- Le bouton de déconnexion affiche un message, mais ne ferme pas encore réellement la session.
- La sauvegarde du profil affiche un message, mais ne modifie pas encore les données côté serveur.
- La pièce justificative peut être sélectionnée, mais n'est pas encore envoyée ni enregistrée.
- Les notifications visibles dans le template sont encore partiellement statiques.
- Aucun ensemble de tests automatisés n'est actuellement présent.

## 12. Commandes utiles

Vérifier Django :

```powershell
.\.venv\Scripts\python.exe manage.py check
```

Appliquer les migrations :

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

Démarrer le serveur :

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Créer un administrateur :

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Administration :

```text
http://127.0.0.1:8000/admin/
```

Connexion membre :

```text
http://127.0.0.1:8000/connexion/
```

## Conclusion

Le projet fonctionne avec Django et PostgreSQL. Les tables sont créées dans `caisse_gmmg`. Les éléments les plus susceptibles d'être inutilisés sont l'ancienne base `db.sqlite3`, l'ancien logo JPEG et l'application `apps/core`. Les migrations et la configuration de production doivent être conservées.
