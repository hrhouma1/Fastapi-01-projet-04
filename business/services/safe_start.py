#!/usr/bin/env python3
"""
Script de démarrage sécurisé pour l'API FastAPI CRUD
Usage: python business/services/safe_start.py [--port 8000] [--auto-port] [--force-kill]
"""

import argparse
import socket
import subprocess
import sys
import time
import os

def is_port_in_use(port, host='localhost'):
    """Vérifie si un port est utilisé"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def find_process_on_port_windows(port):
    """Trouve le processus utilisant un port sur Windows"""
    try:
        import subprocess
        result = subprocess.run(
            f'netstat -ano | findstr :{port}',
            shell=True, capture_output=True, text=True
        )
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        return {'pid': parts[-1], 'port': port}
        return None
    except Exception:
        return None

def kill_process_windows(pid, force=False):
    """Arrête un processus sur Windows"""
    try:
        cmd = f'taskkill /PID {pid}'
        if force:
            cmd += ' /F'
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False

def find_free_port(start_port, max_attempts=10):
    """Trouve un port libre"""
    for i in range(max_attempts):
        port = start_port + i
        if not is_port_in_use(port):
            return port
    return None

def check_environment():
    """Vérifie que l'environnement est correctement configuré"""
    if not os.path.exists('business/api/main.py'):
        print("❌ Fichier business/api/main.py non trouvé")
        print("   Assurez-vous d'être dans le répertoire racine du projet")
        return False
    
    try:
        import fastapi
        import uvicorn
        print("✅ Dépendances FastAPI disponibles")
        return True
    except ImportError as e:
        print(f"❌ Dépendances manquantes : {e}")
        print("   Exécutez : pip install -r requirements.txt")
        return False

def main():
    parser = argparse.ArgumentParser(description='Démarrage sécurisé de l\'API FastAPI CRUD')
    parser.add_argument('--port', type=int, default=8000, help='Port de démarrage (défaut: 8000)')
    parser.add_argument('--host', default='0.0.0.0', help='Adresse d\'écoute (défaut: 0.0.0.0)')
    parser.add_argument('--force-kill', action='store_true', help='Forcer l\'arrêt des processus conflictuels')
    parser.add_argument('--auto-port', action='store_true', help='Chercher automatiquement un port libre')
    parser.add_argument('--no-reload', action='store_true', help='Désactiver le rechargement automatique')
    
    args = parser.parse_args()
    
    print("🚀 Démarrage sécurisé de l'API FastAPI CRUD")
    print("=" * 50)
    
    # Vérifier l'environnement
    if not check_environment():
        sys.exit(1)
    
    original_port = args.port
    
    # Vérifier si le port est utilisé
    if is_port_in_use(args.port):
        print(f"⚠️  Port {args.port} déjà utilisé")
        
        # Chercher le processus sur Windows
        if os.name == 'nt':  # Windows
            proc_info = find_process_on_port_windows(args.port)
            if proc_info:
                print(f"   Processus PID : {proc_info['pid']}")
                
                if args.force_kill:
                    print(f"🔄 Arrêt forcé du processus {proc_info['pid']}...")
                    if kill_process_windows(proc_info['pid'], force=True):
                        print("✅ Processus arrêté")
                        time.sleep(2)  # Attendre que le port se libère
                    else:
                        print("❌ Impossible d'arrêter le processus")
                        if args.auto_port:
                            pass  # Continuer avec recherche de port
                        else:
                            sys.exit(1)
                elif args.auto_port:
                    pass  # Continuer avec recherche de port
                else:
                    print("\nOptions disponibles :")
                    print("1. Arrêter manuellement l'autre processus (Ctrl+C dans son terminal)")
                    print("2. Relancer avec --auto-port pour utiliser un autre port")
                    print("3. Relancer avec --force-kill pour arrêter automatiquement")
                    print(f"4. Utiliser : taskkill /PID {proc_info['pid']} /F")
                    sys.exit(1)
        
        # Chercher un port libre si demandé
        if args.auto_port and is_port_in_use(args.port):
            new_port = find_free_port(args.port + 1)
            if new_port:
                args.port = new_port
                print(f"🔄 Utilisation du port {new_port} au lieu de {original_port}")
            else:
                print("❌ Aucun port libre trouvé dans la plage")
                sys.exit(1)
    else:
        print(f"✅ Port {args.port} disponible")
    
    # Préparer la commande uvicorn
    cmd = [
        sys.executable, '-m', 'uvicorn',
        'business.api.main:app', 
        '--host', args.host, 
        '--port', str(args.port)
    ]
    
    if not args.no_reload:
        cmd.append('--reload')
    
    print(f"\n🌐 Démarrage de l'API sur http://{args.host}:{args.port}")
    print(f"📚 Documentation : http://localhost:{args.port}/docs")
    print(f"🔄 Rechargement automatique : {'activé' if not args.no_reload else 'désactivé'}")
    print("\n⏹️  Appuyez sur Ctrl+C pour arrêter le serveur")
    print("-" * 50)
    
    try:
        # Démarrer l'application
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n👋 Arrêt de l'API FastAPI")
        print("   Merci d'avoir utilisé l'API CRUD !")
    except FileNotFoundError:
        print("❌ Erreur : uvicorn non trouvé")
        print("   Assurez-vous que l'environnement virtuel est activé")
        print("   Et que les dépendances sont installées : pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
