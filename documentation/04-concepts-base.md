# Module 4 : Concepts de base - FastAPI, SQLAlchemy et Pydantic

## Objectifs pédagogiques

À la fin de ce module, vous serez capable de :
- Comprendre le fonctionnement de FastAPI et ses décorateurs
- Maîtriser les concepts de base de SQLAlchemy (ORM, modèles, sessions)
- Utiliser Pydantic pour la validation des données
- Comprendre l'injection de dépendances
- Gérer les erreurs HTTP correctement

## FastAPI - Framework web moderne

### Qu'est-ce que FastAPI

FastAPI est un framework web moderne pour créer des APIs avec Python. Il se base sur les standards Python modernes comme les type hints.

### Décorateurs de routes

Les décorateurs définissent les endpoints de votre API :

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

**Décorateurs disponibles :**
- `@app.get()` : Pour récupérer des données (lecture)
- `@app.post()` : Pour créer de nouvelles ressources
- `@app.put()` : Pour mettre à jour des ressources existantes
- `@app.delete()` : Pour supprimer des ressources
- `@app.patch()` : Pour des mises à jour partielles

### Paramètres d'URL

FastAPI peut extraire automatiquement les paramètres depuis l'URL :

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

**Types supportés :**
- `int` : Nombres entiers
- `str` : Chaînes de caractères
- `float` : Nombres décimaux
- `bool` : Booléens
- `UUID` : Identifiants uniques

### Paramètres de requête

Les paramètres optionnels sont automatiquement détectés :

```python
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

Appel : `GET /items/?skip=5&limit=20`

### Corps de requête

FastAPI utilise Pydantic pour valider automatiquement les données :

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int

@app.post("/users/")
def create_user(user: User):
    return {"message": f"User {user.name} created"}
```

### Réponses HTTP

Vous pouvez spécifier le modèle de réponse :

```python
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    # FastAPI validera automatiquement la réponse
    return User(name="John", email="john@example.com", age=30)
```

### Tags pour la documentation

Organisez vos endpoints dans la documentation :

```python
@app.get("/users/", tags=["Users"])
def get_users():
    pass

@app.get("/items/", tags=["Items"])
def get_items():
    pass
```

## SQLAlchemy - ORM pour Python

### Qu'est-ce qu'un ORM

Un ORM (Object-Relational Mapping) permet de manipuler une base de données avec des objets Python plutôt qu'avec du SQL.

**Avantages :**
- Code plus lisible et maintenable
- Protection contre les injections SQL
- Indépendance du type de base de données
- Relations entre objets automatiques

### Moteur de base de données

Le moteur gère la connexion à la base de données :

```python
from sqlalchemy import create_engine

# SQLite (fichier local)
engine = create_engine("sqlite:///./test.db")

# PostgreSQL (serveur)
engine = create_engine("postgresql://user:password@localhost/dbname")

# MySQL (serveur)
engine = create_engine("mysql://user:password@localhost/dbname")
```

### Sessions

Une session représente une transaction avec la base de données :

```python
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine)

# Utilisation
db = SessionLocal()
try:
    # Opérations sur la base
    db.add(user)
    db.commit()
finally:
    db.close()
```

### Définition des modèles

Les modèles définissent la structure des tables :

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
```

**Types de colonnes courants :**
- `Integer` : Nombres entiers
- `String` : Texte (avec longueur optionnelle)
- `Boolean` : Vrai/Faux
- `DateTime` : Date et heure
- `Text` : Texte long
- `Float` : Nombres décimaux

**Contraintes :**
- `primary_key=True` : Clé primaire
- `unique=True` : Valeur unique
- `nullable=False` : Champ obligatoire
- `default=value` : Valeur par défaut
- `index=True` : Index pour optimiser les recherches

### Relations entre modèles

SQLAlchemy gère automatiquement les relations :

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    # Relation : un utilisateur a plusieurs articles
    articles = relationship("Article", back_populates="owner")

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relation : un article appartient à un utilisateur
    owner = relationship("User", back_populates="articles")
```

