from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Schémas pour les articles
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: int  # Prix en centimes
    is_available: bool = True

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    is_available: Optional[bool] = None

class Item(ItemBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schémas pour les utilisateurs
class UserBase(BaseModel):
    email: str
    nom: str
    prenom: str
    is_active: bool = True

class UserCreate(UserBase):
    pass

class UserWithItemsCount(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    items_count: int

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[str] = None
    nom: Optional[str] = None
    prenom: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[Item] = []

    class Config:
        from_attributes = True
