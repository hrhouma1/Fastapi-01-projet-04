# API CRUD FastAPI

Une API complète développée avec FastAPI qui implémente toutes les opérations CRUD (Create, Read, Update, Delete) pour la gestion d'utilisateurs et d'articles.

## Fonctionnalités

- ✅ **Opérations CRUD complètes** pour les utilisateurs et articles
- ✅ **Base de données SQLite** avec SQLAlchemy
- ✅ **Validation automatique** des données avec Pydantic
- ✅ **Documentation automatique** avec Swagger UI
- ✅ **Relations entre entités** (utilisateurs ↔ articles)
- ✅ **Gestion des erreurs** et codes de statut HTTP appropriés
- 🆕 **Interface graphique PySide6** moderne et intuitive
- 🆕 **Client API intégré** pour communication GUI ↔ API

## Structure du projet

```
projetsfastapi/
├── venv/             # Environnement virtuel Python (à créer)
├── main.py           # Point d'entrée de l'application FastAPI
├── database.py       # Configuration de la base de données
├── models.py         # Modèles SQLAlchemy (tables de base de données)
├── schemas.py        # Schémas Pydantic (validation et sérialisation)
├── crud.py           # Opérations CRUD
├── requirements.txt  # Dépendances Python (FastAPI + PySide6)
├── exemple_utilisation.py  # Script de test de l'API
├── api_tests.http    # Tests HTTP chronologiques avec REST Client
├── test_coherence.py # Test rapide de cohérence des données
├── setup.bat         # Script de configuration automatique (Windows)
├── setup.sh          # Script de configuration automatique (macOS/Linux)
├── safe_start.py     # Script de démarrage sécurisé avec gestion des ports
├── check_ports.py    # Diagnostic et gestion des ports de développement
├── gui_client/       # 🆕 Interface graphique PySide6
│   ├── __init__.py   #     Package principal GUI
│   ├── api_client.py #     Client de communication API
│   ├── main_window.py #    Interface utilisateur complète
│   └── README.md     #     Guide rapide GUI
├── run_gui.py        # 🆕 Script de lancement interface graphique
├── setup_gui.py      # 🆕 Configuration automatique GUI
├── test_gui_integration.py # 🆕 Tests d'intégration GUI ↔ API
├── GUIDE_GESTION_PROCESSUS.md  # Guide complet de gestion des processus
├── documentation/    # Documentation de formation complète (8 modules)
├── documentation1/   # 🆕 Documentation professionnelle (sans emojis)
│   ├── 01-GUIDE_SEED_DATA.md    # Guide des données d'exemple
│   ├── 02-URLS_TESTS.md         # URLs testables complètes  
│   ├── 03-guide-execution.md    # Guide d'exécution étape par étape
│   └── 04-interface-graphique.md # 🆕 Guide complet de l'interface GUI
├── URLS_TESTS.md     # Liste complète de toutes les URLs à tester
├── seed_data.py      # Script pour ajouter des données d'exemple
├── GUIDE_SEED_DATA.md # Guide détaillé des données d'exemple
├── .gitignore        # Fichiers à ignorer par Git
├── test.db           # Base de données SQLite (créée automatiquement)
└── README.md         # Documentation
```

## Installation et lancement

### Option A : Configuration automatique (recommandée)

**Configuration complète (API + Interface graphique) :**
```bash
# Windows
setup.bat

# macOS/Linux  
./setup.sh

# Configuration spécifique GUI
python setup_gui.py
```

Ces scripts vont automatiquement :
- Créer l'environnement virtuel
- Installer toutes les dépendances (FastAPI + PySide6)
- Vous donner les instructions pour lancer l'API et l'interface

### Option B : Configuration manuelle

### 1. Créer et activer un environnement virtuel

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows :
venv\Scripts\activate
# Sur macOS/Linux :
source venv/bin/activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Lancer l'application

> **⚠️ Important :** Assurez-vous que l'environnement virtuel est activé avant de lancer l'application !

#### Option A : Démarrage sécurisé (recommandé)
```bash
python safe_start.py
```

#### Option B : Démarrage standard
```bash
python main.py
```

#### Option C : Avec uvicorn directement
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### **Gestion des conflits de ports :**

