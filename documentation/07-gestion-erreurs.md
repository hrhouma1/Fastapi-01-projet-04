# Module 7 : Gestion des erreurs et débogage

## Objectifs pédagogiques

À la fin de ce module, vous serez capable de :
- Identifier et résoudre les erreurs les plus courantes
- Implémenter une gestion d'erreurs robuste
- Déboguer votre API efficacement
- Ajouter des logs pour le monitoring
- Optimiser les performances de votre application

## Types d'erreurs courantes

### 1. Erreurs de démarrage

**Problème : Port déjà utilisé**
```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)
```

**Causes :**
- Une autre instance de l'API est déjà lancée
- Un autre programme utilise le port 8000

**Solutions :**
```python
# Solution 1 : Détecter automatiquement un port libre
import socket

def find_free_port(start_port=8000, max_port=8010):
    """Trouve un port libre"""
    for port in range(start_port, max_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
    return None

# Dans main.py
if __name__ == "__main__":
    import uvicorn
    
    port = find_free_port()
    if port:
        print(f"Démarrage sur le port {port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        print("Aucun port libre trouvé")
```

```bash
# Solution 2 : Arrêter le processus existant (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Solution 3 : Utiliser un autre port
uvicorn main:app --port 8001
```

**Problème : Module non trouvé**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solutions :**
```bash
# Vérifier l'environnement virtuel
# Vous devriez voir (venv) au début de votre invite
# Si non:
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Réinstaller les dépendances
pip install -r requirements.txt

# Vérifier les modules installés
pip list
```

### 2. Erreurs de base de données

**Problème : Table n'existe pas**
```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: users
```

**Cause :** Les tables n'ont pas été créées

**Solution :**
```python
# Dans main.py, après les imports
import models
from database import engine

# Créer toutes les tables
models.Base.metadata.create_all(bind=engine)
print("Tables créées avec succès")
```

**Problème : Contrainte d'unicité violée**
```
sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: users.email
```

**Cause :** Tentative de créer un utilisateur avec un email déjà existant

**Solution : Gestion dans le code**
```python
# Dans crud.py
from sqlalchemy.exc import IntegrityError

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        email=user.email,
        nom=user.nom,
        prenom=user.prenom,
        is_active=user.is_active
    )
    
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        if "UNIQUE constraint failed: users.email" in str(e):
            raise ValueError("Cet email est déjà utilisé")
        else:
            raise ValueError(f"Erreur de base de données: {e}")
```

### 3. Erreurs de validation Pydantic

**Problème : Données invalides**
```json
{
  "detail": [
    {
      "loc": ["body", "price"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt",
      "ctx": {"limit_value": 0}
    }
  ]
}
```

**Gestion améliorée des erreurs de validation :**

```python
# schemas.py - Validations personnalisées avec messages clairs
from pydantic import BaseModel, validator, ValidationError

class ItemCreate(BaseModel):
    title: str
    price: int
    description: str = None
    is_available: bool = True
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Le titre ne peut pas être vide')
        if len(v.strip()) < 3:
            raise ValueError('Le titre doit contenir au moins 3 caractères')
        return v.strip()
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Le prix doit être supérieur à 0 centime')
        if v > 1000000:  # 10,000€
            raise ValueError('Le prix ne peut pas dépasser 10,000€ (1,000,000 centimes)')
        return v

# main.py - Gestionnaire d'erreurs de validation
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """
    Gestionnaire personnalisé pour les erreurs de validation Pydantic
    """
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(x) for x in error["loc"][1:])  # Ignore 'body'
        message = error["msg"]
        
        # Messages personnalisés selon le type d'erreur
        if error["type"] == "value_error.missing":
            message = f"Le champ '{field}' est obligatoire"
        elif error["type"] == "type_error.integer":
            message = f"Le champ '{field}' doit être un nombre entier"
        elif error["type"] == "type_error.str":
            message = f"Le champ '{field}' doit être du texte"
        
        errors.append({
            "champ": field,
            "erreur": message,
            "valeur_recue": error.get("input")
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "message": "Données invalides",
            "erreurs": errors
        }
    )
```

### 4. Erreurs logiques métier

**Problème : Créer un article pour un utilisateur inexistant**

