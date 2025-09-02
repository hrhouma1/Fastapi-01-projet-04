#!/usr/bin/env python3
"""
Test rapide de la cohérence des données
Ce script teste que la validation fonctionne correctement
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001"  # Port alternative au cas où 8000 est occupé

def test_coherence():
    """Teste la cohérence des données"""
    
    print("🧪 Test de cohérence des données API")
    print("=" * 50)
    
    # Test 1 : Essayer de créer un article sans utilisateur (doit échouer)
    print("\n1. ❌ Test d'erreur - Créer article pour utilisateur inexistant (ID=999)")
    try:
        response = requests.post(f"{BASE_URL}/users/999/items/", json={
            "title": "Article impossible",
            "description": "Cet article ne devrait pas être créé",
            "price": 1000,
            "is_available": True
        })
        
        if response.status_code == 404:
            print("✅ SUCCÈS - L'API refuse de créer l'article (code 404)")
            print(f"   Message : {response.json().get('detail', 'Aucun détail')}")
        else:
            print(f"❌ ÉCHEC - Code retourné : {response.status_code}")
            print(f"   Réponse : {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("⚠️  API non accessible. Lancez d'abord : python safe_start.py")
        return
    
    # Test 2 : Créer un utilisateur puis un article (doit réussir)
    print("\n2. ✅ Test normal - Créer utilisateur puis article")
    
    # Créer utilisateur
    user_data = {
        "email": "test.coherence@example.com",
        "nom": "Test",
        "prenom": "Cohérence",
        "is_active": True
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    if response.status_code == 200:
        user = response.json()
        user_id = user['id']
        print(f"✅ Utilisateur créé (ID: {user_id})")
        
        # Créer article pour cet utilisateur
        item_data = {
            "title": "Article cohérent",
            "description": "Cet article devrait être créé",
            "price": 5000,
            "is_available": True
        }
        
        response = requests.post(f"{BASE_URL}/users/{user_id}/items/", json=item_data)
        if response.status_code == 200:
            item = response.json()
            print(f"✅ Article créé (ID: {item['id']}) pour l'utilisateur {user_id}")
            
            # Test 3 : Supprimer l'utilisateur (doit supprimer l'article automatiquement)
            print(f"\n3. 🗑️ Test CASCADE - Supprimer utilisateur {user_id}")
            response = requests.delete(f"{BASE_URL}/users/{user_id}")
            if response.status_code == 200:
                result = response.json()
                print("✅ Utilisateur supprimé avec CASCADE")
                print(f"   Message : {result.get('message', 'Aucun message')}")
                print(f"   Articles supprimés : {result.get('articles_supprimés', 0)}")
                
                # Vérifier que l'article a bien été supprimé
                response = requests.get(f"{BASE_URL}/items/{item['id']}")
                if response.status_code == 404:
                    print("✅ Article automatiquement supprimé (CASCADE fonctionne)")
                else:
                    print("❌ L'article existe encore (CASCADE ne fonctionne pas)")
            else:
                print(f"❌ Erreur lors de la suppression : {response.status_code}")
        else:
            print(f"❌ Erreur création article : {response.status_code}")
    else:
        print(f"❌ Erreur création utilisateur : {response.status_code}")
    
    print("\n🎉 Tests de cohérence terminés !")
    print("📚 Pour des tests complets, utilisez : api_tests.http")

if __name__ == "__main__":
    test_coherence()
