# 04 - Interface Graphique avec PySide6

## Vue d'ensemble

Cette section présente l'interface graphique développée avec PySide6 (Qt for Python) pour interagir facilement avec votre API FastAPI CRUD. Cette interface moderne et intuitive permet de gérer les utilisateurs et articles sans avoir besoin de connaître les commandes techniques.

## Fonctionnalités principales

### Gestion des utilisateurs
- Créer de nouveaux utilisateurs
- Visualiser la liste complète des utilisateurs
- Supprimer des utilisateurs (avec leurs articles)
- Indicateur du nombre d'articles par utilisateur

### Gestion des articles
- Créer des articles pour des utilisateurs existants
- Visualiser tous les articles avec détails complets
- Rechercher des articles par mots-clés
- Supprimer des articles individuellement
- Formatage automatique des prix en euros

### Monitoring de connexion
- Indicateur visuel de l'état de connexion à l'API
- Test manuel de connexion
- Vérification automatique périodique
- Configuration de l'URL de l'API

## Installation et configuration

### Prérequis
- Python 3.7 ou supérieur
- L'API FastAPI démarrée (voir guide d'exécution)
- Environnement virtuel activé

### Installation des dépendances

Les nouvelles dépendances ont été ajoutées au fichier `requirements.txt` :

```bash
# Activer l'environnement virtuel
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Installer les nouvelles dépendances
pip install -r requirements.txt
```

**Nouvelles dépendances :**
- `PySide6>=6.7.0` - Interface graphique Qt
- `requests>=2.32.0` - Communication HTTP avec l'API

## Lancement de l'interface

### Méthode 1 : Script de lancement (recommandée)

```bash
python run_gui.py
```

### Méthode 2 : Lancement direct

```bash
python -m gui_client.main_window
```

### Méthode 3 : Import Python

```python
from gui_client import main
main()
```

## Guide d'utilisation

### Étape 1 : Démarrer l'API

Avant de lancer l'interface graphique :

```bash
# Terminal 1 : API FastAPI
python safe_start.py
```

### Étape 2 : Lancer l'interface graphique

```bash
# Terminal 2 : Interface graphique
python run_gui.py
```

### Étape 3 : Vérifier la connexion

1. L'indicateur de connexion (cercle coloré) doit être vert
2. Si rouge, cliquez sur "Tester la connexion"
3. Vérifiez que l'URL est correcte : `http://localhost:8000`

## Utilisation des onglets

### Onglet "Utilisateurs"

**Créer un utilisateur :**
1. Remplissez les champs Email, Nom, Prénom
2. Cochez "Utilisateur actif" si nécessaire
3. Cliquez "Créer l'utilisateur"

**Gérer les utilisateurs :**
- Cliquez "Actualiser" pour recharger la liste
- Sélectionnez un utilisateur pour l'activer pour suppression
- Cliquez "Supprimer" (attention : supprime aussi ses articles)

**Colonnes affichées :**
- ID : Identifiant unique
- Email : Adresse e-mail
- Nom, Prénom : Informations personnelles
- Actif : Statut de l'utilisateur
- Articles : Nombre d'articles possédés

### Onglet "Articles"

**Créer un article :**
1. Sélectionnez le propriétaire dans la liste déroulante
2. Saisissez le titre et la description
3. Indiquez le prix (format: 25.50)
4. Cochez "Article disponible" si applicable
5. Cliquez "Créer l'article"

**Rechercher des articles :**
1. Tapez votre recherche dans le champ
2. Appuyez Entrée ou cliquez "Rechercher"
3. Cliquez "Effacer" pour voir tous les articles

**Gérer les articles :**
- "Actualiser" recharge la liste complète
- Sélectionnez un article pour activer la suppression
- "Supprimer" retire l'article définitivement

**Colonnes affichées :**
- ID : Identifiant unique
- Titre : Nom de l'article
- Description : Aperçu (50 premiers caractères)
- Prix : Formaté en euros (25,00€)
- Disponible : État de disponibilité
- Propriétaire : ID du propriétaire

## Architecture technique

### Structure des fichiers

```
gui_client/
├── __init__.py           # Point d'entrée du package
├── api_client.py         # Client de communication avec l'API
└── main_window.py        # Interface graphique principale

run_gui.py               # Script de lancement
```

### Composants principaux

**FastAPIClient (`api_client.py`)**
- Communication HTTP avec l'API REST
- Gestion des erreurs et timeouts
- Formatage des prix et validation des données
- Méthodes pour tous les endpoints CRUD

**MainWindow (`main_window.py`)**
- Fenêtre principale avec onglets
- StatusIndicator pour l'état de connexion
- UsersTab pour la gestion des utilisateurs
- ItemsTab pour la gestion des articles

**Fonctionnalités avancées :**
- Vérification automatique de connexion (5 secondes)
- Messages d'erreur informatifs
- Validation des saisies utilisateur
- Tables redimensionnables automatiquement
- Interface moderne style "Fusion"

## Gestion des erreurs

### Problèmes courants

**Interface ne se lance pas :**
```bash
# Vérifier l'installation PySide6
pip list | grep -i pyside

# Réinstaller si nécessaire
pip install PySide6
```

**Connexion à l'API échouée :**
1. Vérifiez que l'API FastAPI fonctionne : http://localhost:8000
2. Contrôlez l'URL dans l'interface
3. Testez manuellement avec "Tester la connexion"

**Erreurs de création :**
- Vérifiez que tous les champs sont remplis
- Pour les articles, un utilisateur doit exister
- Les emails doivent être uniques
- Les prix doivent être au format numérique (25.50)

