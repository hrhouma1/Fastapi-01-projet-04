# Construction du projet étape par étape

## Méthodologie de développement

Ce guide suit une approche **bottom-up** : nous commençons par les fondations (base de données) et remontons vers l'interface utilisateur. Cette méthode assure :
- Des fondations solides avant de construire
- La possibilité de tester chaque couche indépendamment
- Une progression logique et compréhensible

## ÉTAPE 1 : Configuration de l'environnement

### 1.1 Création du projet

```bash
# Création du dossier projet
mkdir fastapi-crud-project
cd fastapi-crud-project

# Création de l'environnement virtuel
python -m venv venv

# Activation (Windows)
venv\Scripts\activate
# Activation (Linux/Mac)
source venv/bin/activate
```

### 1.2 Installation des dépendances

```bash
# Installation des dépendances principales
pip install fastapi uvicorn sqlalchemy pydantic[email] python-multipart

# Installation des dépendances de développement
pip install pytest httpx

# Génération du fichier requirements.txt
pip freeze > requirements.txt
```

**Explication des dépendances :**
- `fastapi` : Framework web principal
- `uvicorn` : Serveur ASGI pour FastAPI
- `sqlalchemy` : ORM pour la base de données
- `pydantic[email]` : Validation des données avec support email
- `python-multipart` : Support des formulaires multipart
- `pytest` : Framework de tests
- `httpx` : Client HTTP pour les tests

### 1.3 Structure initiale du projet

```
fastapi-crud-project/
├── venv/                 # Environnement virtuel
├── requirements.txt      # Dépendances
├── main.py              # Point d'entrée (à créer)
├── database.py          # Configuration BDD (à créer)
├── models.py            # Modèles SQLAlchemy (à créer)
├── schemas.py           # Schémas Pydantic (à créer)
├── crud.py              # Opérations CRUD (à créer)
└── sql_app.db          # Base SQLite (générée automatiquement)
```

## ÉTAPE 2 : Configuration de la base de données