**Solution : Validation métier robuste**
```python
# main.py
@app.post("/users/{user_id}/items/", response_model=schemas.Item, status_code=201)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """Créer un article pour un utilisateur avec validation complète"""
    
    # Validation de l'ID utilisateur
    if user_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="L'ID utilisateur doit être un nombre positif"
        )
    
    # Vérifier que l'utilisateur existe
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail=f"Aucun utilisateur trouvé avec l'ID {user_id}. "
                   f"Créez d'abord un utilisateur avec POST /users/"
        )
    
    # Vérifier que l'utilisateur est actif
    if not db_user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Impossible de créer un article pour un utilisateur inactif"
        )
    
    try:
        return crud.create_user_item(db=db, item=item, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log l'erreur pour debugging
        print(f"Erreur inattendue lors de la création d'article: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erreur interne du serveur"
        )
```

## Système de logging avancé

### Configuration du logging

```python
# logging_config.py
import logging
import sys
from datetime import datetime
import os

def setup_logging(level=logging.INFO):
    """
    Configure le système de logging
    """
    # Créer le dossier logs s'il n'existe pas
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Format des logs
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Configuration du logging
    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt=date_format,
        handlers=[
            # Log vers un fichier
            logging.FileHandler(
                f'logs/api_{datetime.now().strftime("%Y%m%d")}.log',
                encoding='utf-8'
            ),
            # Log vers la console
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Logger spécifique pour l'API
    logger = logging.getLogger('api')
    
    return logger

# main.py - Utilisation du logging
from logging_config import setup_logging

# Configurer le logging au début de l'application
logger = setup_logging(logging.INFO)

# Dans les endpoints
@app.post("/users/", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Tentative de création d'utilisateur avec email: {user.email}")
    
    try:
        # Vérifier l'unicité de l'email
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            logger.warning(f"Tentative de création avec email existant: {user.email}")
            raise HTTPException(status_code=400, detail="Email déjà utilisé")
        
        created_user = crud.create_user(db=db, user=user)
        logger.info(f"Utilisateur créé avec succès: ID {created_user.id}, email {created_user.email}")
        
        return created_user
        
    except HTTPException:
        raise  # Re-lever les HTTPException
    except Exception as e:
        logger.error(f"Erreur lors de la création d'utilisateur: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne")
```

### Logging des requêtes

```python
# middleware_logging.py
import time
import logging
from fastapi import Request

logger = logging.getLogger('api.requests')

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware pour logger toutes les requêtes
    """
    start_time = time.time()
    
    # Informations sur la requête
    client_ip = request.client.host if request.client else "unknown"
    method = request.method
    url = str(request.url)
    
    logger.info(f"Requête entrante: {method} {url} de {client_ip}")
    
    # Exécuter la requête
    response = await call_next(request)
    
    # Calculer le temps de traitement
    process_time = time.time() - start_time
    
    # Logger la réponse
    logger.info(f"Réponse: {response.status_code} en {process_time:.3f}s")
    
    # Ajouter le temps dans les headers pour debugging
    response.headers["X-Process-Time"] = str(process_time)
    
    return response
```

## Gestion d'erreurs centralisée

### Gestionnaires d'exceptions personnalisés

```python
# error_handlers.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger('api.errors')

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Gestionnaire pour les exceptions HTTP
    """
    logger.warning(f"HTTPException: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "erreur": True,
            "code": exc.status_code,
            "message": exc.detail,
            "endpoint": str(request.url)
        }
    )

@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    Gestionnaire pour les erreurs de base de données
    """
    logger.error(f"Erreur de base de données: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "erreur": True,
            "code": 500,
            "message": "Erreur de base de données",
            "details": "Une erreur est survenue lors de l'accès aux données"
        }
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """
    Gestionnaire pour les erreurs de validation métier
    """
    logger.warning(f"ValueError: {exc}")
    
    return JSONResponse(
        status_code=400,
        content={
            "erreur": True,
            "code": 400,
            "message": "Données invalides",
            "details": str(exc)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Gestionnaire pour toutes les autres exceptions
    """
    logger.error(f"Erreur inattendue: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "erreur": True,
            "code": 500,
            "message": "Erreur interne du serveur",
            "details": "Une erreur inattendue s'est produite"
        }
    )
```

## Outils de debugging

### 1. Endpoint de debug

