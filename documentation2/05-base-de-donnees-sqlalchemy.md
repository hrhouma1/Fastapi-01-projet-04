# Base de données avec SQLAlchemy

## Introduction à SQLAlchemy

SQLAlchemy est un ORM (Object-Relational Mapping) Python qui permet de :
- **Manipuler** les bases de données avec des objets Python
- **Abstraire** les différences entre moteurs de bases de données
- **Gérer** les relations complexes entre tables
- **Optimiser** les requêtes automatiquement

## Architecture SQLAlchemy

### Core vs ORM

SQLAlchemy propose deux approches :

```python
# CORE : SQL direct avec abstraction minimale
from sqlalchemy import text

result = engine.execute(text("SELECT * FROM users WHERE id = :user_id"), user_id=1)

# ORM : Manipulation d'objets Python
user = session.query(User).filter(User.id == 1).first()
```

**Dans notre projet, nous utilisons l'ORM** pour sa simplicité et sa lisibilité.

### Composants principaux

#### 1. Engine (Moteur)
```python
from sqlalchemy import create_engine

# SQLite (fichier local)
engine = create_engine("sqlite:///./database.db")

# PostgreSQL (production)
engine = create_engine("postgresql://user:password@localhost/dbname")

# MySQL
engine = create_engine("mysql+pymysql://user:password@localhost/dbname")
```

**Rôle de l'Engine :**
- Gère les connexions à la base de données
- Maintient un pool de connexions
- Traduit les requêtes SQLAlchemy en SQL natif

#### 2. Session (Session de travail)
```python
from sqlalchemy.orm import sessionmaker, Session

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Utilisation
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Rôle de la Session :**
- Unité de travail (Unit of Work pattern)
- Gestion des transactions
- Suivi des changements (change tracking)
- Cache de premier niveau

#### 3. Base declarative
```python
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    # ... définition des colonnes
```

**Rôle de Base :**
- Métaclasse pour tous les modèles
- Gestion des métadonnées
- Création automatique des tables

## Modèles SQLAlchemy approfondis

### Définition des colonnes

```python
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    
    # Types de données principaux
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nom = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)  # Texte long
    age = Column(Integer, nullable=True)
    salary = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Timestamps automatiques
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

**Options importantes :**
- `primary_key=True` : Clé primaire
- `index=True` : Création d'un index pour performances
- `unique=True` : Contrainte d'unicité
- `nullable=False` : Champ obligatoire
- `default=value` : Valeur par défaut côté Python
- `server_default=func.now()` : Valeur par défaut côté base

### Relations entre modèles

#### Relation One-to-Many

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    
    # Relation vers les articles (un utilisateur a plusieurs articles)
    items = relationship("Item", back_populates="owner", cascade="all, delete-orphan")

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    
    # Clé étrangère vers User
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relation vers l'utilisateur (plusieurs articles appartiennent à un utilisateur)
    owner = relationship("User", back_populates="items")
```

**Options de cascade :**
- `"all"` : Toutes les opérations se propagent
- `"delete-orphan"` : Supprime les enfants orphelins
- `"save-update"` : Propage les créations/modifications
- `"merge"` : Propage les fusions

#### Relation Many-to-Many

```python
# Table d'association
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    
    # Relation many-to-many
    roles = relationship("Role", secondary=user_roles, back_populates="users")

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    
    # Relation many-to-many inverse
    users = relationship("User", secondary=user_roles, back_populates="roles")
```

#### Relation One-to-One

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    
    # Relation one-to-one
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")

class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True)
    bio = Column(Text)
    avatar_url = Column(String)
    
    # Clé étrangère unique
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    # Relation inverse
    user = relationship("User", back_populates="profile")
```

## Requêtes SQLAlchemy avancées

### Requêtes de base

