# Module 3 : Structure du projet et organisation des fichiers

## Objectifs pédagogiques

À la fin de ce module, vous serez capable de :
- Comprendre la structure d'un projet FastAPI professionnel
- Créer tous les fichiers de base nécessaires
- Comprendre le rôle de chaque fichier
- Organiser votre code de manière maintenant

## Architecture du projet

### Vue d'ensemble

Notre projet suit une architecture modulaire où chaque fichier a une responsabilité spécifique :

```
projetsfastapi/
├── venv/                    # Environnement virtuel (ne pas modifier)
├── documentation/           # Documentation du projet
├── main.py                  # Point d'entrée de l'application
├── database.py              # Configuration de la base de données
├── models.py                # Modèles SQLAlchemy (structure des tables)
├── schemas.py               # Schémas Pydantic (validation des données)
├── crud.py                  # Opérations CRUD (logique métier)
├── requirements.txt         # Dépendances Python
├── api_tests.http          # Tests HTTP pour l'API
├── exemple_utilisation.py   # Script de démonstration
├── test_coherence.py       # Tests de validation
├── safe_start.py           # Script de démarrage sécurisé
├── check_ports.py          # Diagnostic des ports
├── setup.bat               # Configuration automatique Windows
├── setup.sh                # Configuration automatique Unix/Linux
├── .gitignore              # Fichiers à ignorer par Git
└── README.md               # Documentation principale
```

### Principe de séparation des responsabilités

Chaque fichier a un rôle précis :
- **Un seul concept par fichier**
- **Dépendances claires entre les modules**
- **Facilité de maintenance et de test**

## Création des fichiers de base

### 1. Configuration de la base de données (database.py)

Ce fichier configure la connexion à la base de données SQLite.

Créez le fichier `database.py` :

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de données SQLite
# Le fichier test.db sera créé automatiquement dans le dossier du projet
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Créer le moteur de base de données
# check_same_thread=False permet l'utilisation avec FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Créer une classe de session locale
# autocommit=False : Les modifications doivent être explicitement validées
# autoflush=False : Les objets ne sont pas automatiquement synchronisés
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour tous les modèles SQLAlchemy
# Tous nos modèles hériteront de cette classe
Base = declarative_base()
```

**Explication détaillée :**
- `create_engine` : Crée la connexion à la base de données
- `sessionmaker` : Factory pour créer des sessions de base de données  
- `declarative_base` : Classe de base pour tous les modèles

### 2. Modèles de données (models.py)

Ce fichier définit la structure des tables en base de données.

Créez le fichier `models.py` :

```python
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    """
    Modèle représentant un utilisateur dans la base de données
    """
    # Nom de la table en base de données
    __tablename__ = "users"

    # Définition des colonnes
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Colonnes de date automatiques
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relation avec les articles
    # back_populates crée une relation bidirectionnelle
    # cascade="all, delete-orphan" supprime les articles si l'utilisateur est supprimé
    items = relationship("Item", back_populates="owner", cascade="all, delete-orphan")

class Item(Base):
    """
    Modèle représentant un article dans la base de données
    """
    # Nom de la table en base de données
    __tablename__ = "items"

    # Définition des colonnes
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)  # Prix en centimes pour éviter les erreurs d'arrondi
    is_available = Column(Boolean, default=True)
    
    # Colonnes de date automatiques
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Clé étrangère vers la table users
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relation avec l'utilisateur propriétaire
    owner = relationship("User", back_populates="items")
```

**Concepts importants :**
- `primary_key=True` : Clé primaire de la table
- `unique=True` : Valeur unique dans toute la table
- `nullable=False` : Champ obligatoire
- `ForeignKey` : Relation vers une autre table
- `relationship` : Relation objet entre les modèles

### 3. Schémas de validation (schemas.py)

Ce fichier définit les structures de données pour les échanges avec l'API.

Créez le fichier `schemas.py` :

```python
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Schémas pour les articles