```python
# debug_endpoints.py (à n'utiliser qu'en développement)
@app.get("/debug/info", tags=["Debug"])
def debug_info(db: Session = Depends(get_db)):
    """
    Informations de debug (DÉVELOPPEMENT UNIQUEMENT)
    """
    import psutil
    import platform
    
    # Statistiques de la base de données
    users_count = db.query(models.User).count()
    items_count = db.query(models.Item).count()
    
    # Informations système
    system_info = {
        "plateforme": platform.system(),
        "version_python": platform.python_version(),
        "processeur": platform.processor(),
        "memoire_utilisee_mb": psutil.virtual_memory().used // 1024 // 1024,
        "memoire_totale_mb": psutil.virtual_memory().total // 1024 // 1024
    }
    
    # Statistiques de l'API
    api_stats = {
        "utilisateurs_total": users_count,
        "articles_total": items_count,
        "utilisateurs_actifs": db.query(models.User).filter(models.User.is_active == True).count()
    }
    
    return {
        "debug": True,
        "timestamp": datetime.now().isoformat(),
        "systeme": system_info,
        "api": api_stats
    }

@app.get("/debug/logs", tags=["Debug"])
def debug_recent_logs():
    """
    Récupère les logs récents (DÉVELOPPEMENT UNIQUEMENT)
    """
    import os
    from datetime import datetime
    
    log_file = f'logs/api_{datetime.now().strftime("%Y%m%d")}.log'
    
    if not os.path.exists(log_file):
        return {"message": "Aucun fichier de log trouvé"}
    
    # Lire les 100 dernières lignes
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        recent_lines = lines[-100:] if len(lines) > 100 else lines
    
    return {
        "fichier": log_file,
        "lignes_totales": len(lines),
        "lignes_recentes": len(recent_lines),
        "logs": recent_lines
    }
```

### 2. Mode debug pour FastAPI

```python
# main.py - Configuration debug
import os
from fastapi import FastAPI

# Détecter l'environnement
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"

app = FastAPI(
    title="API CRUD FastAPI",
    debug=DEBUG_MODE,  # Active les traces détaillées en cas d'erreur
    # En production, désactivez ces URLs
    docs_url="/docs" if DEBUG_MODE else None,
    redoc_url="/redoc" if DEBUG_MODE else None
)

# Activer CORS seulement en debug
if DEBUG_MODE:
    from fastapi.middleware.cors import CORSMiddleware
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Point d'entrée avec debug
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=DEBUG_MODE,  # Rechargement automatique en debug
        log_level="debug" if DEBUG_MODE else "info"
    )
```

### 3. Script de diagnostic complet

