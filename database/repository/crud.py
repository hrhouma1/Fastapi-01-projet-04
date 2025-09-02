from sqlalchemy.orm import Session
from typing import Optional
from database.models import models
from business.validation import schemas

# Opérations CRUD pour les utilisateurs

def get_user(db: Session, user_id: int):
    """Récupérer un utilisateur par son ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """Récupérer un utilisateur par son email"""
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Récupérer une liste d'utilisateurs avec pagination"""
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    """Créer un nouvel utilisateur"""
    db_user = models.User(
        email=user.email,
        nom=user.nom,
        prenom=user.prenom,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    """Mettre à jour un utilisateur"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return None
    
    update_data = user.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """Supprimer un utilisateur"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

# Opérations CRUD pour les articles

def get_item(db: Session, item_id: int):
    """Récupérer un article par son ID"""
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    """Récupérer une liste d'articles avec pagination"""
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_items_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Récupérer les articles d'un utilisateur spécifique"""
    return db.query(models.Item).filter(models.Item.owner_id == user_id).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    """Créer un nouvel article pour un utilisateur"""
    # Double vérification que l'utilisateur existe
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
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

def update_item(db: Session, item_id: int, item: schemas.ItemUpdate):
    """Mettre à jour un article"""
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        return None
    
    update_data = item.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    """Supprimer un article"""
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        return False
    
    db.delete(db_item)
    db.commit()
    return True

def search_items(db: Session, query: str, limit: int = 50):
    """
    Rechercher des articles par mot-clé dans le titre ou la description
    
    Args:
        db: Session de base de données
        query: Terme de recherche
        limit: Nombre maximum de résultats
    
    Returns:
        Liste des articles correspondants
    """
    # Recherche insensible à la casse dans le titre et la description
    search_pattern = f"%{query}%"
    
    return db.query(models.Item).filter(
        models.Item.title.ilike(search_pattern) |
        models.Item.description.ilike(search_pattern)
    ).limit(limit).all()
