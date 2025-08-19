# Module 5 : Création de l'API CRUD étape par étape

## Objectifs pédagogiques

À la fin de ce module, vous serez capable de :
- Créer une API CRUD complète en suivant les bonnes pratiques
- Implémenter la validation des données et la gestion d'erreurs
- Comprendre l'ordre logique des opérations
- Tester chaque fonctionnalité au fur et à mesure

## Étape 1 : Configuration de la base de données

### Création du fichier database.py

Commencez par configurer la connexion à la base de données. Ce fichier sera utilisé par tous les autres modules.

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

# Configuration de la base de données SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Création du moteur de base de données
# check_same_thread=False est nécessaire pour SQLite avec FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Configuration de la session
# autocommit=False : les transactions doivent être validées manuellement
# autoflush=False : les objets ne sont pas synchronisés automatiquement
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour tous les modèles
Base = declarative_base()
```

**Points importants :**
- SQLite stocke la base dans un fichier local (test.db)
- `check_same_thread=False` permet l'utilisation multi-thread
- `SessionLocal` est une factory qui crée des sessions de base de données

### Test de la configuration

Créez un fichier temporaire pour tester la connexion :

```python
# test_database.py
from database import engine, Base
print("Connexion à la base de données réussie")

# Test de création/suppression d'une table vide
Base.metadata.create_all(bind=engine)
print("Création des tables réussie")
```

Exécutez le test :
```bash
python test_database.py
```

## Étape 2 : Définition des modèles de données

### Analyse des besoins

Avant de créer les modèles, analysons nos entités :

**Utilisateur (User) :**
- Identifiant unique automatique
- Email unique et obligatoire  
- Nom et prénom obligatoires
- Statut actif/inactif
- Dates de création et modification automatiques
- Peut avoir plusieurs articles

**Article (Item) :**
- Identifiant unique automatique
- Titre obligatoire
- Description optionnelle
- Prix en centimes (évite les erreurs d'arrondi)
- Statut disponible/non disponible
- Dates de création et modification automatiques
- Appartient obligatoirement à un utilisateur

### Création du fichier models.py

```python
# models.py
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    """
    Modèle représentant un utilisateur
    """
    __tablename__ = "users"

    # Clé primaire auto-incrémentée
    id = Column(Integer, primary_key=True, index=True)
    
    # Informations utilisateur
    email = Column(String, unique=True, index=True, nullable=False)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Horodatage automatique
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relation avec les articles
    # cascade="all, delete-orphan" : supprimer les articles si l'utilisateur est supprimé
    items = relationship("Item", back_populates="owner", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', nom='{self.nom}')>"

class Item(Base):
    """
    Modèle représentant un article
    """
    __tablename__ = "items"

    # Clé primaire auto-incrémentée
    id = Column(Integer, primary_key=True, index=True)
    
    # Informations article
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)  # Prix en centimes
    is_available = Column(Boolean, default=True)
    
    # Horodatage automatique
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Clé étrangère vers l'utilisateur
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relation avec l'utilisateur propriétaire
    owner = relationship("User", back_populates="items")
    
    def __repr__(self):
        return f"<Item(id={self.id}, title='{self.title}', owner_id={self.owner_id})>"
```

**Explications détaillées :**

1. **Colonnes de base :**
   - `primary_key=True` : Clé primaire unique
   - `index=True` : Index pour améliorer les performances de recherche
   - `unique=True` : Valeur unique dans toute la table
   - `nullable=False` : Champ obligatoire

2. **Types de données :**
   - `Integer` : Nombres entiers
   - `String` : Texte (longueur variable)
   - `Boolean` : Vrai/Faux
   - `DateTime` : Date et heure

3. **Fonctions automatiques :**
   - `server_default=func.now()` : Date de création automatique
   - `onupdate=func.now()` : Date de modification automatique

4. **Relations :**
   - `ForeignKey` : Référence vers une autre table
   - `relationship` : Relation objet entre modèles
   - `back_populates` : Relation bidirectionnelle
   - `cascade` : Action à effectuer sur les objets liés

### Test des modèles

```python
# test_models.py
from database import engine
import models

# Créer toutes les tables
models.Base.metadata.create_all(bind=engine)
print("Tables créées avec succès")

# Vérifier les colonnes créées
inspector = engine.inspect(engine)
print("Tables dans la base :", inspector.get_table_names())

for table_name in inspector.get_table_names():
    columns = inspector.get_columns(table_name)
    print(f"\nColonnes de la table {table_name}:")
    for column in columns:
        print(f"  - {column['name']}: {column['type']}")
```

## Étape 3 : Schémas de validation avec Pydantic

### Principe des schémas

Les schémas Pydantic définissent :
- **Format d'entrée** : Ce que l'API accepte (UserCreate, ItemCreate)
- **Format de sortie** : Ce que l'API retourne (User, Item)
- **Format de mise à jour** : Ce que l'API accepte pour les modifications (UserUpdate, ItemUpdate)

### Création du fichier schemas.py

```python
# schemas.py
from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from datetime import datetime

