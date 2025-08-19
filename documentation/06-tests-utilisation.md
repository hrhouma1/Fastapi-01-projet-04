# Module 6 : Tests et utilisation de l'API

## Objectifs pédagogiques

À la fin de ce module, vous serez capable de :
- Tester votre API avec différents outils et méthodes
- Comprendre l'ordre logique des opérations
- Utiliser la documentation interactive FastAPI
- Créer vos propres scripts de test
- Diagnostiquer et résoudre les problèmes courants

## Finalisation de l'application principale

### Création du point d'entrée (main.py)

Avant de tester, finalisez votre fichier main.py avec tous les endpoints :

```python
# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import models
import schemas  
import crud
from database import SessionLocal, engine

# Créer toutes les tables en base de données
models.Base.metadata.create_all(bind=engine)

# Configuration de l'application FastAPI
app = FastAPI(
    title="API CRUD FastAPI - Formation",
    description="API complète pour la gestion d'utilisateurs et d'articles",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Fonction de dépendance pour la base de données
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

# === ENDPOINTS RACINE ===

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint de bienvenue avec informations sur l'API
    """
    return {
        "message": "Bienvenue dans l'API CRUD FastAPI",
        "version": "1.0.0",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "users": "/users/",
            "items": "/items/"
        }
    }

@app.get("/health", tags=["Root"])
def health_check():
    """
    Vérification de l'état de l'API
    """
    return {
        "status": "healthy",
        "database": "connected"
    }

# === ENDPOINTS UTILISATEURS ===

@app.post("/users/", response_model=schemas.User, status_code=201, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Créer un nouvel utilisateur
    
    **ÉTAPE 1 OBLIGATOIRE** : Vous devez créer des utilisateurs avant de créer des articles
    
    - **email** : Adresse email unique (sera convertie en minuscules)
    - **nom** : Nom de famille (première lettre en majuscule automatiquement)  
    - **prenom** : Prénom (première lettre en majuscule automatiquement)
    - **is_active** : Statut actif (true par défaut)
    """
    # Vérifier l'unicité de l'email
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="L'email est déjà enregistré. Choisissez un autre email."
        )
    
    try:
        return crud.create_user(db=db, user=user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/", response_model=List[schemas.User], tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupérer tous les utilisateurs avec leurs articles
    
    Paramètres de pagination :
    - **skip** : Nombre d'utilisateurs à ignorer (défaut: 0)
    - **limit** : Nombre maximum d'utilisateurs à retourner (défaut: 100, max: 1000)
    """
    if limit > 1000:
        raise HTTPException(
            status_code=400, 
            detail="La limite ne peut pas dépasser 1000"
        )
    
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Récupérer un utilisateur spécifique par son ID avec tous ses articles
    """
    if user_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="L'ID utilisateur doit être un nombre positif"
        )
    
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail=f"Aucun utilisateur trouvé avec l'ID {user_id}"
        )
    return db_user

@app.get("/users/{user_id}/items/", response_model=List[schemas.Item], tags=["Users"])
def read_user_items(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupérer tous les articles d'un utilisateur spécifique
    """
    # Vérifier que l'utilisateur existe
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail=f"Aucun utilisateur trouvé avec l'ID {user_id}"
        )
    
    items = crud.get_items_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return items

@app.put("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Mettre à jour un utilisateur existant
    
    Seuls les champs fournis seront modifiés (mise à jour partielle)
    """
    try:
        db_user = crud.update_user(db, user_id=user_id, user=user)
        if db_user is None:
            raise HTTPException(
                status_code=404,
                detail=f"Aucun utilisateur trouvé avec l'ID {user_id}"
            )
        return db_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Supprimer un utilisateur et tous ses articles (CASCADE)
    
    **ATTENTION** : Cette opération supprime définitivement l'utilisateur
    et tous ses articles associés.
    """
    # Récupérer l'utilisateur pour compter ses articles
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail=f"Aucun utilisateur trouvé avec l'ID {user_id}"
        )
    
    items_count = len(db_user.items)
    
    # Supprimer l'utilisateur
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la suppression"
        )
    
    # Message informatif
    message = f"Utilisateur {user_id} supprimé avec succès"
    if items_count > 0:
        message += f" (avec {items_count} article(s) associé(s))"
    
    return {
        "message": message,
        "user_id": user_id,
        "articles_supprimes": items_count
    }

# === ENDPOINTS ARTICLES ===

@app.post("/users/{user_id}/items/", response_model=schemas.Item, status_code=201, tags=["Items"])
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Créer un nouvel article pour un utilisateur
    
    **ÉTAPE 2** : Vous devez d'abord créer un utilisateur (étape 1) avant de créer des articles
    
    - **title** : Titre de l'article (obligatoire, sera nettoyé automatiquement)
    - **description** : Description détaillée (optionnel)
    - **price** : Prix en centimes (ex: 2500 = 25,00€)
    - **is_available** : Disponibilité (true par défaut)
    """
    # Vérification obligatoire : l'utilisateur doit exister
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail=f"Utilisateur {user_id} non trouvé. Créez d'abord un utilisateur avec POST /users/"
        )
    
    try:
        return crud.create_user_item(db=db, item=item, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/items/", response_model=List[schemas.Item], tags=["Items"])
def read_items(skip: int = 0, limit: int = 100, available_only: bool = False, db: Session = Depends(get_db)):
    """
    Récupérer tous les articles
    
    Paramètres :
    - **skip** : Nombre d'articles à ignorer
    - **limit** : Nombre maximum d'articles à retourner
    - **available_only** : Si true, ne retourne que les articles disponibles
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    
    if available_only:
        items = [item for item in items if item.is_available]
    
    return items

@app.get("/items/{item_id}", response_model=schemas.Item, tags=["Items"])
def read_item(item_id: int, db: Session = Depends(get_db)):
    """
    Récupérer un article spécifique par son ID
    """
    if item_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="L'ID article doit être un nombre positif"
        )
    
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=404,
            detail=f"Aucun article trouvé avec l'ID {item_id}"
        )
    return db_item

@app.put("/items/{item_id}", response_model=schemas.Item, tags=["Items"])
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    """
    Mettre à jour un article existant
    
    Seuls les champs fournis seront modifiés
    """
    try:
        db_item = crud.update_item(db, item_id=item_id, item=item)
        if db_item is None:
            raise HTTPException(
                status_code=404,
                detail=f"Aucun article trouvé avec l'ID {item_id}"
            )
        return db_item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/items/{item_id}", tags=["Items"])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Supprimer un article
    """
    success = crud.delete_item(db, item_id=item_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Aucun article trouvé avec l'ID {item_id}"
        )
    
    return {
        "message": f"Article {item_id} supprimé avec succès",
        "item_id": item_id
    }

# === ENDPOINTS DE RECHERCHE ===

@app.get("/search/items", response_model=List[schemas.Item], tags=["Search"])
def search_items(q: str, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    Rechercher des articles par titre
    
    - **q** : Terme de recherche (dans le titre)
    """
    if len(q.strip()) < 2:
        raise HTTPException(
            status_code=400,
            detail="Le terme de recherche doit contenir au moins 2 caractères"
        )
    
    items = crud.search_items_by_title(db, q.strip(), skip=skip, limit=limit)
    return items

# Point d'entrée pour le développement
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

## Méthodes de test

### 1. Documentation interactive FastAPI

FastAPI génère automatiquement une documentation interactive.

**Lancement de l'API :**
```bash
python main.py
```

**Accès à la documentation :**
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

**Utilisation de Swagger UI :**

1. Ouvrez http://localhost:8000/docs dans votre navigateur
2. Vous voyez tous les endpoints organisés par tags (Users, Items, etc.)
3. Cliquez sur un endpoint pour voir ses détails
4. Cliquez sur "Try it out" pour tester
5. Remplissez les paramètres et cliquez "Execute"
6. Voir la réponse avec le code de statut

**Exemple de test avec Swagger :**

1. **Créer un utilisateur :**
   - Endpoint : `POST /users/`
   - Body :
   ```json
   {
     "email": "marie.dupont@example.com",
     "nom": "Dupont",
     "prenom": "Marie",
     "is_active": true
   }
   ```

2. **Créer un article pour cet utilisateur :**
   - Endpoint : `POST /users/1/items/`
   - Body :
   ```json
   {
     "title": "MacBook Pro",
     "description": "Ordinateur portable excellent état",
     "price": 250000,
     "is_available": true
   }
   ```

### 2. Tests avec des fichiers .http

Créez un fichier `tests_manuels.http` pour tester avec VS Code :

```http
### Variables
@baseUrl = http://localhost:8000

