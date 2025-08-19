@echo off
echo 🚀 Configuration de l'API FastAPI CRUD
echo =====================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou n'est pas dans le PATH
    echo    Veuillez installer Python depuis https://python.org
    pause
    exit /b 1
)

echo ✅ Python détecté
echo.

REM Créer l'environnement virtuel s'il n'existe pas
if not exist "venv" (
    echo 📦 Création de l'environnement virtuel...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Erreur lors de la création de l'environnement virtuel
        pause
        exit /b 1
    )
    echo ✅ Environnement virtuel créé
) else (
    echo ✅ Environnement virtuel existe déjà
)

echo.

REM Activer l'environnement virtuel
echo 🔧 Activation de l'environnement virtuel...
call venv\Scripts\activate

REM Mettre à jour pip
echo 🔧 Mise à jour de pip...
python.exe -m pip install --upgrade pip

REM Installer les dépendances
echo 📚 Installation des dépendances...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Erreur lors de l'installation des dépendances
    pause
    exit /b 1
)

echo.
echo ✅ Configuration terminée avec succès !
echo.
echo 🎯 Pour lancer l'API :
echo    1. Activez l'environnement : venv\Scripts\activate
echo    2. Lancez l'API : python main.py
echo    3. Accédez à la documentation : http://localhost:8000/docs
echo.
echo 🧪 Pour tester l'API :
echo    python exemple_utilisation.py
echo.
pause
