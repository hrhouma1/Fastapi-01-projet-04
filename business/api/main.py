from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from database.models import models
from business.validation import schemas
from database.repository import crud
from database.config.database import SessionLocal, engine

# Créer les tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API CRUD FastAPI",
    description="Une API complète avec toutes les opérations CRUD",
    version="1.0.0"
)

# Dépendance pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Bienvenue dans l'API CRUD FastAPI!", "docs": "/docs"}

# Endpoints pour les utilisateurs
@app.post("/users/", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Créer un nouvel utilisateur"""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="L'email est déjà enregistré")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User], tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupérer tous les utilisateurs avec leurs articles"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Récupérer un utilisateur par son ID avec ses articles"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_user

@app.get("/users/{user_id}/items/", response_model=List[schemas.Item], tags=["Users", "Items"])
def read_user_items(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupérer tous les articles d'un utilisateur spécifique"""
    # Vérifier que l'utilisateur existe
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    items = crud.get_items_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return items

@app.put("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """Mettre à jour un utilisateur"""
    db_user = crud.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_user

@app.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Supprimer un utilisateur et tous ses articles (CASCADE)"""
    # Vérifier que l'utilisateur existe d'abord
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Compter les articles qui seront supprimés
    items_count = len(db_user.items)
    
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Erreur lors de la suppression")
    
    message = f"Utilisateur supprimé avec succès"
    if items_count > 0:
        message += f" (avec {items_count} article(s) associé(s))"
    
    return {"message": message, "articles_supprimés": items_count}

# Endpoints pour les articles
@app.post("/users/{user_id}/items/", response_model=schemas.Item, tags=["Items"])
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    """Créer un nouvel article pour un utilisateur"""
    # Vérifier que l'utilisateur existe
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé. Vous devez d'abord créer un utilisateur.")
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@app.get("/items/", response_model=List[schemas.Item], tags=["Items"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupérer tous les articles"""
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/{item_id}", response_model=schemas.Item, tags=["Items"])
def read_item(item_id: int, db: Session = Depends(get_db)):
    """Récupérer un article par son ID"""
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return db_item

@app.put("/items/{item_id}", response_model=schemas.Item, tags=["Items"])
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    """Mettre à jour un article"""
    db_item = crud.update_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return db_item

@app.delete("/items/{item_id}", tags=["Items"])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Supprimer un article"""
    success = crud.delete_item(db, item_id=item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return {"message": "Article supprimé avec succès"}

# Endpoint de recherche
@app.get("/search/items", response_model=List[schemas.Item], tags=["Search"])
def search_items(q: str, limit: int = 50, db: Session = Depends(get_db)):
    """
    Rechercher des articles par mot-clé dans le titre ou la description
    
    Args:
        q: Terme de recherche (minimum 2 caractères)
        limit: Nombre maximum de résultats (défaut: 50, max: 100)
    """
    if len(q.strip()) < 2:
        raise HTTPException(status_code=400, detail="Le terme de recherche doit contenir au moins 2 caractères")
    
    if limit > 100:
        limit = 100
    
    # Recherche dans la base de données
    items = crud.search_items(db, query=q.strip(), limit=limit)
    return items

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
        print(f"⚠️  Port {port} déjà utilisé, essai du port {port + 1}...")
        port += 1
    
    if port >= 8010:
        print("❌ Aucun port disponible entre 8000 et 8009")
        exit(1)
    
    print(f"🚀 Démarrage de l'API sur le port {port}")
    print(f"📚 Documentation disponible sur: http://localhost:{port}/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
