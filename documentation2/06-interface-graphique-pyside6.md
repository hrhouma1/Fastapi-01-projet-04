# Interface graphique avec PySide6

## Introduction à PySide6

PySide6 est la liaison Python officielle pour Qt 6. Il permet de créer des interfaces graphiques modernes et performantes.

### Avantages de PySide6
- Interface native sur chaque OS
- Performance élevée
- Widgets riches et personnalisables
- Architecture signal/slot robuste
- Intégration facile avec Python

## Architecture de notre interface

### Structure MVC

```
MainWindow (Contrôleur principal)
├── UsersTab (Vue utilisateurs)
│   ├── UserFormWidget (Formulaire)
│   └── UserTableWidget (Tableau)
├── ItemsTab (Vue articles)
│   ├── ItemFormWidget (Formulaire)
│   └── ItemTableWidget (Tableau)
└── APIClient (Modèle de données)
```

### Communication avec l'API

```python
class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_users(self):
        response = self.session.get(f"{self.base_url}/users/")
        response.raise_for_status()
        return response.json()
    
    def create_user(self, user_data):
        response = self.session.post(
            f"{self.base_url}/users/", 
            json=user_data
        )
        response.raise_for_status()
        return response.json()
```

## Widgets principaux

### QMainWindow - Fenêtre principale

```python
from PySide6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionnaire CRUD")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central avec onglets
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Initialisation des composants
        self.init_ui()
        self.setup_signals()
    
    def init_ui(self):
        # Onglet utilisateurs
        self.users_tab = UsersTab(self)
        self.tabs.addTab(self.users_tab, "Utilisateurs")
        
        # Onglet articles
        self.items_tab = ItemsTab(self)
        self.tabs.addTab(self.items_tab, "Articles")
```

### QTableWidget - Tableau de données

```python
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

class UserTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_table()
    
    def setup_table(self):
        # Colonnes
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels([
            "ID", "Email", "Nom", "Prénom", "Actif"
        ])
        
        # Redimensionnement automatique
        header = self.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Email
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
    
    def populate_data(self, users):
        self.setRowCount(len(users))
        for row, user in enumerate(users):
            self.setItem(row, 0, QTableWidgetItem(str(user["id"])))
            self.setItem(row, 1, QTableWidgetItem(user["email"]))
            self.setItem(row, 2, QTableWidgetItem(user["nom"]))
            self.setItem(row, 3, QTableWidgetItem(user["prenom"]))
            self.setItem(row, 4, QTableWidgetItem("Oui" if user["is_active"] else "Non"))
```

## Signaux et slots

### Principe de base

Les signaux et slots permettent la communication entre objets sans couplage fort.

```python
from PySide6.QtCore import Signal, Slot

class UserFormWidget(QWidget):
    # Signal émis lors de la création d'un utilisateur
    user_created = Signal(dict)  # dict contient les données utilisateur
    
    def __init__(self):
        super().__init__()
        self.create_button = QPushButton("Créer")
        self.create_button.clicked.connect(self.create_user)
    
    @Slot()
    def create_user(self):
        user_data = self.get_form_data()
        # Émettre le signal avec les données
        self.user_created.emit(user_data)

# Connexion dans la classe parent
def setup_signals(self):
    self.user_form.user_created.connect(self.on_user_created)

@Slot(dict)
def on_user_created(self, user_data):
    # Traitement des données reçues
    self.refresh_user_table()
```

## Gestion des erreurs

### Messages d'erreur utilisateur

```python
from PySide6.QtWidgets import QMessageBox

def show_error(parent, title, message):
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.exec()

def show_success(parent, message):
    QMessageBox.information(parent, "Succès", message)

# Utilisation dans les méthodes
def create_user(self):
    try:
        user_data = self.get_form_data()
        result = self.api_client.create_user(user_data)
        show_success(self, "Utilisateur créé avec succès")
        self.clear_form()
    except requests.RequestException as e:
        show_error(self, "Erreur", f"Erreur réseau : {str(e)}")
    except ValueError as e:
        show_error(self, "Validation", str(e))
```

## Styles et apparence

### Feuilles de style Qt

```python
def apply_styles(self):
    style = """
    QMainWindow {
        background-color: #f5f5f5;
    }
    
    QTabWidget::pane {
        border: 1px solid #c0c0c0;
        background-color: white;
    }
    
    QTabBar::tab {
        background-color: #e0e0e0;
        padding: 8px 16px;
        margin-right: 2px;
    }
    
    QTabBar::tab:selected {
        background-color: white;
        border-bottom: 2px solid #0078d4;
    }
    
    QPushButton {
        background-color: #0078d4;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
    }
    
    QPushButton:hover {
        background-color: #106ebe;
    }
    
    QPushButton:pressed {
        background-color: #005a9e;
    }
    """
    self.setStyleSheet(style)
```

## Threading et opérations asynchrones

### QThread pour opérations longues

```python
from PySide6.QtCore import QThread, Signal

class APIWorker(QThread):
    # Signaux pour communiquer avec l'interface
    data_loaded = Signal(list)
    error_occurred = Signal(str)
    
    def __init__(self, api_client, operation, **kwargs):
        super().__init__()
        self.api_client = api_client
        self.operation = operation
        self.kwargs = kwargs
    
    def run(self):
        try:
            if self.operation == "load_users":
                data = self.api_client.get_users()
                self.data_loaded.emit(data)
        except Exception as e:
            self.error_occurred.emit(str(e))

# Utilisation dans l'interface
def load_users_async(self):
    self.worker = APIWorker(self.api_client, "load_users")
    self.worker.data_loaded.connect(self.on_users_loaded)
    self.worker.error_occurred.connect(self.on_error)
    self.worker.start()

@Slot(list)
def on_users_loaded(self, users):
    self.populate_user_table(users)
```

## Tests de l'interface

### Tests unitaires avec pytest-qt

```python
import pytest
from PySide6.QtWidgets import QApplication
from gui_client.main_window import MainWindow

@pytest.fixture
def app():
    return QApplication([])

@pytest.fixture
def main_window(app):
    return MainWindow()

def test_main_window_creation(main_window):
    assert main_window.windowTitle() == "Gestionnaire CRUD"
    assert main_window.tabs.count() == 2

def test_user_form_validation(main_window, qtbot):
    user_form = main_window.users_tab.user_form
    
    # Simuler la saisie
    qtbot.keyClicks(user_form.email_input, "test@exemple.com")
    qtbot.keyClicks(user_form.nom_input, "Test")
    qtbot.keyClicks(user_form.prenom_input, "Utilisateur")
    
    # Vérifier les données
    data = user_form.get_form_data()
    assert data["email"] == "test@exemple.com"
    assert data["nom"] == "Test"
    assert data["prenom"] == "Utilisateur"
```

Cette architecture PySide6 offre une interface moderne et réactive pour votre API FastAPI.

Passez au module suivant : **07-questions-exercices.md**
