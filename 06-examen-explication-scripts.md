# Examen - Explication Détaillée des Scripts

## Instructions

Cet examen évalue votre capacité à expliquer le rôle et le fonctionnement de chaque script du projet.
Vous devez donner des explications détaillées et précises.
Durée recommandée : 60 minutes
Total : 100 points

---

## PARTIE 1 - SCRIPTS D'ENTRÉE (30 points)

### Question 1 (10 points)
Expliquez en détail le script `start_api.py` :
- Son rôle principal
- Ce qu'il importe
- Pourquoi il est à la racine
- Comment il gère les erreurs

**Votre explication :**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

### Question 2 (10 points)
Expliquez le script `start_gui.py` :
- Sa fonction principale
- Les dépendances qu'il vérifie
- Les messages d'erreur qu'il affiche
- Son lien avec la couche présentation

**Votre explication :**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

### Question 3 (10 points)
Expliquez le script `check_system.py` :
- Quel problème il résout
- Les options de ligne de commande disponibles
- Son rôle dans le développement
- Pourquoi il est nécessaire

**Votre explication :**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

---

## PARTIE 2 - SCRIPTS DE LA COUCHE PRÉSENTATION (25 points)

### Question 4 (10 points)
Expliquez le script `presentation/gui/main_window.py` :
- Les classes qu'il définit
- Les fonctionnalités de l'interface
- Comment il communique avec l'API
- Les technologies utilisées

**Votre explication :**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

### Question 5 (8 points)
Expliquez le script `presentation/gui/api_client.py` :
- Sa responsabilité principale
- Les méthodes qu'il expose
- Comment il gère les erreurs HTTP
- Son rôle dans l'architecture

**Votre explication :**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

### Question 6 (7 points)
Expliquez le script `presentation/launchers/run_gui.py` :
- Pourquoi il existe séparément
- Ce qu'il fait exactement
- Sa relation avec start_gui.py
- Les imports qu'il effectue

**Votre explication :**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

---

## PARTIE 3 - SCRIPTS DE LA COUCHE BUSINESS (20 points)

### Question 7 (10 points)
Expliquez le script `business/api/main.py` :
- La structure de l'API FastAPI
- Les endpoints principaux
- La gestion des erreurs HTTP
- Les dépendances utilisées

**Votre explication :**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

### Question 8 (5 points)
Expliquez le script `business/validation/schemas.py` :
- Le rôle de Pydantic
- Les classes définies
- La différence entre Create/Update/Response
- L'importance de la validation

**Votre explication :**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

### Question 9 (5 points)
Expliquez le script `business/services/safe_start.py` :
- Les problèmes qu'il résout
- Les fonctionnalités avancées
- Les options de ligne de commande
- Pourquoi il remplace un simple uvicorn

**Votre explication :**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

---

## PARTIE 4 - SCRIPTS DE LA COUCHE DATABASE (15 points)

### Question 10 (5 points)
Expliquez le script `database/config/database.py` :
- La configuration SQLAlchemy
- Le rôle de SessionLocal
- La fonction get_db
- La connexion à SQLite

**Votre explication :**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

### Question 11 (5 points)
Expliquez le script `database/models/models.py` :
- Les modèles définis
- Les relations entre entités
- Les colonnes et leurs types
- Le concept ORM

**Votre explication :**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

### Question 12 (5 points)
Expliquez le script `database/repository/crud.py` :
- Le pattern Repository
- Les opérations CRUD disponibles
- La gestion des sessions
- Les fonctions de recherche

**Votre explication :**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

---

## PARTIE 5 - SCRIPTS SUPPORT ET TESTS (10 points)

### Question 13 (3 points)
Expliquez le script `examples/seed_data.py` :
- Son utilité pour le développement
- Les données qu'il crée
- Les commandes disponibles

**Votre explication :**
_____________________________________________________________
_____________________________________________________________

### Question 14 (3 points)
Expliquez le script `tests/test_coherence.py` :
- Ce qu'il teste
- Pourquoi ces tests sont importants
- Le type de validation effectué

**Votre explication :**
_____________________________________________________________
_____________________________________________________________

### Question 15 (4 points)
Expliquez le script `infrastructure/diagnostics/check_ports.py` :
- Les fonctionnalités de diagnostic
- La gestion des processus
- Les commandes système utilisées
- Son importance pour le développement

**Votre explication :**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

---

## CORRIGÉ DÉTAILLÉ

### PARTIE 1 - Scripts d'entrée

**Question 1 - start_api.py :**
Script d'entrée simplifié qui sert de point d'accès principal pour démarrer l'API. Il importe la fonction main() depuis business.services.safe_start et la lance. Placé à la racine pour faciliter l'utilisation (commande simple : python start_api.py). Gère les erreurs d'importation avec des messages explicites et des suggestions de résolution (installation des dépendances). Ajoute le répertoire courant au sys.path pour assurer les imports corrects.

**Question 2 - start_gui.py :**
Point d'entrée pour l'interface graphique PySide6. Importe et lance la fonction main() depuis presentation.launchers.run_gui. Vérifie la disponibilité de PySide6 et affiche des messages d'aide en cas d'erreur (installation de PySide6, vérification des dépendances). Sert de pont entre l'utilisateur et la couche présentation, masquant la complexité de l'organisation interne.

**Question 3 - check_system.py :**
Script de diagnostic système qui résout les problèmes de ports occupés fréquents en développement. Offre des options pour tuer des processus (--kill-port, --kill-all-python), afficher des commandes utiles (--show-commands). Essentiel pour le workflow de développement car évite les erreurs "port already in use". Importe les fonctionnalités depuis infrastructure.diagnostics.check_ports.

