#!/usr/bin/env python3
"""
Script de diagnostic du système et des ports
Usage: python check_system.py [options]
"""

import sys
import os

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == "__main__":
    try:
        from infrastructure.diagnostics.check_ports import main
        main()
    except ImportError as e:
        print("❌ Erreur d'importation:", e)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)
