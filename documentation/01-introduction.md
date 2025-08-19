# Module 1 : Introduction à l'API CRUD avec FastAPI

## Objectifs pédagogiques

À la fin de ce module, vous serez capable de :
- Comprendre ce qu'est une API REST
- Identifier les opérations CRUD
- Expliquer l'architecture d'une application FastAPI
- Distinguer les rôles de chaque composant du projet

## Qu'est-ce qu'une API REST

### Définition
Une API (Application Programming Interface) REST est un système qui permet à différentes applications de communiquer entre elles via Internet en utilisant le protocole HTTP.

### Principe de fonctionnement
1. Le client (navigateur, application mobile, etc.) envoie une requête HTTP
2. Le serveur traite cette requête 
3. Le serveur renvoie une réponse au format JSON
4. Le client utilise cette réponse pour afficher des informations ou effectuer des actions

### Méthodes HTTP utilisées
- **GET** : Récupérer des données (lecture)
- **POST** : Créer de nouvelles données
- **PUT** : Modifier des données existantes
- **DELETE** : Supprimer des données

## Les opérations CRUD

CRUD est un acronyme qui représente les quatre opérations de base sur les données :

### C - Create (Créer)
- Ajouter de nouvelles données dans la base
- Utilise la méthode HTTP POST
- Exemple : Créer un nouveau utilisateur

### R - Read (Lire)
- Consulter les données existantes
- Utilise la méthode HTTP GET
- Exemple : Afficher la liste des utilisateurs

### U - Update (Mettre à jour)
- Modifier des données existantes
- Utilise la méthode HTTP PUT
- Exemple : Changer le nom d'un utilisateur

### D - Delete (Supprimer)
- Effacer des données
- Utilise la méthode HTTP DELETE
- Exemple : Supprimer un utilisateur

## Architecture de notre projet

Notre API suit une architecture en couches :

### 1. Couche de présentation (Endpoints)
- Fichier : `main.py`
- Rôle : Recevoir les requêtes HTTP et renvoyer les réponses
- Contient les routes (URLs) de l'API

### 2. Couche métier (Logique)
- Fichier : `crud.py` 
- Rôle : Contenir la logique métier et les règles de validation
- Effectue les opérations sur les données

### 3. Couche de données (Modèles)
- Fichiers : `models.py` et `schemas.py`
- Rôle : Définir la structure des données
- `models.py` : Structure en base de données
- `schemas.py` : Structure pour les échanges API

### 4. Couche de persistance (Base de données)
- Fichier : `database.py`
- Rôle : Configuration de la connexion à la base de données
- Utilise SQLite pour la simplicité

## Entités de notre système

### Utilisateur (User)
Un utilisateur représente une personne inscrite dans le système.

**Attributs :**
- id : Identifiant unique (généré automatiquement)
- email : Adresse email (unique, obligatoire)
- nom : Nom de famille (obligatoire)
- prenom : Prénom (obligatoire)
- is_active : Statut actif/inactif (booléen)
- created_at : Date de création (automatique)
- updated_at : Date de dernière modification (automatique)

### Article (Item)
Un article représente un objet mis en vente par un utilisateur.

**Attributs :**
- id : Identifiant unique (généré automatiquement)
- title : Titre de l'article (obligatoire)
- description : Description détaillée (optionnel)
- price : Prix en centimes (obligatoire)
- is_available : Disponibilité (booléen)
- owner_id : Référence vers l'utilisateur propriétaire (obligatoire)
- created_at : Date de création (automatique)
- updated_at : Date de dernière modification (automatique)

### Relation entre entités
- Un utilisateur peut avoir plusieurs articles
- Un article appartient à un seul utilisateur
- Cette relation est appelée "One-to-Many" (Un vers Plusieurs)

## Technologies utilisées

### FastAPI
Framework web moderne pour Python qui génère automatiquement la documentation de l'API.

**Avantages :**
- Rapide à développer
- Documentation automatique
- Validation automatique des données
- Support natif de la programmation asynchrone

### SQLAlchemy
ORM (Object-Relational Mapping) qui permet de manipuler la base de données avec du code Python plutôt qu'avec du SQL.

**Avantages :**
- Code plus lisible
- Protection contre les injections SQL
- Indépendance du type de base de données

### Pydantic
Bibliothèque de validation des données qui assure que les données reçues respectent le format attendu.

**Avantages :**
- Validation automatique
- Conversion de types
- Messages d'erreur clairs

### SQLite
Base de données légère stockée dans un fichier local.

**Avantages :**
- Pas d'installation de serveur nécessaire
- Parfaite pour le développement et les tests
- Facilement portable

## Structure des URLs de l'API

### Endpoints pour les utilisateurs
- `GET /users/` : Lister tous les utilisateurs
- `POST /users/` : Créer un nouvel utilisateur  
- `GET /users/{user_id}` : Récupérer un utilisateur spécifique
- `PUT /users/{user_id}` : Modifier un utilisateur
- `DELETE /users/{user_id}` : Supprimer un utilisateur

### Endpoints pour les articles
- `GET /items/` : Lister tous les articles
- `POST /users/{user_id}/items/` : Créer un article pour un utilisateur
- `GET /items/{item_id}` : Récupérer un article spécifique
- `PUT /items/{item_id}` : Modifier un article
- `DELETE /items/{item_id}` : Supprimer un article
- `GET /users/{user_id}/items/` : Lister les articles d'un utilisateur

## Règles métier importantes

### Ordre des opérations
1. Vous devez toujours créer un utilisateur avant de créer des articles
2. Un article ne peut pas exister sans utilisateur propriétaire
3. La suppression d'un utilisateur supprime automatiquement tous ses articles

### Validation des données
- Les emails doivent être uniques
- Les prix sont stockés en centimes (ex: 2500 = 25,00 euros)
- Tous les champs obligatoires doivent être remplis

### Gestion des erreurs
- Tentative de créer un article sans utilisateur : Erreur 404
- Email déjà utilisé : Erreur 400  
- Ressource non trouvée : Erreur 404
- Données invalides : Erreur 422

## Format des données

### Format JSON
Toutes les données sont échangées au format JSON (JavaScript Object Notation).

**Exemple d'utilisateur :**
```json
{
  "id": 1,
  "email": "marie.dupont@example.com",
  "nom": "Dupont",
  "prenom": "Marie", 
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "items": []
}
```

**Exemple d'article :**
```json
{
  "id": 1,
  "title": "MacBook Pro",
  "description": "Ordinateur portable en excellent état",
  "price": 150000,
  "is_available": true,
  "owner_id": 1,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

## Outils de développement

### Environnement virtuel Python
Isoler les dépendances du projet dans un environnement séparé pour éviter les conflits.

### Serveur de développement
Uvicorn : serveur ASGI qui permet d'exécuter l'application FastAPI en local.

### Documentation interactive
FastAPI génère automatiquement une documentation interactive accessible via le navigateur.

### Outils de test
- Scripts Python pour tester automatiquement l'API
- Fichiers .http pour tester manuellement avec des outils comme REST Client

## Prochaines étapes

Dans le module suivant, vous apprendrez à installer tous les outils nécessaires et à configurer votre environnement de développement.

Assurez-vous de bien comprendre les concepts présentés dans ce module avant de continuer.
