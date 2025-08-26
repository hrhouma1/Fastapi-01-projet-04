# Workflow de l'interface graphique - Analyse complète des appels

## Vue d'ensemble du workflow

Quand vous lancez `python run_gui.py`, voici le flux complet d'exécution avec tous les appels de fonctions et interactions entre composants.

## Diagramme de séquence global

```
Utilisateur → run_gui.py → QApplication → MainWindow → APIClient → FastAPI → SQLAlchemy → SQLite
    |            |             |            |           |         |           |
    |            |             |            |           |         |           |
 Lancement → Initialisation → GUI Setup → Window Init → API Test → Endpoints → ORM → Database
```

## Phase 1 : Démarrage de l'application (run_gui.py)

### Étape 1.1 : Exécution du point d'entrée

```python
# run_gui.py - Point d'entrée
if __name__ == "__main__":
    main()
```

**Flux d'exécution :**
```
python run_gui.py
    ↓
def main() appelée
    ↓
Imports des modules nécessaires
```

### Étape 1.2 : Initialisation de l'application Qt

```python
def main():
    # 1. Création de l'application Qt
    app = QApplication(sys.argv)
    
    # 2. Configuration du style et des propriétés
    app.setApplicationName("FastAPI CRUD GUI")
    app.setApplicationVersion("1.0.0")
```

**Calls Stack :**
```
main()
├── QApplication(sys.argv)          # Initialise le système de fenêtrage Qt
├── app.setApplicationName()        # Configure le nom de l'application
└── app.setApplicationVersion()     # Définit la version
```

### Étape 1.3 : Test de connectivité API

```python
def main():
    # 3. Test de l'API avant lancement GUI
    if not test_api_connection():
        show_api_error()
        return
```

**Détail du test API :**
```python
def test_api_connection():
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False
```

**Flux de test :**
```
test_api_connection()
    ↓
requests.get("http://localhost:8000/")
    ↓
HTTP Request vers FastAPI
    ↓
main.py endpoint "/"
    ↓
return {"message": "API CRUD FastAPI", ...}
```

### Étape 1.4 : Création de la fenêtre principale

```python
def main():
    # 4. Création de la fenêtre principale
    window = MainWindow()
    window.show()
    
    # 5. Démarrage de la boucle d'événements
    sys.exit(app.exec())
```

## Phase 2 : Initialisation de MainWindow (gui_client/main_window.py)

### Étape 2.1 : Construction de MainWindow

```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1. Configuration de base de la fenêtre
        self.setup_window()
        
        # 2. Création du client API
        self.api_client = APIClient("http://localhost:8000")
        
        # 3. Initialisation de l'interface utilisateur
        self.init_ui()
        
        # 4. Configuration des signaux et slots
        self.setup_signals()
        
        # 5. Chargement initial des données
        self.load_initial_data()
```

**Séquence d'initialisation :**
```
MainWindow.__init__()
    ├── super().__init__()              # Initialise QMainWindow
    ├── self.setup_window()             # Configure fenêtre (titre, taille, etc.)
    ├── APIClient("http://localhost:8000")  # Crée le client API
    ├── self.init_ui()                  # Construit l'interface
    ├── self.setup_signals()            # Configure les signaux/slots
    └── self.load_initial_data()        # Charge les données initiales
```

### Étape 2.2 : Configuration de la fenêtre

```python
def setup_window(self):
    self.setWindowTitle("Gestionnaire CRUD FastAPI")
    self.setGeometry(100, 100, 1200, 800)
    self.setWindowIcon(QIcon("icon.png"))  # Si disponible
```

### Étape 2.3 : Initialisation de l'interface utilisateur

```python
def init_ui(self):
    # 1. Création du widget central avec onglets
    self.tabs = QTabWidget()
    self.setCentralWidget(self.tabs)
    
    # 2. Création des onglets
    self.users_tab = UsersTab(self, self.api_client)
    self.items_tab = ItemsTab(self, self.api_client)
    
    # 3. Ajout des onglets au widget principal
    self.tabs.addTab(self.users_tab, "Utilisateurs")
    self.tabs.addTab(self.items_tab, "Articles")
```