class ItemBase(BaseModel):
    """
    Schéma de base pour un article
    Contient les champs communs à la création et à la lecture
    """
    title: str
    description: Optional[str] = None
    price: int  # Prix en centimes
    is_available: bool = True

class ItemCreate(ItemBase):
    """
    Schéma pour créer un nouvel article
    Hérite de ItemBase, aucun champ supplémentaire nécessaire
    """
    pass

class ItemUpdate(BaseModel):
    """
    Schéma pour mettre à jour un article
    Tous les champs sont optionnels pour permettre une mise à jour partielle
    """
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    is_available: Optional[bool] = None

class Item(ItemBase):
    """
    Schéma pour lire un article (réponse de l'API)
    Inclut les champs générés automatiquement (id, dates)
    """
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Permet la conversion depuis les objets SQLAlchemy

# Schémas pour les utilisateurs

class UserBase(BaseModel):
    """
    Schéma de base pour un utilisateur
    """
    email: str
    nom: str
    prenom: str
    is_active: bool = True

class UserCreate(UserBase):
    """
    Schéma pour créer un nouvel utilisateur
    """
    pass

class UserUpdate(BaseModel):
    """
    Schéma pour mettre à jour un utilisateur
    Tous les champs sont optionnels
    """
    email: Optional[str] = None
    nom: Optional[str] = None
    prenom: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    """
    Schéma pour lire un utilisateur (réponse de l'API)
    Inclut la liste de ses articles
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[Item] = []  # Liste des articles de l'utilisateur

    class Config:
        from_attributes = True
```

**Concepts de Pydantic :**
- `BaseModel` : Classe de base pour tous les schémas
- `Optional[Type]` : Champ optionnel
- `List[Type]` : Liste d'éléments d'un type donné
- `from_attributes = True` : Conversion automatique depuis SQLAlchemy

### 4. Opérations CRUD (crud.py)

Ce fichier contient toute la logique métier pour manipuler les données.

Créez le fichier `crud.py` :

```python
from sqlalchemy.orm import Session
from typing import Optional, List
import models
import schemas

# Opérations CRUD pour les utilisateurs

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """
    Récupérer un utilisateur par son ID
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """
    Récupérer un utilisateur par son email
    Utilisé pour vérifier l'unicité de l'email
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """
    Récupérer une liste d'utilisateurs avec pagination
    skip : nombre d'éléments à ignorer
    limit : nombre maximum d'éléments à retourner
    """
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Créer un nouvel utilisateur
    """
    # Créer une instance du modèle à partir du schéma
    db_user = models.User(
        email=user.email,
        nom=user.nom,
        prenom=user.prenom,
        is_active=user.is_active
    )
    
    # Ajouter à la session et sauvegarder
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Récupérer l'objet avec l'ID généré
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate) -> Optional[models.User]:
    """
    Mettre à jour un utilisateur existant
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return None
    
    # Mettre à jour uniquement les champs fournis
    update_data = user.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    """
    Supprimer un utilisateur
    La suppression CASCADE supprimera automatiquement les articles associés
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

# Opérations CRUD pour les articles

def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    """
    Récupérer un article par son ID
    """
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[models.Item]:
    """
    Récupérer une liste d'articles avec pagination
    """
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_items_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Item]:
    """
    Récupérer les articles d'un utilisateur spécifique
    """
    return db.query(models.Item).filter(models.Item.owner_id == user_id).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int) -> models.Item:
    """
    Créer un nouvel article pour un utilisateur
    """
    # Vérification de sécurité : l'utilisateur doit exister
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise ValueError(f"L'utilisateur avec l'ID {user_id} n'existe pas")
    
    # Créer l'article
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
    """
    Mettre à jour un article existant
    """
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        return None
    
    # Mettre à jour uniquement les champs fournis
    update_data = item.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int) -> bool:
    """
    Supprimer un article
    """
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        return False
    
    db.delete(db_item)
    db.commit()
    return True
