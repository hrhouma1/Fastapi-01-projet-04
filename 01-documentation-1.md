# 🛠️ Guide de Gestion des Processus et Ports

## 📋 Table des matières
1. [Comprendre l'erreur de port occupé](#comprendre-lerreur-de-port-occupé)
2. [Identifier les processus et ports](#identifier-les-processus-et-ports)
3. [Arrêter des processus](#arrêter-des-processus)
4. [Commandes spécifiques par technologie](#commandes-spécifiques-par-technologie)
5. [Prévention et bonnes pratiques](#prévention-et-bonnes-pratiques)
6. [Scripts d'automatisation](#scripts-dautomatisation)

---

## 🚨 Comprendre l'erreur de port occupé

### Erreur typique :
```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000): 
[winerror 10048] only one usage of each socket address is normally permitted
```

### Causes communes :
- ✅ Une instance précédente de l'application n'a pas été correctement fermée
- ✅ Un autre service utilise le même port
- ✅ L'application a planté et le port n'a pas été libéré
- ✅ Plusieurs développeurs utilisent le même port simultanément

---

## 🔍 Identifier les processus et ports

### 1. **Vérifier quel processus utilise un port spécifique**

#### Sur Windows :
```bash
# Voir tous les processus utilisant des ports
netstat -ano

# Voir spécifiquement le port 8000
netstat -ano | findstr :8000

# Avec plus de détails
netstat -aon | findstr :8000

# Format plus lisible
netstat -ano | findstr LISTENING | findstr :8000
```

#### Sur macOS/Linux :
```bash
# Voir le processus sur le port 8000
lsof -i :8000

# Voir tous les ports en écoute
netstat -tulpn | grep LISTEN

# Avec ss (plus moderne)
ss -tlnp | grep :8000
```

### 2. **Identifier les processus Python en cours**

#### Sur Windows :
```bash
# Lister tous les processus Python
tasklist /fi "imagename eq python.exe"

# Avec plus de détails
tasklist /fi "imagename eq python.exe" /fo table /v

# Rechercher par nom de fenêtre
tasklist /fi "windowtitle eq FastAPI*"
```

#### Sur macOS/Linux :
```bash
# Processus Python
ps aux | grep python

# Processus contenant "main.py"
ps aux | grep main.py

# Avec pgrep
pgrep -f python
```

### 3. **Commandes de diagnostic avancées**

```bash
# Windows - Voir les connexions réseau en temps réel
netstat -b -p TCP

# Windows - Processus avec le plus de détails
wmic process where "name='python.exe'" get ProcessId,CommandLine,ParentProcessId

# Vérifier les ports disponibles dans une plage
for /L %i in (8000,1,8010) do @netstat -ano | findstr :%i && echo Port %i is in use
```

---

## ⚡ Arrêter des processus

### 1. **Méthodes douces (recommandées)**

#### Arrêt normal avec Ctrl+C :
```bash
# Dans le terminal où l'application tourne
Ctrl + C  # ou Ctrl + Break sur Windows
```

#### Fermeture propre des applications :
```bash
# Python FastAPI avec uvicorn
# Appuyer sur Ctrl+C dans le terminal

# Pour Node.js
Ctrl + C

# Pour les applications en arrière-plan
# Utiliser les gestionnaires de tâches
```

### 2. **Arrêt forcé par PID (Process ID)**

#### Sur Windows :
```bash
# Trouver le PID
netstat -ano | findstr :8000
# Exemple de sortie : TCP 0.0.0.0:8000 0.0.0.0:0 LISTENING 1234

# Arrêter par PID (1234 dans l'exemple)
taskkill /PID 1234 /F

# Arrêter tous les processus Python
taskkill /IM python.exe /F

# Arrêter avec confirmation
taskkill /PID 1234
```

#### Sur macOS/Linux :
```bash
# Trouver le PID
lsof -i :8000
# Exemple : python 1234 user

# Arrêter proprement
kill 1234

# Arrêt forcé
kill -9 1234

# Arrêter par nom
pkill -f "python main.py"
```

### 3. **Libérer un port spécifique**

#### Script Windows PowerShell :
```powershell
# Fonction pour libérer un port
function Stop-ProcessOnPort {
    param([int]$Port)
    
    $process = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    if ($process) {
        $pid = $process.OwningProcess
        Write-Host "Arrêt du processus $pid utilisant le port $Port"
        Stop-Process -Id $pid -Force
    } else {
        Write-Host "Aucun processus trouvé sur le port $Port"
    }
}

# Utilisation
Stop-ProcessOnPort -Port 8000
```

#### Script Bash (macOS/Linux) :
```bash
#!/bin/bash
kill_port() {
    local port=$1
    local pid=$(lsof -ti:$port)
    
    if [ ! -z "$pid" ]; then
        echo "Arrêt du processus $pid utilisant le port $port"
        kill -9 $pid
    else
        echo "Aucun processus trouvé sur le port $port"
    fi
}

# Utilisation
kill_port 8000
```

---

## 💻 Commandes spécifiques par technologie

### **Python / FastAPI / Django**

```bash
# Identifier les processus Python
tasklist | findstr python                    # Windows
ps aux | grep python                         # macOS/Linux

# Arrêter tous les serveurs Python
taskkill /IM python.exe /F                   # Windows
pkill -f python                              # macOS/Linux

# Processus spécifiques
taskkill /F /FI "WINDOWTITLE eq Python*"     # Windows
pkill -f "uvicorn\|gunicorn\|python.*main"   # macOS/Linux
```

### **Node.js / Express / React**

```bash
# Identifier les processus Node.js
tasklist | findstr node                      # Windows  
ps aux | grep node                           # macOS/Linux

# Arrêter les processus Node.js
taskkill /IM node.exe /F                     # Windows
pkill node                                   # macOS/Linux

# Processus spécifiques
taskkill /F /FI "IMAGENAME eq node.exe"      # Windows
pkill -f "npm\|yarn\|webpack\|react-scripts" # macOS/Linux
```

### **Services Web / Apache / Nginx**

```bash
# Windows (si installé comme service)
net stop apache2
net stop nginx

# macOS/Linux
sudo service apache2 stop
sudo service nginx stop
# ou
sudo systemctl stop apache2
sudo systemctl stop nginx
```

---

## 🛡️ Prévention et bonnes pratiques

### 1. **Configuration de ports dynamiques**

#### Python FastAPI (comme dans votre projet) :
```python
import socket
import uvicorn

def find_free_port(start_port=8000, max_port=8010):
    """Trouve un port libre"""
    for port in range(start_port, max_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
    return None

# Utilisation
port = find_free_port()
if port:
    uvicorn.run(app, host="0.0.0.0", port=port)
```

#### Node.js :
```javascript
const net = require('net');

function getAvailablePort(startPort = 3000) {
    return new Promise((resolve, reject) => {
        const server = net.createServer();
        server.listen(startPort, () => {
            const port = server.address().port;
            server.close(() => resolve(port));
        });
        server.on('error', () => {
            getAvailablePort(startPort + 1).then(resolve).catch(reject);
        });
    });
}

// Utilisation
getAvailablePort().then(port => {
    app.listen(port, () => console.log(`Server running on port ${port}`));
});
```

### 2. **Variables d'environnement pour les ports**

```bash
# Fichier .env
PORT=8000
BACKUP_PORTS=8001,8002,8003

# Python
import os
port = int(os.getenv('PORT', 8000))

# Node.js
const port = process.env.PORT || 3000;
```

### 3. **Gestionnaires de processus**

#### PM2 pour Node.js :
```bash
# Installation
npm install -g pm2

# Démarrage
pm2 start app.js --name "mon-api"

# Arrêt
pm2 stop mon-api
pm2 delete mon-api

# Voir tous les processus
pm2 list
```

#### Supervisor pour Python :
```bash
# Installation
pip install supervisor

# Configuration
supervisord -c supervisord.conf

# Contrôle
supervisorctl stop mon-api
supervisorctl start mon-api
```

---

## 🤖 Scripts d'automatisation

### 1. **Script de nettoyage complet (Windows)**

```batch
@echo off
echo 🧹 Nettoyage des processus de développement...

echo Arrêt des processus Python...
taskkill /IM python.exe /F 2>nul

echo Arrêt des processus Node.js...
taskkill /IM node.exe /F 2>nul

echo Vérification des ports critiques...
for %%p in (3000 8000 8080 5000) do (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%%p') do (
        echo Libération du port %%p (PID: %%a)
        taskkill /PID %%a /F 2>nul
    )
)

echo ✅ Nettoyage terminé!
pause
```

### 2. **Script de diagnostic (Windows PowerShell)**

```powershell
# Diagnostic-Ports.ps1
param(
    [int[]]$Ports = @(3000, 8000, 8080, 5000, 3001)
)

Write-Host "🔍 Diagnostic des ports de développement" -ForegroundColor Cyan
Write-Host "=" * 50

foreach ($port in $Ports) {
    $connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    
    if ($connections) {
        foreach ($conn in $connections) {
            $process = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
            Write-Host "Port $port : " -NoNewline -ForegroundColor Yellow
            Write-Host "$($process.ProcessName) (PID: $($conn.OwningProcess))" -ForegroundColor Red
        }
    } else {
        Write-Host "Port $port : " -NoNewline -ForegroundColor Yellow
        Write-Host "LIBRE" -ForegroundColor Green
    }
}

Write-Host "`n📊 Processus de développement actifs :"
@('python', 'node', 'npm', 'yarn', 'code') | ForEach-Object {
    $procs = Get-Process -Name $_ -ErrorAction SilentlyContinue
    if ($procs) {
        Write-Host "$_ : $($procs.Count) processus" -ForegroundColor Cyan
    }
}
```

### 3. **Script universel de démarrage sécurisé**

```python
#!/usr/bin/env python3
"""
Script de démarrage sécurisé pour applications web
Usage: python safe_start.py --app main:app --port 8000
"""

import argparse
import socket
import subprocess
import sys
import time
import psutil

def is_port_in_use(port, host='localhost'):
    """Vérifie si un port est utilisé"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def find_process_on_port(port):
    """Trouve le processus utilisant un port"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    return proc.info
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None

def kill_process_on_port(port, force=False):
    """Arrête le processus sur un port"""
    proc_info = find_process_on_port(port)
    if proc_info:
        try:
            proc = psutil.Process(proc_info['pid'])
            if force:
                proc.kill()
            else:
                proc.terminate()
            print(f"✅ Processus {proc_info['name']} (PID: {proc_info['pid']}) arrêté")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de l'arrêt : {e}")
            return False
    return False

def find_free_port(start_port, max_attempts=10):
    """Trouve un port libre"""
    for i in range(max_attempts):
        port = start_port + i
        if not is_port_in_use(port):
            return port
    return None

def main():
    parser = argparse.ArgumentParser(description='Démarrage sécurisé d\'application web')
    parser.add_argument('--app', required=True, help='Application à démarrer (ex: main:app)')
    parser.add_argument('--port', type=int, default=8000, help='Port de démarrage')
    parser.add_argument('--host', default='0.0.0.0', help='Adresse d\'écoute')
    parser.add_argument('--force-kill', action='store_true', help='Forcer l\'arrêt des processus')
    parser.add_argument('--auto-port', action='store_true', help='Chercher automatiquement un port libre')
    
    args = parser.parse_args()
    
    print(f"🚀 Démarrage de {args.app} sur {args.host}:{args.port}")
    
    # Vérifier si le port est utilisé
    if is_port_in_use(args.port):
        print(f"⚠️  Port {args.port} déjà utilisé")
        
        proc_info = find_process_on_port(args.port)
        if proc_info:
            print(f"   Processus : {proc_info['name']} (PID: {proc_info['pid']})")
            
            if args.force_kill:
                if kill_process_on_port(args.port, force=True):
                    time.sleep(2)  # Attendre que le port se libère
                else:
                    sys.exit(1)
            elif args.auto_port:
                new_port = find_free_port(args.port + 1)
                if new_port:
                    args.port = new_port
                    print(f"🔄 Utilisation du port {new_port}")
                else:
                    print("❌ Aucun port libre trouvé")
                    sys.exit(1)
            else:
                response = input("Voulez-vous arrêter ce processus ? (y/N): ")
                if response.lower() == 'y':
                    if not kill_process_on_port(args.port):
                        sys.exit(1)
                    time.sleep(2)
                else:
                    sys.exit(1)
    
    # Démarrer l'application
    cmd = ['uvicorn', args.app, '--host', args.host, '--port', str(args.port), '--reload']
    print(f"📚 Documentation : http://localhost:{args.port}/docs")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 Arrêt de l'application")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 4. **Utilisation du script sécurisé**

```bash
# Installation des dépendances
pip install psutil

# Démarrage normal
python safe_start.py --app main:app --port 8000

# Avec port automatique si occupé
python safe_start.py --app main:app --port 8000 --auto-port

# Avec arrêt forcé
python safe_start.py --app main:app --port 8000 --force-kill

# Aide
python safe_start.py --help
```

---

## 🎯 Résumé des commandes essentielles

### **Diagnostic rapide :**
```bash
# Windows
netstat -ano | findstr :8000
tasklist | findstr python

# macOS/Linux  
lsof -i :8000
ps aux | grep python
```

### **Arrêt rapide :**
```bash
# Windows
taskkill /F /PID <PID>
taskkill /IM python.exe /F

# macOS/Linux
kill -9 <PID>
pkill -f python
```

### **Libération de port :**
```bash
# Trouver et arrêter automatiquement
netstat -ano | findstr :8000 | for /f "tokens=5" %a in ('more') do taskkill /PID %a /F
```

---

## 📝 Notes importantes

1. **Toujours sauvegarder** vos données avant d'arrêter des processus
2. **Préférer l'arrêt normal** (Ctrl+C) à l'arrêt forcé
3. **Vérifier les dépendances** avant d'arrêter un processus
4. **Utiliser des gestionnaires de processus** en production
5. **Configurer des ports dynamiques** pour éviter les conflits

---

Ce guide vous aidera à gérer efficacement tous les problèmes de ports et processus que vous pourriez rencontrer lors du développement ! 🎉
