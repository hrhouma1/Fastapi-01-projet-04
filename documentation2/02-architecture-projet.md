# Architecture du projet FastAPI CRUD

## Vue d'ensemble de l'architecture

### Architecture 3-tiers

Notre application suit une architecture en couches classique :

```
┌─────────────────────┐
│   PRÉSENTATION     │  Interface graphique PySide6
│   (GUI Client)     │  Communication HTTP/REST
└─────────────────────┘
           │
┌─────────────────────┐
│      MÉTIER        │  API FastAPI
│   (Business Logic) │  Validation, logique métier
└─────────────────────┘
           │
┌─────────────────────┐
│     DONNÉES        │  SQLAlchemy ORM
│   (Data Layer)     │  Base de données SQLite
└─────────────────────┘
```

### Séparation des responsabilités

Chaque composant a un rôle spécifique et bien défini :

#### Couche Présentation (GUI)
- **Responsabilité** : Interface utilisateur et expérience utilisateur
- **Technologies** : PySide6, Qt Designer
- **Communication** : Appels HTTP vers l'API

#### Couche Métier (API)
- **Responsabilité** : Logique métier, validation, orchestration
- **Technologies** : FastAPI, Pydantic
- **Communication** : HTTP REST, JSON

#### Couche Données (Database)
- **Responsabilité** : Persistance, intégrité des données
- **Technologies** : SQLAlchemy, SQLite
- **Communication** : ORM, SQL

## Analyse détaillée des fichiers

### 1. main.py - Point d'entrée de l'API

```python
# Rôle principal
app = FastAPI(
    title="API CRUD FastAPI",
    description="API complète pour gérer utilisateurs et articles",
    version="1.0.0"
)
```

**Responsabilités :**
- Création de l'instance FastAPI
- Définition des endpoints (routes)
- Configuration des middlewares
- Gestion des erreurs globales
- Documentation OpenAPI

**Pattern utilisé :** Controller/Router pattern
- Chaque endpoint est un contrôleur
- Les routes sont organisées par domaine (users, items, search)

### 2. models.py - Modèles de données SQLAlchemy

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    # Relations
    items = relationship("Item", back_populates="owner")
```

**Responsabilités :**
- Définition de la structure des tables
- Relations entre entités
- Contraintes d'intégrité
- Index pour les performances

**Pattern utilisé :** Active Record / Data Mapper
- Les modèles représentent les tables
- SQLAlchemy gère la correspondance objet-relationnel

### 3. schemas.py - Schémas Pydantic

```python
class UserCreate(BaseModel):
    email: EmailStr
    nom: str
    prenom: str
    is_active: bool = True
```

**Responsabilités :**
- Validation des données entrantes
- Sérialisation des données sortantes
- Documentation automatique des APIs
- Conversion de types

**Pattern utilisé :** DTO (Data Transfer Object)
- Les schémas définissent le format des données échangées
- Séparation entre modèles de données et modèles d'API

### 4. crud.py - Opérations base de données

```python
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
```

**Responsabilités :**
- Opérations CRUD (Create, Read, Update, Delete)
- Requêtes complexes et filtres
- Logique d'accès aux données
- Gestion des relations

**Pattern utilisé :** Repository Pattern
- Abstraction de l'accès aux données
- Interface claire pour les opérations de base
- Réutilisabilité du code

### 5. database.py - Configuration base de données

```python
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

**Responsabilités :**
- Configuration de la connexion
- Création du moteur SQLAlchemy
- Gestion des sessions
- Création des tables

**Pattern utilisé :** Factory Pattern
- SessionLocal est une factory pour créer des sessions
- Configuration centralisée de la base

### 6. gui_client/main_window.py - Interface graphique

```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient("http://localhost:8000")
```

**Responsabilités :**
- Interface utilisateur graphique
- Gestion des événements utilisateur
- Communication avec l'API
- Mise à jour de l'affichage

