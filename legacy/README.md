# 📂 Dossier Legacy (Anciens Fichiers)

## ⚠️ FICHIERS DÉPRÉCIÉS

Ce dossier contient les **anciens fichiers** de l'architecture monolithique. 
**Ne pas utiliser** - ils sont conservés uniquement pour référence.

### Fichiers présents :
- `main.py` → Remplacé par `business/api/main.py`
- `models.py` → Remplacé par `database/models/models.py`
- `crud.py` → Remplacé par `database/repository/crud.py`
- `schemas.py` → Remplacé par `business/validation/schemas.py`
- `database.py` → Remplacé par `database/config/database.py`
- `safe_start.py` → Remplacé par `business/services/safe_start.py`
- `check_ports.py` → Remplacé par `infrastructure/diagnostics/check_ports.py`
- `run_gui.py` → Remplacé par `presentation/launchers/run_gui.py`
- `setup_gui.py` → Script de configuration déprécié

## 🗑️ Suppression Future

Ces fichiers peuvent être **supprimés** une fois que vous êtes sûr que la nouvelle architecture fonctionne parfaitement.

## ✅ Utilisez à la place :
```bash
python start_api.py    # Au lieu de l'ancien main.py
python start_gui.py    # Au lieu de l'ancien run_gui.py
python check_system.py # Au lieu de l'ancien check_ports.py
```
