# Cours FastAPI CRUD - Guide complet

## Présentation du cours

Ce cours vous apprend à créer une application web complète avec FastAPI, incluant une API REST, une base de données SQLAlchemy et une interface graphique PySide6.

## Structure du cours

### Module 1 : [Introduction](01-introduction-cours.md)
- Objectifs et prérequis
- Structure générale du projet
- Méthodologie d'apprentissage

### Module 2 : [Architecture du projet](02-architecture-projet.md) 
- Architecture 3-tiers
- Séparation des responsabilités
- Analyse des composants
- Patterns de conception

### Module 3 : [Concepts FastAPI](03-fastapi-concepts.md)
- Création d'endpoints
- Validation Pydantic
- Gestion des erreurs
- Injection de dépendances
- Documentation automatique

### Module 4 : [Construction étape par étape](04-construction-etape-par-etape.md)
- Configuration environnement
- Base de données
- Modèles SQLAlchemy
- Schémas Pydantic
- Opérations CRUD
- API FastAPI complète

### Module 5 : [Base de données SQLAlchemy](05-base-de-donnees-sqlalchemy.md)
- ORM vs SQL direct
- Modèles et relations
- Requêtes avancées
- Optimisation performances
- Migrations

### Module 6 : [Interface graphique PySide6](06-interface-graphique-pyside6.md)
- Architecture MVC
- Widgets principaux
- Signaux et slots
- Communication avec API
- Styles et apparence

### Module 7 : [Questions et exercices](07-questions-exercices.md)
- 30 questions progressives
- Exercices pratiques
- Projet final
- Solutions détaillées

### Module 8 : [Guide d'utilisation](08-guide-utilisation.md)
- Installation et démarrage
- Utilisation de l'API REST
- Interface graphique complète
- Résolution des problèmes
- Maintenance et support

### Module 9 : [Description des scripts](09-description-scripts.md)
- Architecture 3-tiers détaillée
- Description de tous les scripts Python
- Rôle de chaque couche (GUI, API, BDD)
- Interactions et dépendances
- ORM SQLAlchemy expliqué

### Module 10 : [Architecture exhaustive](10-architecture-exhaustive.md)
- Architecture complète niveau par niveau
- Scripts concernés par chaque couche
- Flux de données bidirectionnels
- Patterns architecturaux globaux
- Communication inter-couches détaillée

### Module 12 : [Workflow interface graphique](12-workflow-interface-graphique.md)
- Flux complet de démarrage GUI
- Séquence d'appels et interactions
- Phase par phase depuis run_gui.py
- Workflow des actions utilisateur
- Synchronisation inter-onglets détaillée

### Module 13 : [Classification scripts par couches](13-classification-scripts-couches.md)
- Classification de chaque script Python
- Répartition Présentation/Business/Database
- Justification détaillée par script
- Tableau complet de classification
- Règles et critères de classification

### Module 14 : [Table des scripts](14-table-scripts.md)
- Table complète des 16 scripts Python
- Répartition statistique par couches
- Tables par ordre alphabétique
- Dépendances entre scripts
- Technologies et patterns utilisés

### Module 15 : [Exercice - Organisation par couches](15-exercice-organisation-couches.md)
- Exercice pratique de réorganisation
- Structure de dossiers par couches architecturales
- Scripts de migration automatique
- Validation et tests post-migration
- Questions de réflexion et critères de réussite

## Comment utiliser ce cours

### Progression recommandée
1. Lisez chaque module dans l'ordre
2. Testez tous les exemples de code
3. Faites les exercices proposés
4. Réalisez le projet final

### Temps estimé
- **Lecture théorique** : 6-8 heures
- **Exercices pratiques** : 10-15 heures  
- **Projet final** : 15-20 heures
- **Total** : 30-45 heures

### Prérequis techniques
- Python 3.8+ avec concepts avancés
- Notions de bases de données SQL
- Concepts des API REST
- Environnements virtuels Python

## Support et ressources

### Documentation officielle
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://sqlalchemy.org/)
- [PySide6](https://doc.qt.io/qtforpython/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)

### Outils nécessaires
- Python 3.8+
- IDE (VS Code, PyCharm)
- Git (recommandé)
- Base de données (SQLite inclus)

### Installation rapide

```bash
# Clone du projet
git clone [repository]
cd fastapi-crud-course

# Environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Dépendances
pip install -r requirements.txt

# Lancement
python main.py
```

## Objectifs pédagogiques

À la fin de ce cours, vous serez capable de :

1. **Créer des APIs FastAPI** complètes et documentées
2. **Gérer des bases de données** avec SQLAlchemy ORM
3. **Développer des interfaces** graphiques avec PySide6
4. **Implémenter l'architecture** 3-tiers professionnelle
5. **Optimiser les performances** et gérer les erreurs
6. **Tester et déployer** vos applications

## Licence et utilisation

Ce cours est libre d'utilisation pour l'apprentissage personnel et professionnel.

**Bon apprentissage !**
