# Questions d'évaluation et exercices

## 30 Questions progressives

### Niveau 1 : Concepts de base (Questions 1-10)

**Question 1**
Quelle est la différence entre FastAPI et Flask ? Donnez 3 avantages de FastAPI.

**Question 2**
Que signifie l'acronyme CRUD et quelles sont les méthodes HTTP correspondantes ?

**Question 3**
Dans SQLAlchemy, quelle est la différence entre `Session` et `Engine` ?

**Question 4**
Que fait le décorateur `@app.get("/users/", response_model=List[User])` dans FastAPI ?

**Question 5**
Pourquoi utilise-t-on `Depends(get_db)` dans les fonctions FastAPI ?

**Question 6**
Dans Pydantic, à quoi sert `class Config: orm_mode = True` ?

**Question 7**
Quelle est la différence entre `Column(String, nullable=False)` et `Column(String, default="")` ?

**Question 8**
Que fait `db.commit()` et pourquoi est-il nécessaire ?

**Question 9**
Dans PySide6, quelle est la différence entre un signal et un slot ?

**Question 10**
Pourquoi sépare-t-on les schémas Pydantic (UserCreate, UserUpdate, User) ?

### Niveau 2 : Architecture et bonnes pratiques (Questions 11-20)

**Question 11**
Expliquez l'architecture 3-tiers de notre projet et les responsabilités de chaque couche.

**Question 12**
Que se passe-t-il si on oublie de faire `db.refresh(db_user)` après un `db.commit()` ?

**Question 13**
Pourquoi utilise-t-on `relationship("Item", back_populates="owner")` plutôt qu'une requête directe ?

**Question 14**
Dans FastAPI, quelle est la différence entre lever une `HTTPException` et retourner une erreur ?

**Question 15**
Comment optimiser une requête SQLAlchemy qui fait du N+1 queries ?

**Question 16**
Expliquez le pattern Repository utilisé dans `crud.py`. Quels sont ses avantages ?

**Question 17**
Pourquoi utilise-t-on `yield db` plutôt que `return db` dans `get_db()` ?

**Question 18**
Comment gérer les transactions en cas d'opération sur plusieurs tables liées ?

**Question 19**
Dans l'interface PySide6, comment synchroniser les données entre onglets après une modification ?

**Question 20**
Que se passe-t-il si deux utilisateurs modifient le même enregistrement simultanément ?

### Niveau 3 : Problèmes complexes (Questions 21-30)

**Question 21**
Implémentez une fonction de recherche full-text qui cherche dans plusieurs champs avec pondération.

**Question 22**
Comment implémenter une pagination cursor-based plutôt qu'offset-based ? Avantages/inconvénients ?

**Question 23**
Créez un système de cache Redis pour les requêtes fréquentes. Quand invalider le cache ?

**Question 24**
Implémentez un middleware de limitation de débit (rate limiting) pour l'API.

**Question 25**
Comment gérer l'authentification JWT dans FastAPI avec refresh tokens ?

**Question 26**
Créez un système d'upload de fichiers avec validation et stockage sécurisé.

**Question 27**
Implémentez un système de logs structurés avec corrélation des requêtes.

**Question 28**
Comment migrer de SQLite vers PostgreSQL sans perte de données ?

**Question 29**
Créez un système de notifications en temps réel entre l'API et l'interface graphique.

**Question 30**
Implémentez des tests d'intégration complets qui testent l'API et l'interface ensemble.

## Exercices pratiques

### Exercice 1 : Extension du modèle

Ajoutez une entité `Category` avec :
- Relation many-to-many avec `Item`
- Endpoints CRUD complets
- Interface graphique pour gérer les catégories
- Recherche par catégorie

### Exercice 2 : Système d'authentification

Implémentez :
- Modèle `User` avec mot de passe hashé
- Endpoints login/logout avec JWT
- Middleware d'authentification
- Interface de connexion dans PySide6

### Exercice 3 : API de statistiques

Créez des endpoints pour :
- Nombre d'utilisateurs actifs par mois
- Articles les plus chers par catégorie
- Utilisateurs les plus prolifiques
- Graphiques dans l'interface PySide6

### Exercice 4 : Système de notification

Implémentez :
- Modèle `Notification` 
- WebSocket pour notifications temps réel
- Interface PySide6 avec zone de notifications
- Système de marquage lu/non-lu

### Exercice 5 : Import/Export de données

Créez :
- Import CSV/Excel avec validation
- Export données vers différents formats
- Interface PySide6 pour sélection et progression
- Gestion des erreurs d'import

## Solutions et corrections

### Solution Question 1
FastAPI vs Flask :
1. **Performance** : FastAPI est plus rapide grâce à Starlette et uvloop
2. **Validation** : Validation automatique avec Pydantic
3. **Documentation** : Génération automatique OpenAPI/Swagger
4. **Type hints** : Support natif des annotations Python
5. **Async** : Support natif de l'asynchrone

### Solution Question 15 - N+1 Queries

```python
# Problème N+1
users = db.query(User).all()  # 1 requête
for user in users:
    print(user.items)  # N requêtes supplémentaires

# Solution avec joinedload
from sqlalchemy.orm import joinedload

users = db.query(User).options(joinedload(User.items)).all()
for user in users:
    print(user.items)  # Pas de requête supplémentaire
```

### Solution Question 21 - Recherche full-text

```python
from sqlalchemy import func, case

def advanced_search(db: Session, query: str, limit: int = 50):
    search_pattern = f"%{query}%"
    
    return db.query(
        Item,
        (
            case([
                (Item.title.ilike(search_pattern), 10),
                (Item.description.ilike(search_pattern), 5),
            ], else_=1)
        ).label('relevance')
    ).filter(
        or_(
            Item.title.ilike(search_pattern),
            Item.description.ilike(search_pattern)
        )
    ).order_by('relevance DESC').limit(limit).all()
```

## Projet final

### Objectif
Créer une application de gestion de bibliothèque avec :

### Fonctionnalités requises
1. **Gestion des livres** : CRUD complet
2. **Gestion des auteurs** : Relations many-to-many
3. **Système d'emprunt** : Suivi des prêts/retours
4. **Recherche avancée** : Par titre, auteur, genre, disponibilité
5. **Statistiques** : Livres populaires, retards, etc.
6. **Interface graphique** : Moderne et intuitive

### Architecture technique
- FastAPI avec authentification JWT
- PostgreSQL avec migrations Alembic
- PySide6 avec threading pour l'interface
- Tests complets (unitaires et intégration)
- Documentation API complète
- Logs structurés et monitoring

### Critères d'évaluation
1. **Fonctionnalité** (30%) : Toutes les fonctionnalités fonctionnent
2. **Architecture** (25%) : Code bien structuré et maintenable
3. **Interface** (20%) : Ergonomie et design
4. **Performance** (15%) : Optimisations et bonnes pratiques
5. **Tests et documentation** (10%) : Couverture et qualité

### Temps estimé
40-60 heures pour un développeur intermédiaire.

Cette évaluation complète teste tous les aspects du développement d'applications FastAPI avec interface graphique.