```python
from sqlalchemy.orm import Session

def examples_queries(db: Session):
    # Récupérer tous les utilisateurs
    users = db.query(User).all()
    
    # Récupérer le premier utilisateur
    first_user = db.query(User).first()
    
    # Récupérer par clé primaire
    user = db.query(User).get(1)
    
    # Filtrage simple
    active_users = db.query(User).filter(User.is_active == True).all()
    
    # Filtrage multiple
    users = db.query(User).filter(
        User.is_active == True,
        User.email.like('%@gmail.com')
    ).all()
    
    # Tri
    users = db.query(User).order_by(User.created_at.desc()).all()
    
    # Pagination
    users = db.query(User).offset(10).limit(5).all()
```

### Filtres avancés

```python
from sqlalchemy import and_, or_, not_

def advanced_filters(db: Session):
    # ET logique
    users = db.query(User).filter(
        and_(User.is_active == True, User.age > 18)
    ).all()
    
    # OU logique
    users = db.query(User).filter(
        or_(User.email.like('%@gmail.com'), User.email.like('%@yahoo.com'))
    ).all()
    
    # NOT logique
    users = db.query(User).filter(
        not_(User.is_active == False)
    ).all()
    
    # IN / NOT IN
    users = db.query(User).filter(User.id.in_([1, 2, 3])).all()
    users = db.query(User).filter(~User.id.in_([1, 2, 3])).all()
    
    # LIKE / ILIKE (insensible à la casse)
    users = db.query(User).filter(User.nom.ilike('%dupont%')).all()
    
    # IS NULL / IS NOT NULL
    users = db.query(User).filter(User.bio.is_(None)).all()
    users = db.query(User).filter(User.bio.isnot(None)).all()
    
    # Comparaisons numériques
    users = db.query(User).filter(User.age > 18, User.age <= 65).all()
    
    # Between
    users = db.query(User).filter(User.age.between(18, 65)).all()
```

### Jointures

```python
def join_examples(db: Session):
    # INNER JOIN implicite via relationship
    users_with_items = db.query(User).filter(User.items.any()).all()
    
    # INNER JOIN explicite
    results = db.query(User, Item).join(Item).all()
    
    # LEFT JOIN
    results = db.query(User).outerjoin(Item).all()
    
    # Join avec conditions
    results = db.query(User).join(Item).filter(
        Item.price > 100
    ).all()
    
    # Join sur plusieurs tables
    results = db.query(User).join(Item).join(Category).filter(
        Category.name == 'Electronics'
    ).all()
```

### Agrégations

```python
from sqlalchemy import func

def aggregation_examples(db: Session):
    # Compter
    user_count = db.query(func.count(User.id)).scalar()
    
    # Compter avec filtre
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
    
    # Min, Max, Average
    stats = db.query(
        func.min(Item.price).label('min_price'),
        func.max(Item.price).label('max_price'),
        func.avg(Item.price).label('avg_price')
    ).first()
    
    # Group by
    user_item_counts = db.query(
        User.id,
        User.email,
        func.count(Item.id).label('item_count')
    ).outerjoin(Item).group_by(User.id).all()
    
    # Having
    prolific_users = db.query(
        User.id,
        func.count(Item.id).label('item_count')
    ).join(Item).group_by(User.id).having(
        func.count(Item.id) > 5
    ).all()
```

### Sous-requêtes

```python
def subquery_examples(db: Session):
    # Sous-requête simple
    subquery = db.query(Item.owner_id).filter(Item.price > 1000).subquery()
    wealthy_users = db.query(User).filter(User.id.in_(subquery)).all()
    
    # Existe
    users_with_expensive_items = db.query(User).filter(
        db.query(Item).filter(
            Item.owner_id == User.id,
            Item.price > 1000
        ).exists()
    ).all()
    
    # Sous-requête corrélée
    users_with_item_count = db.query(
        User,
        db.query(func.count(Item.id)).filter(
            Item.owner_id == User.id
        ).scalar_subquery().label('item_count')
    ).all()
```

## Gestion des transactions

### Transactions explicites

