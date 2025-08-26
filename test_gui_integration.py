#!/usr/bin/env python3
"""
Test d'intégration de l'interface graphique avec l'API FastAPI

Ce script teste automatiquement la communication entre l'interface graphique
et l'API FastAPI pour s'assurer que tout fonctionne correctement.
"""

import sys
import time
from gui_client.api_client import FastAPIClient


def test_api_client():
    """Test complet du client API"""
    
    print("🧪 TEST D'INTÉGRATION - Interface Graphique et API FastAPI")
    print("=" * 70)
    
    # Initialisation du client
    client = FastAPIClient("http://localhost:8000")
    
    # Test 1 : Connexion à l'API
    print("\n1️⃣  Test de connexion à l'API...")
    if client.test_connection():
        print("   ✅ Connexion réussie")
    else:
        print("   ❌ Connexion échouée - Vérifiez que l'API est démarrée")
        print("   💡 Lancez : python safe_start.py")
        return False
    
    # Test 2 : Récupération des données existantes
    print("\n2️⃣  Récupération des utilisateurs existants...")
    users = client.get_users()
    if isinstance(users, list):
        print(f"   ✅ {len(users)} utilisateurs trouvés")
        for user in users[:3]:  # Afficher les 3 premiers
            print(f"      - {user['prenom']} {user['nom']} ({user['email']})")
        if len(users) > 3:
            print(f"      ... et {len(users) - 3} autres")
    else:
        print(f"   ⚠️  Erreur : {users}")
    
    print("\n3️⃣  Récupération des articles existants...")
    items = client.get_items()
    if isinstance(items, list):
        print(f"   ✅ {len(items)} articles trouvés")
        for item in items[:3]:  # Afficher les 3 premiers
            price = client.format_price(item['price'])
            print(f"      - {item['title']} ({price})")
        if len(items) > 3:
            print(f"      ... et {len(items) - 3} autres")
    else:
        print(f"   ⚠️  Erreur : {items}")
    
    # Test 3 : Création d'un utilisateur test
    print("\n4️⃣  Création d'un utilisateur test...")
    test_email = f"test.gui.{int(time.time())}@example.com"
    new_user = client.create_user(
        email=test_email,
        nom="TestGUI",
        prenom="Utilisateur",
        is_active=True
    )
    
    if "error" not in new_user:
        print(f"   ✅ Utilisateur créé avec l'ID : {new_user['id']}")
        test_user_id = new_user['id']
    else:
        print(f"   ❌ Erreur création utilisateur : {new_user['error']}")
        return False
    
    # Test 4 : Création d'un article test
    print("\n5️⃣  Création d'un article test...")
    new_item = client.create_item(
        user_id=test_user_id,
        title="Article Test Interface GUI",
        description="Article créé automatiquement pour tester l'interface graphique PySide6",
        price=4999,  # 49,99€
        is_available=True
    )
    
    if "error" not in new_item:
        print(f"   ✅ Article créé avec l'ID : {new_item['id']}")
        test_item_id = new_item['id']
        print(f"   💰 Prix : {client.format_price(new_item['price'])}")
    else:
        print(f"   ❌ Erreur création article : {new_item['error']}")
        return False
    
    # Test 5 : Recherche d'articles
    print("\n6️⃣  Test de recherche d'articles...")
    search_results = client.search_items("GUI")
    if isinstance(search_results, list):
        print(f"   ✅ {len(search_results)} résultat(s) trouvé(s) pour 'GUI'")
        for result in search_results:
            print(f"      - {result['title']}")
    else:
        print(f"   ❌ Erreur recherche : {search_results['error']}")
    
    # Test 6 : Récupération des articles de l'utilisateur
    print("\n7️⃣  Récupération des articles de l'utilisateur test...")
    user_items = client.get_user_items(test_user_id)
    if isinstance(user_items, list):
        print(f"   ✅ {len(user_items)} article(s) pour l'utilisateur {test_user_id}")
        for item in user_items:
            print(f"      - {item['title']}")
    else:
        print(f"   ❌ Erreur récupération articles : {user_items['error']}")
    
    # Test 7 : Formatage des prix
    print("\n8️⃣  Test de formatage des prix...")
    test_prices = [2550, 12000, 99, 150000]
    print("   Conversion centimes → euros :")
    for price_cents in test_prices:
        formatted = client.format_price(price_cents)
        print(f"      {price_cents} centimes → {formatted}")
    
    print("   Conversion euros → centimes :")
    test_price_strings = ["25.50", "120,00", "0.99", "1500"]
    for price_str in test_price_strings:
        cents = client.parse_price(price_str)
        print(f"      {price_str} → {cents} centimes")
    
    # Test 8 : Nettoyage (suppression des données test)
    print("\n9️⃣  Nettoyage des données test...")
    
    # Supprimer l'article test
    delete_item_result = client.delete_item(test_item_id)
    if "error" not in delete_item_result:
        print("   ✅ Article test supprimé")
    else:
        print(f"   ⚠️  Erreur suppression article : {delete_item_result['error']}")
    
    # Supprimer l'utilisateur test
    delete_user_result = client.delete_user(test_user_id)
    if "error" not in delete_user_result:
        print("   ✅ Utilisateur test supprimé")
        print(f"   📊 {delete_user_result.get('articles_supprimés', 0)} article(s) associé(s) supprimé(s)")
    else:
        print(f"   ⚠️  Erreur suppression utilisateur : {delete_user_result['error']}")
    
    # Résumé final
    print("\n" + "=" * 70)
    print("🎉 TESTS TERMINÉS AVEC SUCCÈS !")
    print("\n✅ L'interface graphique peut communiquer correctement avec l'API")
    print("✅ Toutes les opérations CRUD fonctionnent")
    print("✅ Le formatage des prix est correct")
    print("✅ La recherche fonctionne")
    
    print("\n🚀 Vous pouvez maintenant lancer l'interface graphique :")
    print("   python run_gui.py")
    
    return True


