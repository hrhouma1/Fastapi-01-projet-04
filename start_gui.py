#!/usr/bin/env python3
"""
Script principal pour démarrer l'interface graphique
Usage: python start_gui.py
"""

import sys
import os

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == "__main__":
    try:
        from presentation.launchers.run_gui import main
        main()
    except ImportError as e:
        print("❌ Erreur d'importation:", e)
        print("\n💡 Solutions possibles:")
        print("1. Installer PySide6: pip install PySide6")
        print("2. Installer toutes les dépendances: pip install -r config/requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)