```

**Concepts importants :**
- `Session` : Représente une transaction avec la base de données
- `query()` : Crée une requête SQL
- `filter()` : Ajoute une condition WHERE
- `first()` : Récupère le premier résultat
- `all()` : Récupère tous les résultats
- `commit()` : Valide les modifications en base
- `refresh()` : Recharge l'objet depuis la base

### 5. Application principale (main.py)

Ce fichier contient tous les endpoints de l'API.

Créez le fichier `main.py` :

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import crud
from database import SessionLocal, engine

# Créer toutes les tables en base de données
models.Base.metadata.create_all(bind=engine)

# Créer l'instance FastAPI
app = FastAPI(
    title="API CRUD FastAPI",
    description="Une API complète avec toutes les opérations CRUD",
    version="1.0.0"
)

# Fonction de dépendance pour obtenir une session de base de données
def get_db():
    """
    Crée une session de base de données pour chaque requête
    La session est automatiquement fermée après la requête
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint racine
@app.get("/")
def read_root():
    """
    Endpoint de bienvenue qui fournit des informations sur l'API
    """
    return {
        "message": "Bienvenue dans l'API CRUD FastAPI!",
        "documentation": "/docs",
        "version": "1.0.0"
    }

# ENDPOINTS POUR LES UTILISATEURS

@app.post("/users/", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Créer un nouvel utilisateur
    
    Vérifie que l'email n'est pas déjà utilisé avant de créer l'utilisateur
    """
    # Vérifier l'unicité de l'email
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail="L'email est déjà enregistré"
        )
    
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User], tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupérer tous les utilisateurs avec leurs articles
    
    Paramètres de pagination :
    - skip : nombre d'utilisateurs à ignorer
    - limit : nombre maximum d'utilisateurs à retourner
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Récupérer un utilisateur par son ID avec ses articles
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404, 
            detail="Utilisateur non trouvé"
        )
    return db_user

@app.get("/users/{user_id}/items/", response_model=List[schemas.Item], tags=["Users", "Items"])
def read_user_items(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupérer tous les articles d'un utilisateur spécifique
    """
    # Vérifier que l'utilisateur existe
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404, 
            detail="Utilisateur non trouvé"
        )
    
    items = crud.get_items_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return items

@app.put("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Mettre à jour un utilisateur
    """
    db_user = crud.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(
            status_code=404, 
            detail="Utilisateur non trouvé"
        )
    return db_user

@app.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Supprimer un utilisateur et tous ses articles (CASCADE)
    """
    # Vérifier que l'utilisateur existe et compter ses articles
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404, 
            detail="Utilisateur non trouvé"
        )
    
    items_count = len(db_user.items)
    
    # Supprimer l'utilisateur
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Erreur lors de la suppression"
        )
    
    # Message informatif
    message = "Utilisateur supprimé avec succès"
    if items_count > 0:
        message += f" (avec {items_count} article(s) associé(s))"
    
    return {
        "message": message, 
        "articles_supprimes": items_count
    }

# ENDPOINTS POUR LES ARTICLES

@app.post("/users/{user_id}/items/", response_model=schemas.Item, tags=["Items"])
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Créer un nouvel article pour un utilisateur
    
    IMPORTANT : L'utilisateur doit exister avant de pouvoir créer un article
    """
    # Vérification de sécurité : l'utilisateur doit exister
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404, 
            detail="Utilisateur non trouvé. Vous devez d'abord créer un utilisateur."
        )
    
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@app.get("/items/", response_model=List[schemas.Item], tags=["Items"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupérer tous les articles
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/{item_id}", response_model=schemas.Item, tags=["Items"])
def read_item(item_id: int, db: Session = Depends(get_db)):
    """
    Récupérer un article par son ID
    """
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=404, 
            detail="Article non trouvé"
        )
    return db_item

@app.put("/items/{item_id}", response_model=schemas.Item, tags=["Items"])
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    """
    Mettre à jour un article
    """
    db_item = crud.update_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(
            status_code=404, 
            detail="Article non trouvé"
        )
    return db_item

@app.delete("/items/{item_id}", tags=["Items"])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Supprimer un article
    """
    success = crud.delete_item(db, item_id=item_id)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Article non trouvé"
        )
    return {"message": "Article supprimé avec succès"}

# Point d'entrée pour le développement
if __name__ == "__main__":
    import uvicorn
    import socket
    
    def is_port_in_use(port):
        """Vérifier si un port est déjà utilisé"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    
    # Trouver un port disponible
    port = 8000
    while is_port_in_use(port) and port < 8010:
        print(f"Port {port} déjà utilisé, essai du port {port + 1}...")
        port += 1
    
    if port >= 8010:
        print("Aucun port disponible entre 8000 et 8009")
        exit(1)
    
    print(f"Démarrage de l'API sur le port {port}")
    print(f"Documentation disponible sur: http://localhost:{port}/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### 6. Fichier d'exclusion Git (.gitignore)

Créez le fichier `.gitignore` :

```
# Environnement virtuel Python
venv/
env/
ENV/