**Types de relations :**
- **One-to-Many** : Un utilisateur → Plusieurs articles
- **Many-to-One** : Plusieurs articles → Un utilisateur
- **One-to-One** : Un utilisateur → Un profil
- **Many-to-Many** : Plusieurs utilisateurs ↔ Plusieurs groupes

### Requêtes de base

```python
# Créer
user = User(name="John", email="john@example.com")
db.add(user)
db.commit()

# Lire
user = db.query(User).filter(User.id == 1).first()
users = db.query(User).all()
users = db.query(User).limit(10).all()

# Mettre à jour
user = db.query(User).filter(User.id == 1).first()
user.name = "John Doe"
db.commit()

# Supprimer
user = db.query(User).filter(User.id == 1).first()
db.delete(user)
db.commit()
```

### Filtres avancés

```python
# Égalité
users = db.query(User).filter(User.name == "John").all()

# Comparaison
users = db.query(User).filter(User.age > 18).all()

# Like (contient)
users = db.query(User).filter(User.name.like("%john%")).all()

# In (dans une liste)
users = db.query(User).filter(User.id.in_([1, 2, 3])).all()

# Et/Ou
from sqlalchemy import and_, or_

users = db.query(User).filter(
    and_(User.age > 18, User.name == "John")
).all()

users = db.query(User).filter(
    or_(User.age > 65, User.age < 18)
).all()
```

## Pydantic - Validation des données

### Qu'est-ce que Pydantic

Pydantic est une bibliothèque qui utilise les type hints Python pour valider les données.

### Modèles de base

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    name: str
    email: str
    age: int
    is_active: bool = True  # Valeur par défaut
    created_at: Optional[datetime] = None  # Optionnel
```

### Types supportés

**Types de base :**
- `str` : Chaîne de caractères
- `int` : Nombre entier
- `float` : Nombre décimal
- `bool` : Booléen
- `bytes` : Données binaires

**Types complexes :**
- `List[Type]` : Liste d'éléments
- `Dict[str, Type]` : Dictionnaire
- `Optional[Type]` : Valeur optionnelle
- `Union[Type1, Type2]` : Plusieurs types possibles

**Types spécialisés :**
- `EmailStr` : Adresse email valide
- `AnyUrl` : URL valide
- `UUID` : Identifiant unique
- `datetime` : Date et heure

### Validation personnalisée

```python
from pydantic import BaseModel, validator

class User(BaseModel):
    name: str
    age: int
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Le nom ne peut pas être vide')
        return v.title()  # Première lettre en majuscule
    
    @validator('age')
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('L\'âge doit être positif')
        if v > 120:
            raise ValueError('L\'âge doit être réaliste')
        return v
```

### Configuration des modèles

```python
class User(BaseModel):
    name: str
    email: str
    
    class Config:
        # Permet la conversion depuis les objets SQLAlchemy
        from_attributes = True
        
        # Exemple de valeurs pour la documentation
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com"
            }
        }
```

### Sérialisation et désérialisation

```python
# Depuis un dictionnaire
data = {"name": "John", "email": "john@example.com", "age": 30}
user = User(**data)

# Vers un dictionnaire
user_dict = user.model_dump()

# Vers JSON
user_json = user.model_dump_json()

# Depuis JSON
user = User.model_validate_json(user_json)
```

## Injection de dépendances avec FastAPI

### Principe

L'injection de dépendances permet de fournir automatiquement des ressources aux fonctions.

### Dépendance simple

```python
from fastapi import Depends

def get_current_user():
    return {"user": "john"}

@app.get("/profile")
def read_profile(current_user = Depends(get_current_user)):
    return current_user
```

### Dépendance avec paramètres

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

### Dépendances imbriquées

```python
def get_token(token: str):
    return token

def get_current_user(token: str = Depends(get_token)):
    # Validation du token
    return {"user": "john"}

@app.get("/profile")
def read_profile(user = Depends(get_current_user)):
    return user