Si vous obtenez l'erreur `[Errno 10048]` (port déjà utilisé) :

```bash
# Diagnostic des ports
python check_ports.py

# Démarrage avec port automatique
python safe_start.py --auto-port

# Arrêter les processus conflictuels
python safe_start.py --force-kill

# Libérer un port spécifique
python check_ports.py --kill-port 8000
```

### 4. Accéder à l'API

- **API** : http://localhost:8000
- **Documentation Swagger** : http://localhost:8000/docs
- **Documentation ReDoc** : http://localhost:8000/redoc

### 5. 🆕 Lancer l'interface graphique (optionnel)

```bash
# Terminal séparé - Interface graphique moderne
python run_gui.py
```

**Avantages de l'interface graphique :**
- ✅ Gestion visuelle des utilisateurs et articles
- ✅ Recherche en temps réel
- ✅ Formatage automatique des prix
- ✅ Indicateur de connexion à l'API
- ✅ Interface moderne et intuitive

### 6. Désactiver l'environnement virtuel

Quand vous avez terminé de travailler sur le projet :

```bash
deactivate
```

> **💡 Note importante :** Assurez-vous toujours que l'environnement virtuel est activé (vous devriez voir `(venv)` au début de votre invite de commande) avant d'installer des dépendances ou de lancer l'application.

## Endpoints disponibles

### Utilisateurs

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/users/` | **🔴 1ère ÉTAPE** - Créer un utilisateur |
| `GET` | `/users/` | Récupérer tous les utilisateurs |
| `GET` | `/users/{user_id}` | Récupérer un utilisateur par ID |
| `GET` | `/users/{user_id}/items/` | Récupérer tous les articles d'un utilisateur |
| `PUT` | `/users/{user_id}` | Mettre à jour un utilisateur |
| `DELETE` | `/users/{user_id}` | Supprimer un utilisateur et ses articles (CASCADE) |

### Articles

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/users/{user_id}/items/` | **🟡 2ème ÉTAPE** - Créer un article pour un utilisateur existant |
| `GET` | `/items/` | Récupérer tous les articles |
| `GET` | `/items/{item_id}` | Récupérer un article par ID |
| `PUT` | `/items/{item_id}` | Mettre à jour un article |
| `DELETE` | `/items/{item_id}` | Supprimer un article |

### Recherche

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/search/items?q=terme&limit=50` | 🆕 Rechercher des articles par mots-clés |

> **⚠️ ORDRE IMPORTANT :** Vous devez d'abord créer des utilisateurs, puis créer des articles pour ces utilisateurs. La création d'un article pour un utilisateur inexistant retournera une erreur 404.

## Exemples d'utilisation

### Créer un utilisateur

```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "john.doe@example.com",
       "nom": "Doe",
       "prenom": "John",
       "is_active": true
     }'
```

### Créer un article

```bash
curl -X POST "http://localhost:8000/users/1/items/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Mon premier article",
       "description": "Description de l\''article",
       "price": 2500,
       "is_available": true
     }'
```

### Récupérer tous les utilisateurs

```bash
curl -X GET "http://localhost:8000/users/"
```

### Mettre à jour un utilisateur

```bash
curl -X PUT "http://localhost:8000/users/1" \
     -H "Content-Type: application/json" \
     -d '{
       "nom": "Nouveau Nom"
     }'
```

### Supprimer un article

```bash
curl -X DELETE "http://localhost:8000/items/1"
```

### 🆕 Rechercher des articles

```bash
# Recherche simple
curl -X GET "http://localhost:8000/search/items?q=iPhone"

# Recherche avec limite de résultats
curl -X GET "http://localhost:8000/search/items?q=macbook&limit=10"

