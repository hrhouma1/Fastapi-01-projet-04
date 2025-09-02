#!/usr/bin/env python3
"""
Script principal pour démarrer l'API FastAPI
Usage: python start_api.py [options]
"""

import sys
import os

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == "__main__":
    try:
        from business.services.safe_start import main
        main()
    except ImportError as e:
        print("❌ Erreur d'importation:", e)
        print("\n💡 Assurez-vous que les dépendances sont installées:")
        print("   pip install -r config/requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)