# Base de données SQLite
*.db
*.sqlite
*.sqlite3

# Fichiers Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

## Test de la structure

### Vérification des imports

Créez un fichier `test_structure.py` pour vérifier que tous les modules s'importent correctement :

```python
#!/usr/bin/env python3
"""
Test de la structure du projet
Vérifie que tous les modules s'importent correctement
"""

def test_imports():
    """Teste l'importation de tous les modules du projet"""
    
    try:
        import database
        print("✅ Module database importé")
    except ImportError as e:
        print(f"❌ Erreur import database: {e}")
        return False
    
    try:
        import models
        print("✅ Module models importé")
    except ImportError as e:
        print(f"❌ Erreur import models: {e}")
        return False
    
    try:
        import schemas
        print("✅ Module schemas importé")
    except ImportError as e:
        print(f"❌ Erreur import schemas: {e}")
        return False
    
    try:
        import crud
        print("✅ Module crud importé")
    except ImportError as e:
        print(f"❌ Erreur import crud: {e}")
        return False
    
    try:
        import main
        print("✅ Module main importé")
    except ImportError as e:
        print(f"❌ Erreur import main: {e}")
        return False
    
    print("\n🎉 Tous les modules s'importent correctement !")
    return True

def test_database_creation():
    """Teste la création des tables"""
    
    try:
        from database import engine
        import models
        
        # Créer les tables
        models.Base.metadata.create_all(bind=engine)
        print("✅ Tables créées avec succès")
        
        return True
    except Exception as e:
        print(f"❌ Erreur création tables: {e}")
        return False

if __name__ == "__main__":
    print("Test de la structure du projet")
    print("=" * 40)
    
    if test_imports() and test_database_creation():
        print("\n🎉 Structure du projet validée !")
    else:
        print("\n❌ Problèmes détectés dans la structure")
```

### Lancement du test

```bash
python test_structure.py
```

### Premier lancement de l'API

Testez votre API :

```bash
python main.py
```

Puis visitez http://localhost:8000/docs pour voir la documentation automatique.

## Bonnes pratiques de structure

### Nommage des fichiers
- Utilisez des noms descriptifs et en anglais
- Utilisez le snake_case (mots séparés par des underscores)
- Un fichier par concept principal

### Organisation du code
- Importez les modules dans l'ordre : standard, tiers, locaux
- Groupez les fonctions similaires
- Commentez le rôle de chaque fonction importante

### Gestion des dépendances
- Un seul point d'entrée pour la base de données
- Injection de dépendances avec FastAPI
- Séparation claire entre les couches

### Documentation
- Docstrings pour toutes les fonctions publiques
- Commentaires pour les parties complexes
- README à jour

## Prochaines étapes

Dans le module suivant, vous approfondirez les concepts de base de FastAPI, SQLAlchemy et Pydantic nécessaires pour bien comprendre le fonctionnement de votre API.

Assurez-vous que votre structure fonctionne avant de continuer :
- Tous les fichiers sont créés
- Le test de structure passe
- L'API démarre sans erreur
- La documentation s'affiche correctement