**Pattern utilisé :** MVC (Model-View-Controller)
- Vue : Les widgets Qt
- Contrôleur : Les méthodes de gestion d'événements
- Modèle : Les données via l'API

### 7. gui_client/api_client.py - Client API

```python
class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
```

**Responsabilités :**
- Communication HTTP avec l'API
- Gestion des erreurs réseau
- Sérialisation/désérialisation JSON
- Authentification (future)

**Pattern utilisé :** Proxy Pattern
- Représente l'API distante localement
- Encapsule la complexité de la communication réseau

## Flux de données

### Création d'un utilisateur

```
1. GUI → Saisie des données dans le formulaire
2. GUI → Validation locale (champs requis)
3. GUI → APIClient.create_user(data)
4. APIClient → POST /users/ avec données JSON
5. FastAPI → Validation Pydantic (UserCreate)
6. FastAPI → crud.create_user(db, user_data)
7. CRUD → Création en base SQLAlchemy
8. CRUD → Retour du modèle User créé
9. FastAPI → Sérialisation Pydantic (UserResponse)
10. APIClient → Réception JSON et conversion
11. GUI → Mise à jour interface utilisateur
```

### Recherche d'articles

```
1. GUI → Saisie terme recherche
2. GUI → APIClient.search_items(query)
3. APIClient → GET /search/items?q=terme
4. FastAPI → Validation paramètres (longueur minimum)
5. FastAPI → crud.search_items(db, query, limit)
6. CRUD → Requête ILIKE sur titre/description
7. CRUD → Retour liste des articles trouvés
8. FastAPI → Sérialisation List[ItemResponse]
9. APIClient → Réception et traitement JSON
10. GUI → Affichage des résultats dans tableau
```

## Avantages de cette architecture

### Modularité
- Chaque composant peut évoluer indépendamment
- Tests isolés par couche
- Maintenance facilitée

### Scalabilité
- L'API peut servir plusieurs clients
- Base de données peut être changée facilement
- Interface peut être remplacée (web, mobile)

### Réutilisabilité
- L'API peut être utilisée par d'autres applications
- Les modèles peuvent être réutilisés
- Le client API peut servir pour d'autres interfaces

### Testabilité
- Tests unitaires par fonction
- Tests d'intégration par couche
- Mocking facilité par l'architecture en couches

## Patterns de conception utilisés

### 1. Dependency Injection (FastAPI)
```python
def get_items(db: Session = Depends(get_db)):
    # db est injectée automatiquement
```
- Inversion de contrôle
- Tests facilités avec mocks
- Couplage faible entre composants

### 2. Repository Pattern (CRUD)
```python
# Interface claire pour l'accès aux données
def get_user(db: Session, user_id: int)
def create_user(db: Session, user: schemas.UserCreate)
```
- Abstraction de la couche de données
- Changement de base de données transparent
- Tests avec base de données mock

### 3. DTO Pattern (Schemas)
```python
class UserCreate(BaseModel):  # Données entrantes
class UserResponse(BaseModel): # Données sortantes
```
- Validation automatique des données
- Sérialisation/désérialisation
- Documentation API automatique

### 4. Factory Pattern (Database)
```python
SessionLocal = sessionmaker(autocommit=False, bind=engine)
```
- Création standardisée des sessions
- Configuration centralisée
- Gestion du cycle de vie des connexions

### 5. Observer Pattern (PySide6)
```python
button.clicked.connect(self.on_button_click)
```
- Communication par signaux/slots
- Couplage faible entre composants UI
- Réactivité de l'interface

## Évolutions possibles de l'architecture

### Court terme
- Ajout d'authentification JWT
- Cache Redis pour les performances
- Logging structuré

### Moyen terme
- Base de données PostgreSQL
- API versioning
- Tests automatisés CI/CD

### Long terme
- Architecture microservices
- Interface web avec React/Vue
- Déploiement conteneurisé (Docker)

Cette architecture solide permet une évolution progressive tout en maintenant la lisibilité et la maintenabilité du code.

Passez au module suivant : **03-fastapi-concepts.md**
