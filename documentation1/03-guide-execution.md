# 03 - Guide d'Exécution du Projet FastAPI CRUD

## Vue d'ensemble

Ce guide vous accompagne étape par étape pour exécuter et utiliser votre API FastAPI CRUD. Il couvre l'installation, le lancement, les tests et l'utilisation pratique de l'API.

## Prérequis

- Python 3.7 ou supérieur installé
- Terminal/Invite de commandes
- Navigateur web pour tester la documentation interactive

## Étape 1 : Préparation de l'environnement

### 1.1 Vérification de l'installation Python

```bash
python --version
```

Si Python n'est pas installé, téléchargez-le depuis [python.org](https://python.org).

### 1.2 Navigation vers le projet

```bash
cd C:\projetsfastapi
# ou le chemin vers votre dossier de projet
```

### 1.3 Vérification de la structure du projet

```bash
dir  # Windows
ls   # macOS/Linux
```

Vous devriez voir tous les fichiers du projet, y compris `main.py`, `requirements.txt`, et le dossier `venv`.

## Étape 2 : Configuration de l'environnement virtuel

### 2.1 Activation de l'environnement virtuel

**Sur Windows :**
```bash
venv\Scripts\activate
```

**Sur macOS/Linux :**
```bash
source venv/bin/activate
```

**Vérification :** Vous devriez voir `(venv)` au début de votre invite de commandes.

### 2.2 Installation/Vérification des dépendances

```bash
# Vérifier les packages installés
pip list

# Installer les dépendances si nécessaire
pip install -r requirements.txt
```

## Étape 3 : Lancement de l'API

### 3.1 Démarrage sécurisé (méthode recommandée)

```bash
python safe_start.py
```

**Avantages du démarrage sécurisé :**
- Vérification automatique des ports disponibles
- Gestion des conflits de ports
- Messages informatifs détaillés
- Arrêt propre des processus conflictuels

### 3.2 Options de démarrage avancées

```bash
# Avec recherche automatique de port libre
python safe_start.py --auto-port

# Avec arrêt forcé des processus conflictuels
python safe_start.py --force-kill

# Sur un port spécifique
python safe_start.py --port 8080

# Sans rechargement automatique
python safe_start.py --no-reload
```

### 3.3 Démarrage alternatif

```bash
# Méthode classique
python main.py

# Avec uvicorn directement
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Étape 4 : Vérification du fonctionnement

### 4.1 Test de l'API

Une fois l'API démarrée, vous devriez voir :

```
Démarrage sécurisé de l'API FastAPI CRUD
==================================================
Dépendances FastAPI disponibles
Port 8000 disponible
Démarrage de l'API sur http://0.0.0.0:8000
Documentation : http://localhost:8000/docs
Rechargement automatique : activé
```

### 4.2 URLs d'accès principales

- **API racine** : http://localhost:8000
- **Documentation Swagger** : http://localhost:8000/docs
- **Documentation ReDoc** : http://localhost:8000/redoc

### 4.3 Test rapide dans le navigateur

Ouvrez http://localhost:8000 dans votre navigateur. Vous devriez voir :

```json
{
  "message": "Bienvenue dans l'API CRUD FastAPI!",
  "docs": "/docs"
}
```

## Étape 5 : Ajout des données d'exemple

### 5.1 Vérification de l'état de la base de données

```bash
python seed_data.py status
```

### 5.2 Ajout de données d'exemple

```bash
# Ajouter des données d'exemple
python seed_data.py add

# Forcer l'ajout même si des données existent
python seed_data.py add --force

# Remettre à zéro avec nouvelles données
python seed_data.py reset

# Ajout rapide d'un utilisateur de test
python seed_data.py quick
```

### 5.3 Vérification des données ajoutées

Après ajout des données, vous devriez voir :

```
STATUT ACTUEL DE LA BASE DE DONNÉES
=============================================
Utilisateurs total : 5
Utilisateurs actifs : 4
Articles total : 13
Articles disponibles : 10
```

## Étape 6 : Tests et utilisation

### 6.1 Documentation interactive (recommandée)

Allez sur http://localhost:8000/docs et :
1. Explorez les endpoints disponibles
2. Testez les opérations CRUD directement
3. Consultez les modèles de données
4. Exécutez des requêtes en temps réel

### 6.2 Tests avec curl (ligne de commande)

**Lister tous les utilisateurs :**
```bash
curl -X GET "http://localhost:8000/users/"
```

**Créer un utilisateur :**
```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "nouveau@example.com",
       "nom": "Nouveau",
       "prenom": "Utilisateur",
       "is_active": true
     }'