**Hiérarchie des widgets créée :**
```
MainWindow (QMainWindow)
└── QTabWidget (self.tabs)
    ├── UsersTab (Onglet utilisateurs)
    │   ├── QVBoxLayout (Layout principal)
    │   ├── QFormLayout (Formulaire création)
    │   └── QTableWidget (Liste utilisateurs)
    └── ItemsTab (Onglet articles)
        ├── QVBoxLayout (Layout principal)
        ├── QFormLayout (Formulaire création)
        ├── QHBoxLayout (Recherche)
        └── QTableWidget (Liste articles)
```

## Phase 3 : Initialisation du client API (gui_client/api_client.py)

### Étape 3.1 : Création du client API

```python
class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        
        # Configuration de la session
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # Test de connectivité initial
        self.test_connection()
```

**Configuration de session :**
```
APIClient.__init__()
    ├── self.base_url = "http://localhost:8000"
    ├── requests.Session()              # Crée session HTTP persistante
    ├── session.headers.update()        # Configure headers par défaut
    └── self.test_connection()          # Test initial de connectivité
```

## Phase 4 : Chargement initial des données

### Étape 4.1 : Chargement des utilisateurs

```python
def load_initial_data(self):
    # Dans MainWindow
    self.users_tab.load_users()
    self.items_tab.load_items()
    self.items_tab.load_users_combo()
```

**Séquence de chargement utilisateurs :**
```
MainWindow.load_initial_data()
    ↓
UsersTab.load_users()
    ↓
APIClient.get_users()
    ↓
requests.Session.get("http://localhost:8000/users/")
    ↓
FastAPI main.py endpoint GET /users/
    ↓
crud.get_users(db, skip=0, limit=100)
    ↓
db.query(models.User).offset(0).limit(100).all()
    ↓
SQLAlchemy génère: SELECT * FROM users LIMIT 100
    ↓
SQLite exécute la requête
    ↓
Résultats remontent la chaîne:
SQLite → SQLAlchemy → crud.py → main.py → HTTP Response → APIClient → UsersTab
```

### Étape 4.2 : Chargement des articles

```python
# Dans ItemsTab
def load_items(self):
    try:
        items = self.api_client.get_items()
        if isinstance(items, list):
            self.populate_items_table(items)
        else:
            self.show_error(f"Erreur: {items.get('error', 'Erreur inconnue')}")
    except Exception as e:
        self.show_error(f"Erreur de chargement: {str(e)}")
```

**Flux de chargement articles :**
```
ItemsTab.load_items()
    ↓
APIClient.get_items()
    ↓
requests.get("http://localhost:8000/items/")
    ↓
main.py GET /items/ endpoint
    ↓
crud.get_items(db)
    ↓
SQLAlchemy query avec relations:
SELECT items.*, users.nom, users.prenom 
FROM items 
LEFT JOIN users ON items.owner_id = users.id
    ↓
Retour des données avec relations chargées
    ↓
ItemsTab.populate_items_table(items)
```

## Phase 5 : Interactions utilisateur en temps réel

### Étape 5.1 : Création d'un utilisateur (workflow complet)

**Déclenchement :**
```
Utilisateur clique sur "Créer utilisateur"
    ↓
PySide6 émet signal: QPushButton.clicked
    ↓
Slot connecté: UsersTab.create_user()
```

