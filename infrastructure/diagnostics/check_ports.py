#!/usr/bin/env python3
"""
Script de diagnostic des ports pour le développement
Usage: python infrastructure/diagnostics/check_ports.py [--kill-port PORT] [--kill-all-python]
"""

import argparse
import socket
import subprocess
import sys
import os

def is_port_in_use(port, host='localhost'):
    """Vérifie si un port est utilisé"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def get_port_info_windows(port):
    """Obtient les informations d'un port sur Windows"""
    try:
        result = subprocess.run(
            f'netstat -ano | findstr :{port}',
            shell=True, capture_output=True, text=True
        )
        
        processes = []
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        processes.append({
                            'port': port,
                            'pid': parts[-1],
                            'state': 'LISTENING'
                        })
        return processes
    except Exception:
        return []

def get_process_name_windows(pid):
    """Obtient le nom d'un processus par son PID sur Windows"""
    try:
        result = subprocess.run(
            f'tasklist /FI "PID eq {pid}" /FO CSV /NH',
            shell=True, capture_output=True, text=True
        )
        if result.stdout:
            # Nettoyer la sortie CSV
            line = result.stdout.strip().replace('"', '')
            parts = line.split(',')
            if len(parts) >= 1:
                return parts[0]
        return "Inconnu"
    except Exception:
        return "Erreur"

def kill_process_windows(pid, force=True):
    """Arrête un processus sur Windows"""
    try:
        cmd = f'taskkill /PID {pid}'
        if force:
            cmd += ' /F'
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def kill_all_python_windows():
    """Arrête tous les processus Python sur Windows"""
    try:
        result = subprocess.run(
            'taskkill /IM python.exe /F',
            shell=True, capture_output=True, text=True
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def check_development_ports():
    """Vérifie les ports couramment utilisés en développement"""
    common_ports = [3000, 3001, 5000, 8000, 8080, 8001, 9000]
    
    print("🔍 Diagnostic des ports de développement")
    print("=" * 50)
    
    active_ports = []
    
    for port in common_ports:
        if is_port_in_use(port):
            active_ports.append(port)
            print(f"Port {port:>4} : ", end="")
            
            if os.name == 'nt':  # Windows
                processes = get_port_info_windows(port)
                if processes:
                    for proc in processes:
                        process_name = get_process_name_windows(proc['pid'])
                        print(f"🔴 OCCUPÉ - {process_name} (PID: {proc['pid']})")
                else:
                    print("🔴 OCCUPÉ - Processus non identifié")
            else:
                print("🔴 OCCUPÉ")
        else:
            print(f"Port {port:>4} : 🟢 LIBRE")
    
    return active_ports

def show_python_processes():
    """Affiche tous les processus Python actifs"""
    print("\n🐍 Processus Python actifs")
    print("-" * 30)
    
    if os.name == 'nt':  # Windows
        try:
            result = subprocess.run(
                'tasklist /FI "IMAGENAME eq python.exe" /FO TABLE',
                shell=True, capture_output=True, text=True
            )
            if "python.exe" in result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines[3:]:  # Skip header lines
                    if line.strip() and 'python.exe' in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            print(f"  • {parts[0]} (PID: {parts[1]})")
            else:
                print("  Aucun processus Python trouvé")
        except Exception:
            print("  Erreur lors de la recherche des processus Python")
    else:
        # Pour macOS/Linux
        try:
            result = subprocess.run(
                ['ps', 'aux'], capture_output=True, text=True
            )
            python_lines = [line for line in result.stdout.split('\n') if 'python' in line.lower()]
            if python_lines:
                for line in python_lines:
                    parts = line.split()
                    if len(parts) >= 2:
                        print(f"  • PID: {parts[1]} - {' '.join(parts[10:])}")
            else:
                print("  Aucun processus Python trouvé")
        except Exception:
            print("  Erreur lors de la recherche des processus Python")

def main():
    parser = argparse.ArgumentParser(description='Diagnostic et gestion des ports de développement')
    parser.add_argument('--kill-port', type=int, help='Arrêter le processus utilisant ce port')
    parser.add_argument('--kill-all-python', action='store_true', help='Arrêter tous les processus Python')
    parser.add_argument('--show-commands', action='store_true', help='Afficher les commandes utiles')
    
    args = parser.parse_args()
    
    if args.kill_all_python:
        print("⚠️  Arrêt de tous les processus Python...")
        if os.name == 'nt':
            success, output = kill_all_python_windows()
            if success:
                print("✅ Tous les processus Python ont été arrêtés")
            else:
                print(f"❌ Erreur : {output}")
        else:
            print("❌ Fonctionnalité non implémentée pour ce système")
        return
    
    if args.kill_port:
        port = args.kill_port
        print(f"⚠️  Tentative d'arrêt du processus sur le port {port}...")
        
        if os.name == 'nt':
            processes = get_port_info_windows(port)
            if processes:
                for proc in processes:
                    pid = proc['pid']
                    process_name = get_process_name_windows(pid)
                    print(f"   Arrêt de {process_name} (PID: {pid})")
                    
                    success, output = kill_process_windows(pid)
                    if success:
                        print(f"✅ Processus {pid} arrêté")
                    else:
                        print(f"❌ Erreur : {output}")
            else:
                print(f"❌ Aucun processus trouvé sur le port {port}")
        else:
            print("❌ Fonctionnalité non implémentée pour ce système")
        return
    
    if args.show_commands:
        print("🛠️  Commandes utiles pour la gestion des ports")
        print("=" * 50)
        
        if os.name == 'nt':
            print("Windows :")
            print("  • Voir les ports : netstat -ano")
            print("  • Port spécifique : netstat -ano | findstr :8000")
            print("  • Processus Python : tasklist | findstr python")
            print("  • Arrêter par PID : taskkill /PID <PID> /F")
            print("  • Arrêter Python : taskkill /IM python.exe /F")
        else:
            print("macOS/Linux :")
            print("  • Voir les ports : lsof -i")
            print("  • Port spécifique : lsof -i :8000")
            print("  • Processus Python : ps aux | grep python")
            print("  • Arrêter par PID : kill -9 <PID>")
            print("  • Arrêter Python : pkill python")
        
        print("\nScripts de ce projet :")
        print("  • Démarrage sécurisé : python business/services/safe_start.py")
        print("  • Diagnostic : python infrastructure/diagnostics/check_ports.py")
        print("  • Port libre : python business/services/safe_start.py --auto-port")
        print("  • Arrêt forcé : python business/services/safe_start.py --force-kill")
        return
    
    # Diagnostic standard
    active_ports = check_development_ports()
    show_python_processes()
    
    if active_ports:
        print(f"\n📊 Résumé : {len(active_ports)} port(s) occupé(s)")
        print("\nCommandes suggérées :")
        for port in active_ports:
            print(f"  • Libérer le port {port} : python infrastructure/diagnostics/check_ports.py --kill-port {port}")
        print("  • Arrêter tous les Python : python infrastructure/diagnostics/check_ports.py --kill-all-python")
        print("  • Démarrer avec port auto : python business/services/safe_start.py --auto-port")
    else:
        print("\n✅ Tous les ports de développement sont libres !")
        print("   Vous pouvez démarrer votre API : python business/services/safe_start.py")

if __name__ == "__main__":
    main()
