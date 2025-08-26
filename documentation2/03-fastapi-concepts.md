# FastAPI - Concepts et techniques avancées

## Introduction à FastAPI

FastAPI est un framework web moderne pour construire des APIs avec Python. Il combine :
- **Performance** : Parmi les frameworks Python les plus rapides
- **Simplicité** : Syntaxe intuitive basée sur les type hints
- **Documentation** : Génération automatique OpenAPI/Swagger
- **Validation** : Intégrée avec Pydantic

## Anatomie d'une application FastAPI

### 1. Création de l'application

```python
from fastapi import FastAPI

app = FastAPI(
    title="Mon API",
    description="Description de l'API",
    version="1.0.0",
    docs_url="/docs",           # URL de la documentation Swagger
    redoc_url="/redoc"          # URL de la documentation ReDoc
)
```

**Paramètres importants :**
- `title` : Nom affiché dans la documentation
- `description` : Description détaillée
- `version` : Version de l'API pour le suivi
- `docs_url` : Endpoint de la documentation interactive
- `openapi_url` : URL du schéma OpenAPI JSON

### 2. Définition des endpoints

#### GET - Lecture de données

```python
@app.get("/users/", response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupérer la liste des utilisateurs avec pagination
    
    - **skip**: nombre d'éléments à ignorer (défaut: 0)
    - **limit**: nombre maximum d'éléments à retourner (défaut: 100)
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
```

**Éléments clés :**
- `@app.get()` : Décorateur définissant la méthode HTTP et l'URL
- `response_model` : Schéma Pydantic pour la validation de sortie
- Paramètres de requête avec valeurs par défaut
- Injection de dépendance avec `Depends()`
- Docstring pour la documentation automatique

#### POST - Création de données

```python
@app.post("/users/", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Créer un nouvel utilisateur
    
    - **email**: adresse email unique (obligatoire)
    - **nom**: nom de famille (obligatoire)  
    - **prenom**: prénom (obligatoire)
    - **is_active**: statut actif (défaut: true)
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    return crud.create_user(db=db, user=user)
```

**Bonnes pratiques :**
- Status code 201 pour les créations
- Validation des données avec Pydantic
- Vérification d'unicité avant création
- Gestion d'erreurs avec HTTPException

#### PUT - Mise à jour complète

```python
@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Mettre à jour un utilisateur existant
    """
    db_user = crud.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_user
```

#### DELETE - Suppression

```python
@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Supprimer un utilisateur
    """
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return None  # Status 204 No Content
```

## Validation avec Pydantic

### Modèles de base

```python
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr           # Validation email automatique
    nom: str
    prenom: str
    is_active: bool = True    # Valeur par défaut

class UserCreate(UserBase):
    pass  # Hérite de UserBase, utilisé pour les POST

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None  # Champs optionnels pour PUT/PATCH
    nom: Optional[str] = None
    prenom: Optional[str] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True  # Permet la conversion depuis les modèles SQLAlchemy

class User(UserInDB):
    pass  # Modèle de réponse, identique à UserInDB
```

### Validateurs personnalisés

```python
from pydantic import validator
import re

class UserCreate(UserBase):
    @validator('nom', 'prenom')
    def validate_names(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Le nom doit contenir au moins 2 caractères')
        if not re.match(r'^[a-zA-ZÀ-ÿ\s\-\']+$', v):
            raise ValueError('Le nom contient des caractères non autorisés')
        return v.strip().title()  # Normalisation : première lettre majuscule
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Format d\'email invalide')
        domain = v.split('@')[1]
        if '.' not in domain:
            raise ValueError('Domaine email invalide')
        return v.lower()  # Normalisation en minuscules
```

## Gestion des erreurs et exceptions

### HTTPException

```python
from fastapi import HTTPException, status

# Erreur 404
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Utilisateur non trouvé"
)

# Erreur 400 avec détails
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "error": "Validation échouée",
        "field": "email",
        "message": "Email déjà existant"
    }
)
```

### Gestionnaire d'exceptions personnalisé

```python
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """
    Gestionnaire personnalisé pour les erreurs de validation Pydantic
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "Erreurs de validation",
            "details": errors,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

## Injection de dépendances

### Dépendance de base de données

```python
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db():
    """
    Générateur de session de base de données
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utilisation dans un endpoint
@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)
```

### Dépendances avec paramètres

```python
def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    """
    Paramètres communs de pagination et recherche
    """
    if limit > 100:
        limit = 100
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/users/")
def get_users(commons: dict = Depends(common_parameters), db: Session = Depends(get_db)):
    if commons["q"]:
        return crud.search_users(db, query=commons["q"], skip=commons["skip"], limit=commons["limit"])
    return crud.get_users(db, skip=commons["skip"], limit=commons["limit"])
```

### Dépendances de sécurité

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Vérification du token JWT
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token invalide")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

# Endpoint protégé
@app.get("/users/me")
def get_current_user(user_id: int = Depends(verify_token), db: Session = Depends(get_db)):
    return crud.get_user(db, user_id=user_id)
```

## Middleware et fonctionnalités avancées

### Middleware CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://monapp.com"],  # Origines autorisées
    allow_credentials=True,                                          # Cookies autorisés
    allow_methods=["GET", "POST", "PUT", "DELETE"],                 # Méthodes autorisées
    allow_headers=["*"],                                            # Headers autorisés
)
```

### Middleware de logging

```python
import time
import logging
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log toutes les requêtes HTTP
    """
    start_time = time.time()
    
    # Log de la requête entrante
    logging.info(f"Requête: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Log de la réponse
    process_time = time.time() - start_time
    logging.info(f"Réponse: {response.status_code} en {process_time:.3f}s")
    
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## Documentation automatique

### Tags et métadonnées

```python
tags_metadata = [
    {
        "name": "users",
        "description": "Opérations sur les utilisateurs",
    },
    {
        "name": "items",
        "description": "Gestion des articles",
    },
    {
        "name": "search",
        "description": "Fonctionnalités de recherche",
    },
]

app = FastAPI(
    title="API CRUD",
    openapi_tags=tags_metadata
)

@app.post("/users/", tags=["users"], summary="Créer un utilisateur")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Créer un nouvel utilisateur avec les informations suivantes :
    
    - **email** : Adresse email unique (format valide requis)
    - **nom** : Nom de famille (minimum 2 caractères)
    - **prenom** : Prénom (minimum 2 caractères)  
    - **is_active** : Statut actif (optionnel, défaut: true)
    
    Retourne l'utilisateur créé avec son ID généré automatiquement.
    """
    return crud.create_user(db=db, user=user)
```

### Exemples dans la documentation

```python
from fastapi import FastAPI, Body

@app.post("/users/")
def create_user(
    user: schemas.UserCreate = Body(
        ...,
        example={
            "email": "john.doe@exemple.com",
            "nom": "Doe",
            "prenom": "John",
            "is_active": True
        }
    )
):
    return crud.create_user(db=db, user=user)
```

## Tests avec FastAPI

### Configuration des tests

```python
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Base de données de test en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/users/",
        json={
            "email": "test@exemple.com",
            "nom": "Test",
            "prenom": "Utilisateur",
            "is_active": True
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@exemple.com"
    assert "id" in data
```

Cette approche méthodique de FastAPI garantit des APIs robustes, bien documentées et facilement testables.

Passez au module suivant : **04-construction-etape-par-etape.md**
