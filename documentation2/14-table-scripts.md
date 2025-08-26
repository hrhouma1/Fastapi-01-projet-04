# Table de classification des scripts Python

## Table complète des scripts par couches architecturales

| N° | Nom du Script | Couche | Type | Description |
|----|---------------|--------|------|-------------|
| 1 | `main.py` | Business Logique | API | Point d'entrée FastAPI avec endpoints REST |
| 2 | `database.py` | Database | Config | Configuration SQLAlchemy et sessions BDD |
| 3 | `models.py` | Database | ORM | Modèles SQLAlchemy et relations |
| 4 | `schemas.py` | Business Logique | Validation | Schémas Pydantic et validation métier |
| 5 | `crud.py` | Database | Repository | Opérations CRUD et accès aux données |
| 6 | `gui_client/main_window.py` | Présentation | Interface | Fenêtre principale PySide6 |
| 7 | `gui_client/api_client.py` | Présentation | Communication | Client HTTP pour communication avec API |
| 8 | `gui_client/__init__.py` | Présentation | Package | Marqueur de package GUI |
| 9 | `run_gui.py` | Présentation | Launcher | Point d'entrée interface graphique |
| 10 | `setup_gui.py` | Présentation | Setup | Installation et configuration GUI |
| 11 | `safe_start.py` | Business Logique | Service | Démarrage sécurisé de l'API |
| 12 | `seed_data.py` | Database | Utilitaire | Génération de données de test |
| 13 | `exemple_utilisation.py` | Business Logique | Documentation | Exemples d'utilisation de l'API |
| 14 | `test_coherence.py` | Business Logique | Tests | Tests de cohérence système |
| 15 | `test_gui_integration.py` | Présentation | Tests | Tests d'intégration GUI-API |
| 16 | `check_ports.py` | Infrastructure | Diagnostic | Vérification des ports réseau |

## Répartition par couches

### Couche PRÉSENTATION (5 scripts)
| Script | Rôle Principal |
|--------|----------------|
| `gui_client/main_window.py` | Interface graphique principale |
| `gui_client/api_client.py` | Client de communication HTTP |
| `gui_client/__init__.py` | Package GUI |
| `run_gui.py` | Launcher interface |
| `setup_gui.py` | Configuration GUI |

### Couche BUSINESS LOGIQUE (4 scripts)
| Script | Rôle Principal |
|--------|----------------|
| `main.py` | API REST FastAPI |
| `schemas.py` | Validation Pydantic |
| `safe_start.py` | Service de démarrage |
| `exemple_utilisation.py` | Documentation API |

### Couche DATABASE (3 scripts)
| Script | Rôle Principal |
|--------|----------------|
| `database.py` | Configuration BDD |
| `models.py` | Modèles ORM |
| `crud.py` | Repository et accès données |

### Scripts TRANSVERSAUX (4 scripts)
| Script | Couche Principale | Rôle |
|--------|-------------------|------|
| `seed_data.py` | Database | Données de test |
| `test_coherence.py` | Business Logique | Tests système |
| `test_gui_integration.py` | Présentation | Tests GUI |
| `check_ports.py` | Infrastructure | Diagnostic réseau |

## Statistics par couche

| Couche | Nombre de Scripts | Pourcentage |
|--------|-------------------|-------------|
| **Présentation** | 5 | 31.25% |
| **Business Logique** | 4 | 25% |
| **Database** | 3 | 18.75% |
| **Transversaux** | 4 | 25% |
| **TOTAL** | **16** | **100%** |

## Table par ordre alphabétique

| Script | Couche |
|--------|--------|
| `check_ports.py` | Infrastructure |
| `crud.py` | Database |
| `database.py` | Database |
| `exemple_utilisation.py` | Business Logique |
| `gui_client/__init__.py` | Présentation |
| `gui_client/api_client.py` | Présentation |
| `gui_client/main_window.py` | Présentation |
| `main.py` | Business Logique |
| `models.py` | Database |
| `run_gui.py` | Présentation |
| `safe_start.py` | Business Logique |
| `schemas.py` | Business Logique |
| `seed_data.py` | Database |
| `setup_gui.py` | Présentation |
| `test_coherence.py` | Business Logique |
| `test_gui_integration.py` | Présentation |

## Table des dépendances principales

| Script | Dépend de | Utilisé par |
|--------|-----------|-------------|
| `main.py` | `schemas.py`, `crud.py`, `database.py` | `gui_client/api_client.py` |
| `crud.py` | `models.py`, `database.py` | `main.py` |
| `models.py` | `database.py` | `crud.py` |
| `schemas.py` | - | `main.py` |
| `database.py` | - | `models.py`, `crud.py` |
| `gui_client/main_window.py` | `gui_client/api_client.py` | `run_gui.py` |
| `gui_client/api_client.py` | - | `gui_client/main_window.py` |
| `run_gui.py` | `gui_client/main_window.py` | - |

## Table des technologies par script

| Script | Technologies Principales |
|--------|-------------------------|
| `main.py` | FastAPI, Uvicorn, Pydantic |
| `database.py` | SQLAlchemy, SQLite |
| `models.py` | SQLAlchemy ORM |
| `schemas.py` | Pydantic, typing |
| `crud.py` | SQLAlchemy Session |
| `gui_client/main_window.py` | PySide6, Qt |
| `gui_client/api_client.py` | requests, JSON |
| `run_gui.py` | PySide6, sys |
| `setup_gui.py` | subprocess, pip |
| `safe_start.py` | subprocess, socket |

## Table des patterns architecturaux

| Script | Pattern Principal |
|--------|-------------------|
| `main.py` | Controller, Dependency Injection |
| `crud.py` | Repository |
| `models.py` | Active Record, ORM |
| `schemas.py` | DTO (Data Transfer Object) |
| `database.py` | Factory |
| `gui_client/main_window.py` | MVC, Observer |
| `gui_client/api_client.py` | Proxy |
| `safe_start.py` | Service Layer |

Cette table offre une vue d'ensemble complète et structurée de tous les scripts Python du projet FastAPI CRUD.
