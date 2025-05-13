from ursina import *
from core.api.auth_handlers import AuthHandlers

class LoginForm(Entity):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.on_login_success = None
        self.error_message = None

        self.handlers = AuthHandlers()
        self._setup_ui()
        self.start_button.on_click = self.submit_form

    def _setup_ui(self):
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

        self.error_display = Text(
            text="",
            position=(-0.78, -2),
            color=color.red,
            scale=7,
            parent=self,
            z=-1.1,
            visible=False
        )

    def submit_form(self):
        email = self.email_input.text
        password = self.password_input.text
        
        self.error_display.visible = False
        self.error_display.text = ""
        
        success, response = self.handlers.handle_login(email, password)
        
        if success:
            try:
                print("Login bem-sucedido!")
                user_data = response.get('playerData', {})
                user_id = response['user']['id']
                
                if self.on_login_success:
                    self.on_login_success(user_id, user_data)
            except (KeyError, TypeError) as e:
                print(f"Error processing login response: {e}")
                self.error_display.text = "Erro inesperado no login"
                self.error_display.visible = True
        else:
            error_msg = response if isinstance(response, str) else response.get('message', 'Erro desconhecido no login')
            print(error_msg)
            self.error_display.text = error_msg
            self.error_display.visible = True

class RegisterForm(Entity):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.handlers = AuthHandlers()
        self._setup_ui()
        self.start_button.on_click = self.submit_form

    def _setup_ui(self):
        self.nickname_text = Text(
            text="Nickname",
            position=(-1.8, 1),
            color=color.white,
            scale=5.5,
            parent=self,
            z=-1.1
        )

        self.nickname_input = InputField(
            scale=(4, 0.4),
            position=(0, 0.63),
            parent=self,
            z=-1.1
        )

        self.nickname_input.text_field.scale = (2.62, 16)

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
    def submit_form(self):
        nickname = self.nickname_input.text
        email = self.email_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text
        
        success, message = self.handlers.handle_register(
            nickname,
            email, 
            password, 
            confirm_password
        )
        print(message)
