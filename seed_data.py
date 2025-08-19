#!/usr/bin/env python3
"""
Script pour ajouter des données d'exemple (seed data) à la base de données
Usage: python seed_data.py [add|clear|status|reset]
"""

import sys
from database import SessionLocal
import models
import schemas
import crud
from database import engine

# Données d'exemple pour les utilisateurs
USERS_DATA = [
    {
        "email": "alice.martin@example.com",
        "nom": "Martin",
        "prenom": "Alice",
        "is_active": True
    },
    {
        "email": "bob.wilson@example.com", 
        "nom": "Wilson",
        "prenom": "Bob",
        "is_active": True
    },
    {
        "email": "claire.dubois@example.com",
        "nom": "Dubois",
        "prenom": "Claire",
        "is_active": True
    },
    {
        "email": "david.bernard@example.com",
        "nom": "Bernard", 
        "prenom": "David",
        "is_active": False
    },
    {
        "email": "emma.petit@example.com",
        "nom": "Petit",
        "prenom": "Emma",
        "is_active": True
    }
]

# Données d'exemple pour les articles (par utilisateur)
ITEMS_DATA = {
    1: [  # Articles pour Alice Martin
        {
            "title": "iPhone 15 Pro",
            "description": "Smartphone Apple neuf, 256GB, couleur titane naturel. Encore sous garantie.",
            "price": 120000,  # 1200.00€
            "is_available": True
        },
        {
            "title": "MacBook Pro 16 pouces",
            "description": "Ordinateur portable Apple M3, 32GB RAM, 1TB SSD. Parfait état, utilisé 6 mois.",
            "price": 280000,  # 2800.00€
            "is_available": True
        },
        {
            "title": "AirPods Pro 2ème génération",
            "description": "Écouteurs sans fil avec réduction de bruit active. Boîtier de charge inclus.",
            "price": 25000,   # 250.00€
            "is_available": False
        }
    ],
    2: [  # Articles pour Bob Wilson
        {
            "title": "Vélo électrique VTT",
            "description": "VTT électrique Decathlon, batterie 500Wh, autonomie 80km. Très bon état.",
            "price": 180000,  # 1800.00€
            "is_available": True
        },
        {
            "title": "Console PlayStation 5",
            "description": "Console Sony PS5 avec lecteur disque, 2 manettes, 5 jeux inclus.",
            "price": 55000,   # 550.00€
            "is_available": True
        }
    ],
    3: [  # Articles pour Claire Dubois
        {
            "title": "Appareil photo Canon EOS R6",
            "description": "Boîtier nu en excellent état, moins de 10000 déclenchements. Facture d'achat fournie.",
            "price": 160000,  # 1600.00€
            "is_available": True
        },
        {
            "title": "Objectif Canon RF 24-70mm f/2.8",
            "description": "Objectif professionnel, aucune rayure, parfait pour portraits et paysages.",
            "price": 135000,  # 1350.00€
            "is_available": True
        },
        {
            "title": "Drone DJI Air 2S",
            "description": "Drone avec caméra 4K, mallette de transport, 3 batteries. Parfait pour débuter.",
            "price": 95000,   # 950.00€
            "is_available": False
        }
    ],
    4: [  # Articles pour David Bernard (utilisateur inactif)
        {
            "title": "Livre Python pour débutants",
            "description": "Collection de livres de programmation Python, très bon état.",
            "price": 3500,    # 35.00€
            "is_available": False
        }
    ],
    5: [  # Articles pour Emma Petit
        {
            "title": "Chaise de bureau ergonomique",
            "description": "Chaise Herman Miller Aeron, taille B, excellent support lombaire.",
            "price": 45000,   # 450.00€
            "is_available": True
        },
        {
            "title": "Bureau assis-debout électrique",
            "description": "Bureau réglable en hauteur, plateau 160x80cm, très stable.",
            "price": 65000,   # 650.00€
            "is_available": True
        },
        {
            "title": "Écran 4K 27 pouces",
            "description": "Moniteur Dell UltraSharp, calibré couleur, parfait pour design graphique.",
            "price": 42000,   # 420.00€
            "is_available": True
        },
        {
            "title": "Clavier mécanique",
            "description": "Clavier Keychron K2, switches Cherry MX Blue, rétroéclairage RGB.",
            "price": 8500,    # 85.00€
            "is_available": True
        }
    ]
}

