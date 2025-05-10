from ursina import *

class LoginForm(Entity):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.copyright_text = Text(
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

        self.copyright_text = Text(
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

class RegisterForm(Entity):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.email_input = InputField(
            placeholder='E-mail',
            scale=(4, 0.4),
            position=(0, -0.5),
            parent=self,
            z=-1.1
        )
        self.email_input.text_field.scale = (2.62, 16)

        self.password_input = InputField(
            placeholder='Senha',
            scale=(4, 0.4),
            position=(0, -1.2),
            parent=self,
            z=-1.1
        )
        self.password_input.text_field.scale = (2.62, 16)

        self.confirm_password_input = InputField(
            placeholder='Confirmar Senha',
            scale=(4, 0.4),
            position=(0, -1.9),
            parent=self,
            z=-1.1
        )
        self.confirm_password_input.text_field.scale = (2.62, 16)

  
