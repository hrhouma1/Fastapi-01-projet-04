#!/usr/bin/env python3
"""
Exemple d'utilisation de l'API CRUD FastAPI
Ce script démontre comment utiliser tous les endpoints de l'API

PRÉREQUIS :
1. Activer l'environnement virtuel : venv\Scripts\activate (Windows) ou source venv/bin/activate (macOS/Linux)
2. Installer les dépendances : pip install -r requirements.txt
3. Lancer l'API : python main.py
4. Exécuter ce script : python exemple_utilisation.py
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"

def test_api():
    """Teste tous les endpoints de l'API"""
    
    print("🚀 Test de l'API CRUD FastAPI")
    print("=" * 50)
    
    # 1. Créer un utilisateur
    print("\n1. 📝 Création d'un utilisateur...")
    user_data = {
        "email": "marie.dupont@example.com",
        "nom": "Dupont",
        "prenom": "Marie",
        "is_active": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        if response.status_code == 200:
            user = response.json()
            user_id = user['id']
            print(f"✅ Utilisateur créé avec l'ID: {user_id}")
            print(f"   Email: {user['email']}")
        else:
            print(f"❌ Erreur lors de la création: {response.status_code}")
            print(f"   Message: {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'API.")
        print("   Assurez-vous que l'API est lancée avec: python main.py")
        return
    
    # 2. Récupérer tous les utilisateurs
    print("\n2. 📋 Récupération de tous les utilisateurs...")
    response = requests.get(f"{BASE_URL}/users/")
    if response.status_code == 200:
        users = response.json()
        print(f"✅ {len(users)} utilisateur(s) trouvé(s)")
        for user in users:
            print(f"   - {user['prenom']} {user['nom']} ({user['email']})")
    
    # 3. Créer un article pour l'utilisateur
    print(f"\n3. 🛍️ Création d'un article pour l'utilisateur {user_id}...")
    item_data = {
        "title": "Ordinateur portable",
        "description": "MacBook Pro 16 pouces, excellent état",
        "price": 150000,  # 1500€ en centimes
        "is_available": True
    }
    
    response = requests.post(f"{BASE_URL}/users/{user_id}/items/", json=item_data)
    if response.status_code == 200:
        item = response.json()
        item_id = item['id']
        print(f"✅ Article créé avec l'ID: {item_id}")
        print(f"   Titre: {item['title']}")
        print(f"   Prix: {item['price']/100:.2f}€")
    
    # 4. Récupérer tous les articles
    print("\n4. 📦 Récupération de tous les articles...")
    response = requests.get(f"{BASE_URL}/items/")
    if response.status_code == 200:
        items = response.json()
        print(f"✅ {len(items)} article(s) trouvé(s)")
        for item in items:
            print(f"   - {item['title']} - {item['price']/100:.2f}€")
    
    # 5. Mettre à jour l'utilisateur
    print(f"\n5. ✏️ Mise à jour de l'utilisateur {user_id}...")
    update_data = {
        "nom": "Durand",
        "prenom": "Marie-Claire"
    }
    
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
    if response.status_code == 200:
        updated_user = response.json()
        print("✅ Utilisateur mis à jour")
        print(f"   Nouveau nom: {updated_user['prenom']} {updated_user['nom']}")
    
    # 6. Mettre à jour l'article
    print(f"\n6. 🔄 Mise à jour de l'article {item_id}...")
    item_update = {
        "price": 120000,  # 1200€ en centimes
        "description": "MacBook Pro 16 pouces, excellent état - Prix réduit!"
    }
    
    response = requests.put(f"{BASE_URL}/items/{item_id}", json=item_update)
    if response.status_code == 200:
        updated_item = response.json()
        print("✅ Article mis à jour")
        print(f"   Nouveau prix: {updated_item['price']/100:.2f}€")
    
    # 7. Récupérer l'utilisateur spécifique
    print(f"\n7. 🔍 Récupération de l'utilisateur {user_id}...")
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    if response.status_code == 200:
        user = response.json()
        print("✅ Utilisateur trouvé avec ses articles:")
        print(f"   {user['prenom']} {user['nom']} ({user['email']})")
        print(f"   Articles: {len(user['items'])}")
        for item in user['items']:
            print(f"     - {item['title']} - {item['price']/100:.2f}€")
    
    # 8. Supprimer l'article
    print(f"\n8. 🗑️ Suppression de l'article {item_id}...")
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    if response.status_code == 200:
        print("✅ Article supprimé avec succès")
    
    # 9. Supprimer l'utilisateur
    print(f"\n9. 🗑️ Suppression de l'utilisateur {user_id}...")
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    if response.status_code == 200:
        print("✅ Utilisateur supprimé avec succès")
    
    print("\n🎉 Test terminé avec succès!")
    print("📚 Consultez la documentation sur: http://localhost:8000/docs")

if __name__ == "__main__":
    test_api()
