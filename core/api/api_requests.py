import requests

class APIClient:
    def __init__(self, base_url="http://localhost:3000/auth"):
        self.base_url = base_url
        self.base_ranking_url = "http://localhost:3000/ranking"
    
    def register_user(self, nickname, email, password, confirm_password):
        try:
            response = requests.post(
                f"{self.base_url}/register",
                json={
                    "nickname" : nickname,
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
        
    def save_player_data(self, user_id, damage, gold, gold_per_second, floor, dash_unlocked, movespeed, dps):
        try:
            response = requests.post(
                f"{self.base_url}/save-player-data",
                json={
                    "userId": user_id,
                    "damage": damage,
                    "gold": gold,
                    "gold_per_second": gold_per_second,
                    "floor": floor,
                    "dash_unlocked": dash_unlocked,
                    "movespeed": movespeed,
                    "dps": dps
                }
            )
            return self._handle_response(response)
                
        except requests.exceptions.RequestException as e:
            return False, f"Erro de conexão: {str(e)}"
        

    def get_players_ranking(self):
        try:
            response = requests.get(f"{self.base_ranking_url}/players-ranking")
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return False, f"Erro de conexão: {str(e)}"