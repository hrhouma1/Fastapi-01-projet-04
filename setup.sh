#!/bin/bash

echo "🚀 Configuration de l'API FastAPI CRUD"
echo "====================================="
echo

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    echo "   Veuillez installer Python depuis https://python.org"
    exit 1
fi

echo "✅ Python détecté"
echo

# Créer l'environnement virtuel s'il n'existe pas
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Erreur lors de la création de l'environnement virtuel"
        exit 1
    fi
    echo "✅ Environnement virtuel créé"
else
    echo "✅ Environnement virtuel existe déjà"
fi

echo

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Mettre à jour pip
echo "🔧 Mise à jour de pip..."
python3 -m pip install --upgrade pip

# Installer les dépendances
echo "📚 Installation des dépendances..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de l'installation des dépendances"
    exit 1
fi

echo
echo "✅ Configuration terminée avec succès !"
echo
echo "🎯 Pour lancer l'API :"
echo "   1. Activez l'environnement : source venv/bin/activate"
echo "   2. Lancez l'API : python main.py"
echo "   3. Accédez à la documentation : http://localhost:8000/docs"
echo
echo "🧪 Pour tester l'API :"
echo "   python exemple_utilisation.py"
echo
