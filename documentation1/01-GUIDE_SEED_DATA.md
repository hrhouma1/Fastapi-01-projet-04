# Guide des données d'exemple (Seed Data)

## Qu'est-ce que les seed data ?

Les "seed data" sont des données d'exemple pré-définies que vous pouvez ajouter rapidement à votre base de données pour tester votre API sans avoir à créer manuellement des utilisateurs et des articles.

## Utilisation du script seed_data.py

### Commandes disponibles

```bash
# Voir l'aide
python seed_data.py

# Voir l'état actuel de la base de données
python seed_data.py status

# Ajouter les données d'exemple (si base vide)
python seed_data.py add

# Ajouter même s'il y a déjà des données
python seed_data.py add --force

# Ajout rapide d'un utilisateur de test
python seed_data.py quick

# Supprimer toutes les données
python seed_data.py clear

# Remettre à zéro et ajouter les données d'exemple
python seed_data.py reset
```

## Données créées automatiquement

### 5 Utilisateurs d'exemple

1. **Alice Martin** (alice.martin@example.com) - Actif
   - iPhone 15 Pro - 1200€ (disponible)
   - MacBook Pro 16" - 2800€ (disponible)
   - AirPods Pro - 250€ (non disponible)

2. **Bob Wilson** (bob.wilson@example.com) - Actif
   - Vélo électrique VTT - 1800€ (disponible)
   - Console PlayStation 5 - 550€ (disponible)

3. **Claire Dubois** (claire.dubois@example.com) - Actif
   - Appareil photo Canon EOS R6 - 1600€ (disponible)
   - Objectif Canon RF 24-70mm - 1350€ (disponible)
   - Drone DJI Air 2S - 950€ (non disponible)

4. **David Bernard** (david.bernard@example.com) - Inactif
   - Livre Python pour débutants - 35€ (non disponible)

5. **Emma Petit** (emma.petit@example.com) - Actif
   - Chaise de bureau ergonomique - 450€ (disponible)
   - Bureau assis-debout électrique - 650€ (disponible)
   - Écran 4K 27" - 420€ (disponible)
   - Clavier mécanique - 85€ (disponible)

### Total : 5 utilisateurs, 13 articles

## Utilisation recommandée

### 1. Première utilisation
```bash
# Lancer l'API
python safe_start.py

# Dans un nouveau terminal
python seed_data.py add
```

### 2. Tester votre API avec les données
Maintenant vous pouvez tester ces URLs directement :

**Lister les utilisateurs :**
- http://localhost:8000/users/

**Voir un utilisateur spécifique :**
- http://localhost:8000/users/1 (Alice Martin)
- http://localhost:8000/users/2 (Bob Wilson)
- http://localhost:8000/users/3 (Claire Dubois)

**Lister tous les articles :**
- http://localhost:8000/items/

**Articles d'un utilisateur :**
- http://localhost:8000/users/1/items/ (Articles d'Alice)
- http://localhost:8000/users/5/items/ (Articles d'Emma - 4 articles)

**Rechercher des articles :**
- http://localhost:8000/search/items?q=iPhone
- http://localhost:8000/search/items?q=Canon
- http://localhost:8000/search/items?q=vélo

### 3. Réinitialiser si besoin
```bash
# Si vous voulez repartir à zéro
python seed_data.py reset
```

## Avantages des seed data

### Pour le développement
- **Données réalistes** : Articles avec vrais noms, prix et descriptions
- **Variété de cas** : Utilisateurs actifs/inactifs, articles disponibles/non disponibles
- **Test rapide** : Plus besoin de créer manuellement des données
- **Démonstration** : Parfait pour montrer votre API

### Pour les tests
- **Données cohérentes** : Toujours les mêmes données pour les tests
- **Relations testables** : Utilisateurs avec plusieurs articles
- **Cas d'erreur** : Utilisateur inactif pour tester les validations

### Pour l'apprentissage
- **Exemples concrets** : Voir comment les données sont structurées
- **URLs pré-testables** : Toutes les URLs du guide URLS_TESTS.md fonctionnent immédiatement
- **Pas de frustration** : Commencer directement avec du contenu

## Workflow recommandé pour les étudiants

### Étape 1 : Installation et lancement
```bash
# Configurer l'environnement
python setup.py  # ou setup.bat sur Windows

# Lancer l'API
python safe_start.py
```

### Étape 2 : Ajouter les données d'exemple
```bash
# Dans un nouveau terminal
python seed_data.py add
```

### Étape 3 : Tester immédiatement
- Ouvrir http://localhost:8000/docs
- Tester les URLs du fichier URLS_TESTS.md
- Utiliser le fichier api_tests.http

### Étape 4 : Comprendre et modifier
- Regarder le code dans seed_data.py
- Modifier les données d'exemple
- Tester vos propres créations via Swagger

## Personnaliser les données d'exemple

### Modifier les utilisateurs
Dans `seed_data.py`, éditez la variable `USERS_DATA` :

```python
USERS_DATA = [
    {
        "email": "votre.email@example.com",
        "nom": "VotreNom", 
        "prenom": "VotrePrenom",
        "is_active": True
    },
    # Ajoutez d'autres utilisateurs...
]
```

### Modifier les articles
Dans `seed_data.py`, éditez la variable `ITEMS_DATA` :

```python
ITEMS_DATA = {
    1: [  # Articles pour l'utilisateur ID 1
        {
            "title": "Votre article",
            "description": "Description de votre article",
            "price": 10000,  # Prix en centimes (100€)
            "is_available": True
        }
    ]
}
```

## Gestion des erreurs courantes

### Erreur : "Email déjà utilisé"
```bash
# Solution : utiliser --force ou reset
python seed_data.py add --force
# ou
python seed_data.py reset
```

### Erreur : "Modules non trouvés"
```bash
# Solution : activer l'environnement virtuel
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/macOS
```

### Base de données corrompue
```bash
# Solution : supprimer et recréer
python seed_data.py clear
python seed_data.py add
```

## Commandes utiles pour le debugging

```bash
# Voir rapidement l'état
python seed_data.py status

# Nettoyer et recommencer
python seed_data.py reset

# Ajouter juste un utilisateur de test rapide
python seed_data.py quick

# Forcer l'ajout même si des données existent
python seed_data.py add --force
```

## Intégration avec les autres outils

### Avec safe_start.py
```bash
# Terminal 1 : Lancer l'API
python safe_start.py

# Terminal 2 : Ajouter les données
python seed_data.py add

# Terminal 2 : Tester
python test_coherence.py
```

### Avec api_tests.http
1. Lancez `python seed_data.py add`
2. Ouvrez `api_tests.http` dans VS Code
3. Tous les tests fonctionneront immédiatement

### Avec URLS_TESTS.md
1. Ajoutez les données : `python seed_data.py add`
2. Consultez URLS_TESTS.md
3. Testez toutes les URLs listées - elles retourneront du contenu réel

## Résumé

Le script `seed_data.py` vous fait gagner du temps en créant instantanément un environnement de test complet avec des données réalistes. C'est l'outil parfait pour :

- **Commencer rapidement** sans créer manuellement des données
- **Tester toutes les fonctionnalités** de votre API
- **Démontrer votre projet** avec du contenu professionnel
- **Apprendre** avec des exemples concrets

**Usage recommandé :** `python seed_data.py add` dès que vous lancez votre API pour la première fois !
