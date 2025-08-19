# Module 8 : Production et déploiement

## Objectifs pédagogiques

À la fin de ce module, vous serez capable de :
- Préparer votre API pour la production
- Configurer la sécurité de base
- Créer une documentation complète
- Déployer votre API sur différentes plateformes

## Préparation pour la production

### Configuration des environnements

Créez un fichier `config.py` :

```python
import os
from typing import Optional

class Settings:
    # Base de données
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./production.db")
    
    # Sécurité
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # API
    API_TITLE: str = os.getenv("API_TITLE", "API CRUD FastAPI")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")
    
    # CORS
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080").split(",")
    
    # Limites
    MAX_CONNECTIONS_COUNT: int = int(os.getenv("MAX_CONNECTIONS_COUNT", "10"))
    MIN_CONNECTIONS_COUNT: int = int(os.getenv("MIN_CONNECTIONS_COUNT", "5"))

settings = Settings()
```

### Fichier .env pour la configuration

Créez `.env` :

```env
# Environnement
DEBUG=false
API_TITLE=API CRUD FastAPI - Production
API_VERSION=1.0.0

# Base de données
DATABASE_URL=sqlite:///./production.db

# Sécurité
SECRET_KEY=your-super-secret-key-here-change-this-in-production

# CORS
ALLOWED_ORIGINS=https://yourfrontend.com,https://www.yourfrontend.com

# Limites
MAX_CONNECTIONS_COUNT=50
MIN_CONNECTIONS_COUNT=10
```

### Structure finale du projet

```
projetsfastapi/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers/
│       ├── __init__.py
│       ├── users.py
│       └── items.py
├── documentation/
├── tests/
├── logs/
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Sécurité de base

### Headers de sécurité

```python
# security.py
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

def add_security_headers(app: FastAPI):
    """Ajoute les headers de sécurité"""
    
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        
        # Headers de sécurité
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response
    
    # Redirection HTTPS en production
    if not settings.DEBUG:
        app.add_middleware(HTTPSRedirectMiddleware)
    
    # Hosts autorisés
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["localhost", "127.0.0.1", "yourdomain.com"]
    )
```

### Authentification simple

```python
# auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta

security = HTTPBearer()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expiré")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")

# Protection d'un endpoint
@app.delete("/admin/users/{user_id}")
def admin_delete_user(user_id: int, token_data = Depends(verify_token)):
    # Vérifier les droits admin
    if token_data.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Droits insuffisants")
    # Logique de suppression...
```

## Documentation complète

### README.md final

```markdown
# API CRUD FastAPI - Guide Complet

## Description
API REST complète pour la gestion d'utilisateurs et d'articles avec toutes les opérations CRUD.

## Fonctionnalités
- Gestion complète des utilisateurs
- Gestion des articles liés aux utilisateurs
- Validation automatique des données
- Documentation interactive
- Gestion d'erreurs robuste
- Logging complet
- Tests automatisés

## Installation rapide

### Prérequis
- Python 3.8+
- pip

### Installation
```bash
git clone <votre-repo>
cd projetsfastapi
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Démarrage
```bash
python main.py
```

### Documentation
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Utilisateurs
- `POST /users/` - Créer utilisateur
- `GET /users/` - Liste des utilisateurs
- `GET /users/{id}` - Détails utilisateur
- `PUT /users/{id}` - Modifier utilisateur
- `DELETE /users/{id}` - Supprimer utilisateur

### Articles
- `POST /users/{id}/items/` - Créer article
- `GET /items/` - Liste des articles
- `GET /items/{id}` - Détails article
- `PUT /items/{id}` - Modifier article
- `DELETE /items/{id}` - Supprimer article

## Tests
```bash
python test_complet.py
```

## Production
Voir `documentation/08-production-deploiement.md`

## Licence
MIT
```

### Script de déploiement

```python
# deploy.py
import os
import subprocess
import shutil

def prepare_production():
    """Prépare l'application pour la production"""
    
    print("🚀 Préparation pour la production...")
    
    # Créer les dossiers nécessaires
    os.makedirs("logs", exist_ok=True)
    os.makedirs("backups", exist_ok=True)
    
    # Copier les fichiers de configuration
    if not os.path.exists(".env"):
        shutil.copy("env.example", ".env")
        print("⚠️  Fichier .env créé - Modifiez la configuration !")
    
    # Installer les dépendances de production
    subprocess.run(["pip", "install", "-r", "requirements.txt"])
    
    # Créer les tables
    subprocess.run(["python", "-c", "from database import engine; import models; models.Base.metadata.create_all(bind=engine)"])
    
    print("✅ Préparation terminée")

def backup_database():
    """Sauvegarde la base de données"""
    from datetime import datetime
    
    if os.path.exists("test.db"):
        backup_name = f"backups/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy("test.db", backup_name)
        print(f"✅ Base de données sauvegardée: {backup_name}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "prepare":
            prepare_production()
        elif sys.argv[1] == "backup":
            backup_database()
    else:
        print("Usage: python deploy.py [prepare|backup]")
```

