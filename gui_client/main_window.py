"""
Fenêtre principale de l'interface graphique pour l'API FastAPI CRUD
"""

import sys
from typing import List, Dict, Optional
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QComboBox, QCheckBox, QSpinBox, QTextEdit, QSplitter, QGroupBox, QFormLayout,
    QHeaderView, QStatusBar, QFrame, QProgressBar
)
from PySide6.QtCore import Qt, QTimer, Signal, QThread
from PySide6.QtGui import QIcon, QFont, QPalette, QColor

from .api_client import FastAPIClient


class StatusIndicator(QFrame):
    """Indicateur de statut de connexion à l'API"""
    
    def __init__(self):
        super().__init__()
        self.setFixedSize(12, 12)
        self.setFrameStyle(QFrame.StyledPanel)
        self.set_disconnected()
    
    def set_connected(self):
        """Affiche l'état connecté (vert)"""
        self.setStyleSheet("background-color: #4CAF50; border-radius: 6px;")
        self.setToolTip("Connecté à l'API")
    
    def set_disconnected(self):
        """Affiche l'état déconnecté (rouge)"""
        self.setStyleSheet("background-color: #F44336; border-radius: 6px;")
        self.setToolTip("Déconnecté de l'API")
    
    def set_connecting(self):
        """Affiche l'état en cours de connexion (orange)"""
        self.setStyleSheet("background-color: #FF9800; border-radius: 6px;")
        self.setToolTip("Connexion en cours...")