```python
# diagnostic_complet.py
import requests
import json
import sqlite3
import os
from datetime import datetime

class APIDiagnostic:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.errors = []
        self.warnings = []
        
    def log_error(self, message):
        self.errors.append(f"❌ {message}")
        print(f"❌ {message}")
    
    def log_warning(self, message):
        self.warnings.append(f"⚠️  {message}")
        print(f"⚠️  {message}")
    
    def log_success(self, message):
        print(f"✅ {message}")
    
    def test_api_connection(self):
        """Test de connectivité de l'API"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                self.log_success("API accessible")
                return True
            else:
                self.log_error(f"API répond avec le code {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            self.log_error("API non accessible - Vérifiez qu'elle est démarrée")
            return False
        except Exception as e:
            self.log_error(f"Erreur de connexion: {e}")
            return False
    
    def test_database(self):
        """Test de la base de données"""
        if not os.path.exists("test.db"):
            self.log_error("Fichier de base de données test.db non trouvé")
            return False
        
        try:
            conn = sqlite3.connect("test.db")
            cursor = conn.cursor()
            
            # Vérifier les tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = ['users', 'items']
            for table in expected_tables:
                if table in tables:
                    self.log_success(f"Table {table} présente")
                else:
                    self.log_error(f"Table {table} manquante")
            
            # Vérifier les données
            cursor.execute("SELECT COUNT(*) FROM users")
            users_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM items")
            items_count = cursor.fetchone()[0]
            
            print(f"📊 Base de données: {users_count} utilisateurs, {items_count} articles")
            
            conn.close()
            return True
            
        except Exception as e:
            self.log_error(f"Erreur base de données: {e}")
            return False
    
    def test_crud_operations(self):
        """Test des opérations CRUD"""
        if not self.test_api_connection():
            return False
        
        try:
            # Test POST utilisateur
            user_data = {
                "email": f"diagnostic_{datetime.now().strftime('%Y%m%d_%H%M%S')}@test.com",
                "nom": "Diagnostic",
                "prenom": "Test",
                "is_active": True
            }
            
            response = requests.post(f"{self.base_url}/users/", json=user_data)
            if response.status_code == 201:
                user = response.json()
                user_id = user["id"]
                self.log_success("Création d'utilisateur OK")
            else:
                self.log_error(f"Échec création utilisateur: {response.status_code}")
                return False
            
            # Test GET utilisateur
            response = requests.get(f"{self.base_url}/users/{user_id}")
            if response.status_code == 200:
                self.log_success("Lecture d'utilisateur OK")
            else:
                self.log_error("Échec lecture utilisateur")
            
            # Test POST article
            item_data = {
                "title": "Article de diagnostic",
                "price": 1000,
                "is_available": True
            }
            
            response = requests.post(f"{self.base_url}/users/{user_id}/items/", json=item_data)
            if response.status_code == 201:
                item = response.json()
                item_id = item["id"]
                self.log_success("Création d'article OK")
            else:
                self.log_error(f"Échec création article: {response.status_code}")
            
            # Nettoyage
            requests.delete(f"{self.base_url}/items/{item_id}")
            requests.delete(f"{self.base_url}/users/{user_id}")
            self.log_success("Nettoyage des données de test OK")
            
            return True
            
        except Exception as e:
            self.log_error(f"Erreur lors des tests CRUD: {e}")
            return False
    
    def run_complete_diagnostic(self):
        """Exécute un diagnostic complet"""
        print("🔍 DIAGNOSTIC COMPLET DE L'API")
        print("=" * 50)
        
        # Tests
        self.test_api_connection()
        self.test_database()
        self.test_crud_operations()
        
        # Résumé
        print("\n📊 RÉSUMÉ DU DIAGNOSTIC")
        print("=" * 30)
        print(f"Erreurs: {len(self.errors)}")
        print(f"Avertissements: {len(self.warnings)}")
        
        if self.errors:
            print("\n❌ ERREURS DÉTECTÉES:")
            for error in self.errors:
                print(f"  {error}")
        
        if self.warnings:
            print("\n⚠️  AVERTISSEMENTS:")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if not self.errors:
            print("\n🎉 Aucune erreur détectée - API fonctionnelle!")

if __name__ == "__main__":
    diagnostic = APIDiagnostic()
    diagnostic.run_complete_diagnostic()
```

## Optimisation des performances

### 1. Monitoring des performances

```python
# performance_monitor.py
import time
import functools
import logging

logger = logging.getLogger('api.performance')

def monitor_performance(func):
    """
    Décorateur pour monitorer les performances des fonctions
    """
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        execution_time = time.time() - start_time
        
        if execution_time > 1.0:  # Log si > 1 seconde
            logger.warning(f"Fonction lente détectée: {func.__name__} - {execution_time:.3f}s")
        else:
            logger.debug(f"{func.__name__} exécutée en {execution_time:.3f}s")
        
        return result
    
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        
        if execution_time > 1.0:
            logger.warning(f"Fonction lente détectée: {func.__name__} - {execution_time:.3f}s")
        
        return result
    
    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

# Utilisation dans les endpoints
@app.get("/users/", response_model=List[schemas.User])
@monitor_performance
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)
```

### 2. Cache simple

```python
# cache_utils.py
import time
from typing import Any, Optional

class SimpleCache:
    def __init__(self, default_ttl: int = 300):  # 5 minutes par défaut
        self.cache = {}
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            data, expiry = self.cache[key]
            if time.time() < expiry:
                return data
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        if ttl is None:
            ttl = self.default_ttl
        expiry = time.time() + ttl
        self.cache[key] = (value, expiry)
    
    def clear(self):
        self.cache.clear()

# Instance globale
cache = SimpleCache()

# Utilisation dans les endpoints
@app.get("/users/", response_model=List[schemas.User])
def read_users_cached(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cache_key = f"users_{skip}_{limit}"
    
    # Vérifier le cache
    cached_result = cache.get(cache_key)
    if cached_result:
        logger.info(f"Données récupérées du cache: {cache_key}")
        return cached_result
    
    # Si pas en cache, récupérer de la DB
    users = crud.get_users(db, skip=skip, limit=limit)
    
    # Mettre en cache pour 60 secondes
    cache.set(cache_key, users, ttl=60)
    
    return users
```

## Prochaines étapes

Dans le dernier module, vous apprendrez à préparer votre API pour la production, incluant le déploiement, la sécurité et la documentation finale.

Testez tous les outils de debugging de ce module et assurez-vous que votre gestion d'erreurs fonctionne correctement.