### Test 1 - Vérification de l'API
GET {{baseUrl}}/
Content-Type: application/json

### Test 2 - Vérification de santé
GET {{baseUrl}}/health

### Test 3 - Lister utilisateurs (vide au début)
GET {{baseUrl}}/users/

### Test 4 - Créer premier utilisateur
POST {{baseUrl}}/users/
Content-Type: application/json

{
  "email": "alice.martin@example.com",
  "nom": "Martin",
  "prenom": "Alice",
  "is_active": true
}

### Test 5 - Créer deuxième utilisateur  
POST {{baseUrl}}/users/
Content-Type: application/json

{
  "email": "bob.wilson@example.com",
  "nom": "Wilson",
  "prenom": "Bob",
  "is_active": true
}

### Test 6 - Lister les utilisateurs
GET {{baseUrl}}/users/

### Test 7 - Récupérer utilisateur spécifique
GET {{baseUrl}}/users/1

### Test 8 - Créer article pour utilisateur 1
POST {{baseUrl}}/users/1/items/
Content-Type: application/json

{
  "title": "iPhone 15 Pro",
  "description": "Smartphone neuf, toujours sous garantie",
  "price": 120000,
  "is_available": true
}

### Test 9 - Créer article pour utilisateur 2
POST {{baseUrl}}/users/2/items/
Content-Type: application/json

