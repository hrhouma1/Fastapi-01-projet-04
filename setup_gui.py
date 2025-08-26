#!/usr/bin/env python3
"""
Script de configuration de l'interface graphique PySide6

Usage: python setup_gui.py
"""

import os
import sys
import subprocess
import platform


def check_python_version():
    """Vérifie la version de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 ou supérieur requis")
        print(f"   Version actuelle : {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} détecté")
    return True


def check_virtual_env():
    """Vérifie si on est dans un environnement virtuel"""
    in_venv = (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )
    
    if in_venv:
        print("✅ Environnement virtuel activé")
        return True
    else:
        print("⚠️  Environnement virtuel non détecté")
        print("   Recommandation : activez votre venv")
        if platform.system() == "Windows":
            print("   Windows : venv\\Scripts\\activate")
        else:
            print("   macOS/Linux : source venv/bin/activate")
        return False


def install_dependencies():
    """Installe les dépendances GUI"""
    print("\n📦 Installation des dépendances GUI...")
    
    dependencies = [
        "PySide6>=6.7.0",
        "requests>=2.32.0"
    ]
    
    try:
        for dep in dependencies:
            print(f"   Installaton de {dep}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", dep
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   ✅ {dep} installé")
            else:
                print(f"   ❌ Erreur installation {dep}:")
                print(f"      {result.stderr}")
                return False
        
        print("✅ Toutes les dépendances GUI installées")
        return True
        
    except Exception as e:
        print(f"❌ Erreur d'installation : {e}")
        return False


def test_imports():
    """Teste l'importation des modules requis"""
    print("\n🧪 Test d'importation des modules...")
    
    modules_to_test = [
        ("PySide6.QtWidgets", "QApplication"),
        ("PySide6.QtCore", "Qt"),
        ("PySide6.QtGui", "QIcon"),
        ("requests", None)
    ]
    
    for module_name, class_name in modules_to_test:
        try:
            module = __import__(module_name, fromlist=[class_name] if class_name else [])
            if class_name:
                getattr(module, class_name)
            print(f"   ✅ {module_name} disponible")
        except ImportError as e:
            print(f"   ❌ Erreur import {module_name} : {e}")
            return False
    
    print("✅ Tous les modules requis sont disponibles")
    return True


def test_gui_creation():
    """Teste la création d'une application GUI basique"""
    print("\n🖥️  Test de création GUI...")
    
    try:
        from PySide6.QtWidgets import QApplication, QLabel, QWidget
        from PySide6.QtCore import Qt
        
        # Créer une application temporaire
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Créer une fenêtre de test
        window = QWidget()
        window.setWindowTitle("Test GUI FastAPI")
        window.resize(300, 100)
        
        label = QLabel("Interface GUI prête ! 🎉")
        label.setAlignment(Qt.AlignCenter)
        
        print("   ✅ Composants GUI créés avec succès")
        
        # Test de notre client API
        from gui_client.api_client import FastAPIClient
        client = FastAPIClient()
        print("   ✅ Client API importé")
        
        print("✅ Interface graphique prête à être utilisée")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur création GUI : {e}")
        return False


def create_desktop_shortcut():
    """Crée un raccourci sur le bureau (optionnel)"""
    print("\n🖱️  Création d'un raccourci... (optionnel)")
    
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        if not os.path.exists(desktop):
            desktop = os.path.join(os.path.expanduser("~"), "Bureau")  # Français
        
        if os.path.exists(desktop):
            shortcut_content = f"""#!/bin/bash
cd "{os.getcwd()}"
python run_gui.py
"""
            
            shortcut_path = os.path.join(desktop, "FastAPI_GUI.sh")
            
            if platform.system() != "Windows":
                with open(shortcut_path, 'w') as f:
                    f.write(shortcut_content)
                os.chmod(shortcut_path, 0o755)
                print(f"   ✅ Raccourci créé : {shortcut_path}")
            else:
                print("   ℹ️  Création de raccourci Windows non implémentée")
        else:
            print("   ℹ️  Bureau non trouvé, raccourci non créé")
            
    except Exception as e:
        print(f"   ⚠️  Erreur création raccourci : {e}")


def show_usage_instructions():
    """Affiche les instructions d'utilisation"""
    print("\n" + "🎉" * 30)
    print("🎉 CONFIGURATION GUI TERMINÉE AVEC SUCCÈS ! 🎉") 
    print("🎉" * 30)
    
    print("\n📋 INSTRUCTIONS D'UTILISATION :")
    print("\n1️⃣  Démarrer l'API FastAPI :")
    print("     python safe_start.py")
    
    print("\n2️⃣  Lancer l'interface graphique :")
    print("     python run_gui.py")
    
    print("\n3️⃣  Test d'intégration (optionnel) :")
    print("     python test_gui_integration.py")
    
    print("\n💡 CONSEILS :")
    print("   • L'API doit être démarrée AVANT l'interface")
    print("   • Indicateur vert = connexion OK")
    print("   • Utilisez 'python seed_data.py add' pour des données test")
    
    print("\n📚 DOCUMENTATION :")
    print("   • Guide complet : documentation1/04-interface-graphique.md")
    print("   • README GUI : gui_client/README.md")
    
    print("\n🔧 DÉVELOPPEMENT :")
    print("   • Code source GUI : gui_client/")
    print("   • Client API : gui_client/api_client.py")
    print("   • Interface principale : gui_client/main_window.py")


def main():
    """Configuration principale de l'interface graphique"""
    
    print("🖥️  CONFIGURATION DE L'INTERFACE GRAPHIQUE PYSIDE6")
    print("=" * 60)
    print("Interface moderne pour l'API FastAPI CRUD")
    print("=" * 60)
    
    # Vérifications préalables
    if not check_python_version():
        return False
    
    check_virtual_env()  # Avertissement seulement
    
    # Installation des dépendances
    if not install_dependencies():
        return False
    
    # Tests d'importation
    if not test_imports():
        return False
    
    # Test de création GUI
    if not test_gui_creation():
        return False
    
    # Raccourci optionnel
    create_desktop_shortcut()
    
    # Instructions finales
    show_usage_instructions()
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Configuration interrompue par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur critique : {e}")
        sys.exit(1)