class SeedDataManager:
    def __init__(self):
        self.db = SessionLocal()
        
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()
    
    def create_tables(self):
        """Crée les tables si elles n'existent pas"""
        print("Création des tables si nécessaire...")
        models.Base.metadata.create_all(bind=engine)
        print("✅ Tables vérifiées/créées")
    
    def get_status(self):
        """Affiche le statut actuel de la base de données"""
        users_count = self.db.query(models.User).count()
        items_count = self.db.query(models.Item).count()
        active_users = self.db.query(models.User).filter(models.User.is_active == True).count()
        available_items = self.db.query(models.Item).filter(models.Item.is_available == True).count()
        
        print("📊 STATUT ACTUEL DE LA BASE DE DONNÉES")
        print("=" * 45)
        print(f"👥 Utilisateurs total : {users_count}")
        print(f"👥 Utilisateurs actifs : {active_users}")
        print(f"📦 Articles total : {items_count}")
        print(f"📦 Articles disponibles : {available_items}")
        
        if users_count > 0:
            print("\n👥 LISTE DES UTILISATEURS :")
            users = self.db.query(models.User).all()
            for user in users:
                status = "🟢 Actif" if user.is_active else "🔴 Inactif"
                items_count = len(user.items)
                print(f"  • {user.prenom} {user.nom} ({user.email}) - {status} - {items_count} article(s)")
        
        return users_count, items_count
    
    def clear_all_data(self):
        """Supprime toutes les données"""
        print("🗑️  SUPPRESSION DE TOUTES LES DONNÉES...")
        
        # Supprimer tous les articles
        items_deleted = self.db.query(models.Item).count()
        self.db.query(models.Item).delete()
        
        # Supprimer tous les utilisateurs
        users_deleted = self.db.query(models.User).count()
        self.db.query(models.User).delete()
        
        self.db.commit()
        
        print(f"✅ {users_deleted} utilisateur(s) supprimé(s)")
        print(f"✅ {items_deleted} article(s) supprimé(s)")
        print("🎉 Base de données nettoyée !")
    
    def add_seed_data(self, force=False):
        """Ajoute les données d'exemple"""
        
        # Vérifier s'il y a déjà des données
        existing_users = self.db.query(models.User).count()
        if existing_users > 0 and not force:
            print(f"⚠️  Il y a déjà {existing_users} utilisateur(s) dans la base.")
            print("   Utilisez --force pour ajouter quand même les données")
            print("   Ou utilisez 'python seed_data.py reset' pour tout remettre à zéro")
            return
        
        print("📝 AJOUT DES DONNÉES D'EXEMPLE...")
        print("=" * 40)
        
        created_users = 0
        created_items = 0
        
        # Ajouter les utilisateurs
        for user_data in USERS_DATA:
            try:
                # Vérifier si l'email existe déjà
                existing_user = crud.get_user_by_email(self.db, user_data["email"])
                if existing_user:
                    print(f"⚠️  Utilisateur {user_data['email']} existe déjà, ignoré")
                    continue
                
                user_schema = schemas.UserCreate(**user_data)
                user = crud.create_user(self.db, user_schema)
                created_users += 1
                status = "🟢" if user.is_active else "🔴"
                print(f"✅ Utilisateur créé : {user.prenom} {user.nom} {status}")
                
            except Exception as e:
                print(f"❌ Erreur lors de la création de l'utilisateur {user_data['email']}: {e}")
        
        print()  # Ligne vide
        
        # Ajouter les articles
        for user_id, items_data in ITEMS_DATA.items():
            try:
                # Vérifier que l'utilisateur existe
                user = crud.get_user(self.db, user_id)
                if not user:
                    print(f"⚠️  Utilisateur ID {user_id} non trouvé, articles ignorés")
                    continue
                
                print(f"📦 Ajout d'articles pour {user.prenom} {user.nom} :")
                
                for item_data in items_data:
                    try:
                        item_schema = schemas.ItemCreate(**item_data)
                        item = crud.create_user_item(self.db, item_schema, user_id)
                        created_items += 1
                        status = "🟢 Disponible" if item.is_available else "🔴 Non dispo"
                        price_euro = item.price / 100
                        print(f"  ✅ {item.title} - {price_euro:.2f}€ - {status}")
                        
                    except Exception as e:
                        print(f"  ❌ Erreur article '{item_data['title']}': {e}")
                        
            except Exception as e:
                print(f"❌ Erreur pour l'utilisateur ID {user_id}: {e}")
        
        print()  # Ligne vide
        print("🎉 DONNÉES D'EXEMPLE AJOUTÉES AVEC SUCCÈS !")
        print(f"📊 Résumé : {created_users} utilisateurs, {created_items} articles créés")
        print()
        print("🔗 URLs à tester maintenant :")
        print("  • http://localhost:8000/users/")
        print("  • http://localhost:8000/items/")
        print("  • http://localhost:8000/docs")
    
    def add_sample_user(self):
        """Ajoute rapidement un utilisateur et quelques articles pour test"""
        print("🚀 AJOUT RAPIDE D'UN UTILISATEUR DE TEST...")
        
        # Créer utilisateur de test
        user_data = {
            "email": "test.demo@example.com",
            "nom": "Demo",
            "prenom": "Test",
            "is_active": True
        }
        
        try:
            existing_user = crud.get_user_by_email(self.db, user_data["email"])
            if existing_user:
                print(f"✅ L'utilisateur de test existe déjà (ID: {existing_user.id})")
                user = existing_user
            else:
                user_schema = schemas.UserCreate(**user_data)
                user = crud.create_user(self.db, user_schema)
                print(f"✅ Utilisateur de test créé (ID: {user.id})")
            
            # Ajouter quelques articles
            sample_items = [
                {
                    "title": "Article de démonstration 1",
                    "description": "Ceci est un article d'exemple pour tester l'API",
                    "price": 5000,  # 50.00€
                    "is_available": True
                },
                {
                    "title": "Article de démonstration 2", 
                    "description": "Un second article pour les tests",
                    "price": 7500,  # 75.00€
                    "is_available": False
                }
            ]
            
            for item_data in sample_items:
                item_schema = schemas.ItemCreate(**item_data)
                item = crud.create_user_item(self.db, item_schema, user.id)
                price_euro = item.price / 100
                status = "🟢" if item.is_available else "🔴"
                print(f"  ✅ {item.title} - {price_euro:.2f}€ {status}")
            
            print(f"\n🔗 Testez maintenant : http://localhost:8000/users/{user.id}")
            
        except Exception as e:
            print(f"❌ Erreur : {e}")

