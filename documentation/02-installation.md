# Module 2 : Installation et configuration de l'environnement

## Objectifs pédagogiques

À la fin de ce module, vous serez capable de :
- Installer Python et vérifier votre installation
- Créer et activer un environnement virtuel
- Installer toutes les dépendances nécessaires
- Configurer votre éditeur de code
- Lancer votre première application FastAPI

## Prérequis système

### Système d'exploitation supporté
- Windows 10/11
- macOS 10.14 ou plus récent  
- Linux (Ubuntu, Debian, CentOS, etc.)

### Espace disque requis
- Minimum : 500 MB d'espace libre
- Recommandé : 2 GB d'espace libre

## Installation de Python

### Vérification de Python existant

Avant d'installer Python, vérifiez s'il est déjà présent sur votre système.

**Sur Windows :**
1. Ouvrez l'invite de commande (cmd)
2. Tapez la commande suivante :
```bash
python --version
```

**Sur macOS/Linux :**
1. Ouvrez le terminal
2. Tapez la commande suivante :
```bash
python3 --version
```

### Si Python n'est pas installé

#### Installation sur Windows
1. Rendez-vous sur https://python.org
2. Cliquez sur "Downloads" 
3. Téléchargez la version la plus récente de Python (3.11 ou 3.12)
4. Exécutez le fichier téléchargé
5. **IMPORTANT** : Cochez "Add Python to PATH" pendant l'installation
6. Cliquez sur "Install Now"
7. Attendez la fin de l'installation

#### Installation sur macOS
1. Rendez-vous sur https://python.org
2. Téléchargez la version pour macOS
3. Ouvrez le fichier .pkg téléchargé
4. Suivez les instructions d'installation

#### Installation sur Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Vérification de l'installation

Après installation, vérifiez que Python fonctionne :

**Windows :**
```bash
python --version
pip --version
```

**macOS/Linux :**
```bash
python3 --version
pip3 --version
```

Vous devriez voir s'afficher les numéros de version de Python et pip.

## Configuration du projet

### Création du dossier de travail

1. Créez un dossier pour votre projet sur votre bureau ou dans vos documents
2. Nommez-le `projetsfastapi`

**Via l'explorateur de fichiers :**
- Clic droit → Nouveau dossier → `projetsfastapi`

**Via la ligne de commande :**
```bash
mkdir projetsfastapi
cd projetsfastapi
```

### Navigation dans le dossier

Ouvrez une invite de commande dans votre dossier projet :

**Windows :**
- Ouvrez l'explorateur de fichiers
- Naviguez vers votre dossier `projetsfastapi`  
- Dans la barre d'adresse, tapez `cmd` et appuyez sur Entrée

**macOS :**
- Ouvrez le terminal
- Naviguez avec `cd` vers votre dossier

**Linux :**
- Ouvrez le terminal
- Naviguez avec `cd` vers votre dossier

## Création de l'environnement virtuel

### Pourquoi un environnement virtuel

Un environnement virtuel permet d'isoler les dépendances de votre projet. Cela évite les conflits entre différents projets Python.

### Création de l'environnement

Dans votre invite de commande, dans le dossier `projetsfastapi` :

**Windows :**
```bash
python -m venv venv
```

**macOS/Linux :**
```bash
python3 -m venv venv
```

Cette commande crée un dossier `venv` contenant l'environnement virtuel.

### Activation de l'environnement virtuel

**Windows :**
```bash
venv\Scripts\activate
```

**macOS/Linux :**
```bash
source venv/bin/activate
```

### Vérification de l'activation

Après activation, vous devriez voir `(venv)` au début de votre invite de commande.

**Exemple sur Windows :**
```
(venv) C:\Users\VotreNom\projetsfastapi>
```

### Désactivation de l'environnement (pour plus tard)

Pour désactiver l'environnement virtuel quand vous avez fini de travailler :
```bash
deactivate
```

## Installation des dépendances

### Mise à jour de pip

Avant d'installer les dépendances, mettez à jour pip :

**Windows :**
```bash
python.exe -m pip install --upgrade pip
```

**macOS/Linux :**
```bash
python3 -m pip install --upgrade pip
```

### Création du fichier requirements.txt

Créez un fichier `requirements.txt` dans votre dossier projet avec le contenu suivant :

```
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
sqlalchemy>=2.0.25
pydantic>=2.6.0
python-multipart>=0.0.9
```

### Installation des dépendances

Avec votre environnement virtuel activé, installez les dépendances :

```bash
pip install -r requirements.txt
```

Cette commande va installer :
- **FastAPI** : Le framework web
- **Uvicorn** : Le serveur de développement
- **SQLAlchemy** : L'ORM pour la base de données
- **Pydantic** : La validation des données  
- **python-multipart** : Support des formulaires

### Vérification de l'installation

Vérifiez que toutes les dépendances sont installées :

```bash
pip list
```

Vous devriez voir toutes les bibliothèques installées avec leurs versions.

## Configuration de l'éditeur de code

### VS Code (recommandé)

1. Téléchargez VS Code sur https://code.visualstudio.com
2. Installez VS Code
3. Ouvrez VS Code
4. Installez les extensions suivantes :
   - Python (de Microsoft)
   - REST Client (de Huachao Mao)

### Configuration de VS Code pour le projet

1. Ouvrez VS Code
2. Fichier → Ouvrir le dossier
3. Sélectionnez votre dossier `projetsfastapi`
4. VS Code devrait détecter automatiquement votre environnement virtuel

## Test de l'installation

### Création d'un fichier de test

Créez un fichier `test_installation.py` avec le contenu suivant :