**Traitement côté GUI :**
```python
def create_user(self):
    # 1. Récupération des données du formulaire
    user_data = {
        "email": self.email_input.text(),
        "nom": self.nom_input.text(),
        "prenom": self.prenom_input.text(),
        "is_active": self.active_checkbox.isChecked()
    }
    
    # 2. Validation côté client
    if not self.validate_user_data(user_data):
        return
    
    # 3. Appel API
    result = self.api_client.create_user(user_data)
    
    # 4. Traitement du résultat
    if isinstance(result, dict) and "id" in result:
        self.show_success("Utilisateur créé avec succès")
        self.clear_form()
        self.load_users()  # Rafraîchir la liste
        self.parent_window.refresh_all_users_data()  # Synchroniser
    else:
        self.show_error(f"Erreur: {result.get('error', 'Erreur inconnue')}")
```

**Flux API complet :**
```
UsersTab.create_user()
    ↓
APIClient.create_user(user_data)
    ↓
session.post("http://localhost:8000/users/", json=user_data)
    ↓
FastAPI main.py POST /users/
    ↓
Pydantic validation avec schemas.UserCreate:
- Validation email format
- Validation longueur nom/prenom
- Validation types de données
    ↓
Si validation OK: crud.create_user(db, user)
    ↓
SQLAlchemy ORM:
user = models.User(**user_data)
db.add(user)
db.commit()
db.refresh(user)  # Récupère l'ID généré
    ↓
SQL généré:
INSERT INTO users (email, nom, prenom, is_active, created_at) 
VALUES (?, ?, ?, ?, ?)
    ↓
SQLite exécute l'insertion
    ↓
Remontée du résultat:
SQLite → SQLAlchemy → crud.py → main.py → HTTP 201 → APIClient → UsersTab
```

### Étape 5.2 : Recherche d'articles (workflow détaillé)

**Déclenchement :**
```
Utilisateur tape dans le champ de recherche
    ↓
Utilisateur clique "Rechercher"
    ↓
QPushButton.clicked signal
    ↓
ItemsTab.search_items() slot
```

**Traitement recherche :**
```python
def search_items(self):
    query = self.search_input.text().strip()
    
    # Validation locale
    if len(query) < 2:
        self.show_warning("Minimum 2 caractères")
        return
    
    # Feedback visuel
    self.search_btn.setText("Recherche...")
    self.search_btn.setEnabled(False)
    
    try:
        # Appel API de recherche
        results = self.api_client.search_items(query)
        
        if isinstance(results, list):
            self.populate_items_table(results)
            self.show_status(f"{len(results)} résultat(s) trouvé(s)")
        else:
            self.show_error(f"Erreur: {results.get('error')}")
    
    finally:
        # Restaurer le bouton
        self.search_btn.setText("Rechercher")
        self.search_btn.setEnabled(True)
```

**Flux de recherche API :**
```
ItemsTab.search_items()
    ↓
APIClient.search_items(query="iPhone", limit=50)
    ↓
session.get("http://localhost:8000/search/items?q=iPhone&limit=50")
    ↓
FastAPI main.py GET /search/items
    ↓
Validation paramètres:
- q >= 2 caractères
- limit <= 100
    ↓
crud.search_items(db, query="iPhone", limit=50)
    ↓
SQLAlchemy requête ILIKE (insensible à la casse):
db.query(models.Item).filter(
    or_(
        models.Item.title.ilike('%iPhone%'),
        models.Item.description.ilike('%iPhone%')
    )
).limit(50).all()
    ↓
SQL généré:
SELECT * FROM items 
WHERE (title ILIKE '%iPhone%' OR description ILIKE '%iPhone%')
LIMIT 50
    ↓
SQLite exécute la recherche
    ↓
Résultats filtrés remontent:
SQLite → SQLAlchemy → crud.py → main.py → HTTP 200 → APIClient → ItemsTab
```

## Phase 6 : Synchronisation inter-onglets

### Étape 6.1 : Problème de synchronisation résolu

**Situation :** Utilisateur créé dans l'onglet "Utilisateurs" doit apparaître dans la liste déroulante de l'onglet "Articles"