def main():
    """Point d'entrée principal"""
    
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("📚 GESTIONNAIRE DE DONNÉES D'EXEMPLE")
        print("=" * 40)
        print()
        print("Usage: python seed_data.py [commande]")
        print()
        print("Commandes disponibles :")
        print("  add      - Ajouter les données d'exemple")
        print("  add --force - Ajouter même s'il y a déjà des données") 
        print("  quick    - Ajouter rapidement un utilisateur de test")
        print("  clear    - Supprimer toutes les données")
        print("  status   - Afficher le statut de la base de données")
        print("  reset    - Supprimer tout puis ajouter les données d'exemple")
        print()
        print("Exemples :")
        print("  python seed_data.py status")
        print("  python seed_data.py add")
        print("  python seed_data.py reset")
        return
    
    command = sys.argv[1].lower()
    force = "--force" in sys.argv
    
    # Créer le gestionnaire
    manager = SeedDataManager()
    
    try:
        # Créer les tables si nécessaire
        manager.create_tables()
        
        if command == "status":
            manager.get_status()
            
        elif command == "clear":
            users_count, items_count = manager.get_status()
            if users_count > 0 or items_count > 0:
                confirm = input("\n⚠️  Êtes-vous sûr de vouloir supprimer TOUTES les données ? (oui/non): ")
                if confirm.lower() in ['oui', 'o', 'yes', 'y']:
                    manager.clear_all_data()
                else:
                    print("❌ Suppression annulée")
            else:
                print("ℹ️  La base de données est déjà vide")
                
        elif command == "add":
            manager.add_seed_data(force=force)
            
        elif command == "quick":
            manager.add_sample_user()
            
        elif command == "reset":
            print("🔄 REMISE À ZÉRO ET AJOUT DES DONNÉES...")
            manager.clear_all_data()
            print()
            manager.add_seed_data(force=True)
            
        else:
            print(f"❌ Commande inconnue : {command}")
            print("Utilisez 'python seed_data.py' pour voir l'aide")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Opération interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
