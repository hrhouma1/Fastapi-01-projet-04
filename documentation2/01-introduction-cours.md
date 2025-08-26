# Cours FastAPI CRUD - Introduction

## Objectifs du cours

Ce cours vous apprendra à construire une application web complète avec FastAPI, incluant :

- Une API REST complète avec opérations CRUD
- Une base de données SQLite avec SQLAlchemy
- Une interface graphique moderne avec PySide6
- La gestion des erreurs et la validation des données
- Les tests et la documentation automatique

## Prérequis

### Connaissances requises
- Python intermédiaire (classes, modules, gestion d'erreurs)
- Notions de bases de données (SQL de base)
- Concepts des API REST (GET, POST, PUT, DELETE)
- Ligne de commande et environnements virtuels

### Outils nécessaires
- Python 3.8 ou supérieur
- Un éditeur de code (VS Code, PyCharm, etc.)
- Git (optionnel mais recommandé)

## Structure du cours

### Module 1 : Architecture et concepts fondamentaux
- Architecture du projet FastAPI
- Rôle de chaque composant
- Patterns et bonnes pratiques

### Module 2 : FastAPI en détail
- Création d'endpoints
- Validation avec Pydantic
- Gestion des erreurs
- Documentation automatique

### Module 3 : Base de données avec SQLAlchemy
- Modèles de données
- Relations entre tables
- Opérations CRUD
- Migrations et seeds

### Module 4 : Interface graphique avec PySide6
- Architecture MVC
- Communication avec l'API
- Gestion des événements
- Design responsive

### Module 5 : Intégration et déploiement
- Tests automatisés
- Gestion des erreurs
- Configuration de production
- Bonnes pratiques

### Module 6 : Évaluation
- 30 questions progressives
- Exercices pratiques
- Projets d'application

## Méthodologie pédagogique

### Approche progressive
1. **Concepts théoriques** : Explication des principes
2. **Exemples concrets** : Code commenté et détaillé
3. **Exercices guidés** : Application immédiate
4. **Projets pratiques** : Mise en situation réelle

### Format des leçons
- Introduction du concept
- Explication technique détaillée
- Exemples de code avec commentaires
- Cas d'usage et bonnes pratiques
- Exercices de validation

## Architecture générale du projet

```
projetsfastapi/
├── main.py              # Point d'entrée FastAPI
├── models.py            # Modèles SQLAlchemy
├── schemas.py           # Schémas Pydantic
├── crud.py              # Opérations base de données
├── database.py          # Configuration BDD
├── requirements.txt     # Dépendances Python
├── gui_client/          # Interface graphique
│   ├── main_window.py   # Fenêtre principale
│   └── api_client.py    # Client API
├── documentation2/      # Ce cours
└── venv/               # Environnement virtuel
```

## Concepts clés abordés

### FastAPI
- Décorateurs de routes
- Injection de dépendances
- Middleware et authentification
- Documentation OpenAPI automatique
- Validation de données avec Pydantic

### SQLAlchemy
- ORM (Object Relational Mapping)
- Définition de modèles
- Relations entre tables
- Sessions et transactions
- Requêtes et filtres

### PySide6
- Architecture Qt/QML
- Widgets et layouts
- Signaux et slots
- Gestion des événements
- Communication réseau

### Architecture logicielle
- Séparation des responsabilités
- Pattern Repository
- Architecture en couches
- Gestion des erreurs centralisée
- Tests unitaires et d'intégration

## Livrables du cours

À la fin de ce cours, vous aurez :

1. **Une API FastAPI complète** avec toutes les opérations CRUD
2. **Une interface graphique fonctionnelle** pour interagir avec l'API
3. **Une base de données structurée** avec relations
4. **Des tests automatisés** pour valider le fonctionnement
5. **Une documentation complète** générée automatiquement
6. **Les compétences** pour créer vos propres applications similaires

## Temps estimé

- **Lecture théorique** : 4-6 heures
- **Exercices pratiques** : 8-12 heures
- **Projet final** : 6-8 heures
- **Total** : 18-26 heures (selon expérience)

## Comment utiliser ce cours

1. **Lisez d'abord** chaque module dans l'ordre
2. **Testez tous les exemples** de code proposés
3. **Faites les exercices** avant de passer au module suivant
4. **Posez-vous les questions** : "Pourquoi cette solution ?"
5. **Expérimentez** : modifiez le code pour comprendre

## Support et ressources

### Documentation officielle
- FastAPI : https://fastapi.tiangolo.com/
- SQLAlchemy : https://sqlalchemy.org/
- PySide6 : https://doc.qt.io/qtforpython/

### Ressources complémentaires
- Python.org pour les bases du langage
- Real Python pour des tutoriels avancés
- GitHub pour des exemples de projets

Commencez par le module suivant : **02-architecture-projet.md**
