"""
Client API pour communiquer avec le service FastAPI CRUD
"""

import requests
import json
from typing import List, Dict, Optional, Union


class FastAPIClient:
    """Client pour interagir avec l'API FastAPI CRUD"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialise le client API
        
        Args:
            base_url: URL de base de l'API FastAPI (ex: http://localhost:8000)
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def test_connection(self) -> bool:
        """
        Teste la connexion à l'API
        
        Returns:
            bool: True si la connexion fonctionne, False sinon
        """
        try:
            response = self.session.get(f"{self.base_url}/")
            return response.status_code == 200
        except Exception:
            return False
    
    def get_health(self) -> Dict:
        """
        Récupère l'état de santé de l'API
        
        Returns:
            Dict: Réponse de l'endpoint /health ou erreur
        """
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== UTILISATEURS ====================
    
    def get_users(self, skip: int = 0, limit: int = 100) -> Union[List[Dict], Dict]:
        """
        Récupère la liste des utilisateurs
        
        Args:
            skip: Nombre d'utilisateurs à ignorer
            limit: Nombre maximum d'utilisateurs à récupérer
        
        Returns:
            List[Dict] ou Dict: Liste des utilisateurs ou message d'erreur
        """
        try:
            params = {"skip": skip, "limit": limit}
            response = self.session.get(f"{self.base_url}/users/", params=params)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_user(self, user_id: int) -> Union[Dict, Dict]:
        """
        Récupère un utilisateur par son ID
        
        Args:
            user_id: ID de l'utilisateur
        
        Returns:
            Dict: Données de l'utilisateur ou message d'erreur
        """
        try:
            response = self.session.get(f"{self.base_url}/users/{user_id}")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    def create_user(self, email: str, nom: str, prenom: str, is_active: bool = True) -> Union[Dict, Dict]:
        """
        Crée un nouvel utilisateur
        
        Args:
            email: Email de l'utilisateur
            nom: Nom de famille
            prenom: Prénom
            is_active: Si l'utilisateur est actif (défaut: True)
        
        Returns:
            Dict: Données de l'utilisateur créé ou message d'erreur
        """
        try:
            data = {
                "email": email,
                "nom": nom,
                "prenom": prenom,
                "is_active": is_active
            }
            response = self.session.post(f"{self.base_url}/users/", json=data)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    def update_user(self, user_id: int, **kwargs) -> Union[Dict, Dict]:
        """
        Met à jour un utilisateur
        
        Args:
            user_id: ID de l'utilisateur
            **kwargs: Champs à mettre à jour (nom, prenom, is_active)
        
        Returns:
            Dict: Données de l'utilisateur mis à jour ou message d'erreur
        """
        try:
            # Filtrer les valeurs None
            data = {k: v for k, v in kwargs.items() if v is not None}
            response = self.session.put(f"{self.base_url}/users/{user_id}", json=data)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    def delete_user(self, user_id: int) -> Union[Dict, Dict]:
        """
        Supprime un utilisateur et ses articles
        
        Args:
            user_id: ID de l'utilisateur
        
        Returns:
            Dict: Message de confirmation ou erreur
        """
        try:
            response = self.session.delete(f"{self.base_url}/users/{user_id}")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== ARTICLES ====================
    
    def get_items(self, skip: int = 0, limit: int = 100) -> Union[List[Dict], Dict]:
        """
        Récupère la liste des articles
        
        Args:
            skip: Nombre d'articles à ignorer
            limit: Nombre maximum d'articles à récupérer
        
        Returns:
            List[Dict] ou Dict: Liste des articles ou message d'erreur
        """
        try:
            params = {"skip": skip, "limit": limit}
            response = self.session.get(f"{self.base_url}/items/", params=params)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_item(self, item_id: int) -> Union[Dict, Dict]:
        """
        Récupère un article par son ID
        
        Args:
            item_id: ID de l'article
        
        Returns:
            Dict: Données de l'article ou message d'erreur
        """
        try:
            response = self.session.get(f"{self.base_url}/items/{item_id}")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_user_items(self, user_id: int, skip: int = 0, limit: int = 100) -> Union[List[Dict], Dict]:
        """
        Récupère les articles d'un utilisateur
        
        Args:
            user_id: ID de l'utilisateur
            skip: Nombre d'articles à ignorer
            limit: Nombre maximum d'articles à récupérer
        
        Returns:
            List[Dict] ou Dict: Liste des articles ou message d'erreur
        """
        try:
            params = {"skip": skip, "limit": limit}
            response = self.session.get(f"{self.base_url}/users/{user_id}/items/", params=params)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    def create_item(self, user_id: int, title: str, description: str, price: int, is_available: bool = True) -> Union[Dict, Dict]:
        """
        Crée un nouvel article pour un utilisateur
        
        Args:
            user_id: ID du propriétaire de l'article
            title: Titre de l'article
            description: Description de l'article
            price: Prix en centimes (ex: 2500 pour 25.00€)
            is_available: Si l'article est disponible (défaut: True)
        
        Returns:
            Dict: Données de l'article créé ou message d'erreur
        """
        try:
            data = {
                "title": title,
                "description": description,
                "price": price,
                "is_available": is_available
            }
            response = self.session.post(f"{self.base_url}/users/{user_id}/items/", json=data)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    def update_item(self, item_id: int, **kwargs) -> Union[Dict, Dict]:
        """
        Met à jour un article
        
        Args:
            item_id: ID de l'article
            **kwargs: Champs à mettre à jour (title, description, price, is_available)
        
        Returns:
            Dict: Données de l'article mis à jour ou message d'erreur
        """
        try:
            # Filtrer les valeurs None
            data = {k: v for k, v in kwargs.items() if v is not None}
            response = self.session.put(f"{self.base_url}/items/{item_id}", json=data)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    def delete_item(self, item_id: int) -> Union[Dict, Dict]:
        """
        Supprime un article
        
        Args:
            item_id: ID de l'article
        
        Returns:
            Dict: Message de confirmation ou erreur
        """
        try:
            response = self.session.delete(f"{self.base_url}/items/{item_id}")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== RECHERCHE ====================
    
    def search_items(self, query: str, limit: int = 50) -> Union[List[Dict], Dict]:
        """
        Recherche des articles par mot-clé
        
        Args:
            query: Terme de recherche
            limit: Nombre maximum de résultats
        
        Returns:
            List[Dict] ou Dict: Liste des articles trouvés ou message d'erreur
        """
        try:
            params = {"q": query, "limit": limit}
            response = self.session.get(f"{self.base_url}/search/items", params=params)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== UTILITAIRES ====================
    
    def format_price(self, price_cents: int) -> str:
        """
        Formate un prix en centimes vers un affichage en euros
        
        Args:
            price_cents: Prix en centimes
        
        Returns:
            str: Prix formaté (ex: "25,00€")
        """
        euros = price_cents / 100
        return f"{euros:,.2f}€".replace(",", " ").replace(".", ",")
    
    def parse_price(self, price_str: str) -> int:
        """
        Analyse une chaîne de prix et retourne le montant en centimes
        
        Args:
            price_str: Prix sous forme de chaîne (ex: "25.50", "25,50")
        
        Returns:
            int: Prix en centimes
        """
        try:
            # Nettoyer la chaîne
            clean_price = price_str.replace("€", "").replace(" ", "").replace(",", ".")
            euros = float(clean_price)
            return int(euros * 100)
        except ValueError:
            return 0
