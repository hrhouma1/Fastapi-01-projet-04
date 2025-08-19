# URLs de test - API CRUD FastAPI

## URLs principales d'accès

### Interface principale
```
http://localhost:8000/                    # Page d'accueil de l'API
http://localhost:8001/                    # Si le port 8000 est occupé
```

### Documentation interactive
```
http://localhost:8000/docs                # Documentation Swagger UI (interface de test)
http://localhost:8000/redoc               # Documentation ReDoc (alternative)
http://localhost:8001/docs                # Si port alternatif
http://localhost:8001/redoc               # Si port alternatif
```

### Vérification de l'état
```
http://localhost:8000/health              # Vérification que l'API fonctionne
```

## URLs des endpoints UTILISATEURS

### Créer un utilisateur (POST)
**URL :** `http://localhost:8000/users/`
**Méthode :** POST
**Test via navigateur :** Non (nécessite un outil POST)
**Test via Swagger :** http://localhost:8000/docs - section "Users"

### Lister tous les utilisateurs (GET)
```
http://localhost:8000/users/              # Tous les utilisateurs
http://localhost:8000/users/?skip=0&limit=10   # Avec pagination
http://localhost:8000/users/?skip=5&limit=5    # Ignorer 5 premiers, prendre 5 suivants
```

### Récupérer un utilisateur spécifique (GET)
```
http://localhost:8000/users/1             # Alice Martin (utilisateur avec 3 articles)
http://localhost:8000/users/2             # Bob Wilson (utilisateur avec 2 articles)
http://localhost:8000/users/3             # Claire Dubois (utilisateur avec 3 articles)
http://localhost:8000/users/4             # David Bernard (utilisateur inactif, 1 article)
http://localhost:8000/users/5             # Emma Petit (utilisateur avec 4 articles)
http://localhost:8000/users/999           # Test erreur 404 (utilisateur inexistant)
```

### Récupérer les articles d'un utilisateur (GET)
```
http://localhost:8000/users/1/items/      # Articles d'Alice Martin (iPhone, MacBook, AirPods)
http://localhost:8000/users/2/items/      # Articles de Bob Wilson (vélo électrique, PS5)
http://localhost:8000/users/3/items/      # Articles de Claire Dubois (Canon EOS, objectif, drone)
http://localhost:8000/users/4/items/      # Articles de David Bernard (livre Python)
http://localhost:8000/users/5/items/      # Articles d'Emma Petit (bureau, chaise, écran, clavier)
http://localhost:8000/users/1/items/?skip=0&limit=2  # Premiers 2 articles d'Alice
http://localhost:8000/users/5/items/?skip=2&limit=2  # Articles 3-4 d'Emma
http://localhost:8000/users/999/items/    # Test erreur 404 (utilisateur inexistant)
```

### Modifier un utilisateur (PUT)
**URL :** `http://localhost:8000/users/1`
**Méthode :** PUT
**Test via navigateur :** Non (nécessite un outil PUT)
**Test via Swagger :** http://localhost:8000/docs - section "Users"

### Supprimer un utilisateur (DELETE)
**URL :** `http://localhost:8000/users/1`
**Méthode :** DELETE
**Test via navigateur :** Non (nécessite un outil DELETE)
**Test via Swagger :** http://localhost:8000/docs - section "Users"

## URLs des endpoints ARTICLES

### Créer un article (POST)
**URL :** `http://localhost:8000/users/1/items/`
**Méthode :** POST
**Test via navigateur :** Non (nécessite un outil POST)
**Test via Swagger :** http://localhost:8000/docs - section "Items"

### Lister tous les articles (GET)
```
http://localhost:8000/items/              # Tous les articles
http://localhost:8000/items/?skip=0&limit=10     # Avec pagination
http://localhost:8000/items/?available_only=true # Seulement les articles disponibles
```

### Récupérer un article spécifique (GET)
```
http://localhost:8000/items/1             # iPhone 15 Pro (Alice Martin)
http://localhost:8000/items/2             # MacBook Pro 16 pouces (Alice Martin)
http://localhost:8000/items/3             # AirPods Pro 2ème génération (Alice Martin)
http://localhost:8000/items/4             # Vélo électrique VTT (Bob Wilson)
http://localhost:8000/items/5             # Console PlayStation 5 (Bob Wilson)
http://localhost:8000/items/6             # Appareil photo Canon EOS R6 (Claire Dubois)
http://localhost:8000/items/7             # Objectif Canon RF 24-70mm (Claire Dubois)
http://localhost:8000/items/8             # Drone DJI Air 2S (Claire Dubois)
http://localhost:8000/items/9             # Livre Python pour débutants (David Bernard)
http://localhost:8000/items/10            # Chaise de bureau ergonomique (Emma Petit)
http://localhost:8000/items/11            # Bureau assis-debout électrique (Emma Petit)
http://localhost:8000/items/12            # Écran 4K 27 pouces (Emma Petit)
http://localhost:8000/items/13            # Clavier mécanique (Emma Petit)
http://localhost:8000/items/999           # Test erreur 404 (article inexistant)
```