### PARTIE 2 - Couche Présentation

**Question 4 - main_window.py :**
Définit la classe MainWindow (fenêtre principale), UsersTab et ItemsTab (onglets), StatusIndicator (indicateur de connexion). Implémente une interface complète avec tableaux, formulaires, recherche. Communique avec l'API via api_client.py en HTTP REST. Utilise PySide6/Qt pour l'interface native, avec gestion des événements, validation des formulaires, et mise à jour en temps réel de l'état de connexion.

**Question 5 - api_client.py :**
Classe FastAPIClient responsable de toutes les communications HTTP avec l'API. Expose des méthodes pour chaque endpoint (get_users, create_user, etc.). Gère les erreurs HTTP avec des codes de statut appropriés et messages explicites. Centralise la logique de communication, formatage des données, et gestion des sessions HTTP. Abstrait les détails HTTP pour l'interface graphique.

**Question 6 - run_gui.py :**
Script interne de lancement qui contient la logique réelle de démarrage de l'interface. Existe séparément pour séparer le point d'entrée (start_gui.py) de l'implémentation. Effectue les imports PySide6, configure l'application Qt, et lance la boucle d'événements. Relation : start_gui.py → run_gui.py → main_window.py.

### PARTIE 3 - Couche Business

**Question 7 - main.py (API) :**
Application FastAPI complète avec endpoints REST pour users et items. Structure : définition de l'app, fonction get_db pour les sessions, endpoints CRUD avec décorateurs (@app.get, @app.post). Gère les erreurs HTTP (404, 400) avec HTTPException. Utilise les dépendances : FastAPI pour l'API, SQLAlchemy pour la DB, Pydantic pour la validation, CRUD pour les opérations.

**Question 8 - schemas.py :**
Définit les schémas Pydantic pour la validation automatique des données. Classes : UserCreate (création), UserUpdate (modification), User (réponse), ItemCreate, ItemUpdate, Item. Différences : Create contient tous les champs requis, Update permet des champs optionnels, Response inclut les champs calculés (ID, timestamps). Validation automatique des types, formats email, contraintes de données.

**Question 9 - safe_start.py :**
Remplace le simple "uvicorn main:app" par un démarrage intelligent. Résout : détection des ports occupés, arrêt automatique des processus conflictuels, recherche de ports libres. Options : --auto-port, --force-kill, --no-reload. Nécessaire car les développeurs rencontrent souvent des conflits de ports, et ce script automatise la résolution.

### PARTIE 4 - Couche Database

**Question 10 - database.py :**
Configure SQLAlchemy avec l'URL de la base SQLite. SessionLocal = factory pour créer des sessions DB. get_db() = fonction générateur pour l'injection de dépendance FastAPI, assure la fermeture automatique des sessions. Base = classe de base pour tous les modèles ORM.

**Question 11 - models.py :**
Définit User et Item comme classes SQLAlchemy. Relations : User.items (one-to-many), Item.owner (many-to-one) avec back_populates. Colonnes typées (String, Integer, Boolean, DateTime) avec contraintes (nullable, unique, index). ORM = mapping objet-relationnel, transforme les tables en classes Python.

**Question 12 - crud.py :**
Implémente le pattern Repository pour isoler l'accès aux données. Fonctions CRUD : get_user, create_user, update_user, delete_user, idem pour items. Gère les sessions SQLAlchemy, les requêtes SQL via l'ORM, les fonctions de recherche (search_items avec LIKE). Sépare la logique d'accès aux données de la logique métier.

### PARTIE 5 - Scripts Support

**Question 13 - seed_data.py :**
Utilitaire de développement pour peupler la base avec des données d'exemple. Crée des utilisateurs et articles de test. Commandes : add (ajouter), status (état), quick (utilisateur rapide), reset (réinitialiser). Facilite les tests et démonstrations.

**Question 14 - test_coherence.py :**
Teste la logique métier et la cohérence des données. Valide l'ordre des opérations (créer utilisateur avant article), les contraintes de validation, les relations entre entités. Important pour vérifier que les règles business sont respectées.

**Question 15 - check_ports.py :**
Script de diagnostic complet des ports système. Fonctionnalités : liste des ports occupés, identification des processus, arrêt forcé. Utilise netstat (Windows) ou lsof (Unix), tasklist/taskkill. Crucial en développement pour résoudre les conflits de ports rapidement.

---

## CRITÈRES D'ÉVALUATION

### Excellente réponse (9-10 points)
- Explication complète et précise
- Mentionne les technologies utilisées
- Explique le rôle dans l'architecture
- Donne des détails techniques pertinents

### Bonne réponse (7-8 points)
- Explication correcte mais incomplète
- Comprend le rôle principal
- Quelques détails techniques manquants

### Réponse acceptable (5-6 points)
- Comprend l'objectif de base
- Explication superficielle
- Manque de précision technique

### Réponse insuffisante (0-4 points)
- Explication incorrecte ou très incomplète
- Confusion sur le rôle du script
- Absence de compréhension technique

## CONSEILS POUR RÉUSSIR

1. **Lisez le code** : Ouvrez chaque script et analysez sa structure
2. **Tracez les imports** : Comprenez les dépendances entre scripts
3. **Testez les scripts** : Lancez-les pour voir leur comportement
4. **Analysez les commentaires** : Les docstrings expliquent les objectifs
5. **Comprenez l'architecture** : Chaque script a un rôle précis dans sa couche