## Déploiement avec Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copier les requirements et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Créer les dossiers nécessaires
RUN mkdir -p logs backups

# Exposer le port
EXPOSE 8000

# Variables d'environnement
ENV PYTHONPATH=/app
ENV DEBUG=false

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=false
      - DATABASE_URL=sqlite:///./data/production.db
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    restart: unless-stopped
```

## Métriques et monitoring

### Endpoint de health check

```python
@app.get("/health")
def health_check():
    """Health check pour les load balancers"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.API_VERSION
    }

@app.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    """Métriques basiques pour monitoring"""
    
    users_count = db.query(models.User).count()
    items_count = db.query(models.Item).count()
    active_users = db.query(models.User).filter(models.User.is_active == True).count()
    
    return {
        "users_total": users_count,
        "users_active": active_users,
        "items_total": items_count,
        "uptime": "TODO: calculer uptime",
        "memory_usage": "TODO: usage mémoire"
    }
```

## Tests finaux

### Script de validation production

```python
# validate_production.py
import requests
import os
import sqlite3

def validate_production_ready():
    """Valide que l'application est prête pour la production"""
    
    checks = []
    
    # 1. Vérifier la configuration
    if os.path.exists(".env"):
        checks.append(("✅", "Fichier .env présent"))
    else:
        checks.append(("❌", "Fichier .env manquant"))
    
    # 2. Vérifier la base de données
    if os.path.exists("production.db"):
        checks.append(("✅", "Base de données production présente"))
    else:
        checks.append(("⚠️", "Base de données production non initialisée"))
    
    # 3. Vérifier les logs
    if os.path.exists("logs"):
        checks.append(("✅", "Dossier logs présent"))
    else:
        checks.append(("❌", "Dossier logs manquant"))
    
    # 4. Test API
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            checks.append(("✅", "API répond correctement"))
        else:
            checks.append(("❌", f"API erreur {response.status_code}"))
    except:
        checks.append(("❌", "API non accessible"))
    
    # Affichage
    print("🔍 VALIDATION PRODUCTION")
    print("=" * 30)
    for status, message in checks:
        print(f"{status} {message}")
    
    # Résumé
    errors = [c for c in checks if c[0] == "❌"]
    if errors:
        print(f"\n❌ {len(errors)} erreur(s) détectée(s)")
        print("Corrigez les erreurs avant de déployer")
        return False
    else:
        print("\n🎉 Application prête pour la production!")
        return True

if __name__ == "__main__":
    validate_production_ready()
```

## Commandes de déploiement

### Script deploy.sh

```bash
#!/bin/bash

echo "🚀 Déploiement de l'API FastAPI"
echo "================================"

# Arrêter l'ancienne version
echo "Arrêt de l'ancienne version..."
docker-compose down

# Sauvegarder la base de données
echo "Sauvegarde de la base de données..."
python deploy.py backup

# Construire la nouvelle image
echo "Construction de la nouvelle image..."
docker-compose build

# Démarrer les services
echo "Démarrage des services..."
docker-compose up -d

# Vérifier le déploiement
sleep 10
echo "Vérification du déploiement..."
curl -f http://localhost:8000/health || exit 1

echo "✅ Déploiement réussi!"
echo "📚 Documentation: http://localhost:8000/docs"
```

## Checklist finale

Avant de déployer en production :

- [ ] Variables d'environnement configurées
- [ ] Base de données initialisée  
- [ ] Tests passent tous
- [ ] Logs configurés
- [ ] HTTPS configuré
- [ ] Sauvegardes configurées
- [ ] Monitoring en place
- [ ] Documentation à jour
- [ ] Secrets sécurisés
- [ ] Performance testée

## Conclusion

Votre API FastAPI CRUD est maintenant complète et prête pour la production. Vous avez appris :

- La création d'une API REST complète
- La validation des données
- La gestion d'erreurs
- Les tests automatisés
- Le déploiement sécurisé
- Le monitoring et la maintenance

Continuez à améliorer votre API en ajoutant de nouvelles fonctionnalités selon vos besoins !
