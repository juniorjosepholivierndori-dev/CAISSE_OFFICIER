# Guide des URLs et Profils - Caisse des Officiers

Ce document récapitule l'ensemble des routes et pages disponibles sur l'application web, classées par profil utilisateur, ainsi que les comptes de test et les points d'accès API.

---

## 🌐 1. Pages Publiques (Accès sans authentification)

| Page | URL | Description |
| :--- | :--- | :--- |
| **Connexion** | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) ou [http://127.0.0.1:8000/connexion/](http://127.0.0.1:8000/connexion/) | Formulaire d'authentification pour tous les utilisateurs |
| **Inscription** | [http://127.0.0.1:8000/inscription/](http://127.0.0.1:8000/inscription/) | Création de compte pour un nouvel officier / adhérent |
| **Inscription Réussie** | [http://127.0.0.1:8000/inscription-reussie/](http://127.0.0.1:8000/inscription-reussie/) | Message de confirmation après la soumission du formulaire |
| **Déconnexion** | [http://127.0.0.1:8000/deconnexion/](http://127.0.0.1:8000/deconnexion/) | Fermeture de la session utilisateur |

---

## 🛡️ 2. Profil Administrateur (`ADMIN`)

> **Compte de test par défaut :**  
> - **Identifiant :** `admin`  
> - **Mot de passe :** `Admin123!`

| Page | URL | Description |
| :--- | :--- | :--- |
| **Tableau de bord Admin** | [http://127.0.0.1:8000/accounts/profile-admin/](http://127.0.0.1:8000/accounts/profile-admin/) | Vue d'ensemble, statistiques globales et activité récente |
| **Gestion des Utilisateurs** | [http://127.0.0.1:8000/accounts/utilisateurs/](http://127.0.0.1:8000/accounts/utilisateurs/) | Liste des membres, gestion des statuts et attributions de rôles |
| **Gestion des Cotisations** | [http://127.0.0.1:8000/accounts/cotisations/](http://127.0.0.1:8000/accounts/cotisations/) | Suivi et enregistrement global de toutes les cotisations |
| **Gestion des Prêts** | [http://127.0.0.1:8000/accounts/prets/](http://127.0.0.1:8000/accounts/prets/) | Supervision de l'ensemble des prêts octroyés |
| **Validation des Prêts** | [http://127.0.0.1:8000/accounts/validation/](http://127.0.0.1:8000/accounts/validation/) | Interface pour approuver ou rejeter les demandes de prêt |
| **Gestion des Remboursements** | [http://127.0.0.1:8000/accounts/remboursements/](http://127.0.0.1:8000/accounts/remboursements/) | Suivi de l'ensemble des remboursements enregistrés |
| **Paramètres du Compte** | [http://127.0.0.1:8000/accounts/parametres/](http://127.0.0.1:8000/accounts/parametres/) | Modification des informations et du mot de passe admin |
| **Django Admin** | [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) | Console d'administration native de Django |

---

## 💼 3. Profil Trésorier (`TRESORIER`)

> **Compte de test par défaut :**  
> - **Identifiant :** `tresorier`  
> - **Mot de passe :** `Tresorier123`

| Page | URL | Description |
| :--- | :--- | :--- |
| **Tableau de bord Trésorier** | [http://127.0.0.1:8000/profil-tresorier/](http://127.0.0.1:8000/profil-tresorier/) | Résumé financier, compteurs d'opérations et activités récentes |
| **Gestion des Cotisations** | [http://127.0.0.1:8000/cotisations/](http://127.0.0.1:8000/cotisations/) | Formulaire de saisie et liste des cotisations |
| **Gestion des Prêts** | [http://127.0.0.1:8000/pret/](http://127.0.0.1:8000/pret/) | Enregistrement et traitement des prêts |
| **Enregistrement Remboursements** | [http://127.0.0.1:8000/remboursements/](http://127.0.0.1:8000/remboursements/) | Saisie des remboursements perçus des adhérents |
| **Historique des Transactions** | [http://127.0.0.1:8000/historique/](http://127.0.0.1:8000/historique/) | Journal complet des opérations et mouvements de caisse |

---

## 🎖️ 4. Profil Officier / Adhérent (`OFFICIER`)

> **Compte de test par défaut :**  
> - **Identifiant :** `officier`  
> - **Mot de passe :** `Officier123!`

| Page | URL | Description |
| :--- | :--- | :--- |
| **Profil Officier** | [http://127.0.0.1:8000/profil-officier/](http://127.0.0.1:8000/profil-officier/) | Tableau de bord personnel de l'adhérent / officier |
| **Mes Cotisations** | [http://127.0.0.1:8000/officier/cotisations/](http://127.0.0.1:8000/officier/cotisations/) | Historique personnel des cotisations versées |
| **Mes Prêts** | [http://127.0.0.1:8000/officier/prets/](http://127.0.0.1:8000/officier/prets/) | Formulaire de demande de prêt et suivi des emprunts |
| **Mes Remboursements** | [http://127.0.0.1:8000/officier/remboursements/](http://127.0.0.1:8000/officier/remboursements/) | Liste et suivi des remboursements effectués |
| **Suivi des Validations** | [http://127.0.0.1:8000/officier/validation/](http://127.0.0.1:8000/officier/validation/) | Suivi du statut des demandes (En attente, Validé, Rejeté) |

---

## 🔌 5. Endpoints API & AJAX

| Service / Endpoint | Méthode | URL | Description |
| :--- | :---: | :--- | :--- |
| **Recherche mécano** | `GET` | [http://127.0.0.1:8000/api/rechercher-mecano/](http://127.0.0.1:8000/api/rechercher-mecano/) | Recherche dynamique d'adhérent par numéro mécano |
| **Données Profil** | `GET` | [http://127.0.0.1:8000/api/profil/](http://127.0.0.1:8000/api/profil/) | Récupération des informations du profil connecté |
| **Obtention Token JWT** | `POST` | `http://127.0.0.1:8000/api/token/` | Génération de token d'accès JWT |
| **Rafraîchissement JWT** | `POST` | `http://127.0.0.1:8000/api/token/refresh/` | Renouvellement du token JWT expiré |
