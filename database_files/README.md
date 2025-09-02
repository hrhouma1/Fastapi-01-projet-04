# 💾 Dossier Database Files

## Fichiers de Base de Données

Ce dossier contient les **fichiers de base de données** générés par l'application.

### Fichiers présents :
- `test.db` - Base de données SQLite principale

## ⚠️ Important

- Ce dossier est **automatiquement créé** au démarrage de l'API
- Les fichiers `.db` sont **ignorés par Git** (voir `.gitignore`)
- **Ne pas versionner** les fichiers de base de données
- Pour réinitialiser : supprimez `test.db` et redémarrez l'API

## 🔄 Régénération

Si vous supprimez `test.db`, il sera automatiquement recréé au prochain démarrage :

```bash
python start_api.py
```
