# Examen - Scripts et Organisation par Couches

## Instructions

Cet examen évalue votre connaissance des scripts du projet et leur organisation par couches.
Durée recommandée : 30 minutes
Total : 100 points

---

## PARTIE 1 - IDENTIFICATION DES SCRIPTS (50 points)

### Question 1 (5 points)
Le script `start_api.py` se trouve dans :

a) La couche Business
b) La racine du projet (script d'entrée)
c) La couche Infrastructure
d) Le dossier config/

### Question 2 (5 points)
Quel est le rôle principal du script `check_system.py` ?

a) Démarrer l'interface graphique
b) Configurer la base de données
c) Diagnostiquer les ports et processus système
d) Valider les données utilisateur

### Question 3 (5 points)
Le fichier `main_window.py` appartient à quelle couche ?

a) Business
b) Database
c) Présentation
d) Infrastructure

### Question 4 (5 points)
Que fait le script `api_client.py` ?

a) Démarre l'API FastAPI
b) Communique avec l'API via HTTP
c) Gère la base de données
d) Configure les ports

### Question 5 (5 points)
Le script `safe_start.py` est responsable de :

a) Démarrer l'interface graphique
b) Démarrer l'API avec gestion des ports
c) Créer des données de test
d) Vérifier la cohérence des données

### Question 6 (5 points)
Dans quelle couche se trouve le fichier `crud.py` ?

a) Présentation
b) Business
c) Database
d) Infrastructure

### Question 7 (5 points)
Le script `models.py` contient :

a) Les endpoints de l'API
b) Les modèles SQLAlchemy pour la base de données
c) L'interface graphique
d) Les tests unitaires

### Question 8 (5 points)
Que fait le script `schemas.py` ?

a) Configure la base de données
b) Définit les schémas de validation Pydantic
c) Gère l'interface utilisateur
d) Diagnostique le système

### Question 9 (5 points)
Le fichier `database.py` est responsable de :

a) Stocker les données utilisateur
b) Configurer SQLAlchemy et les sessions
c) Créer l'interface graphique
d) Gérer les ports

### Question 10 (5 points)
Le script `run_gui.py` se trouve dans :

a) presentation/gui/
b) presentation/launchers/
c) business/services/
d) La racine du projet

---

## PARTIE 2 - CLASSIFICATION PAR COUCHES (30 points)

### Question 11 (15 points)
Classez ces scripts dans leur couche appropriée :

**Scripts :**
- main.py (API)
- api_client.py
- check_ports.py
- models.py
- schemas.py
- main_window.py

**Couches :**

**PRÉSENTATION :**
_________________________________
_________________________________

**BUSINESS :**
_________________________________
_________________________________

**DATABASE :**
_________________________________
_________________________________

**INFRASTRUCTURE :**
_________________________________
_________________________________

### Question 12 (15 points)
Pour chaque script, indiquez son chemin complet dans l'architecture :

1. Script de démarrage API : ___________________________
2. Interface graphique principale : ___________________________
3. Opérations CRUD : ___________________________
4. Configuration base de données : ___________________________
5. Validation des données : ___________________________

---

## PARTIE 3 - FONCTIONNALITÉS DES SCRIPTS (20 points)

### Question 13 (10 points)
Expliquez la différence entre `start_api.py` et `safe_start.py` :

**start_api.py :**
_____________________________________________________________
_____________________________________________________________

**safe_start.py :**
_____________________________________________________________
_____________________________________________________________

### Question 14 (10 points)
Décrivez le rôle de ces 3 scripts dans l'écosystème de l'application :

**check_system.py :**
_____________________________________________________________

**start_gui.py :**
_____________________________________________________________

**seed_data.py :**
_____________________________________________________________

---

## CORRIGÉ

### PARTIE 1 - Identification

1. **b)** La racine du projet (script d'entrée)
2. **c)** Diagnostiquer les ports et processus système
3. **c)** Présentation
4. **b)** Communique avec l'API via HTTP
5. **b)** Démarrer l'API avec gestion des ports
6. **c)** Database
7. **b)** Les modèles SQLAlchemy pour la base de données
8. **b)** Définit les schémas de validation Pydantic
9. **b)** Configurer SQLAlchemy et les sessions
10. **b)** presentation/launchers/

### PARTIE 2 - Classification

**Question 11 :**

**PRÉSENTATION :**
- api_client.py
- main_window.py

**BUSINESS :**
- main.py (API)
- schemas.py

**DATABASE :**
- models.py

**INFRASTRUCTURE :**
- check_ports.py

**Question 12 :**

1. Script de démarrage API : `start_api.py` (racine)
2. Interface graphique principale : `presentation/gui/main_window.py`
3. Opérations CRUD : `database/repository/crud.py`
4. Configuration base de données : `database/config/database.py`
5. Validation des données : `business/validation/schemas.py`

### PARTIE 3 - Fonctionnalités

**Question 13 :**

**start_api.py :** Script d'entrée simplifié qui importe et lance safe_start.py. Situé à la racine pour faciliter l'utilisation.

**safe_start.py :** Script complet de démarrage avec gestion avancée des ports, détection des conflits, arrêt forcé des processus, et recherche automatique de ports libres.

**Question 14 :**

**check_system.py :** Diagnostic système, vérification des ports occupés, arrêt de processus, affichage des commandes utiles.

**start_gui.py :** Lance l'interface graphique PySide6 avec gestion des erreurs d'importation et messages d'aide.

**seed_data.py :** Ajoute des données d'exemple dans la base de données pour faciliter les tests et la démonstration.

---

## ANALYSE DÉTAILLÉE DES SCRIPTS

### Scripts d'Entrée (Racine)
- **start_api.py** : Point d'entrée pour l'API
- **start_gui.py** : Point d'entrée pour l'interface
- **check_system.py** : Point d'entrée pour le diagnostic

### Scripts de Présentation
- **presentation/gui/main_window.py** : Interface graphique complète
- **presentation/gui/api_client.py** : Client HTTP pour communication
- **presentation/launchers/run_gui.py** : Lanceur de l'interface

### Scripts Business
- **business/api/main.py** : API FastAPI avec tous les endpoints
- **business/validation/schemas.py** : Schémas Pydantic de validation
- **business/services/safe_start.py** : Service de démarrage sécurisé

### Scripts Database
- **database/config/database.py** : Configuration SQLAlchemy
- **database/models/models.py** : Modèles ORM User et Item
- **database/repository/crud.py** : Opérations CRUD complètes

### Scripts Infrastructure
- **infrastructure/diagnostics/check_ports.py** : Diagnostic système complet

### Scripts Support
- **examples/seed_data.py** : Génération de données de test
- **examples/exemple_utilisation.py** : Exemples d'usage de l'API
- **tests/test_coherence.py** : Tests de validation
- **tests/test_gui_integration.py** : Tests interface graphique

---

## BARÈME DE NOTATION

- **90-100 points :** Maîtrise parfaite de l'organisation des scripts
- **80-89 points :** Bonne connaissance avec erreurs mineures
- **70-79 points :** Compréhension correcte mais incomplète
- **60-69 points :** Bases acquises, révisions nécessaires
- **Moins de 60 :** Étude approfondie de la structure recommandée

## CONSEILS D'ÉTUDE

1. Explorez chaque dossier et lisez les en-têtes des fichiers
2. Tracez les imports entre les scripts
3. Testez les scripts d'entrée pour comprendre leur rôle
4. Analysez la structure des packages Python
5. Comprenez la logique de séparation par responsabilités