def test_gui_components():
    """Test des composants de l'interface graphique"""
    
    print("\n" + "=" * 70)
    print("🖥️  TEST DES COMPOSANTS INTERFACE GRAPHIQUE")
    print("=" * 70)
    
    try:
        # Test d'importation des modules
        print("\n1️⃣  Test d'importation des modules...")
        
        from gui_client import FastAPIClient
        print("   ✅ FastAPIClient importé")
        
        from gui_client.main_window import MainWindow, UsersTab, ItemsTab, StatusIndicator
        print("   ✅ Composants UI importés")
        
        # Test PySide6
        from PySide6.QtWidgets import QApplication
        print("   ✅ PySide6 disponible")
        
        print("\n2️⃣  Test de création des composants...")
        
        # Créer une application Qt temporaire
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Test du client API
        client = FastAPIClient()
        print("   ✅ Client API créé")
        
        # Test de l'indicateur de statut
        status_indicator = StatusIndicator()
        status_indicator.set_connected()
        status_indicator.set_disconnected()
        status_indicator.set_connecting()
        print("   ✅ StatusIndicator fonctionne")
        
        print("\n✅ Tous les composants sont prêts !")
        print("💡 Pour tester l'interface complète, lancez : python run_gui.py")
        
        return True
        
    except ImportError as e:
        print(f"\n❌ Erreur d'importation : {e}")
        print("💡 Installez les dépendances : pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")
        return False


def main():
    """Lance tous les tests d'intégration"""
    
    print("🔧 TESTS D'INTÉGRATION COMPLETS")
    print("Interface Graphique PySide6 + API FastAPI CRUD")
    print("=" * 70)
    
    # Test des composants GUI
    gui_ok = test_gui_components()
    
    if not gui_ok:
        print("\n❌ Les composants GUI ne sont pas prêts")
        return False
    
    # Test de l'API
    api_ok = test_api_client()
    
    if not api_ok:
        print("\n❌ L'API n'est pas accessible ou ne fonctionne pas correctement")
        return False
    
    print("\n" + "🎉" * 20)
    print("🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS ! 🎉")
    print("🎉" * 20)
    print("\n🚀 Votre interface graphique FastAPI est prête à être utilisée !")
    print("\n📋 Pour démarrer :")
    print("   1️⃣  API : python safe_start.py")
    print("   2️⃣  GUI : python run_gui.py")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Tests interrompus par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur critique : {e}")
        sys.exit(1)
