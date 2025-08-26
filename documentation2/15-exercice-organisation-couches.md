# Exercice : Organisation du projet par couches architecturales

## Objectif de l'exercice

Réorganiser le projet FastAPI CRUD actuel en structurant les fichiers selon les couches architecturales pour améliorer la maintenabilité et la lisibilité du code.

## Contexte

Actuellement, tous les scripts Python sont mélangés à la racine du projet. Cet exercice propose de les organiser selon l'architecture 3-tiers :
- **Présentation** : Interface utilisateur et clients
- **Business Logique** : API et règles métier  
- **Database** : Persistance et accès aux données
- **Infrastructure** : Services transversaux

## Structure cible proposée

```
projetsfastapi/
├── presentation/                 # COUCHE PRÉSENTATION (5 scripts)
│   ├── gui/
│   │   ├── main_window.py       # Interface graphique principale
│   │   ├── api_client.py        # Client HTTP API
│   │   └── __init__.py          # Package GUI
│   ├── launchers/
│   │   ├── run_gui.py           # Démarrage interface
│   │   └── setup_gui.py         # Configuration GUI
│   └── tests/
│       └── test_gui_integration.py  # Tests GUI
│
├── business/                     # COUCHE BUSINESS LOGIQUE (4 scripts)
│   ├── api/
│   │   └── main.py              # FastAPI endpoints
│   ├── validation/
│   │   └── schemas.py           # Schémas Pydantic
│   ├── services/
│   │   └── safe_start.py        # Service démarrage
│   └── examples/
│       └── exemple_utilisation.py  # Documentation API
│
├── database/                     # COUCHE DATABASE (3 scripts)
│   ├── config/
│   │   └── database.py          # Configuration SQLAlchemy
│   ├── models/
│   │   └── models.py            # Modèles ORM
│   ├── repository/
│   │   └── crud.py              # Opérations CRUD
│   └── fixtures/
│       └── seed_data.py         # Données de test
│
├── infrastructure/               # COUCHE TRANSVERSALE
│   ├── diagnostics/
│   │   └── check_ports.py       # Vérification ports
│   └── tests/
│       └── test_coherence.py    # Tests système
│
├── config/                       # FICHIERS DE CONFIGURATION
│   ├── requirements.txt
│   ├── setup.bat
│   └── setup.sh
│
├── documentation/                # DOCUMENTATION EXISTANTE
└── documentation2/              # COURS COMPLET
```

## Exercice 1 : Planification des migrations

### Instructions
1. Analysez la structure actuelle du projet
2. Identifiez quels fichiers appartiennent à quelle couche (utilisez la table du module 14)
3. Planifiez l'ordre des migrations pour éviter les conflits

### Table de migration à compléter

| Script Actuel | Couche | Nouveau Chemin | Priorité Migration |
|---------------|--------|----------------|-------------------|
| `main.py` | Business Logique | `business/api/main.py` | 1 (critique) |
| `gui_client/main_window.py` | Présentation | `presentation/gui/main_window.py` | 1 (critique) |
| `models.py` | Database | `database/models/models.py` | 1 (critique) |
| `crud.py` | Database | `database/repository/crud.py` | 1 (critique) |
| `database.py` | Database | `database/config/database.py` | 2 |
| `schemas.py` | Business Logique | `business/validation/schemas.py` | 2 |
| `gui_client/api_client.py` | Présentation | `presentation/gui/api_client.py` | 2 |
| `run_gui.py` | Présentation | `presentation/launchers/run_gui.py` | 3 |
| `safe_start.py` | Business Logique | `business/services/safe_start.py` | 3 |
| `seed_data.py` | Database | `database/fixtures/seed_data.py` | 4 |
| `setup_gui.py` | Présentation | `presentation/launchers/setup_gui.py` | 4 |
| `exemple_utilisation.py` | Business Logique | `business/examples/exemple_utilisation.py` | 4 |
| `test_coherence.py` | Infrastructure | `infrastructure/tests/test_coherence.py` | 5 |
| `test_gui_integration.py` | Infrastructure | `presentation/tests/test_gui_integration.py` | 5 |
| `check_ports.py` | Infrastructure | `infrastructure/diagnostics/check_ports.py` | 5 |
| `gui_client/__init__.py` | Présentation | `presentation/gui/__init__.py` | 6 |

## Exercice 2 : Analyse des imports

### Instructions
Identifiez tous les imports qui devront être modifiés après la migration.

### Exemple d'analyse pour `main.py` :

#### Imports actuels dans `main.py` :
```python
from database import SessionLocal, engine
from crud import create_user, get_users, get_user, update_user, delete_user
from crud import create_item, get_items, get_item, update_item, delete_item, search_items
import schemas
import models
```

#### Imports après migration vers `business/api/main.py` :
```python
from database.config.database import SessionLocal, engine
from database.repository.crud import create_user, get_users, get_user, update_user, delete_user
from database.repository.crud import create_item, get_items, get_item, update_item, delete_item, search_items
from business.validation import schemas
from database.models import models
```

### À faire pour chaque script :
1. Listez les imports actuels
2. Calculez les nouveaux chemins relatifs
3. Identifiez les imports circulaires potentiels

## Exercice 3 : Script de migration automatique

### Instructions
Créez un script Python `migrate_to_layers.py` qui :

