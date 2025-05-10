import requests

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
            return self._handle_response(response)
                
        except requests.exceptions.RequestException as e:
            return False, f"Erro de conexão: {str(e)}"
    
    def login_user(self, email, password):
        try:
            response = requests.post(
                f"{self.base_url}/login",
                json={
                    "email": email,
                    "password": password
                }
            )
            return self._handle_response(response)
                
        except requests.exceptions.RequestException as e:
            return False, f"Erro de conexão: {str(e)}"
    
    def _handle_response(self, response):
        if response.status_code in (200, 201):
            return True, response.json()
        else:
            return False, response.json().get("message", "Erro desconhecido")