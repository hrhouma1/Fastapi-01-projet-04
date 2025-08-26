"""
Interface graphique PySide6 pour l'API FastAPI CRUD

Ce package contient tous les composants nécessaires pour une interface graphique
moderne permettant de gérer les utilisateurs et articles via l'API FastAPI.

Modules:
- api_client: Client pour communiquer avec l'API REST
- main_window: Fenêtre principale et composants UI
"""

from .api_client import FastAPIClient
from .main_window import MainWindow, main

__version__ = "1.0.0"
__author__ = "FastAPI CRUD GUI"

__all__ = ["FastAPIClient", "MainWindow", "main"]