```python
def transaction_example(db: Session):
    try:
        # Début de transaction (implicite)
        user = User(email="test@exemple.com", nom="Test")
        db.add(user)
        
        # Flush pour obtenir l'ID sans committer
        db.flush()
        
        item = Item(title="Article test", price=99.99, owner_id=user.id)
        db.add(item)
        
        # Commit pour finaliser la transaction
        db.commit()
        
    except Exception as e:
        # Rollback en cas d'erreur
        db.rollback()
        raise e
```

### Transactions avec context manager

```python
from contextlib import contextmanager

@contextmanager
def db_transaction(db: Session):
    """Context manager pour les transactions"""
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# Utilisation
def create_user_with_item(user_data: dict, item_data: dict):
    with db_transaction(SessionLocal()) as db:
        user = User(**user_data)
        db.add(user)
        db.flush()  # Pour obtenir l'ID
        
        item = Item(**item_data, owner_id=user.id)
        db.add(item)
        # Commit automatique si pas d'exception
```

## Optimisation des performances

### Chargement des relations

#### Lazy Loading (par défaut)
```python
# La relation est chargée à la demande
user = db.query(User).first()
items = user.items  # Requête SQL supplémentaire ici
```

#### Eager Loading
```python
from sqlalchemy.orm import joinedload, selectinload, subqueryload

# Join Load : une seule requête avec JOIN
users = db.query(User).options(joinedload(User.items)).all()

# Select In Load : deux requêtes optimisées
users = db.query(User).options(selectinload(User.items)).all()

# Subquery Load : sous-requête
users = db.query(User).options(subqueryload(User.items)).all()
```

### Requêtes optimisées

```python
def optimized_queries(db: Session):
    # Sélection de colonnes spécifiques
    emails = db.query(User.email).filter(User.is_active == True).all()
    
    # Utilisation d'index
    user = db.query(User).filter(User.email == "test@exemple.com").first()
    
    # Batch operations
    db.query(User).filter(User.is_active == False).update({
        User.is_active: True
    })
    
    # Bulk insert
    users_data = [
        {"email": f"user{i}@exemple.com", "nom": f"User{i}"}
        for i in range(100)
    ]
    db.bulk_insert_mappings(User, users_data)
```

### Index et contraintes

```python
from sqlalchemy import Index, UniqueConstraint, CheckConstraint

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    age = Column(Integer)
    
    # Index composé
    __table_args__ = (
        Index('idx_user_name', 'nom', 'prenom'),
        UniqueConstraint('email', name='uq_user_email'),
        CheckConstraint('age >= 0', name='ck_user_age_positive'),
    )
```

## Migration et versioning

### Avec Alembic (outil officiel SQLAlchemy)

```bash
# Installation
pip install alembic

# Initialisation
alembic init alembic

# Génération d'une migration
alembic revision --autogenerate -m "Ajout table users"

# Application des migrations
alembic upgrade head

# Historique
alembic history

# Retour en arrière
alembic downgrade -1
```

### Configuration Alembic

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from models import Base  # Import de nos modèles

# Configuration de la target metadata
target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
```

## Bonnes pratiques

### 1. Structure des modèles
```python
class BaseModel(Base):
    """Modèle de base avec timestamps"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    # ... autres champs
```

### 2. Gestion des erreurs
```python
from sqlalchemy.exc import IntegrityError

def create_user_safe(db: Session, user_data: dict):
    try:
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()
        if "UNIQUE constraint failed" in str(e):
            raise ValueError("Un utilisateur avec cet email existe déjà")
        raise
```

### 3. Sessions et connexions
```python
# Toujours fermer les sessions
def good_practice():
    db = SessionLocal()
    try:
        # Opérations sur db
        pass
    finally:
        db.close()

# Ou avec context manager
@contextmanager
def get_db_context():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Cette approche méthodique de SQLAlchemy garantit une base de données robuste et performante pour votre application FastAPI.

Passez au module suivant : **06-interface-graphique-pyside6.md**
