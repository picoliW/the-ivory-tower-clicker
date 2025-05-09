from ursina import *



class LoginForm(Entity):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.email_input = InputField(
            placeholder='E-mail',
            scale=(2, 0.4),
            position=(0, -0.5),
            parent=self,
            z=-1.1
        )

        self.email_input.text_field.scale = (6, 13)

        self.password_input = InputField(
            placeholder='Senha',
            scale=(2, 0.4),
            position=(0, -1.2),
            parent=self,
            z=-1.1
        )

        self.password_input.text_field.scale = (6, 13)

        MAX_CHARS = 5  

        def limit_input(text_field):
            if len(text_field.text) > MAX_CHARS:
                text_field.text = text_field.text[:MAX_CHARS]


        self.email_input.text_field.on_value_changed = lambda: limit_input(self.email_input.text_field)
        self.password_input.text_field.on_value_changed = lambda: limit_input(self.password_input.text_field)


class RegisterForm(Entity):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.email_input = InputField(
            placeholder='E-mail',
            scale=(1.5, 0.4),
            position=(1.8, 0.4),
            parent=self,
            z=-1.1
        )

        self.password_input = InputField(
            placeholder='Senha',
            scale=(1.5, 0.4),
            position=(1.8, 0),
            parent=self,
            z=-1.1
        )

        self.confirm_password_input = InputField(
            placeholder='Confirmar Senha',
            scale=(1.5, 0.4),
            position=(1.8, -0.4),
            parent=self,
            z=-1.1
        )

  
