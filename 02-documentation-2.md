# Architecture 3-Couches - Documentation Technique

## Identification des Dossiers d'Architecture

Dans ce projet, seuls **4 dossiers** correspondent réellement à l'architecture applicative 3-couches :

### 1. PRESENTATION (Couche Présentation)
**Dossier :** `presentation/`

**Responsabilité :** Interface utilisateur et clients
- Interface graphique PySide6
- Clients HTTP pour communication avec l'API
- Scripts de lancement des interfaces

**Structure :**
```
presentation/
├── gui/
│   ├── api_client.py     # Client HTTP
│   ├── main_window.py    # Interface graphique
│   └── __init__.py
└── launchers/
    └── run_gui.py        # Script de lancement
```

### 2. BUSINESS (Couche Logique Métier)
**Dossier :** `business/`

**Responsabilité :** Logique applicative et règles métier
- API REST FastAPI avec endpoints
- Validation des données avec Pydantic
- Services métier et règles business

**Structure :**
```
business/
├── api/
│   └── main.py           # API FastAPI
├── validation/
│   └── schemas.py        # Schémas Pydantic
└── services/
    └── safe_start.py     # Services métier
```

### 3. DATABASE (Couche Données)
**Dossier :** `database/`

**Responsabilité :** Persistance et accès aux données
- Configuration de la base de données
- Modèles ORM SQLAlchemy
- Opérations CRUD sur les données

**Structure :**
```
database/
├── config/
│   └── database.py       # Configuration SQLAlchemy
├── models/
│   └── models.py         # Modèles ORM
└── repository/
    └── crud.py           # Opérations CRUD
```

### 4. INFRASTRUCTURE (Couche Infrastructure)
**Dossier :** `infrastructure/`

**Responsabilité :** Services transversaux et techniques
- Diagnostic système
- Gestion des ports et processus
- Monitoring et outils techniques

**Structure :**
```
infrastructure/
└── diagnostics/
    └── check_ports.py    # Diagnostic ports
```

## Dossiers Non-Architecturaux

Les autres dossiers ne font **PAS partie** de l'architecture 3-couches :

### Dossiers de Support
- **`config/`** - Fichiers de configuration (requirements.txt, setup scripts)
- **`tests/`** - Tests et validation du code
- **`examples/`** - Exemples d'utilisation et données de test
- **`database_files/`** - Fichiers de base de données générés

### Dossiers Dépréciés/Utilitaires
- **`legacy/`** - Anciens fichiers de l'architecture monolithique
- **`scripts/`** - Scripts utilitaires futurs (vide actuellement)
- **`venv/`** - Environnement virtuel Python
- **`__pycache__/`** - Cache Python généré

## Architecture 3-Couches Classique

### Définition Standard
Une architecture 3-couches sépare l'application en trois niveaux distincts :

1. **Couche Présentation** - Interface utilisateur
2. **Couche Logique Métier** - Règles business et traitement
3. **Couche Données** - Persistance et accès aux données

### Adaptation dans ce Projet
Ce projet implémente une **architecture 4-couches** en ajoutant :

4. **Couche Infrastructure** - Services techniques transversaux

Cette couche supplémentaire améliore la séparation des préoccupations en isolant les aspects techniques (monitoring, diagnostic) des autres couches métier.

## Flux de Communication

### Communication Inter-Couches
```
Utilisateur
    ↓
PRESENTATION (Interface PySide6)
    ↓ (HTTP REST)
BUSINESS (FastAPI + Validation)
    ↓ (Appels de méthodes)
DATABASE (CRUD + ORM)
    ↓ (SQL)
Base de données SQLite
```

### Règles de Communication
1. **Présentation** communique uniquement avec **Business**
2. **Business** communique uniquement avec **Database**  
3. **Infrastructure** peut être utilisée par toutes les couches
4. Aucune couche ne peut contourner la couche immédiatement inférieure

## Séparation des Responsabilités

### Couche Présentation
- Affichage des données à l'utilisateur
- Capture des actions utilisateur
- Formatage des données pour l'affichage
- Gestion des événements interface

### Couche Business
- Validation des données d'entrée
- Application des règles métier
- Orchestration des opérations
- Gestion des erreurs métier

### Couche Database  
- Persistance des données
- Requêtes et modifications en base
- Gestion des transactions
- Mapping objet-relationnel

### Couche Infrastructure
- Services techniques (ports, processus)
- Monitoring et diagnostic
- Configuration système
- Outils de développement

## Avantages de cette Architecture

### Maintenabilité
- Code organisé par responsabilité claire
- Modifications isolées dans une couche
- Impact limité lors des changements

### Testabilité
- Tests unitaires par couche
- Isolation des dépendances
- Mocking facilité entre couches

### Évolutivité
- Remplacement d'une couche sans impact
- Ajout de fonctionnalités par couche
- Migration vers microservices facilitée

### Collaboration
- Équipes spécialisées par couche
- Développement parallèle possible
- Réduction des conflits de code

## Conclusion

L'architecture de ce projet respecte les principes de l'architecture 3-couches classique tout en ajoutant une couche infrastructure pour améliorer la séparation des préoccupations techniques. Les 4 dossiers principaux (presentation, business, database, infrastructure) constituent le coeur architectural de l'application, tandis que les autres dossiers fournissent le support nécessaire au développement et au déploiement.