### Messages d'erreur types

**"Aucun utilisateur disponible"**
→ Créez d'abord un utilisateur avant de créer un article

**"Prix invalide"**  
→ Utilisez le format décimal : 25.50 (pas de symboles)

**"Erreur lors du chargement"**
→ Vérifiez la connexion API et relancez si nécessaire

## Fonctionnalités avancées

### Configuration de l'URL
- Modifiez l'URL dans le champ en en-tête
- Testez avec différents ports (8001, 8002, etc.)
- La configuration est conservée durant la session

### Recherche d'articles
- Recherche dans les titres ET descriptions
- Résultats en temps réel
- Supporte les recherches partielles
- Insensible à la casse

### Indicateurs visuels
- Vert : Connecté et fonctionnel
- Orange : Connexion en cours
- Rouge : API non disponible ou erreur

### Gestion des données
- Actualisation automatique après créations/suppressions
- Validation côté client avant envoi
- Formatage automatique des prix
- Gestion des articles orphelins

## Personnalisation et extension

### Ajout de nouvelles fonctionnalités

**Modifier un utilisateur :**
```python
# Dans UsersTab, ajouter :
def edit_selected_user(self):
    # Ouvrir une boîte de dialogue d'édition
    # Utiliser api_client.update_user()
```

**Filtrage avancé :**
```python
# Dans ItemsTab, ajouter :
def filter_by_price_range(self, min_price, max_price):
    # Filtrer les articles par gamme de prix
```

**Export de données :**
```python
# Ajouter bouton d'export CSV/Excel
def export_data(self, data, filename):
    # Exporter vers fichier
```

### Personnalisation de l'interface

**Thème sombre :**
```python
# Dans main(), après app.setStyle("Fusion")
app.setStyleSheet("QWidget { background-color: #2b2b2b; color: white; }")
```

**Icônes personnalisées :**
```python
# Ajouter des icônes aux boutons
self.create_user_btn.setIcon(QIcon("icons/user-plus.png"))
```

## Intégration avec l'API

### Endpoints utilisés

L'interface utilise tous les endpoints de l'API :

**Utilisateurs :**
- `GET /users/` - Liste des utilisateurs
- `POST /users/` - Création d'utilisateur  
- `DELETE /users/{id}` - Suppression d'utilisateur

**Articles :**
- `GET /items/` - Liste des articles
- `GET /users/{id}/items/` - Articles d'un utilisateur
- `POST /users/{id}/items/` - Création d'article
- `DELETE /items/{id}` - Suppression d'article
- `GET /search/items` - Recherche d'articles

**Système :**
- `GET /` - Test de connexion
- `GET /health` - État de santé (si disponible)

### Format des données

**Création d'utilisateur :**
```json
{
  "email": "test@example.com",
  "nom": "Dupont",
  "prenom": "Jean",
  "is_active": true
}
```

**Création d'article :**
```json
{
  "title": "iPhone 15 Pro",
  "description": "Smartphone dernière génération",
  "price": 120000,
  "is_available": true
}
```

## Conseils d'utilisation

### Workflow recommandé

1. **Démarrer l'API** : `python safe_start.py`
2. **Ajouter des données test** : `python seed_data.py add`
3. **Lancer l'interface** : `python run_gui.py`
4. **Tester la connexion** (indicateur vert)
5. **Explorer les données** existantes
6. **Créer de nouvelles données** via l'interface

### Bonnes pratiques

**Pour les utilisateurs :**
- Utilisez des emails valides et uniques
- Activez les utilisateurs par défaut
- Utilisez des noms complets pour faciliter l'identification

**Pour les articles :**
- Choisissez des titres descriptifs
- Rédigez des descriptions complètes
- Utilisez des prix réalistes (en euros)
- Marquez comme disponible si en vente

**Pour la performance :**
- Utilisez la recherche pour les grandes listes
- Actualisez manuellement si nécessaire
- Fermez l'application proprement

## Résolution de problèmes

### Diagnostic rapide

**L'interface ne répond plus :**
1. Vérifiez que l'API fonctionne toujours
2. Redémarrez l'interface graphique
3. Contrôlez les logs de l'API

**Données manquantes :**
1. Cliquez "Actualiser" sur l'onglet concerné
2. Vérifiez la connexion réseau
3. Consultez les messages d'erreur

**Erreurs de création :**
1. Validez le format des données
2. Assurez-vous que l'utilisateur propriétaire existe
3. Vérifiez l'unicité des emails

### Support et débogage

**Logs de l'API :**
Consultez la sortie du terminal où `python safe_start.py` fonctionne.

**Logs de l'interface :**
Les erreurs s'affichent dans des boîtes de dialogue ou dans le terminal.

**Test manuel :**
Utilisez `http://localhost:8000/docs` pour tester l'API directement.

## Améliorations futures possibles

### Interface utilisateur
- Mode sombre/clair commutable
- Historique des actions
- Sauvegarde des préférences
- Raccourcis clavier
- Drag & drop pour l'organisation

### Fonctionnalités métier
- Édition en ligne des données
- Filtres avancés et tri
- Export/Import de données
- Statistiques et graphiques
- Gestion des images d'articles

### Performance et robustesse
- Cache local des données
- Mode hors ligne partiel
- Synchronisation automatique
- Récupération après erreur
- Optimisation pour grandes listes

L'interface graphique PySide6 transforme votre API FastAPI en une application complète et facile à utiliser pour tous types d'utilisateurs !