### Modifier un article (PUT)
**URL :** `http://localhost:8000/items/1`
**Méthode :** PUT
**Test via navigateur :** Non (nécessite un outil PUT)
**Test via Swagger :** http://localhost:8000/docs - section "Items"

### Supprimer un article (DELETE)
**URL :** `http://localhost:8000/items/1`
**Méthode :** DELETE
**Test via navigateur :** Non (nécessite un outil DELETE)
**Test via Swagger :** http://localhost:8000/docs - section "Items"

## URLs de recherche

### Rechercher des articles
```
http://localhost:8000/search/items?q=iPhone        # Rechercher "iPhone" (iPhone 15 Pro)
http://localhost:8000/search/items?q=MacBook       # Rechercher "MacBook" (MacBook Pro)
http://localhost:8000/search/items?q=vélo          # Rechercher "vélo" (vélo électrique)
http://localhost:8000/search/items?q=Canon         # Rechercher "Canon" (appareil photo + objectif)
http://localhost:8000/search/items?q=bureau        # Rechercher "bureau" (chaise + bureau)
http://localhost:8000/search/items?q=Python        # Rechercher "Python" (livre)
http://localhost:8000/search/items?q=écran         # Rechercher "écran" (écran 4K)
http://localhost:8000/search/items?q=Pro           # Rechercher "Pro" (iPhone Pro, MacBook Pro, AirPods Pro)
http://localhost:8000/search/items?q=électrique    # Rechercher "électrique" (vélo + bureau)
http://localhost:8000/search/items?q=Apple         # Rechercher "Apple" (plusieurs articles)
http://localhost:8000/search/items?q=console       # Rechercher "console" (PlayStation)
http://localhost:8000/search/items?q=drone         # Rechercher "drone" (DJI Air 2S)
http://localhost:8000/search/items?q=test&limit=5  # Avec limitation des résultats
http://localhost:8000/search/items?q=a             # Test recherche trop courte (erreur)
```

## URLs de débogage (si activées)

### Informations de débogage
```
http://localhost:8000/debug/info          # Informations système et statistiques
http://localhost:8000/debug/logs          # Logs récents de l'API
```

### Métriques
```
http://localhost:8000/metrics             # Statistiques de l'API
```

## URLs de test d'erreurs

### Tests d'erreurs 404 (ressource non trouvée)
```
http://localhost:8000/users/999           # Utilisateur inexistant
http://localhost:8000/users/0             # Utilisateur ID 0 (invalide)
http://localhost:8000/items/999           # Article inexistant
http://localhost:8000/items/0             # Article ID 0 (invalide)
http://localhost:8000/users/999/items/    # Articles d'un utilisateur inexistant
http://localhost:8000/users/100/items/    # Articles d'un autre utilisateur inexistant
```

### Tests d'erreurs 400 (données invalides)
```
http://localhost:8000/users/-1            # ID utilisateur négatif
http://localhost:8000/users/abc           # ID utilisateur non numérique
http://localhost:8000/items/-1            # ID article négatif
http://localhost:8000/items/abc           # ID article non numérique
http://localhost:8000/search/items?q=a    # Recherche trop courte (1 caractère)
http://localhost:8000/search/items?q=     # Recherche vide
http://localhost:8000/users/?skip=-1      # Pagination skip négatif
http://localhost:8000/users/?limit=-1     # Pagination limit négatif
http://localhost:8000/users/?limit=1000   # Pagination limit trop élevé
```

### Tests d'erreurs 422 (données de création invalides - via Swagger)
Ces URLs nécessitent des outils POST, testez via http://localhost:8000/docs :
- POST /users/ avec email invalide (sans @)
- POST /users/ avec nom vide
- POST /users/1/items/ avec prix négatif
- POST /users/1/items/ avec titre vide

## Comment tester ces URLs

### 1. URLs testables directement dans le navigateur (méthode GET)
Copiez-collez ces URLs dans votre navigateur :
- Toutes les URLs marquées GET
- http://localhost:8000/
- http://localhost:8000/docs
- http://localhost:8000/users/
- http://localhost:8000/items/
- etc.

### 2. URLs nécessitant des outils spéciaux (POST, PUT, DELETE)
Utilisez l'une de ces méthodes :