### 2.1 Création de database.py

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de données SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Création du moteur SQLAlchemy
# check_same_thread=False nécessaire pour SQLite avec FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Factory pour créer des sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour les modèles
Base = declarative_base()
```

**Concepts clés :**
- **Engine** : Point de connexion à la base de données
- **SessionLocal** : Factory pour créer des sessions de travail
- **Base** : Classe mère pour tous les modèles SQLAlchemy

### 2.2 Fonction de gestion des sessions

```python
# Ajout dans database.py
def get_db():
    """
    Générateur de session de base de données.
    Assure la fermeture automatique de la session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Pattern utilisé :** Generator Pattern
- `yield` suspend l'exécution et retourne la session
- Le bloc `finally` garantit la fermeture même en cas d'erreur
- FastAPI gère automatiquement le cycle de vie via l'injection de dépendance

## ÉTAPE 3 : Définition des modèles de données

### 3.1 Création de models.py

```python
# models.py
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    """
    Modèle représentant un utilisateur
    """
    __tablename__ = "users"
    
    # Clé primaire avec auto-incrémentation
    id = Column(Integer, primary_key=True, index=True)
    
    # Email unique avec index pour les recherches rapides
    email = Column(String, unique=True, index=True, nullable=False)
    
    # Informations personnelles
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    
    # Statut actif/inactif
    is_active = Column(Boolean, default=True)
    
    # Timestamp de création automatique
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relation one-to-many avec les articles
    items = relationship("Item", back_populates="owner", cascade="all, delete-orphan")

class Item(Base):
    """
    Modèle représentant un article
    """
    __tablename__ = "items"
    
    # Clé primaire
    id = Column(Integer, primary_key=True, index=True)
    
    # Informations de l'article
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    
    # Statut disponible/indisponible
    is_available = Column(Boolean, default=True)
    
    # Timestamps automatiques
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Clé étrangère vers User
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relation many-to-one avec User
    owner = relationship("User", back_populates="items")
```

**Concepts avancés :**

#### Relations SQLAlchemy
- `relationship()` : Définit les relations entre modèles
- `back_populates` : Relation bidirectionnelle
- `cascade="all, delete-orphan"` : Supprime les articles quand l'utilisateur est supprimé

#### Index et contraintes
- `index=True` : Crée un index pour les recherches rapides
- `unique=True` : Contrainte d'unicité
- `nullable=False` : Champ obligatoire

#### Timestamps automatiques
- `server_default=func.now()` : Valeur par défaut côté base
- `onupdate=func.now()` : Mise à jour automatique

## ÉTAPE 4 : Schémas Pydantic

### 4.1 Création de schemas.py

```python
# schemas.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime

# Schémas de base (communs)
class UserBase(BaseModel):
    email: EmailStr
    nom: str
    prenom: str
    is_active: bool = True

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

# Schémas pour la création (POST)
class UserCreate(UserBase):
    @validator('nom', 'prenom')
    def validate_names(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Le nom doit contenir au moins 2 caractères')
        return v.strip().title()
    
    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Le prix doit être positif')
        return round(v, 2)

class ItemCreate(ItemBase):
    pass

# Schémas pour la mise à jour (PUT/PATCH)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nom: Optional[str] = None
    prenom: Optional[str] = None
    is_active: Optional[bool] = None

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None

# Schémas pour la réponse (avec ID et timestamps)
class User(UserBase):
    id: int
    created_at: datetime
    items: List['Item'] = []  # Relation chargée optionnellement
    
    class Config:
        orm_mode = True  # Permet la conversion depuis SQLAlchemy

class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: int
    
    class Config:
        orm_mode = True

# Nécessaire pour les références circulaires
User.model_rebuild()
```

**Architecture des schémas :**
- **Base** : Champs communs pour validation
- **Create** : Validation stricte pour création
- **Update** : Tous champs optionnels pour mise à jour
- **Response** : Inclut ID et métadonnées pour les réponses API

## ÉTAPE 5 : Opérations CRUD

### 5.1 Création de crud.py

```python
# crud.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional, List
import models
import schemas

# ================== UTILISATEURS ==================

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Récupérer un utilisateur par son ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Récupérer un utilisateur par son email"""
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """Récupérer une liste d'utilisateurs avec pagination"""
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Créer un nouvel utilisateur"""
    # Vérification d'unicité de l'email
    existing_user = get_user_by_email(db, email=user.email)
    if existing_user:
        raise ValueError("Un utilisateur avec cet email existe déjà")
    
    # Création du modèle SQLAlchemy
    db_user = models.User(
        email=user.email,
        nom=user.nom,
        prenom=user.prenom,
        is_active=user.is_active
    )
    
    # Ajout à la session et commit
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Récupère l'ID généré
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate) -> Optional[models.User]:
    """Mettre à jour un utilisateur existant"""
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        return None
    
    # Mise à jour uniquement des champs fournis
    update_data = user.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    """Supprimer un utilisateur"""
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

# ================== ARTICLES ==================

def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    """Récupérer un article par son ID"""
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[models.Item]:
    """Récupérer une liste d'articles avec pagination"""
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_items_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Item]:
    """Récupérer les articles d'un utilisateur spécifique"""
    return db.query(models.Item).filter(
        models.Item.owner_id == user_id
    ).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int) -> models.Item:
    """Créer un nouvel article pour un utilisateur"""
    # Vérification que l'utilisateur existe
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        raise ValueError(f"L'utilisateur avec l'ID {user_id} n'existe pas")
    
    db_item = models.Item(
        title=item.title,
        description=item.description,
        price=item.price,
        is_available=item.is_available,
        owner_id=user_id
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: schemas.ItemUpdate) -> Optional[models.Item]:
    """Mettre à jour un article"""
    db_item = get_item(db, item_id=item_id)
    if not db_item:
        return None
    
    update_data = item.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int) -> bool:
    """Supprimer un article"""
    db_item = get_item(db, item_id=item_id)
    if not db_item:
        return False
    
    db.delete(db_item)
    db.commit()
    return True

# ================== RECHERCHE ==================

def search_items(db: Session, query: str, limit: int = 50) -> List[models.Item]:
    """
    Rechercher des articles par mot-clé dans le titre ou la description
    """
    search_pattern = f"%{query}%"
    
    return db.query(models.Item).filter(
        or_(
            models.Item.title.ilike(search_pattern),
            models.Item.description.ilike(search_pattern)
        )
    ).limit(limit).all()