# === SCHÉMAS POUR LES ARTICLES ===

class ItemBase(BaseModel):
    """
    Schéma de base contenant les champs communs pour les articles
    """
    title: str
    description: Optional[str] = None
    price: int  # Prix en centimes (ex: 2500 = 25.00€)
    is_available: bool = True
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Le titre ne peut pas être vide')
        return v.strip()
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Le prix doit être supérieur à 0')
        return v

class ItemCreate(ItemBase):
    """
    Schéma pour créer un nouvel article
    Hérite de ItemBase sans modifications
    """
    pass

class ItemUpdate(BaseModel):
    """
    Schéma pour mettre à jour un article
    Tous les champs sont optionnels pour permettre les mises à jour partielles
    """
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    is_available: Optional[bool] = None
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Le titre ne peut pas être vide')
        return v.strip() if v else v
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Le prix doit être supérieur à 0')
        return v

class Item(ItemBase):
    """
    Schéma pour lire un article (réponse de l'API)
    Inclut tous les champs générés automatiquement
    """
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Permet la conversion depuis SQLAlchemy

# === SCHÉMAS POUR LES UTILISATEURS ===

class UserBase(BaseModel):
    """
    Schéma de base contenant les champs communs pour les utilisateurs
    """
    email: str
    nom: str
    prenom: str
    is_active: bool = True
    
    @validator('email')
    def email_must_be_valid(cls, v):
        # Validation basique d'email (Pydantic fait déjà une validation)
        if not v or '@' not in v:
            raise ValueError('Email invalide')
        return v.lower().strip()
    
    @validator('nom', 'prenom')
    def names_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Le nom et le prénom ne peuvent pas être vides')
        return v.strip().title()  # Première lettre en majuscule

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
    
    @validator('email')
    def email_must_be_valid(cls, v):
        if v is not None and (not v or '@' not in v):
            raise ValueError('Email invalide')
        return v.lower().strip() if v else v
    
    @validator('nom', 'prenom')
    def names_must_not_be_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Le nom et le prénom ne peuvent pas être vides')
        return v.strip().title() if v else v

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

**Points importants :**

1. **Validation personnalisée :**
   - `@validator` permet de valider les données
   - Lever `ValueError` pour signaler une erreur
   - Transformation des données (strip, title, lower)

2. **Types optionnels :**
   - `Optional[Type]` pour les champs facultatifs
   - `List[Type]` pour les listes
   - Valeurs par défaut avec `= None` ou `= valeur`

3. **Configuration :**
   - `from_attributes = True` permet la conversion depuis SQLAlchemy

### Test des schémas

```python
# test_schemas.py
import schemas

# Test de validation réussie
try:
    user_data = {
        "email": "john.doe@example.com",
        "nom": "doe",
        "prenom": "john",
        "is_active": True
    }
    user = schemas.UserCreate(**user_data)
    print(f"Utilisateur valide: {user}")
    print(f"Nom formaté: {user.nom}")  # Doit être "Doe"
    print(f"Email formaté: {user.email}")  # Doit être en minuscules
except ValueError as e:
    print(f"Erreur de validation: {e}")

# Test de validation échoue
try:
    invalid_user = schemas.UserCreate(
        email="invalid-email",  # Email invalide
        nom="",  # Nom vide
        prenom="John",
        is_active=True
    )
except ValueError as e:
    print(f"Validation échouée (normal): {e}")

# Test article
try:
    item = schemas.ItemCreate(
        title="MacBook Pro",
        description="Ordinateur portable",
        price=250000,  # 2500.00€
        is_available=True
    )
    print(f"Article valide: {item}")
except ValueError as e:
    print(f"Erreur: {e}")
```

## Étape 4 : Implémentation des opérations CRUD

### Principe CRUD

Chaque entité a besoin de 5 opérations de base :
- **Create** : Créer une nouvelle ressource
- **Read** : Lire une ou plusieurs ressources
- **Update** : Modifier une ressource existante
- **Delete** : Supprimer une ressource

### Création du fichier crud.py