**A) Documentation Swagger (plus simple)**
1. Allez sur http://localhost:8000/docs
2. Cliquez sur l'endpoint que vous voulez tester
3. Cliquez sur "Try it out"
4. Remplissez les données
5. Cliquez "Execute"

**B) Extension VS Code REST Client**
Utilisez le fichier `api_tests.http` fourni

**C) Scripts Python**
Exécutez `python test_coherence.py` ou `python exemple_utilisation.py`

## Séquence de test recommandée

### Étape 1 : Vérifier que l'API fonctionne
```
http://localhost:8000/                    # Doit afficher message de bienvenue
http://localhost:8000/health              # Doit retourner "status": "healthy"
```

### Étape 2A : Vérifier l'état initial (base vide)
```
http://localhost:8000/users/              # Doit être vide [] (si pas de seed data)
http://localhost:8000/items/              # Doit être vide [] (si pas de seed data)
```

### Étape 2B : Ou ajouter des données d'exemple (recommandé)
Exécutez `python seed_data.py add` puis testez :
```
http://localhost:8000/users/              # 5 utilisateurs avec données réalistes
http://localhost:8000/items/              # 13 articles avec descriptions détaillées
```

### Étape 3 : Créer des données via Swagger
1. Allez sur http://localhost:8000/docs
2. Créez un utilisateur avec POST /users/
3. Créez des articles avec POST /users/{id}/items/

### Étape 4 : Vérifier les données créées
```
http://localhost:8000/users/              # 5 utilisateurs (Alice, Bob, Claire, David, Emma)
http://localhost:8000/users/1             # Alice Martin avec iPhone, MacBook, AirPods
http://localhost:8000/users/5             # Emma Petit avec 4 articles de bureau
http://localhost:8000/items/              # 13 articles avec prix et descriptions
http://localhost:8000/items/1             # iPhone 15 Pro - 1200€
http://localhost:8000/items/4             # Vélo électrique - 1800€
```

### Étape 5 : Tester les recherches avec données réelles
```
http://localhost:8000/search/items?q=iPhone    # Trouve iPhone 15 Pro
http://localhost:8000/search/items?q=Canon     # Trouve appareil photo + objectif
http://localhost:8000/search/items?q=bureau    # Trouve chaise + bureau
http://localhost:8000/search/items?q=Pro       # Trouve iPhone Pro, MacBook Pro, AirPods Pro
```

## URLs de ports alternatifs

Si le port 8000 est occupé, l'API se lance automatiquement sur un port alternatif :

```
http://localhost:8001/                    # Port alternatif 8001
http://localhost:8002/                    # Port alternatif 8002
http://localhost:8003/                    # etc.
```

Remplacez `8000` par le port affiché dans votre terminal quand vous lancez l'API.

## URLs avec différents paramètres de filtre

### Pagination avancée
```
http://localhost:8000/users/?skip=0&limit=2        # Premiers 2 utilisateurs
http://localhost:8000/users/?skip=2&limit=2        # Utilisateurs 3-4
http://localhost:8000/users/?skip=0&limit=1        # Un seul utilisateur
http://localhost:8000/items/?skip=0&limit=5        # 5 premiers articles
http://localhost:8000/items/?skip=10&limit=3       # Articles 11-13
```

### Filtres de disponibilité
```
http://localhost:8000/items/?available_only=true   # Seulement articles disponibles (10 articles)
http://localhost:8000/items/?available_only=false  # Tous les articles (13 articles)
```

### Recherches avancées avec limites
```
http://localhost:8000/search/items?q=Pro&limit=1   # 1 seul résultat pour "Pro"
http://localhost:8000/search/items?q=Pro&limit=2   # 2 premiers résultats pour "Pro"
http://localhost:8000/search/items?q=Pro&limit=10  # Maximum 10 résultats
```

## URLs avec différents formats de réponse

### Format JSON (par défaut)
```
http://localhost:8000/users/              # Retourne du JSON
http://localhost:8000/items/              # Retourne du JSON avec tous les champs
```

### Headers personnalisés
L'API ajoute automatiquement des headers comme `X-Process-Time` pour indiquer le temps de traitement.

### Réponses avec données utilisateur complètes
```
http://localhost:8000/users/1             # Utilisateur avec ses articles inclus
http://localhost:8000/users/2             # Autre utilisateur avec relation articles
```

## URLs pour les tests de performance

### Tests de charge basiques
```
http://localhost:8000/                    # Page simple pour test de rapidité
http://localhost:8000/health              # Endpoint très rapide
http://localhost:8000/users/              # Test avec base de données
```

Utilisez `python test_performance.py` pour des tests automatisés.

## URLs COMPLÈTES avec données d'exemple (après seed_data.py)

