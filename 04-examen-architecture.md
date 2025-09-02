# Examen - Architecture FastAPI CRUD

## Instructions

Cet examen évalue votre compréhension de l'architecture en couches du projet FastAPI CRUD.
Durée recommandée : 45 minutes
Total : 100 points

---

## PARTIE 1 - QUESTIONS À CHOIX MULTIPLES (40 points)

### Question 1 (5 points)
Combien de couches architecturales principales ce projet implémente-t-il ?

a) 2 couches (Frontend/Backend)
b) 3 couches (Présentation/Business/Données)
c) 4 couches (Présentation/Business/Database/Infrastructure)
d) 5 couches avec sécurité

### Question 2 (5 points)
Quel dossier contient la logique métier de l'application ?

a) presentation/
b) business/
c) database/
d) infrastructure/

### Question 3 (5 points)
Le fichier `api_client.py` se trouve dans quelle couche ?

a) Couche Business
b) Couche Database
c) Couche Présentation
d) Couche Infrastructure

### Question 4 (5 points)
Quelle technologie est utilisée pour l'interface graphique ?

a) Tkinter
b) PyQt5
c) PySide6
d) Kivy

### Question 5 (5 points)
Les opérations CRUD sont implémentées dans quel fichier ?

a) business/api/main.py
b) database/repository/crud.py
c) presentation/gui/main_window.py
d) infrastructure/diagnostics/check_ports.py

### Question 6 (5 points)
Quel script utilise-t-on pour démarrer l'API ?

a) python main.py
b) python run_api.py
c) python start_api.py
d) python launch_server.py

### Question 7 (5 points)
La validation des données est assurée par :

a) SQLAlchemy
b) FastAPI directement
c) Pydantic
d) PySide6

### Question 8 (5 points)
Le dossier `legacy/` contient :

a) Les fichiers de configuration
b) Les anciens fichiers dépréciés
c) Les tests unitaires
d) La documentation

---

## PARTIE 2 - QUESTIONS COURTES (30 points)

### Question 9 (10 points)
Expliquez le principe de séparation des responsabilités dans cette architecture. Donnez un exemple concret pour chaque couche.

**Réponse attendue :**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

### Question 10 (10 points)
Décrivez le flux de données lorsqu'un utilisateur crée un nouvel article via l'interface graphique.

**Réponse attendue :**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

### Question 11 (10 points)
Quels sont les avantages de cette architecture par rapport à une architecture monolithique ? Citez au moins 3 avantages.

**Réponse attendue :**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

---

## PARTIE 3 - ANALYSE DE CODE (20 points)

### Question 12 (20 points)
Analysez ce fragment de code et identifiez :
1. Dans quelle couche il devrait se trouver
2. Quelles dépendances il utilise
3. S'il respecte les principes architecturaux

```python
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from database.repository import crud
from business.validation import schemas
from database.config.database import get_db

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    return crud.create_user(db=db, user=user)
```

**Analyse :**

1. Couche appropriée :
_____________________________________________________________

2. Dépendances utilisées :
_____________________________________________________________
_____________________________________________________________

3. Respect des principes architecturaux (justifiez) :
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

---

## PARTIE 4 - EXERCICE PRATIQUE (10 points)

### Question 13 (10 points)
Vous devez ajouter une nouvelle fonctionnalité : "Statistiques des utilisateurs".
Cette fonctionnalité doit afficher le nombre total d'utilisateurs et d'articles.

Indiquez dans quels fichiers et dossiers vous ajouteriez du code, et justifiez vos choix :

**Plan d'implémentation :**

1. Couche Database :
_____________________________________________________________
_____________________________________________________________

2. Couche Business :
_____________________________________________________________
_____________________________________________________________

3. Couche Présentation :
_____________________________________________________________
_____________________________________________________________

4. Justification de l'organisation :
_____________________________________________________________
_____________________________________________________________

---

## CORRIGÉ

### PARTIE 1 - QCM
1. c) 4 couches
2. b) business/
3. c) Couche Présentation
4. c) PySide6
5. b) database/repository/crud.py
6. c) python start_api.py
7. c) Pydantic
8. b) Les anciens fichiers dépréciés

### PARTIE 2 - Questions courtes

**Question 9 :** La séparation des responsabilités divise l'application en couches spécialisées :
- Présentation : gestion de l'interface utilisateur (main_window.py)
- Business : logique métier et validation (schemas.py, main.py API)
- Database : persistance des données (crud.py, models.py)
- Infrastructure : services techniques (check_ports.py)

**Question 10 :** Flux de création d'article :
1. Utilisateur saisit données dans l'interface PySide6
2. Interface appelle api_client.py
3. Client HTTP envoie requête POST à FastAPI
4. FastAPI valide avec Pydantic schemas
5. API appelle crud.create_user_item()
6. CRUD utilise SQLAlchemy pour insérer en base
7. Réponse remonte la chaîne jusqu'à l'interface

**Question 11 :** Avantages :
- Maintenabilité : modifications isolées par couche
- Testabilité : tests unitaires par couche
- Évolutivité : remplacement d'une couche sans impact
- Collaboration : équipes spécialisées par domaine

### PARTIE 3 - Analyse de code

1. **Couche :** Business (couche API FastAPI)
2. **Dépendances :** FastAPI, SQLAlchemy, schemas Pydantic, CRUD repository
3. **Respect des principes :** Oui, le code respecte l'architecture :
   - Utilise la couche Database via crud
   - Valide avec la couche Business (schemas)
   - Ne contient pas de logique de présentation

### PARTIE 4 - Exercice pratique

1. **Database :** Ajouter fonction get_statistics() dans crud.py
2. **Business :** Ajouter endpoint /statistics dans main.py et schéma StatisticsResponse
3. **Présentation :** Ajouter onglet Statistiques dans main_window.py
4. **Justification :** Chaque couche garde sa responsabilité, communication respectée

---

## BARÈME DE NOTATION

- **90-100 points :** Excellente maîtrise de l'architecture
- **80-89 points :** Bonne compréhension avec quelques lacunes
- **70-79 points :** Compréhension correcte mais incomplète
- **60-69 points :** Compréhension de base, révisions nécessaires
- **Moins de 60 :** Révision complète recommandée

## CONSEILS POUR LA RÉVISION

1. Étudiez la structure des dossiers et leur rôle
2. Tracez le flux de données entre les couches
3. Analysez les imports entre les modules
4. Pratiquez avec les scripts de démarrage
5. Comprenez les responsabilités de chaque couche