1. **Crée la structure de dossiers**
```python
import os

def create_directory_structure():
    """Crée la structure de dossiers par couches"""
    dirs_to_create = [
        "presentation/gui",
        "presentation/launchers", 
        "presentation/tests",
        "business/api",
        "business/validation",
        "business/services", 
        "business/examples",
        "database/config",
        "database/models",
        "database/repository",
        "database/fixtures",
        "infrastructure/diagnostics",
        "infrastructure/tests",
        "config"
    ]
    
    for dir_path in dirs_to_create:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Créé: {dir_path}")
```

2. **Déplace les fichiers**
```python
import shutil

def migrate_files():
    """Déplace les fichiers selon la mapping table"""
    migrations = {
        # Couche Business
        "main.py": "business/api/main.py",
        "schemas.py": "business/validation/schemas.py",
        "safe_start.py": "business/services/safe_start.py",
        "exemple_utilisation.py": "business/examples/exemple_utilisation.py",
        
        # Couche Database  
        "database.py": "database/config/database.py",
        "models.py": "database/models/models.py",
        "crud.py": "database/repository/crud.py",
        "seed_data.py": "database/fixtures/seed_data.py",
        
        # Couche Présentation
        "gui_client/main_window.py": "presentation/gui/main_window.py",
        "gui_client/api_client.py": "presentation/gui/api_client.py", 
        "gui_client/__init__.py": "presentation/gui/__init__.py",
        "run_gui.py": "presentation/launchers/run_gui.py",
        "setup_gui.py": "presentation/launchers/setup_gui.py",
        "test_gui_integration.py": "presentation/tests/test_gui_integration.py",
        
        # Couche Infrastructure
        "check_ports.py": "infrastructure/diagnostics/check_ports.py",
        "test_coherence.py": "infrastructure/tests/test_coherence.py",
        
        # Configuration
        "requirements.txt": "config/requirements.txt",
        "setup.bat": "config/setup.bat", 
        "setup.sh": "config/setup.sh"
    }
    
    for old_path, new_path in migrations.items():
        if os.path.exists(old_path):
            shutil.move(old_path, new_path)
            print(f"📦 Déplacé: {old_path} → {new_path}")
```

3. **Met à jour les imports**
```python
def update_imports_in_file(filepath, import_mappings):
    """Met à jour les imports dans un fichier"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old_import, new_import in import_mappings.items():
        content = content.replace(old_import, new_import)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"🔧 Imports mis à jour: {filepath}")
```

## Exercice 4 : Validation post-migration

### Instructions
Créez un script de validation `validate_migration.py` qui vérifie :

1. **Structure des dossiers**
```python
def validate_structure():
    """Vérifie que tous les dossiers sont créés"""
    required_dirs = [
        "presentation/gui", "business/api", "database/config", 
        "infrastructure/diagnostics"
    ]
    
    for dir_path in required_dirs:
        assert os.path.exists(dir_path), f"❌ Manque: {dir_path}"
    
    print("✅ Structure validée")
```

2. **Présence des fichiers**
```python
def validate_files():
    """Vérifie que tous les fichiers sont déplacés"""
    critical_files = [
        "business/api/main.py",
        "presentation/gui/main_window.py", 
        "database/models/models.py",
        "database/repository/crud.py"
    ]
    
    for filepath in critical_files:
        assert os.path.exists(filepath), f"❌ Manque: {filepath}"
    
    print("✅ Fichiers validés")
```

3. **Imports fonctionnels**
```python
def validate_imports():
    """Teste que les imports fonctionnent"""
    try:
        from business.api.main import app
        from database.models.models import User, Item  
        from database.repository.crud import get_users
        from presentation.gui.main_window import MainWindow
        print("✅ Imports validés")
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
```

## Exercice 5 : Documentation post-migration

### Instructions
Après la migration, mettez à jour :

1. **README.md** avec la nouvelle structure
2. **Documentation2** avec les nouveaux chemins
3. **Scripts de démarrage** avec les nouveaux chemins
4. **Tests** pour qu'ils pointent vers les bons modules

## Questions de réflexion

1. **Avantages** : Quels sont les bénéfices de cette organisation ?
2. **Inconvénients** : Quelles difficultés cette migration peut-elle créer ?
3. **Alternatives** : Existe-t-il d'autres façons d'organiser le code ?
4. **Maintenance** : Comment cette structure facilite-t-elle la maintenance ?
5. **Collaboration** : En quoi cette organisation améliore-t-elle le travail en équipe ?

## Critères de réussite

- [ ] Structure de dossiers créée correctement
- [ ] Tous les fichiers déplacés sans perte
- [ ] Imports mis à jour et fonctionnels  
- [ ] Application démarre sans erreur
- [ ] Tests passent avec succès
- [ ] Documentation mise à jour
- [ ] Performance maintenue

## Extension possible

Une fois la migration réussie, proposez :
- **Refactoring** : Améliorer le code maintenant mieux organisé
- **Nouveaux modules** : Ajouter des fonctionnalités par couche
- **Tests unitaires** : Un test par couche architecturale
- **CI/CD** : Pipeline de déploiement par couche

Cet exercice vous permettra de maîtriser l'organisation d'un projet Python selon les bonnes pratiques architecturales !