### URLs de recherche thématique
```
http://localhost:8000/search/items?q=Apple         # Articles Apple (iPhone, MacBook, AirPods)
http://localhost:8000/search/items?q=électrique    # Articles électriques (vélo, bureau)
http://localhost:8000/search/items?q=photo         # Matériel photo (Canon, objectif)
http://localhost:8000/search/items?q=gaming        # Gaming (PlayStation, écran)
http://localhost:8000/search/items?q=bureau        # Matériel bureau (4 articles Emma)
http://localhost:8000/search/items?q=1000          # Articles > 1000€ (par description)
http://localhost:8000/search/items?q=Pro           # Articles "Pro" (iPhone, MacBook, AirPods)
```

### URLs par gammes de prix (recherche dans description)
```
http://localhost:8000/search/items?q=35             # Articles à 35€ (livre Python)
http://localhost:8000/search/items?q=250           # Articles à 250€ (AirPods)
http://localhost:8000/search/items?q=1200          # Articles à 1200€ (iPhone)
http://localhost:8000/search/items?q=2800          # Articles à 2800€ (MacBook)
```

### URLs de test de performances
```
http://localhost:8000/users/?limit=100             # Test pagination importante
http://localhost:8000/items/?limit=100             # Test pagination articles
http://localhost:8000/search/items?q=e&limit=50    # Recherche large avec limite
```

### URLs de test d'utilisation réelle
```
http://localhost:8000/users/1/items/?limit=2       # Alice : 2 premiers articles
http://localhost:8000/users/5/items/?skip=2        # Emma : articles 3-4
http://localhost:8000/users/3/items/?available_only=true  # Claire : articles disponibles
```

## Résumé des URLs principales à retenir

| URL | Description | Testable au navigateur | Données après seed |
|-----|-------------|----------------------|-------------------|
| `http://localhost:8000/` | Page d'accueil | ✅ | Message de bienvenue |
| `http://localhost:8000/docs` | Documentation interactive | ✅ | Interface Swagger complète |
| `http://localhost:8000/health` | État de l'API | ✅ | Status: healthy |
| `http://localhost:8000/users/` | Liste des utilisateurs | ✅ | 5 utilisateurs réalistes |
| `http://localhost:8000/items/` | Liste des articles | ✅ | 13 articles variés |
| `http://localhost:8000/users/1` | Alice Martin | ✅ | 3 articles Apple |
| `http://localhost:8000/users/5` | Emma Petit | ✅ | 4 articles bureau |
| `http://localhost:8000/items/1` | iPhone 15 Pro | ✅ | 1200€, disponible |
| `http://localhost:8000/items/4` | Vélo électrique | ✅ | 1800€, disponible |
| `http://localhost:8000/search/items?q=iPhone` | Recherche iPhone | ✅ | 1 résultat : iPhone 15 Pro |
| `http://localhost:8000/search/items?q=Canon` | Recherche Canon | ✅ | 2 résultats : appareil + objectif |
| `http://localhost:8000/search/items?q=Pro` | Recherche "Pro" | ✅ | 3 résultats : iPhone, MacBook, AirPods |

## TOUTES les URLs de l'API (liste exhaustive)

### Endpoints CRUD complets
**UTILISATEURS (Users) :**
```
GET    http://localhost:8000/users/              # Lister utilisateurs
POST   http://localhost:8000/users/              # Créer utilisateur
GET    http://localhost:8000/users/1             # Lire utilisateur 1
PUT    http://localhost:8000/users/1             # Modifier utilisateur 1
DELETE http://localhost:8000/users/1             # Supprimer utilisateur 1
GET    http://localhost:8000/users/1/items/      # Articles de l'utilisateur 1
POST   http://localhost:8000/users/1/items/      # Créer article pour utilisateur 1
```

**ARTICLES (Items) :**
```
GET    http://localhost:8000/items/              # Lister articles
GET    http://localhost:8000/items/1             # Lire article 1
PUT    http://localhost:8000/items/1             # Modifier article 1
DELETE http://localhost:8000/items/1             # Supprimer article 1
```

**RECHERCHE :**
```
GET    http://localhost:8000/search/items?q=X    # Rechercher articles
```

**SYSTÈME :**
```
GET    http://localhost:8000/                    # Page d'accueil
GET    http://localhost:8000/health              # État de santé
GET    http://localhost:8000/docs                # Documentation Swagger
GET    http://localhost:8000/redoc               # Documentation ReDoc
GET    http://localhost:8000/openapi.json        # Schéma OpenAPI
```

### Total : 16 endpoints différents + variations de paramètres

Pour tous les autres tests (POST, PUT, DELETE), utilisez la documentation Swagger sur http://localhost:8000/docs

> **💡 Conseil pour débutants :** Commencez par `python seed_data.py add` puis testez toutes les URLs GET dans votre navigateur !