```

### 6.3 URLs testables directement dans le navigateur

**Endpoints de consultation (GET) :**
- http://localhost:8000/ - Message de bienvenue
- http://localhost:8000/users/ - Liste des utilisateurs
- http://localhost:8000/items/ - Liste des articles
- http://localhost:8000/users/1 - Détails utilisateur #1
- http://localhost:8000/users/1/items/ - Articles de l'utilisateur #1

### 6.4 Scripts de test automatisés

**Test de cohérence :**
```bash
python test_coherence.py
```

**Test complet avec démonstration :**
```bash
python exemple_utilisation.py
```

**Tests chronologiques avec REST Client :**
- Ouvrez `api_tests.http` dans VS Code
- Installez l'extension REST Client
- Exécutez les requêtes une par une

## Étape 7 : Opérations CRUD complètes

### 7.1 Utilisateurs

| Opération | Méthode | Endpoint | Description |
|-----------|---------|----------|-------------|
| **Créer** | `POST` | `/users/` | Ajouter un nouvel utilisateur |
| **Lire** | `GET` | `/users/` | Liste tous les utilisateurs |
| **Lire** | `GET` | `/users/{id}` | Détails d'un utilisateur |
| **Modifier** | `PUT` | `/users/{id}` | Mettre à jour un utilisateur |
| **Supprimer** | `DELETE` | `/users/{id}` | Supprimer un utilisateur |

### 7.2 Articles

| Opération | Méthode | Endpoint | Description |
|-----------|---------|----------|-------------|
| **Créer** | `POST` | `/users/{id}/items/` | Ajouter un article à un utilisateur |
| **Lire** | `GET` | `/items/` | Liste tous les articles |
| **Lire** | `GET` | `/items/{id}` | Détails d'un article |
| **Modifier** | `PUT` | `/items/{id}` | Mettre à jour un article |
| **Supprimer** | `DELETE` | `/items/{id}` | Supprimer un article |

### 7.3 Relations entre entités

- Un **utilisateur** peut avoir plusieurs **articles**
- Un **article** appartient à un seul **utilisateur**
- La suppression d'un **utilisateur** supprime ses **articles** (CASCADE)

## Étape 8 : Gestion et maintenance

### 8.1 Arrêt de l'API

**Arrêt normal :**
- Dans le terminal où l'API tourne : `Ctrl+C`

**Arrêt forcé si nécessaire :**
```bash
python check_ports.py --kill-port 8000
```

### 8.2 Diagnostic des ports

```bash
# Vérifier les ports utilisés
python check_ports.py

# Afficher toutes les commandes utiles
python check_ports.py --show-commands

# Arrêter tous les processus Python
python check_ports.py --kill-all-python
```

### 8.3 Redémarrage en cas de problème

```bash
# Redémarrage sécurisé
python safe_start.py

# Avec port automatique
python safe_start.py --auto-port

# Avec nettoyage des processus
python safe_start.py --force-kill
```

## Étape 9 : Ressources complémentaires

### 9.1 Documentation du projet

- `01-GUIDE_SEED_DATA.md` - Guide des données d'exemple
- `02-URLS_TESTS.md` - Liste complète des URLs testables
- `documentation/` - Formation complète (8 modules)
- `GUIDE_GESTION_PROCESSUS.md` - Gestion avancée des processus

### 9.2 Fichiers de test

- `api_tests.http` - Tests chronologiques avec REST Client
- `exemple_utilisation.py` - Démonstration automatisée
- `test_coherence.py` - Tests de validation
- `seed_data.py` - Gestion des données d'exemple

### 9.3 Outils de diagnostic

- `safe_start.py` - Démarrage sécurisé
- `check_ports.py` - Diagnostic et gestion des ports
- `setup.bat` / `setup.sh` - Configuration automatique

## Résolution des problèmes courants

### Erreur de port occupé

```bash
# Diagnostic
python check_ports.py

# Solutions
python safe_start.py --auto-port
python safe_start.py --force-kill
```

### Environnement virtuel non activé

```bash
# Réactivation
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### Dépendances manquantes

```bash
# Réinstallation
pip install -r requirements.txt
```

### Base de données vide

```bash
# Ajout de données d'exemple
python seed_data.py add
```

## Prochaines étapes recommandées

1. **Explorez la documentation interactive** sur http://localhost:8000/docs
2. **Testez tous les endpoints** avec des données réelles
3. **Consultez les guides avancés** dans le dossier documentation/
4. **Personnalisez l'API** selon vos besoins spécifiques
5. **Implémentez de nouvelles fonctionnalités** (authentification, cache, etc.)

## Félicitations !

Votre API FastAPI CRUD est maintenant opérationnelle et prête à être utilisée pour tous vos besoins de gestion de données !

Pour toute question ou problème, consultez la documentation complète ou les fichiers de diagnostic inclus dans le projet.