# Recherche avec espaces (URL encodée)
curl -X GET "http://localhost:8000/search/items?q=Python%20livre"
```

## Modèles de données

### Utilisateur

```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "nom": "Doe",
  "prenom": "John",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "items": []
}
```

### Article

```json
{
  "id": 1,
  "title": "Mon article",
  "description": "Description de l'article",
  "price": 2500,
  "is_available": true,
  "owner_id": 1,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

## Fonctionnalités avancées

- **Pagination** : Paramètres `skip` et `limit` pour la pagination des listes
- **Validation automatique** : Pydantic valide automatiquement les données d'entrée
- **Relations CASCADE** : La suppression d'un utilisateur supprime automatiquement ses articles
- **Timestamps automatiques** : Dates de création et modification gérées automatiquement
- **Gestion des erreurs** : Messages d'erreur appropriés avec codes de statut HTTP

## Technologies utilisées

- **FastAPI** : Framework web moderne et rapide
- **SQLAlchemy** : ORM pour la gestion de base de données
- **Pydantic** : Validation et sérialisation des données
- **SQLite** : Base de données légère
- **Uvicorn** : Serveur ASGI haute performance

## Test de l'API

### Option 1 : Tests HTTP chronologiques (recommandé) 

Un fichier `api_tests.http` complet avec l'ordre logique est inclus :

```bash
# 1. Lancez l'API
python safe_start.py

# 2. Ouvrez api_tests.http dans VS Code avec l'extension REST Client
# 3. Exécutez les requêtes dans l'ordre chronologique
```

Ce fichier contient :
- ✅ **35+ tests chronologiques** dans l'ordre logique
- 🔴 **Étape 1** : Création des utilisateurs (obligatoire)
- 🟡 **Étape 2** : Création des articles pour ces utilisateurs
- 🔵 **Étape 3** : Consultations et modifications
- ⚫ **Étape 4** : Nettoyage des données
- ❌ **Tests d'erreurs** pour valider la cohérence

### Option 2 : Test de cohérence rapide

```bash
# Teste la validation et l'ordre logique (utilisateurs → articles)
python test_coherence.py
```

### Option 3 : Script de test automatisé complet

```bash
# Assurez-vous que l'API est lancée (python safe_start.py)
python exemple_utilisation.py
```

### Option 4 : Test manuel avec curl

Vous pouvez aussi tester manuellement avec les exemples curl fournis dans la section "Exemples d'utilisation".

### Option 5 : Documentation interactive

Accédez à http://localhost:8000/docs pour tester l'API directement depuis votre navigateur avec l'interface Swagger.

### Option 6 : Guide des URLs de test

Consultez le fichier `URLS_TESTS.md` qui contient **toutes les URLs** que vous pouvez tester :
- URLs directement testables dans le navigateur  
- URLs nécessitant des outils spéciaux
- Séquence de test recommandée
- Gestion des ports alternatifs

### Option 7 : Données d'exemple (recommandé pour débuter)

Ajoutez rapidement des données d'exemple dans votre base de données :

```bash
# Ajouter des utilisateurs et articles d'exemple
python seed_data.py add

# Voir l'état de la base de données
python seed_data.py status

# Ajout rapide d'un utilisateur de test
python seed_data.py quick

# Remettre à zéro et ajouter les données d'exemple
python seed_data.py reset
```

> **💡 Conseil :** Utilisez `seed_data.py add` pour avoir immédiatement des données à tester, puis consultez `URLS_TESTS.md` pour savoir quelles URLs visiter.

## 🛠️ Outils de diagnostic et gestion

### Diagnostic des ports

```bash
# Vérifier quels ports sont utilisés
python check_ports.py

# Afficher les commandes utiles
python check_ports.py --show-commands

# Arrêter tous les processus Python
python check_ports.py --kill-all-python
```

### Démarrage sécurisé

```bash
# Démarrage normal
python safe_start.py

# Avec recherche automatique de port libre
python safe_start.py --auto-port

# Avec arrêt forcé des processus conflictuels
python safe_start.py --force-kill

# Sur un port spécifique
python safe_start.py --port 8080

# Sans rechargement automatique
python safe_start.py --no-reload
```

### Guide complet

Consultez le fichier `GUIDE_GESTION_PROCESSUS.md` pour un guide détaillé sur :
- 🔍 Identification des processus et ports
- ⚡ Arrêt des processus (Windows/macOS/Linux)
- 🛡️ Prévention des conflits
- 🤖 Scripts d'automatisation
- 📚 Commandes par technologie (Python, Node.js, etc.)

## Développement

L'API est prête à être utilisée et peut être facilement étendue avec de nouvelles fonctionnalités :

- Authentification et autorisation
- Upload de fichiers
- Système de cache
- Tests automatisés
- Déploiement avec Docker

Bonne utilisation de votre API CRUD FastAPI ! 🚀