**Solution implémentée :**
```python
# Dans MainWindow
def refresh_all_users_data(self):
    """Synchronise les données utilisateurs entre tous les onglets"""
    self.items_tab.refresh_users_combo()

# Dans UsersTab.create_user()
if success:
    self.parent_window.refresh_all_users_data()  # Déclenche synchronisation

# Dans ItemsTab
def refresh_users_combo(self):
    current_selection = self.owner_combo.currentData()  # Sauvegarde sélection
    
    # Recharge les utilisateurs
    users = self.api_client.get_users()
    self.owner_combo.clear()
    
    for user in users:
        self.owner_combo.addItem(f"{user['prenom']} {user['nom']}", user['id'])
    
    # Restaure la sélection si possible
    if current_selection:
        index = self.owner_combo.findData(current_selection)
        if index >= 0:
            self.owner_combo.setCurrentIndex(index)
```

**Flux de synchronisation :**
```
UsersTab: Utilisateur créé avec succès
    ↓
self.parent_window.refresh_all_users_data()
    ↓
MainWindow.refresh_all_users_data()
    ↓
ItemsTab.refresh_users_combo()
    ↓
APIClient.get_users() (nouvel appel API)
    ↓
FastAPI récupère liste utilisateurs mise à jour
    ↓
ComboBox mis à jour avec nouvel utilisateur
```

## Phase 7 : Gestion des erreurs et feedback

### Étape 7.1 : Gestion des erreurs réseau

```python
# Dans APIClient
def _make_request(self, method, endpoint, **kwargs):
    url = f"{self.base_url}{endpoint}"
    
    try:
        response = self.session.request(method, url, timeout=10, **kwargs)
        response.raise_for_status()
        return response.json()
    
    except requests.Timeout:
        return {"error": "Timeout - API non accessible"}
    except requests.ConnectionError:
        return {"error": "Connexion impossible - Vérifiez que l'API est démarrée"}
    except requests.HTTPError as e:
        if e.response.status_code == 422:
            # Erreur de validation Pydantic
            return {"error": "Données invalides", "details": e.response.json()}
        return {"error": f"Erreur HTTP {e.response.status_code}"}
    except Exception as e:
        return {"error": f"Erreur inattendue: {str(e)}"}
```

### Étape 7.2 : Messages utilisateur

```python
# Dans les onglets (UsersTab, ItemsTab)
def show_success(self, message):
    QMessageBox.information(self, "Succès", message)

def show_error(self, message):
    QMessageBox.critical(self, "Erreur", message)

def show_warning(self, message):
    QMessageBox.warning(self, "Attention", message)
```

## Diagramme de workflow complet

```
1. DÉMARRAGE
   python run_gui.py → QApplication → MainWindow

2. INITIALISATION
   MainWindow → APIClient → Test API → Interface Setup

3. CHARGEMENT INITIAL
   load_initial_data() → get_users() → get_items() → populate_tables()

4. INTERACTIONS UTILISATEUR
   User Action → Signal → Slot → Validation → API Call → Update GUI

5. SYNCHRONISATION
   Data Change → refresh_all_users_data() → Update All Tabs

6. GESTION D'ERREURS
   Exception → Error Handler → User Feedback → Recovery Action
```

## Performance et optimisations

### Optimisations implémentées

1. **Session HTTP persistante** : Réutilisation des connexions
2. **Chargement asynchrone** : Interface réactive pendant les appels API
3. **Cache local** : Évite les appels API répétitifs
4. **Validation côté client** : Réduit les erreurs serveur
5. **Feedback visuel** : Utilisateur informé des actions en cours

### Points d'amélioration possibles

1. **Threading** : Appels API dans des threads séparés
2. **Pagination** : Chargement progressif des listes importantes
3. **Cache intelligent** : Invalidation automatique du cache
4. **Retry automatique** : Nouvelle tentative en cas d'échec réseau
5. **Websockets** : Notifications temps réel entre clients

Ce workflow détaillé montre comment chaque composant interagit dans l'écosystème de l'application, depuis le clic utilisateur jusqu'à la mise à jour de l'interface graphique.
