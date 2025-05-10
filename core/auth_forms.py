from ursina import *
import requests
from core.api.api_requests import APIClient

class LoginForm(Entity):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.email_text = Text(
            text="E-Mail",
            position=(-1.8, -0.1),
            color=color.white,
            scale=5.5,
            parent=self,
            z=-1.1
        )

        self.email_input = InputField(
            scale=(4, 0.4),
            position=(0, -0.5),
            parent=self,
            z=-1.1
        )

        self.email_input.text_field.scale = (2.62, 16)

        self.password_text = Text(
            text="Password",
            position=(-1.8, -0.8),
            color=color.white,
            scale=5.5,
            parent=self,
            z=-1.1
        )

        self.password_input = InputField(
            scale=(4, 0.4),
            position=(0, -1.2),
            parent=self,
            z=-1.1
        )
        self.password_input.text_field.scale = (2.62, 16)

        self.start_button = Button(
            text='Submit',
            scale=(1, .3),
            position=(0, -1.8),
            color=color.blue,        
            text_color=color.white,
            parent=self,
            text_size=.3,
            z=-1.1,
        )

        self.api = APIClient()  
        self.start_button.on_click = self.submit_form 
    
    def submit_form(self):
        email = self.email_input.text
        password = self.password_input.text
        
        if not email or not password:
            print("Por favor, preencha todos os campos")
            return
            
        success, response = self.api.login_user(email, password)
        
        if success:
            print("Login bem-sucedido!")
            print("Dados do usuário:", response.get("user"))
        else:
            print(f"Erro no login: {response}")

class RegisterForm(Entity):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.email_text = Text(
            text="E-mail",
            position=(-1.8, 0.4),
            color=color.white,
            scale=5.5,
            parent=self,
            z=-1.1
        )

        self.email_input = InputField(
            scale=(4, 0.4),
            position=(0, 0),
            parent=self,
            z=-1.1
        )
        self.email_input.text_field.scale = (2.62, 16)

        self.password_text = Text(
            text="Password",
            position=(-1.8, -.24),
            color=color.white,
            scale=5.5,
            parent=self,
            z=-1.1
        )

        self.password_input = InputField(
            scale=(4, 0.4),
            position=(0, -.6),
            parent=self,
            z=-1.1
        )
        self.password_input.text_field.scale = (2.62, 16)

        self.confirm_password_text = Text(
            text="Confirm Password",
            position=(-1.8, -.84),
            color=color.white,
            scale=5.5,
            parent=self,
            z=-1.1
        )

        self.confirm_password_input = InputField(
            scale=(4, 0.4),
            position=(0, -1.2),
            parent=self,
            z=-1.1
        )
        self.confirm_password_input.text_field.scale = (2.62, 16)

        self.start_button = Button(
            text='Submit',
            scale=(1, .3),
            position=(0, -1.8),
            color=color.blue,        
            text_color=color.white,
            parent=self,
            text_size=.3,
            z=-1.1,
        )

        self.api = APIClient() 
        self.start_button.on_click = self.submit_form
    
    def submit_form(self):
        email = self.email_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text
        
        if not email or not password or not confirm_password:
            print("Por favor, preencha todos os campos")
            return
            
        if password != confirm_password:
            print("As senhas não coincidem")
            return
            
        success, message = self.api.register_user(email, password, confirm_password)
        
        if success:
            print("Registro bem-sucedido!")
        else:
            print(f"Erro no registro: {message}")

  
