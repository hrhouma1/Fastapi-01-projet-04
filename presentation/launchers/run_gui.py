#!/usr/bin/env python3
"""
Script de lancement de l'interface graphique PySide6
Usage: python presentation/launchers/run_gui.py
"""

import sys
import os

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from presentation.gui.main_window import main
    
    if __name__ == "__main__":
        print("🚀 Démarrage de l'interface graphique...")
        print("📱 Application FastAPI CRUD - Interface PySide6")
        print("-" * 50)
        main()
        
except ImportError as e:
    print("❌ Erreur d'importation:", e)
    print("\n💡 Solutions possibles:")
    print("1. Installer PySide6: pip install PySide6")
    print("2. Installer les dépendances: pip install -r requirements.txt")
    print("3. Vérifier que vous êtes dans le bon répertoire")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erreur inattendue: {e}")
    sys.exit(1)
