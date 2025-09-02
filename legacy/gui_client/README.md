# Interface Graphique FastAPI CRUD

Interface moderne développée avec PySide6 pour interagir avec l'API FastAPI CRUD.

## Démarrage rapide

### 1. Installation
```bash
# Installer les dépendances
pip install -r requirements.txt
```

### 2. Lancement
```bash
# Démarrer l'API FastAPI (Terminal 1)
python safe_start.py

# Lancer l'interface graphique (Terminal 2)  
python run_gui.py
```

### 3. Utilisation
- L'interface se connecte automatiquement à `http://localhost:8000`
- Indicateur vert = API connectée ✅
- Indicateur rouge = API déconnectée ❌

## Fonctionnalités

### Onglet Utilisateurs
- ➕ Créer des utilisateurs
- 📋 Visualiser la liste complète
- 🗑️ Supprimer des utilisateurs

### Onglet Articles  
- ➕ Créer des articles
- 🔍 Rechercher par mots-clés
- 📋 Visualiser avec prix formatés
- 🗑️ Supprimer individuellement

## Architecture

```
gui_client/
├── __init__.py          # Package principal
├── api_client.py        # Communication avec API
├── main_window.py       # Interface utilisateur
└── README.md           # Ce fichier

run_gui.py              # Script de lancement
test_gui_integration.py # Tests automatiques
```

## Test de l'intégration
```bash
# Tester la communication API ↔ GUI
python test_gui_integration.py
```

## Dépendances
- **PySide6** : Interface graphique Qt
- **requests** : Communication HTTP
- **FastAPI** : API backend (doit être démarrée)

## Documentation complète
Consultez `documentation1/04-interface-graphique.md` pour le guide détaillé.

---
**💡 Astuce :** Utilisez `python seed_data.py add` pour avoir des données de test immédiatement !