```python
# crud.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
import models
import schemas

# === OPÉRATIONS CRUD POUR LES UTILISATEURS ===

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """
    Récupérer un utilisateur par son ID
    
    Args:
        db: Session de base de données
        user_id: ID de l'utilisateur à récupérer
        
    Returns:
        L'utilisateur trouvé ou None si inexistant
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
    
    Args:
        db: Session de base de données
        skip: Nombre d'éléments à ignorer (pour la pagination)
        limit: Nombre maximum d'éléments à retourner
        
    Returns:
        Liste des utilisateurs
    """
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Créer un nouvel utilisateur
    
    Args:
        db: Session de base de données
        user: Données de l'utilisateur à créer
        
    Returns:
        L'utilisateur créé avec son ID généré
        
    Raises:
        IntegrityError: Si l'email existe déjà
    """
    # Créer une instance du modèle SQLAlchemy
    db_user = models.User(
        email=user.email,
        nom=user.nom,
        prenom=user.prenom,
        is_active=user.is_active
    )
    
    # Ajouter à la session et sauvegarder
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)  # Récupérer l'objet avec l'ID et les dates générées
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError("Email déjà utilisé")

def update_user(db: Session, user_id: int, user: schemas.UserUpdate) -> Optional[models.User]:
    """
    Mettre à jour un utilisateur existant
    
    Args:
        db: Session de base de données
        user_id: ID de l'utilisateur à modifier
        user: Nouvelles données (seuls les champs fournis seront modifiés)
        
    Returns:
        L'utilisateur modifié ou None si inexistant
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return None
    
    # Mettre à jour uniquement les champs fournis (exclude_unset=True)
    update_data = user.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError("Email déjà utilisé par un autre utilisateur")

def delete_user(db: Session, user_id: int) -> bool:
    """
    Supprimer un utilisateur
    
    Args:
        db: Session de base de données
        user_id: ID de l'utilisateur à supprimer
        
    Returns:
        True si supprimé, False si inexistant
        
    Note:
        La suppression CASCADE supprime automatiquement tous les articles associés
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

# === OPÉRATIONS CRUD POUR LES ARTICLES ===

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
    return (
        db.query(models.Item)
        .filter(models.Item.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int) -> models.Item:
    """
    Créer un nouvel article pour un utilisateur
    
    Args:
        db: Session de base de données
        item: Données de l'article à créer
        user_id: ID de l'utilisateur propriétaire
        
    Returns:
        L'article créé
        
    Raises:
        ValueError: Si l'utilisateur n'existe pas
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

# === FONCTIONS UTILITAIRES ===

def get_user_with_items_count(db: Session, user_id: int) -> Optional[dict]:
    """
    Récupérer un utilisateur avec le nombre de ses articles
    """
    user = get_user(db, user_id)
    if user is None:
        return None
    
    items_count = db.query(models.Item).filter(models.Item.owner_id == user_id).count()
    
    return {
        "user": user,
        "items_count": items_count
    }

def search_items_by_title(db: Session, title: str, skip: int = 0, limit: int = 100) -> List[models.Item]:
    """
    Rechercher des articles par titre (recherche partielle)
    """
    return (
        db.query(models.Item)
        .filter(models.Item.title.contains(title))
        .offset(skip)
        .limit(limit)
        .all()
    )
```

### Test des opérations CRUD

```python
# test_crud.py
from database import SessionLocal
import models
import schemas
import crud
from database import engine

# Créer les tables
models.Base.metadata.create_all(bind=engine)

# Créer une session de test
db = SessionLocal()

try:
    print("=== Test des opérations CRUD ===")
    
    # 1. Créer un utilisateur
    print("\n1. Création d'un utilisateur")
    user_data = schemas.UserCreate(
        email="test@example.com",
        nom="Test",
        prenom="User",
        is_active=True
    )
    
    user = crud.create_user(db, user_data)
    print(f"Utilisateur créé: {user}")
    user_id = user.id
    
    # 2. Lire l'utilisateur
    print("\n2. Lecture de l'utilisateur")
    read_user = crud.get_user(db, user_id)
    print(f"Utilisateur lu: {read_user}")
    
    # 3. Créer un article
    print("\n3. Création d'un article")
    item_data = schemas.ItemCreate(
        title="Test Item",
        description="Un article de test",
        price=1000,
        is_available=True
    )
    
    item = crud.create_user_item(db, item_data, user_id)
    print(f"Article créé: {item}")
    item_id = item.id
    
    # 4. Lire tous les articles
    print("\n4. Lecture de tous les articles")
    items = crud.get_items(db)
    print(f"Articles trouvés: {len(items)}")
    for item in items:
        print(f"  - {item.title} ({item.price} centimes)")
    
    # 5. Mettre à jour l'article
    print("\n5. Mise à jour de l'article")
    item_update = schemas.ItemUpdate(price=1500, description="Article mis à jour")
    updated_item = crud.update_item(db, item_id, item_update)
    print(f"Article mis à jour: {updated_item.price} centimes")
    
    # 6. Supprimer l'article
    print("\n6. Suppression de l'article")
    success = crud.delete_item(db, item_id)
    print(f"Article supprimé: {success}")
    
    # 7. Supprimer l'utilisateur
    print("\n7. Suppression de l'utilisateur")
    success = crud.delete_user(db, user_id)
    print(f"Utilisateur supprimé: {success}")
    
    print("\n✅ Tous les tests CRUD ont réussi!")
    
except Exception as e:
    print(f"❌ Erreur lors des tests: {e}")
    db.rollback()

finally:
    db.close()
```

## Prochaines étapes

Dans la prochaine section, nous créerons l'application FastAPI principale qui expose tous ces endpoints via HTTP, puis nous implémenterons les tests complets.

Vérifiez que cette étape fonctionne avant de continuer :
- Le test de CRUD doit passer sans erreur
- Les modèles doivent se créer correctement
- Les validations Pydantic doivent fonctionner