```python
#!/usr/bin/env python3
"""
Test d'installation des dépendances
"""

def test_imports():
    """Teste que toutes les dépendances sont installées"""
    
    try:
        import fastapi
        print(f"✅ FastAPI version {fastapi.__version__}")
    except ImportError:
        print("❌ FastAPI non installé")
        return False
    
    try:
        import uvicorn
        print(f"✅ Uvicorn version {uvicorn.__version__}")
    except ImportError:
        print("❌ Uvicorn non installé")
        return False
    
    try:
        import sqlalchemy
        print(f"✅ SQLAlchemy version {sqlalchemy.__version__}")
    except ImportError:
        print("❌ SQLAlchemy non installé")
        return False
    
    try:
        import pydantic
        print(f"✅ Pydantic version {pydantic.__version__}")
    except ImportError:
        print("❌ Pydantic non installé")
        return False
    
    print("\n🎉 Toutes les dépendances sont correctement installées !")
    return True

if __name__ == "__main__":
    test_imports()
```

### Exécution du test

Dans votre invite de commande, avec l'environnement virtuel activé :

```bash
python test_installation.py
```

Vous devriez voir s'afficher les versions de toutes les bibliothèques installées.

## Création de votre première API

### Fichier minimal

Créez un fichier `hello_api.py` pour tester que tout fonctionne :

```python
from fastapi import FastAPI

# Création de l'instance FastAPI
app = FastAPI(title="Ma première API", version="1.0.0")

@app.get("/")
def read_root():
    """Endpoint de base qui retourne un message de bienvenue"""
    return {"message": "Bienvenue dans votre première API FastAPI !"}

@app.get("/hello/{name}")
def say_hello(name: str):
    """Endpoint qui salue une personne par son nom"""
    return {"message": f"Bonjour {name} !"}
```

### Lancement de l'API

Dans votre invite de commande :

```bash
uvicorn hello_api:app --reload --host 0.0.0.0 --port 8000
```

### Vérification du fonctionnement

1. Ouvrez votre navigateur web
2. Allez sur http://localhost:8000
3. Vous devriez voir : `{"message": "Bienvenue dans votre première API FastAPI !"}`
4. Testez aussi : http://localhost:8000/hello/VotreNom

### Documentation automatique

FastAPI génère automatiquement une documentation interactive :

1. Allez sur http://localhost:8000/docs
2. Explorez la documentation interactive (Swagger UI)
3. Testez vos endpoints directement depuis cette page

### Arrêt du serveur

Pour arrêter le serveur de développement :
- Appuyez sur `Ctrl + C` dans votre invite de commande

## Scripts d'automatisation

### Script de configuration automatique Windows

Créez un fichier `setup.bat` :

```batch
@echo off
echo Configuration de l'environnement FastAPI
echo ========================================

REM Vérifier Python
python --version
if errorlevel 1 (
    echo Erreur : Python n'est pas installé
    pause
    exit /b 1
)

REM Créer l'environnement virtuel
if not exist "venv" (
    echo Création de l'environnement virtuel...
    python -m venv venv
)

REM Activer l'environnement virtuel
call venv\Scripts\activate

REM Mettre à jour pip
python.exe -m pip install --upgrade pip

REM Installer les dépendances
pip install -r requirements.txt

echo Configuration terminée avec succès !
pause
```

### Script de configuration automatique macOS/Linux

Créez un fichier `setup.sh` :

```bash
#!/bin/bash

echo "Configuration de l'environnement FastAPI"
echo "========================================"

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "Erreur : Python3 n'est pas installé"
    exit 1
fi

# Créer l'environnement virtuel
if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Mettre à jour pip
python3 -m pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt

echo "Configuration terminée avec succès !"
```

Rendez le script exécutable :
```bash
chmod +x setup.sh
```

## Résolution des problèmes courants

### Erreur "Python n'est pas reconnu"

**Cause :** Python n'est pas dans le PATH système.

**Solution Windows :**
1. Recherchez "Variables d'environnement" dans le menu Démarrer
2. Cliquez sur "Modifier les variables d'environnement système"
3. Cliquez sur "Variables d'environnement"
4. Dans "Variables système", sélectionnez "Path" et cliquez sur "Modifier"
5. Ajoutez le chemin vers votre installation Python

### Erreur "pip n'est pas reconnu"

**Solution :** Utilisez `python -m pip` au lieu de `pip`

### Erreur de permissions

**Windows :** Exécutez l'invite de commande en tant qu'administrateur
**macOS/Linux :** Utilisez `sudo` devant la commande si nécessaire

### L'environnement virtuel ne s'active pas

**Vérifiez :**
1. Que vous êtes dans le bon dossier
2. Que le dossier `venv` existe
3. Que vous utilisez la bonne commande pour votre système

### Port 8000 déjà utilisé

**Solution :** Utilisez un autre port
```bash
uvicorn hello_api:app --reload --port 8001
```

## Fichiers créés à cette étape

À la fin de ce module, votre dossier projet devrait contenir :

```
projetsfastapi/
├── venv/                    # Environnement virtuel
├── requirements.txt         # Liste des dépendances  
├── test_installation.py     # Script de test
├── hello_api.py            # Première API de test
├── setup.bat               # Script Windows (optionnel)
└── setup.sh                # Script Unix/Linux (optionnel)
```

## Prochaines étapes

Dans le module suivant, vous découvrirez en détail la structure d'un projet FastAPI et créerez les fichiers de base de votre API CRUD.

Avant de continuer, assurez-vous que :
- Votre environnement virtuel s'active correctement
- Toutes les dépendances sont installées
- Votre première API fonctionne sur http://localhost:8000
