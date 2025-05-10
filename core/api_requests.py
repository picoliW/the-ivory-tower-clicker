import requests
from ursina import *

class APIClient:
    def __init__(self, base_url="http://localhost:3000/auth"):
        self.base_url = base_url
    
    def register_user(self, email, password, confirm_password):
        try:
            response = requests.post(
                f"{self.base_url}/register",
                json={
                    "email": email,
                    "password": password,
                    "confirmPassword": confirm_password
                }
            )
            
            if response.status_code == 201:
                return True, response.json().get("message", "Registro bem-sucedido")
            else:
                return False, response.json().get("message", "Erro desconhecido no registro")
                
        except requests.exceptions.RequestException as e:
            return False, f"Erro de conexão: {str(e)}"