```

**Bonnes pratiques CRUD :**

#### Gestion des erreurs
- Vérification d'existence avant opération
- Exceptions explicites avec messages clairs
- Retour de None pour les éléments non trouvés

#### Performance
- Utilisation d'index pour les recherches fréquentes
- Pagination systématique avec skip/limit
- Requêtes optimisées avec filtres appropriés

#### Intégrité des données
- Vérification des contraintes métier
- Validation des relations (foreign keys)
- Transactions automatiques avec commit/rollback

## ÉTAPE 6 : API FastAPI

### 6.1 Création de main.py

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import uvicorn

import crud
import models
import schemas
from database import SessionLocal, engine, get_db

# Création des tables si elles n'existent pas
models.Base.metadata.create_all(bind=engine)

# Création de l'application FastAPI
app = FastAPI(
    title="API CRUD FastAPI",
    description="API complète pour la gestion d'utilisateurs et d'articles",
    version="1.0.0",
    contact={
        "name": "Développeur API",
        "email": "dev@exemple.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# ================== ENDPOINTS UTILISATEURS ==================

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Créer un nouvel utilisateur
    
    - **email**: adresse email unique (obligatoire)
    - **nom**: nom de famille (obligatoire)
    - **prenom**: prénom (obligatoire)
    - **is_active**: statut actif (défaut: true)
    """
    try:
        return crud.create_user(db=db, user=user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/", response_model=List[schemas.User], tags=["users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupérer la liste des utilisateurs
    
    - **skip**: nombre d'éléments à ignorer (pagination)
    - **limit**: nombre maximum d'éléments à retourner
    """
    if limit > 100:
        limit = 100
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User, tags=["users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Récupérer un utilisateur par son ID
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User, tags=["users"])
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Mettre à jour un utilisateur existant
    """
    db_user = crud.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Supprimer un utilisateur
    """
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return None

# ================== ENDPOINTS ARTICLES ==================

@app.post("/users/{user_id}/items/", response_model=schemas.Item, status_code=status.HTTP_201_CREATED, tags=["items"])
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Créer un nouvel article pour un utilisateur
    """
    try:
        return crud.create_user_item(db=db, item=item, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/items/", response_model=List[schemas.Item], tags=["items"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupérer la liste des articles
    """
    if limit > 100:
        limit = 100
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/{item_id}", response_model=schemas.Item, tags=["items"])
def read_item(item_id: int, db: Session = Depends(get_db)):
    """
    Récupérer un article par son ID
    """
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return db_item

@app.put("/items/{item_id}", response_model=schemas.Item, tags=["items"])
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    """
    Mettre à jour un article
    """
    db_item = crud.update_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return db_item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["items"])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Supprimer un article
    """
    success = crud.delete_item(db, item_id=item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return None

# ================== ENDPOINT RECHERCHE ==================

@app.get("/search/items", response_model=List[schemas.Item], tags=["search"])
def search_items(q: str, limit: int = 50, db: Session = Depends(get_db)):
    """
    Rechercher des articles par mot-clé dans le titre ou la description
    
    - **q**: terme de recherche (minimum 2 caractères)
    - **limit**: nombre maximum de résultats (défaut: 50, max: 100)
    """
    if len(q.strip()) < 2:
        raise HTTPException(
            status_code=400, 
            detail="Le terme de recherche doit contenir au moins 2 caractères"
        )
    
    if limit > 100:
        limit = 100
    
    items = crud.search_items(db, query=q.strip(), limit=limit)
    return items

# ================== ENDPOINT RACINE ==================

@app.get("/", tags=["root"])
def read_root():
    """
    Endpoint racine de l'API
    """
    return {
        "message": "API CRUD FastAPI",
        "version": "1.0.0",
        "documentation": "/docs",
        "redoc": "/redoc"
    }

# ================== LANCEMENT DU SERVEUR ==================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Rechargement automatique en développement
        log_level="info"
    )
```

### 6.2 Test de l'API

```bash
# Lancement du serveur
python main.py

# Ou avec uvicorn directement
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**URLs importantes :**
- API : http://localhost:8000
- Documentation Swagger : http://localhost:8000/docs
- Documentation ReDoc : http://localhost:8000/redoc
- Schéma OpenAPI : http://localhost:8000/openapi.json

### 6.3 Tests manuels avec curl

```bash
# Créer un utilisateur
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@exemple.com",
       "nom": "Dupont",
       "prenom": "Jean",
       "is_active": true
     }'

# Lister les utilisateurs
curl "http://localhost:8000/users/"

# Créer un article
curl -X POST "http://localhost:8000/users/1/items/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "MacBook Pro",
       "description": "Ordinateur portable Apple",
       "price": 2499.99,
       "is_available": true
     }'

# Rechercher des articles
curl "http://localhost:8000/search/items?q=MacBook&limit=10"
```

L'API est maintenant fonctionnelle avec toutes les opérations CRUD et la recherche.

Passez au module suivant : **05-base-de-donnees-sqlalchemy.md**
