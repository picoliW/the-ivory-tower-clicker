from core.api.api_requests import APIClient

class AuthHandlers:
    def __init__(self):
        self.api = APIClient()
    
    def handle_login(self, email, password):
        if not email or not password:
            return False, "Por favor, preencha todos os campos"
            
        success, response = self.api.login_user(email, password)
        
        if success:
            return True, response
        return False, response
    
    def handle_register(self, email, password, confirm_password):
        if not email or not password or not confirm_password:
            return False, "Por favor, preencha todos os campos"
            
        if password != confirm_password:
            return False, "As senhas não coincidem"
            
        success, response = self.api.register_user(email, password, confirm_password)
        
        if success:
            return True, "Registro bem-sucedido!"
        return False, response