class UsersTab(QWidget):
    """Onglet de gestion des utilisateurs"""
    
    def __init__(self, api_client: FastAPIClient):
        super().__init__()
        self.api_client = api_client
        self.setup_ui()
        self.refresh_users()
    
    def setup_ui(self):
        """Configure l'interface utilisateur de l'onglet utilisateurs"""
        layout = QVBoxLayout(self)
        
        # Section de création d'utilisateur
        create_group = QGroupBox("Créer un nouvel utilisateur")
        create_layout = QFormLayout(create_group)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("exemple@email.com")
        create_layout.addRow("Email:", self.email_input)
        
        self.nom_input = QLineEdit()
        create_layout.addRow("Nom:", self.nom_input)
        
        self.prenom_input = QLineEdit()
        create_layout.addRow("Prénom:", self.prenom_input)
        
        self.active_checkbox = QCheckBox("Utilisateur actif")
        self.active_checkbox.setChecked(True)
        create_layout.addRow("Statut:", self.active_checkbox)
        
        self.create_user_btn = QPushButton("Créer l'utilisateur")
        self.create_user_btn.clicked.connect(self.create_user)
        create_layout.addRow(self.create_user_btn)
        
        layout.addWidget(create_group)
        
        # Section liste des utilisateurs
        list_group = QGroupBox("Liste des utilisateurs")
        list_layout = QVBoxLayout(list_group)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("Actualiser")
        self.refresh_btn.clicked.connect(self.refresh_users)
        self.delete_user_btn = QPushButton("Supprimer")
        self.delete_user_btn.clicked.connect(self.delete_selected_user)
        self.delete_user_btn.setEnabled(False)
        
        buttons_layout.addWidget(self.refresh_btn)
        buttons_layout.addWidget(self.delete_user_btn)
        buttons_layout.addStretch()
        list_layout.addLayout(buttons_layout)
        
        # Table des utilisateurs
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels([
            "ID", "Email", "Nom", "Prénom", "Actif", "Articles"
        ])
        self.users_table.horizontalHeader().setStretchLastSection(True)
        self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.users_table.selectionModel().selectionChanged.connect(self.on_user_selected)
        list_layout.addWidget(self.users_table)
        
        layout.addWidget(list_group)
    
    def create_user(self):
        """Crée un nouvel utilisateur"""
        email = self.email_input.text().strip()
        nom = self.nom_input.text().strip()
        prenom = self.prenom_input.text().strip()
        is_active = self.active_checkbox.isChecked()
        
        if not email or not nom or not prenom:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs obligatoires.")
            return
        
        result = self.api_client.create_user(email, nom, prenom, is_active)
        
        if "error" in result:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la création: {result['error']}")
        else:
            QMessageBox.information(self, "Succès", f"Utilisateur créé avec l'ID: {result['id']}")
            # Vider les champs
            self.email_input.clear()
            self.nom_input.clear()
            self.prenom_input.clear()
            self.active_checkbox.setChecked(True)
            self.refresh_users()
            # Signaler aux autres onglets de se mettre à jour
            if hasattr(self, 'parent_window') and hasattr(self.parent_window, 'refresh_all_users_data'):
                self.parent_window.refresh_all_users_data()
    
    def refresh_users(self):
        """Actualise la liste des utilisateurs"""
        users = self.api_client.get_users()
        
        if isinstance(users, dict) and "error" in users:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement: {users['error']}")
            return
        
        self.users_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            self.users_table.setItem(row, 0, QTableWidgetItem(str(user['id'])))
            self.users_table.setItem(row, 1, QTableWidgetItem(user['email']))
            self.users_table.setItem(row, 2, QTableWidgetItem(user['nom']))
            self.users_table.setItem(row, 3, QTableWidgetItem(user['prenom']))
            self.users_table.setItem(row, 4, QTableWidgetItem("Oui" if user['is_active'] else "Non"))
            self.users_table.setItem(row, 5, QTableWidgetItem(str(len(user.get('items', [])))))
        
        # Ajuster la taille des colonnes
        self.users_table.resizeColumnsToContents()
    
    def on_user_selected(self):
        """Appelé quand un utilisateur est sélectionné"""
        selected = self.users_table.selectionModel().hasSelection()
        self.delete_user_btn.setEnabled(selected)
    
    def delete_selected_user(self):
        """Supprime l'utilisateur sélectionné"""
        current_row = self.users_table.currentRow()
        if current_row < 0:
            return
        
        user_id = self.users_table.item(current_row, 0).text()
        user_name = f"{self.users_table.item(current_row, 3).text()} {self.users_table.item(current_row, 2).text()}"
        
        reply = QMessageBox.question(
            self, "Confirmer la suppression",
            f"Êtes-vous sûr de vouloir supprimer l'utilisateur {user_name} ?\n"
            "Tous ses articles seront également supprimés.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            result = self.api_client.delete_user(int(user_id))
            
            if "error" in result:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression: {result['error']}")
            else:
                QMessageBox.information(self, "Succès", result['message'])
                self.refresh_users()
                # Signaler aux autres onglets de se mettre à jour
                if hasattr(self, 'parent_window') and hasattr(self.parent_window, 'refresh_all_users_data'):
                    self.parent_window.refresh_all_users_data()


class ItemsTab(QWidget):
    """Onglet de gestion des articles"""
    
    def __init__(self, api_client: FastAPIClient):
        super().__init__()
        self.api_client = api_client
        self.setup_ui()
        self.refresh_items()
        self.refresh_users_combo()
    
    def setup_ui(self):
        """Configure l'interface utilisateur de l'onglet articles"""
        layout = QVBoxLayout(self)
        
        # Section de création d'article
        create_group = QGroupBox("Créer un nouvel article")
        create_layout = QFormLayout(create_group)
        
        # Layout pour propriétaire avec bouton de rafraîchissement
        owner_layout = QHBoxLayout()
        self.owner_combo = QComboBox()
        self.refresh_owners_btn = QPushButton("↻")
        self.refresh_owners_btn.setMaximumWidth(30)
        self.refresh_owners_btn.setToolTip("Actualiser la liste des utilisateurs")
        self.refresh_owners_btn.clicked.connect(self.refresh_users_combo)
        
        owner_layout.addWidget(self.owner_combo)
        owner_layout.addWidget(self.refresh_owners_btn)
        
        owner_widget = QWidget()
        owner_widget.setLayout(owner_layout)
        create_layout.addRow("Propriétaire:", owner_widget)
        
        self.title_input = QLineEdit()
        create_layout.addRow("Titre:", self.title_input)
        
        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(60)
        create_layout.addRow("Description:", self.description_input)
        
        # Prix avec indication
        price_layout = QHBoxLayout()
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("25.50")
        price_layout.addWidget(self.price_input)
        price_layout.addWidget(QLabel("€"))
        create_layout.addRow("Prix:", price_layout)
        
        self.available_checkbox = QCheckBox("Article disponible")
        self.available_checkbox.setChecked(True)
        create_layout.addRow("Statut:", self.available_checkbox)
        
        self.create_item_btn = QPushButton("Créer l'article")
        self.create_item_btn.clicked.connect(self.create_item)
        create_layout.addRow(self.create_item_btn)
        
        layout.addWidget(create_group)
        
        # Section recherche
        search_group = QGroupBox("Rechercher des articles")
        search_layout = QHBoxLayout(search_group)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher par titre ou description...")
        self.search_input.returnPressed.connect(self.search_items)
        search_layout.addWidget(self.search_input)
        
        self.search_btn = QPushButton("Rechercher")
        self.search_btn.clicked.connect(self.search_items)
        search_layout.addWidget(self.search_btn)
        
        self.clear_search_btn = QPushButton("Effacer")
        self.clear_search_btn.clicked.connect(self.clear_search)
        search_layout.addWidget(self.clear_search_btn)
        
        layout.addWidget(search_group)
        
        # Section liste des articles
        list_group = QGroupBox("Liste des articles")
        list_layout = QVBoxLayout(list_group)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        self.refresh_items_btn = QPushButton("Actualiser")
        self.refresh_items_btn.clicked.connect(self.refresh_items)
        self.delete_item_btn = QPushButton("Supprimer")
        self.delete_item_btn.clicked.connect(self.delete_selected_item)
        self.delete_item_btn.setEnabled(False)
        
        buttons_layout.addWidget(self.refresh_items_btn)
        buttons_layout.addWidget(self.delete_item_btn)
        buttons_layout.addStretch()
        list_layout.addLayout(buttons_layout)
        
        # Table des articles
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(6)
        self.items_table.setHorizontalHeaderLabels([
            "ID", "Titre", "Description", "Prix", "Disponible", "Propriétaire"
        ])
        self.items_table.horizontalHeader().setStretchLastSection(True)
        self.items_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.items_table.selectionModel().selectionChanged.connect(self.on_item_selected)
        list_layout.addWidget(self.items_table)
        
        layout.addWidget(list_group)
    
    def refresh_users_combo(self):
        """Actualise la liste des utilisateurs dans le combo"""
        users = self.api_client.get_users()
        
        # Conserver la sélection actuelle si possible
        current_user_id = None
        if self.owner_combo.currentIndex() >= 0:
            current_user_id = self.owner_combo.currentData()
        
        self.owner_combo.clear()
        if isinstance(users, list):
            for user in users:
                self.owner_combo.addItem(
                    f"{user['prenom']} {user['nom']} ({user['email']})",
                    user['id']
                )
        
        # Restaurer la sélection si possible
        if current_user_id is not None:
            for i in range(self.owner_combo.count()):
                if self.owner_combo.itemData(i) == current_user_id:
                    self.owner_combo.setCurrentIndex(i)
                    break
    
    def create_item(self):
        """Crée un nouvel article"""
        if self.owner_combo.count() == 0:
            QMessageBox.warning(self, "Erreur", "Aucun utilisateur disponible. Créez d'abord un utilisateur.")
            return
        
        user_id = self.owner_combo.currentData()
        title = self.title_input.text().strip()
        description = self.description_input.toPlainText().strip()
        price_str = self.price_input.text().strip()
        is_available = self.available_checkbox.isChecked()
        
        if not title or not description or not price_str:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs obligatoires.")
            return
        
        try:
            price_cents = self.api_client.parse_price(price_str)
        except:
            QMessageBox.warning(self, "Erreur", "Prix invalide. Utilisez le format: 25.50")
            return
        
        result = self.api_client.create_item(user_id, title, description, price_cents, is_available)
        
        if "error" in result:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la création: {result['error']}")
        else:
            QMessageBox.information(self, "Succès", f"Article créé avec l'ID: {result['id']}")
            # Vider les champs
            self.title_input.clear()
            self.description_input.clear()
            self.price_input.clear()
            self.available_checkbox.setChecked(True)
            self.refresh_items()
    
    def refresh_items(self):
        """Actualise la liste des articles"""
        items = self.api_client.get_items()
        
        if isinstance(items, dict) and "error" in items:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement: {items['error']}")
            return
        
        self._populate_items_table(items)
    
    def search_items(self):
        """Recherche des articles"""
        query = self.search_input.text().strip()
        if not query:
            self.refresh_items()
            return
        
        if len(query) < 2:
            QMessageBox.warning(self, "Recherche", "Veuillez saisir au moins 2 caractères pour la recherche.")
            return
        
        # Afficher un message pendant la recherche
        self.search_btn.setText("Recherche...")
        self.search_btn.setEnabled(False)
        
        try:
            items = self.api_client.search_items(query)
            
            if isinstance(items, dict) and "error" in items:
                QMessageBox.warning(self, "Recherche", f"Erreur lors de la recherche: {items['error']}")
                return
            
            if isinstance(items, list):
                if len(items) == 0:
                    QMessageBox.information(self, "Recherche", f"Aucun article trouvé pour '{query}'.")
                else:
                    # Afficher le nombre de résultats trouvés
                    self.status_label = QLabel(f"🔍 {len(items)} résultat(s) trouvé(s) pour '{query}'")
                    self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold; padding: 5px;")
                    
                self._populate_items_table(items)
            
        finally:
            # Remettre le bouton dans son état normal
            self.search_btn.setText("Rechercher")
            self.search_btn.setEnabled(True)
    
    def clear_search(self):
        """Efface la recherche et affiche tous les articles"""
        self.search_input.clear()
        self.refresh_items()
    
    def _populate_items_table(self, items: List[Dict]):
        """Remplit la table avec les articles"""
        self.items_table.setRowCount(len(items))
        
        for row, item in enumerate(items):
            self.items_table.setItem(row, 0, QTableWidgetItem(str(item['id'])))
            self.items_table.setItem(row, 1, QTableWidgetItem(item['title']))
            self.items_table.setItem(row, 2, QTableWidgetItem(item['description'][:50] + "..."))
            self.items_table.setItem(row, 3, QTableWidgetItem(self.api_client.format_price(item['price'])))
            self.items_table.setItem(row, 4, QTableWidgetItem("Oui" if item['is_available'] else "Non"))
            self.items_table.setItem(row, 5, QTableWidgetItem(f"ID: {item['owner_id']}"))
        
        # Ajuster la taille des colonnes
        self.items_table.resizeColumnsToContents()
    
    def on_item_selected(self):
        """Appelé quand un article est sélectionné"""
        selected = self.items_table.selectionModel().hasSelection()
        self.delete_item_btn.setEnabled(selected)
    
    def delete_selected_item(self):
        """Supprime l'article sélectionné"""
        current_row = self.items_table.currentRow()
        if current_row < 0:
            return
        
        item_id = self.items_table.item(current_row, 0).text()
        item_title = self.items_table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, "Confirmer la suppression",
            f"Êtes-vous sûr de vouloir supprimer l'article '{item_title}' ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            result = self.api_client.delete_item(int(item_id))
            
            if "error" in result:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression: {result['error']}")
            else:
                QMessageBox.information(self, "Succès", result['message'])
                self.refresh_items()


class MainWindow(QMainWindow):
    """Fenêtre principale de l'application"""
    
    def __init__(self):
        super().__init__()
        self.api_client = FastAPIClient()
        self.setup_ui()
        self.setup_status_bar()
        self.setup_connection_timer()
        self.setup_signals()
    
    def setup_ui(self):
        """Configure l'interface utilisateur principale"""
        self.setWindowTitle("Interface Graphique - API FastAPI CRUD")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central avec onglets
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # En-tête avec informations de connexion
        header_group = QGroupBox("Configuration de l'API")
        header_layout = QHBoxLayout(header_group)
        
        header_layout.addWidget(QLabel("URL de l'API:"))
        self.api_url_input = QLineEdit(self.api_client.base_url)
        self.api_url_input.textChanged.connect(self.update_api_url)
        header_layout.addWidget(self.api_url_input)
        
        self.test_connection_btn = QPushButton("Tester la connexion")
        self.test_connection_btn.clicked.connect(self.test_connection)
        header_layout.addWidget(self.test_connection_btn)
        
        self.status_indicator = StatusIndicator()
        header_layout.addWidget(self.status_indicator)
        
        layout.addWidget(header_group)
        
        # Onglets principales
        self.tab_widget = QTabWidget()
        
        # Onglet utilisateurs
        self.users_tab = UsersTab(self.api_client)
        self.tab_widget.addTab(self.users_tab, "Utilisateurs")
        
        # Onglet articles
        self.items_tab = ItemsTab(self.api_client)
        self.tab_widget.addTab(self.items_tab, "Articles")
        
        layout.addWidget(self.tab_widget)
    
    def setup_status_bar(self):
        """Configure la barre de statut"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Prêt")
    
    def setup_connection_timer(self):
        """Configure le timer pour vérifier la connexion"""
        self.connection_timer = QTimer()
        self.connection_timer.timeout.connect(self.check_connection)
        self.connection_timer.start(5000)  # Vérifier toutes les 5 secondes
        self.check_connection()  # Vérification initiale
    
    def update_api_url(self, url: str):
        """Met à jour l'URL de l'API"""
        self.api_client.base_url = url.rstrip('/')
    
    def test_connection(self):
        """Teste la connexion à l'API manuellement"""
        self.status_indicator.set_connecting()
        self.status_bar.showMessage("Test de connexion...")
        
        if self.api_client.test_connection():
            self.status_indicator.set_connected()
            self.status_bar.showMessage("Connexion réussie")
            QMessageBox.information(self, "Connexion", "Connexion à l'API réussie !")
        else:
            self.status_indicator.set_disconnected()
            self.status_bar.showMessage("Connexion échouée")
            QMessageBox.warning(self, "Connexion", "Impossible de se connecter à l'API.\nVérifiez que le serveur FastAPI est démarré.")
    
    def check_connection(self):
        """Vérifie automatiquement la connexion à l'API"""
        if self.api_client.test_connection():
            self.status_indicator.set_connected()
            self.status_bar.showMessage("Connecté à l'API")
        else:
            self.status_indicator.set_disconnected()
            self.status_bar.showMessage("API non disponible")
    
    def setup_signals(self):
        """Configure les signaux entre onglets"""
        # Connecter les onglets à la fenêtre principale pour synchronisation
        self.users_tab.parent_window = self
        self.items_tab.parent_window = self
    
    def refresh_all_users_data(self):
        """Met à jour toutes les données utilisateur dans tous les onglets"""
        # Actualiser la combobox des utilisateurs dans l'onglet articles
        self.items_tab.refresh_users_combo()
        print("🔄 Mise à jour de la liste des utilisateurs dans tous les onglets")


def main():
    """Point d'entrée de l'application"""
    app = QApplication(sys.argv)
    
    # Style de l'application
    app.setStyle("Fusion")
    
    # Fenêtre principale
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
