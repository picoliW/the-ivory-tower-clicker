from core.api.api_requests import APIClient

class AuthHandlers:
    def __init__(self):
        self.api = APIClient()
    
    def handle_login(self, email, password):
        if not email or not password:
            return False, "Please fill in all fields"
            
        success, response = self.api.login_user(email, password)
        
        if success:
            return True, response
        return False, response
    
    def handle_register(self, email, password, confirm_password):
        if not email or not password or not confirm_password:
            return False, "Please fill in all fields"
            
        if password != confirm_password:
            return False, "Passwords do not match"
            
        success, response = self.api.register_user(email, password, confirm_password)
        
        if success:
            return True, "Login successful"
        return False, response