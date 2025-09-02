#!/usr/bin/env python3
"""
Script de lancement de l'interface graphique pour l'API FastAPI CRUD

Usage:
    python run_gui.py

Prérequis:
    - L'API FastAPI doit être démarrée (python safe_start.py)
    - PySide6 doit être installé (pip install -r requirements.txt)
"""

import sys
import os

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui_client.main_window import main

if __name__ == "__main__":
    print("🖥️  Démarrage de l'interface graphique FastAPI CRUD...")
    print("📡 Connexion par défaut : http://localhost:8000")
    print("⚠️  Assurez-vous que l'API FastAPI est démarrée !")
    print("=" * 60)
    
    try:
        main()
    except ImportError as e:
        print(f"❌ Erreur d'importation : {e}")
        print("📦 Installez les dépendances : pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Interface graphique fermée par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        sys.exit(1)