{
  "title": "Vélo électrique",
  "description": "VTT électrique, très bon état",
  "price": 80000,
  "is_available": true
}

### Test 10 - Lister tous les articles
GET {{baseUrl}}/items/

### Test 11 - Récupérer article spécifique
GET {{baseUrl}}/items/1

### Test 12 - Récupérer articles d'un utilisateur
GET {{baseUrl}}/users/1/items/

### Test 13 - Mettre à jour un article
PUT {{baseUrl}}/items/1
Content-Type: application/json

{
  "price": 110000,
  "description": "iPhone 15 Pro - PRIX RÉDUIT ! Smartphone neuf sous garantie"
}

### Test 14 - Mettre à jour un utilisateur
PUT {{baseUrl}}/users/1
Content-Type: application/json

{
  "nom": "Martin-Dubois"
}

### Test 15 - Rechercher articles
GET {{baseUrl}}/search/items?q=iPhone

### Test 16 - Test d'erreur - Créer article sans utilisateur
POST {{baseUrl}}/users/999/items/
Content-Type: application/json

{
  "title": "Article impossible",
  "price": 1000
}

### Test 17 - Test d'erreur - Email en double
POST {{baseUrl}}/users/
Content-Type: application/json

{
  "email": "alice.martin@example.com",
  "nom": "Dupont",
  "prenom": "Marie"
}

### Test 18 - Supprimer un article
DELETE {{baseUrl}}/items/1

### Test 19 - Supprimer un utilisateur (CASCADE)
DELETE {{baseUrl}}/users/2

### Test 20 - Vérification finale
GET {{baseUrl}}/users/
```

### 3. Script de test automatique

Créez un fichier `test_complet.py` :

```python
#!/usr/bin/env python3
"""
Test complet de l'API avec vérifications automatiques
"""

import requests
import json
import time
from typing import Optional

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 10  # Timeout en secondes

class APITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def test_endpoint(self, name: str, method: str, endpoint: str, 
                     data: Optional[dict] = None, expected_status: int = 200) -> dict:
        """
        Teste un endpoint et enregistre le résultat
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, timeout=TIMEOUT)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, timeout=TIMEOUT)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, timeout=TIMEOUT)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, timeout=TIMEOUT)
            
            success = response.status_code == expected_status
            result = {
                "name": name,
                "method": method,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "success": success,
                "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            }
            
            self.test_results.append(result)
            
            status_icon = "✅" if success else "❌"
            print(f"{status_icon} {name}: {method} {endpoint} -> {response.status_code}")
            
            return result
            
        except Exception as e:
            result = {
                "name": name,
                "method": method,
                "endpoint": endpoint,
                "success": False,
                "error": str(e)
            }
            self.test_results.append(result)
            print(f"❌ {name}: Erreur - {e}")
            return result
    
    def run_complete_test(self):
        """
        Exécute une série complète de tests
        """
        print("🚀 Début des tests automatiques de l'API")
        print("=" * 60)
        
        # Test 1 : Vérification de l'API
        self.test_endpoint("API Root", "GET", "/")
        
        # Test 2 : Health check
        self.test_endpoint("Health Check", "GET", "/health")
        
        # Test 3 : Lister utilisateurs (vide)
        self.test_endpoint("Liste utilisateurs vide", "GET", "/users/")
        
        # Test 4 : Créer utilisateur 1
        user1_data = {
            "email": "test1@example.com",
            "nom": "Test",
            "prenom": "User1",
            "is_active": True
        }
        result = self.test_endpoint("Créer utilisateur 1", "POST", "/users/", user1_data, 201)
        user1_id = result.get("response", {}).get("id") if result["success"] else None
        
        # Test 5 : Créer utilisateur 2
        user2_data = {
            "email": "test2@example.com",
            "nom": "Test",
            "prenom": "User2",
            "is_active": True
        }
        result = self.test_endpoint("Créer utilisateur 2", "POST", "/users/", user2_data, 201)
        user2_id = result.get("response", {}).get("id") if result["success"] else None
        
        # Test 6 : Lister utilisateurs (2 utilisateurs)
        self.test_endpoint("Liste utilisateurs", "GET", "/users/")
        
        # Test 7 : Récupérer utilisateur spécifique
        if user1_id:
            self.test_endpoint("Récupérer utilisateur 1", "GET", f"/users/{user1_id}")
        
        # Test 8 : Créer article pour utilisateur 1
        if user1_id:
            item1_data = {
                "title": "Article Test 1",
                "description": "Description du premier article",
                "price": 5000,
                "is_available": True
            }
            result = self.test_endpoint("Créer article 1", "POST", f"/users/{user1_id}/items/", item1_data, 201)
            item1_id = result.get("response", {}).get("id") if result["success"] else None
        
        # Test 9 : Créer article pour utilisateur 2
        if user2_id:
            item2_data = {
                "title": "Article Test 2",
                "description": "Description du second article",
                "price": 7500,
                "is_available": True
            }
            self.test_endpoint("Créer article 2", "POST", f"/users/{user2_id}/items/", item2_data, 201)
        
        # Test 10 : Lister tous les articles
        self.test_endpoint("Liste articles", "GET", "/items/")
        
        # Test 11 : Articles d'un utilisateur
        if user1_id:
            self.test_endpoint("Articles utilisateur 1", "GET", f"/users/{user1_id}/items/")
        
        # Test 12 : Mise à jour article
        if 'item1_id' in locals() and item1_id:
            update_data = {
                "price": 4500,
                "description": "Article mis à jour"
            }
            self.test_endpoint("Mise à jour article", "PUT", f"/items/{item1_id}", update_data)
        
        # Test 13 : Recherche
        self.test_endpoint("Recherche articles", "GET", "/search/items?q=Test")
        
        # Test 14 : Test d'erreur - Créer article sans utilisateur
        error_item = {
            "title": "Article impossible",
            "price": 1000
        }
        self.test_endpoint("Erreur article sans user", "POST", "/users/999/items/", error_item, 404)
        
        # Test 15 : Test d'erreur - Email en double
        duplicate_user = {
            "email": "test1@example.com",
            "nom": "Duplicate",
            "prenom": "User"
        }
        self.test_endpoint("Erreur email dupliqué", "POST", "/users/", duplicate_user, 400)
        
        # Nettoyage : Supprimer les données de test
        if user1_id:
            self.test_endpoint("Supprimer utilisateur 1", "DELETE", f"/users/{user1_id}")
        if user2_id:
            self.test_endpoint("Supprimer utilisateur 2", "DELETE", f"/users/{user2_id}")
        
        # Vérification finale
        self.test_endpoint("Vérification finale", "GET", "/users/")
        
        self.print_summary()
    
    def print_summary(self):
        """
        Affiche un résumé des tests
        """
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        successful_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - successful_tests
        
        print(f"Total de tests : {total_tests}")
        print(f"Réussis : {successful_tests} ✅")
        print(f"Échoués : {failed_tests} ❌")
        print(f"Taux de réussite : {(successful_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ TESTS ÉCHOUÉS :")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['name']}")
                    if "error" in result:
                        print(f"    Erreur: {result['error']}")
                    elif "status_code" in result:
                        print(f"    Code reçu: {result['status_code']}, attendu: {result['expected_status']}")

def main():
    """
    Point d'entrée principal
    """
    print("Vérification de la disponibilité de l'API...")
    
    # Vérifier que l'API est accessible
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API accessible, démarrage des tests...\n")
        else:
            print(f"❌ API répond avec le code {response.status_code}")
            return
    except Exception as e:
        print(f"❌ API non accessible: {e}")
        print("Lancez d'abord l'API avec: python main.py")
        return
    
    # Lancer les tests
    tester = APITester(BASE_URL)
    tester.run_complete_test()

if __name__ == "__main__":
    main()
```

### 4. Test de performance simple

Créez un fichier `test_performance.py` :

```python
#!/usr/bin/env python3
"""
Test de performance basique de l'API
"""

import requests
import time
import statistics
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:8000"

def test_endpoint_performance(endpoint: str, method: str = "GET", data: dict = None, num_requests: int = 100):
    """
    Teste les performances d'un endpoint
    """
    times = []
    
    def make_request():
        start_time = time.time()
        try:
            if method.upper() == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}")
            elif method.upper() == "POST":
                response = requests.post(f"{BASE_URL}{endpoint}", json=data)
            
            end_time = time.time()
            return {
                "time": end_time - start_time,
                "status": response.status_code,
                "success": response.status_code < 400
            }
        except Exception as e:
            return {
                "time": 999,
                "status": 0,
                "success": False,
                "error": str(e)
            }
    
    print(f"Test de performance: {method} {endpoint}")
    print(f"Nombre de requêtes: {num_requests}")
    
    # Tests séquentiels
    start_total = time.time()
    results = []
    
    for i in range(num_requests):
        result = make_request()
        results.append(result)
        times.append(result["time"])
        
        if (i + 1) % 10 == 0:
            print(f"  {i + 1}/{num_requests} requêtes terminées")
    
    end_total = time.time()
    
    # Statistiques
    successful_requests = [r for r in results if r["success"]]
    successful_times = [r["time"] for r in successful_requests]
    
    if successful_times:
        print(f"\n📊 Statistiques:")
        print(f"  Requêtes réussies: {len(successful_requests)}/{num_requests}")
        print(f"  Temps total: {end_total - start_total:.2f}s")
        print(f"  Temps moyen par requête: {statistics.mean(successful_times):.3f}s")
        print(f"  Temps médian: {statistics.median(successful_times):.3f}s")
        print(f"  Temps minimum: {min(successful_times):.3f}s")
        print(f"  Temps maximum: {max(successful_times):.3f}s")
        print(f"  Requêtes par seconde: {len(successful_requests)/(end_total - start_total):.2f}")
    else:
        print("❌ Aucune requête réussie")

def main():
    print("🚀 Test de performance de l'API")
    print("=" * 50)
    
    # Créer un utilisateur de test pour les performances
    user_data = {
        "email": "perf.test@example.com",
        "nom": "Performance",
        "prenom": "Test",
        "is_active": True
    }
    
    try:
        # Créer l'utilisateur
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        if response.status_code == 201:
            user_id = response.json()["id"]
            print(f"✅ Utilisateur de test créé (ID: {user_id})\n")
            
            # Tests de performance
            test_endpoint_performance("/", "GET", num_requests=50)
            print()
            test_endpoint_performance("/users/", "GET", num_requests=50)
            print()
            test_endpoint_performance(f"/users/{user_id}", "GET", num_requests=50)
            
            # Nettoyer
            requests.delete(f"{BASE_URL}/users/{user_id}")
            print(f"\n🧹 Utilisateur de test supprimé")
            
        else:
            # L'utilisateur existe peut-être déjà, essayer de le trouver
            response = requests.get(f"{BASE_URL}/users/")
            if response.status_code == 200:
                users = response.json()
                test_user = next((u for u in users if u["email"] == user_data["email"]), None)
                if test_user:
                    print(f"✅ Utilisateur de test trouvé (ID: {test_user['id']})\n")
                    test_endpoint_performance("/", "GET", num_requests=50)
    
    except Exception as e:
        print(f"❌ Erreur lors du test de performance: {e}")

if __name__ == "__main__":
    main()
```

## Ordre logique des opérations

### Séquence correcte

**OBLIGATOIRE : Respectez cet ordre pour éviter les erreurs**

1. **Créer des utilisateurs** (POST /users/)
2. **Créer des articles** pour ces utilisateurs (POST /users/{id}/items/)
3. **Consulter les données** (GET)
4. **Modifier les données** (PUT)
5. **Supprimer d'abord les articles** (DELETE /items/{id})
6. **Puis supprimer les utilisateurs** (DELETE /users/{id})

### Exemple de séquence complète

```python
# Script d'exemple complet
import requests

BASE_URL = "http://localhost:8000"

def exemple_complet():
    print("Exemple complet d'utilisation de l'API")
    
    # 1. Créer un utilisateur
    user_data = {
        "email": "exemple@test.com",
        "nom": "Exemple",
        "prenom": "Utilisateur"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    user = response.json()
    user_id = user["id"]
    print(f"1. Utilisateur créé: {user_id}")
    
    # 2. Créer des articles
    articles = [
        {"title": "Article 1", "price": 1000},
        {"title": "Article 2", "price": 2000}
    ]
    
    article_ids = []
    for article_data in articles:
        response = requests.post(f"{BASE_URL}/users/{user_id}/items/", json=article_data)
        article = response.json()
        article_ids.append(article["id"])
        print(f"2. Article créé: {article['id']}")
    
    # 3. Consulter les données
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    user_with_items = response.json()
    print(f"3. Utilisateur avec {len(user_with_items['items'])} articles")
    
    # 4. Modifier un article
    response = requests.put(f"{BASE_URL}/items/{article_ids[0]}", json={"price": 1500})
    print("4. Article modifié")
    
    # 5. Supprimer les articles
    for article_id in article_ids:
        requests.delete(f"{BASE_URL}/items/{article_id}")
        print(f"5. Article {article_id} supprimé")
    
    # 6. Supprimer l'utilisateur
    requests.delete(f"{BASE_URL}/users/{user_id}")
    print(f"6. Utilisateur {user_id} supprimé")

if __name__ == "__main__":
    exemple_complet()
```

## Diagnostic des problèmes

### Problèmes courants et solutions

**1. Port déjà utilisé :**
```
Error: [Errno 10048] only one usage of each socket address is normally permitted
```
Solution : Utilisez un autre port ou arrêtez l'autre processus

**2. Module non trouvé :**
```
ModuleNotFoundError: No module named 'fastapi'
```
Solution : Activez votre environnement virtuel et installez les dépendances

**3. Erreur 404 lors de création d'article :**
```
{"detail": "Utilisateur non trouvé. Créez d'abord un utilisateur."}
```
Solution : Créez d'abord un utilisateur avec POST /users/

**4. Erreur 400 email dupliqué :**
```
{"detail": "L'email est déjà enregistré"}
```
Solution : Utilisez un email différent ou supprimez l'utilisateur existant

**5. Erreur de validation :**
```
{"detail": [{"loc": ["body", "price"], "msg": "ensure this value is greater than 0"}]}
```
Solution : Vérifiez que vos données respectent les contraintes de validation

### Script de diagnostic

Créez un fichier `diagnostic.py` :

```python
#!/usr/bin/env python3
"""
Script de diagnostic pour l'API
"""

import requests
import sys

def diagnostic_complet():
    print("🔍 Diagnostic de l'API")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    # Test 1 : Connectivité
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ API accessible (code: {response.status_code})")
    except Exception as e:
        print(f"❌ API non accessible: {e}")
        print("   Solution: Lancez l'API avec 'python main.py'")
        return False
    
    # Test 2 : Endpoints principaux
    endpoints = [
        ("/", "GET"),
        ("/users/", "GET"),
        ("/items/", "GET")
    ]
    
    for endpoint, method in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            if response.status_code == 200:
                print(f"✅ {endpoint} accessible")
            else:
                print(f"⚠️  {endpoint} retourne {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} erreur: {e}")
    
    # Test 3 : Documentation
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("✅ Documentation accessible sur /docs")
        else:
            print("⚠️  Documentation non accessible")
    except:
        print("❌ Documentation non accessible")
    
    return True

if __name__ == "__main__":
    if diagnostic_complet():
        print("\n🎉 API fonctionnelle!")
        print("Accédez à http://localhost:8000/docs pour tester")
```

## Prochaines étapes

Dans le module suivant, vous apprendrez à gérer les erreurs, diagnostiquer les problèmes et optimiser votre API pour la production.

Assurez-vous que tous vos tests passent avant de continuer vers le module de gestion d'erreurs et débogage.
