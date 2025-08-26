# Guide d'utilisation de l'application FastAPI CRUD

## Vue d'ensemble

Ce guide explique comment utiliser l'application FastAPI CRUD complète, comprenant :
- Une API REST pour la gestion des données
- Une interface graphique moderne
- Une base de données intégrée
- Des fonctionnalités de recherche avancées

## Installation et démarrage

### Prérequis système
- Python 3.8 ou version supérieure
- 4 Go de RAM minimum
- 1 Go d'espace disque libre
- Connexion Internet (pour l'installation des dépendances)

### Installation rapide

```bash
# 1. Cloner ou télécharger le projet
cd projetsfastapi

# 2. Créer l'environnement virtuel
python -m venv venv

# 3. Activer l'environnement
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Installation GUI (optionnel)
python setup_gui.py
```

### Démarrage de l'application

#### Méthode 1 : Démarrage automatique (recommandé)
```bash
python safe_start.py
```

#### Méthode 2 : Démarrage manuel
```bash
python main.py
```

#### Méthode 3 : Avec uvicorn
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Vérification du fonctionnement

Une fois l'API démarrée, vous devriez voir :
```
Démarrage sécurisé de l'API FastAPI CRUD
Dépendances FastAPI disponibles
Port 8000 disponible
Démarrage de l'API sur http://0.0.0.0:8000
Documentation : http://localhost:8000/docs
```

## Utilisation de l'API REST

### Accès à la documentation

#### Documentation interactive Swagger
- URL : http://localhost:8000/docs
- Permet de tester toutes les fonctionnalités
- Interface graphique intuitive
- Exemples de requêtes automatiques

#### Documentation ReDoc
- URL : http://localhost:8000/redoc
- Présentation alternative de la documentation
- Format plus adapté à la lecture

### Endpoints principaux

#### Gestion des utilisateurs

**Créer un utilisateur**
```http
POST /users/
Content-Type: application/json

{
    "email": "utilisateur@exemple.com",
    "nom": "Dupont",
    "prenom": "Jean",
    "is_active": true
}
```

**Lister les utilisateurs**
```http
GET /users/?skip=0&limit=50
```

**Récupérer un utilisateur**
```http
GET /users/1
```

**Modifier un utilisateur**
```http
PUT /users/1
Content-Type: application/json

{
    "nom": "Martin",
    "is_active": false
}
```

**Supprimer un utilisateur**
```http
DELETE /users/1
```

#### Gestion des articles

**Créer un article pour un utilisateur**
```http
POST /users/1/items/
Content-Type: application/json

{
    "title": "MacBook Pro 16 pouces",
    "description": "Ordinateur portable Apple dernière génération",
    "price": 2499.99,
    "is_available": true
}
```

**Lister tous les articles**
```http
GET /items/?skip=0&limit=50
```

**Rechercher des articles**
```http
GET /search/items?q=macbook&limit=20
```

### Codes de réponse HTTP

- **200 OK** : Requête réussie
- **201 Created** : Ressource créée avec succès
- **204 No Content** : Suppression réussie
- **400 Bad Request** : Données invalides
- **404 Not Found** : Ressource non trouvée
- **422 Unprocessable Entity** : Erreur de validation

### Exemples avec curl

```bash
# Créer un utilisateur
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
         "email": "test@exemple.com",
         "nom": "Test",
         "prenom": "Utilisateur",
         "is_active": true
     }'

# Lister les utilisateurs
curl "http://localhost:8000/users/"

# Créer un article
curl -X POST "http://localhost:8000/users/1/items/" \
     -H "Content-Type: application/json" \
     -d '{
         "title": "Article test",
         "description": "Description de test",
         "price": 99.99,
         "is_available": true
     }'

# Rechercher des articles
curl "http://localhost:8000/search/items?q=test&limit=10"
```

## Utilisation de l'interface graphique

### Lancement de l'interface

```bash
python run_gui.py
```

### Vue d'ensemble de l'interface

L'interface se compose de deux onglets principaux :
- **Utilisateurs** : Gestion des utilisateurs
- **Articles** : Gestion des articles

### Onglet Utilisateurs

#### Créer un utilisateur
1. Remplir le formulaire dans la section "Créer un utilisateur"
2. **Email** : Adresse email unique (obligatoire)
3. **Nom** : Nom de famille (obligatoire)
4. **Prénom** : Prénom (obligatoire)
5. **Statut** : Cocher "Utilisateur actif" si nécessaire
6. Cliquer sur "Créer l'utilisateur"

#### Consulter les utilisateurs
- Le tableau affiche tous les utilisateurs existants
- Colonnes : ID, Email, Nom, Prénom, Statut
- Clic sur "Actualiser" pour rafraîchir les données

#### Modifier un utilisateur
1. Sélectionner une ligne dans le tableau
2. Cliquer sur "Modifier l'utilisateur sélectionné"
3. Modifier les champs souhaités
4. Valider les modifications

#### Supprimer un utilisateur
1. Sélectionner une ligne dans le tableau
2. Cliquer sur "Supprimer l'utilisateur sélectionné"
3. Confirmer la suppression

### Onglet Articles

#### Créer un article
1. **Propriétaire** : Sélectionner un utilisateur dans la liste
2. **Titre** : Nom de l'article (obligatoire)
3. **Description** : Description détaillée (optionnel)
4. **Prix** : Prix en euros (obligatoire)
5. **Statut** : Cocher "Article disponible" si en vente
6. Cliquer sur "Créer l'article"

#### Rechercher des articles
1. Saisir un terme de recherche (minimum 2 caractères)
2. Cliquer sur "Rechercher"
3. Les résultats s'affichent dans le tableau
4. Cliquer sur "Effacer" pour revenir à la liste complète

#### Consulter les articles
- Le tableau affiche tous les articles
- Colonnes : ID, Titre, Description, Prix, Disponible, Propriétaire
- Clic sur "Actualiser" pour rafraîchir

#### Gérer la synchronisation
- Bouton "↻" à côté de la liste des propriétaires pour rafraîchir
- Les données se synchronisent automatiquement après création/suppression

### Messages et notifications

#### Types de messages
- **Succès** (vert) : Opération réussie
- **Avertissement** (jaune) : Attention requise
- **Erreur** (rouge) : Échec de l'opération

#### Gestion des erreurs courantes
- **"Email déjà existant"** : Choisir une autre adresse email
- **"Utilisateur non trouvé"** : Actualiser la liste des propriétaires
- **"API non accessible"** : Vérifier que l'API est démarrée
- **"Champ obligatoire"** : Remplir tous les champs requis

## Données d'exemple

### Ajout de données de test

```bash
# Méthode 1 : Script automatique
python seed_data.py add

# Méthode 2 : Interface graphique Swagger
# Aller sur http://localhost:8000/docs
# Utiliser les endpoints POST pour créer des données
```

### Données créées automatiquement

**Utilisateurs d'exemple :**
- Jean Dupont (jean.dupont@exemple.com)
- Marie Martin (marie.martin@exemple.com)
- Pierre Durand (pierre.durand@exemple.com)
- Sophie Bernard (sophie.bernard@exemple.com)
- Lucas Moreau (lucas.moreau@exemple.com)

**Articles d'exemple :**
- iPhone 15 Pro (1299.99 €)
- MacBook Pro 16 pouces (2499.99 €)
- iPad Air (699.99 €)
- Chaise de bureau ergonomique (299.99 €)
- Machine à café Nespresso (199.99 €)

## Tests et validation

### Tests manuels recommandés

#### Test complet utilisateur
1. Créer un nouvel utilisateur
2. Vérifier qu'il apparaît dans la liste
3. Modifier ses informations
4. Créer un article pour cet utilisateur
5. Rechercher l'article créé
6. Supprimer l'utilisateur
7. Vérifier que ses articles sont supprimés

#### Test de recherche
1. Rechercher "iPhone" → doit trouver les articles Apple
2. Rechercher "bureau" → doit trouver les meubles
3. Rechercher "xyz" → doit retourner "Aucun résultat"
4. Rechercher "i" → doit afficher erreur "2 caractères minimum"

#### Test de validation
1. Tenter de créer un utilisateur sans email
2. Tenter de créer un utilisateur avec email invalide
3. Tenter de créer un article avec prix négatif
4. Tenter de créer un article sans titre

### Vérification des performances

L'application doit répondre dans les délais suivants :
- **Création d'utilisateur** : < 200ms
- **Liste des utilisateurs** : < 100ms
- **Recherche d'articles** : < 300ms
- **Chargement interface** : < 2 secondes

## Résolution des problèmes

### Problèmes courants et solutions

#### L'API ne démarre pas

**Symptômes :** Erreur au lancement de `python safe_start.py`

**Solutions :**
1. Vérifier que le port 8000 est libre :
   ```bash
   python check_ports.py
   ```

2. Vérifier les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Vérifier la version Python :
   ```bash
   python --version  # Doit être 3.8+
   ```

#### L'interface graphique ne se lance pas

**Symptômes :** Erreur au lancement de `python run_gui.py`

**Solutions :**
1. Installer les dépendances GUI :
   ```bash
   python setup_gui.py
   ```

2. Vérifier PySide6 :
   ```bash
   pip install PySide6 requests
   ```

#### Erreur "API non accessible"

**Symptômes :** Interface affiche des erreurs de connexion

**Solutions :**
1. Vérifier que l'API est démarrée
2. Tester l'URL : http://localhost:8000
3. Vérifier le firewall/antivirus
4. Redémarrer l'API et l'interface

#### Base de données corrompue

**Symptômes :** Erreurs SQL ou données manquantes

**Solutions :**
1. Supprimer le fichier `sql_app.db`
2. Redémarrer l'API (recrée automatiquement)
3. Réimporter les données de test

#### Performances dégradées

**Symptômes :** Réponses lentes, interface qui rame

**Solutions :**
1. Redémarrer l'API
2. Vérifier l'utilisation mémoire/CPU
3. Limiter le nombre d'articles affichés
4. Utiliser la pagination

### Logs et débogage

#### Consultation des logs API
Les logs s'affichent directement dans le terminal de l'API :
```
INFO: 127.0.0.1:52345 - "GET /users/ HTTP/1.1" 200 OK
INFO: 127.0.0.1:52345 - "POST /users/ HTTP/1.1" 201 Created
```

#### Activation du mode debug
```bash
# Variable d'environnement
export DEBUG=true  # Linux/Mac
set DEBUG=true     # Windows

# Puis démarrer l'API
python safe_start.py
```

## Sauvegarde et maintenance

### Sauvegarde des données

**Sauvegarde manuelle :**
```bash
# Copier le fichier de base de données
copy sql_app.db sql_app_backup.db
```

**Restauration :**
```bash
# Arrêter l'API
# Remplacer le fichier
copy sql_app_backup.db sql_app.db
# Redémarrer l'API
```

### Maintenance périodique

**Nettoyage recommandé :**
1. Vérification mensuelle des logs
2. Sauvegarde hebdomadaire des données
3. Mise à jour trimestrielle des dépendances
4. Test complet après chaque modification

### Mise à jour de l'application

```bash
# 1. Sauvegarde
copy sql_app.db sql_app_backup.db

# 2. Mise à jour du code
git pull origin main  # Si utilisation de Git

# 3. Mise à jour des dépendances
pip install -r requirements.txt --upgrade

# 4. Test des fonctionnalités
python safe_start.py
```

## Support et assistance

### Ressources d'aide

**Documentation technique :**
- Module 1-7 de ce cours pour comprendre le fonctionnement
- Documentation officielle FastAPI : https://fastapi.tiangolo.com/
- Documentation PySide6 : https://doc.qt.io/qtforpython/

**Tests automatiques :**
```bash
python test_coherence.py
```

**Vérification de l'intégration GUI-API :**
```bash
python test_gui_integration.py
```

### Bonnes pratiques d'utilisation

1. **Démarrage :** Toujours utiliser `safe_start.py`
2. **Sauvegarde :** Sauvegarder avant modifications importantes
3. **Validation :** Tester les nouvelles données avant production
4. **Performance :** Utiliser la pagination pour les gros volumes
5. **Sécurité :** Éviter les caractères spéciaux dans les saisies

Cette application est maintenant prête à être utilisée en environnement de développement ou de formation.