```

### Dépendances au niveau application

```python
# Applique la dépendance à tous les endpoints
app = FastAPI(dependencies=[Depends(verify_api_key)])
```

## Gestion des erreurs HTTP

### Codes de statut courants

- **200 OK** : Requête réussie
- **201 Created** : Ressource créée avec succès
- **400 Bad Request** : Données invalides
- **401 Unauthorized** : Authentification requise
- **403 Forbidden** : Accès interdit
- **404 Not Found** : Ressource non trouvée
- **422 Unprocessable Entity** : Validation échouée
- **500 Internal Server Error** : Erreur serveur

### Lever des exceptions

```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur non trouvé"
        )
    
    return user
```

### Gestionnaires d'exceptions personnalisés

```python
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": f"Erreur de validation: {exc}"}
    )
```

### Validation automatique

FastAPI valide automatiquement :

```python
class UserCreate(BaseModel):
    name: str
    age: int

@app.post("/users/")
def create_user(user: UserCreate):
    # Si les données sont invalides, FastAPI retourne
    # automatiquement une erreur 422 avec les détails
    return {"message": "Utilisateur créé"}
```

## Middleware et CORS

### Middleware CORS

Pour permettre les requêtes depuis un navigateur web :

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],  # Méthodes HTTP autorisées
    allow_headers=["*"],  # Headers autorisés
)
```

### Middleware personnalisé

```python
import time

@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## Documentation automatique

### Configuration de la documentation

```python
app = FastAPI(
    title="Mon API",
    description="Une API complète avec FastAPI",
    version="1.0.0",
    docs_url="/docs",  # URL de Swagger UI
    redoc_url="/redoc",  # URL de ReDoc
)
```

### Documentation des endpoints

```python
@app.post(
    "/users/",
    response_model=User,
    status_code=201,
    summary="Créer un utilisateur",
    description="Crée un nouvel utilisateur avec les informations fournies",
    response_description="L'utilisateur créé",
    tags=["Users"]
)
def create_user(user: UserCreate):
    """
    Créer un nouvel utilisateur:
    
    - **name**: nom complet de l'utilisateur
    - **email**: adresse email unique
    - **age**: âge de l'utilisateur
    """
    return user
```

## Tests unitaires de base

### Configuration des tests

```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_user():
    response = client.post(
        "/users/",
        json={"name": "John", "email": "john@example.com", "age": 30}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "John"
```

### Exécution des tests

```bash
pip install pytest
pytest test_main.py
```

## Logging et debugging

### Configuration du logging

```python
import logging

# Configuration basique
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/users/")
def get_users():
    logger.info("Récupération de la liste des utilisateurs")
    return users
```

### Mode debug

```python
# En développement uniquement
uvicorn.run(app, host="0.0.0.0", port=8000, debug=True, reload=True)
```

## Exercices pratiques

### Exercice 1 : Endpoint simple

Créez un endpoint qui retourne les informations système :

```python
import platform
from datetime import datetime

@app.get("/system/info")
def get_system_info():
    return {
        "os": platform.system(),
        "python_version": platform.python_version(),
        "current_time": datetime.now().isoformat()
    }
```

### Exercice 2 : Validation personnalisée

Créez un modèle Product avec validation :

```python
class Product(BaseModel):
    name: str
    price: float
    category: str
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Le prix doit être positif')
        return v
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Le nom ne peut pas être vide')
        return v.title()
```

### Exercice 3 : Requête avec filtres

Créez un endpoint de recherche d'utilisateurs :

```python
@app.get("/users/search")
def search_users(
    name: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(User)
    
    if name:
        query = query.filter(User.name.contains(name))
    if min_age:
        query = query.filter(User.age >= min_age)
    if max_age:
        query = query.filter(User.age <= max_age)
    
    return query.all()
```

## Prochaines étapes

Dans le module suivant, vous appliquerez tous ces concepts pour créer votre API CRUD complète étape par étape, en comprenant chaque ligne de code.

Assurez-vous de bien maîtriser :
- Les décorateurs FastAPI et leurs paramètres
- La définition de modèles SQLAlchemy
- La validation avec Pydantic
- L'injection de dépendances
- La gestion des erreurs HTTP
