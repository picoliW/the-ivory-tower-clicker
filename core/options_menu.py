from ursina import *
from auth_forms import LoginForm, RegisterForm

class OptionsMenu(Entity):
    def __init__(self, on_close=None):
        super().__init__()
        self.on_close = on_close
        self.login_button = None
        self.register_button = None
        self.login_form = None
        self.register_form = None

        self.background = Entity(
            parent=self,
            model='quad',
            color=color.azure,
            scale=(7, 5),
            z=-1
        )

        self.title = Text(
            text='Opções',
            origin=(0, 0),
            scale=(2,2),
            position=(0, 1.1),
            parent=self,
            z=-1
        )

        self.settings_button = Button(
            scale=(1.8, .5),
            position=(-1.8, 1.73),
            parent=self,
            color=color.white,
            on_click=self.settings_clicked,
            z=-1
        )

        self.settings_icon = Entity(
            parent=self.settings_button,
            model='quad',
            texture='../assets/config_icons/config.png', 
            scale=(.25, .65),  
            z=-0.1,  
        )

        self.account_button = Button(
            scale=(1.8, .5),
            position=(1.8, 1.73),
            parent=self,
            color=color.white,
            on_click=self.account_clicked,
            z=-1
        )
        
        self.account_icon = Entity(
            parent=self.account_button,
            model='quad',
            texture='../assets/config_icons/account.png', 
            scale=(.3, 1),  
            z=-0.1,  
        )

        self.close_button = Button(
            scale=(0.8, 0.3),
            position=(3.15, 2.25),
            parent=self,
            color=color.clear,
            on_click=self.close,
            z=-1
        )

        self.close_icon = Entity(
            parent=self.close_button,
            model='quad',
            texture='../assets/config_icons/x.png', 
            scale=(0.6, 0.9),  
            z=-0.1,  
        )

    def settings_clicked(self):
        for btn in [self.login_button, self.register_button]:
            if btn: destroy(btn)

        for form in [self.login_form, self.register_form]:
            if form: destroy(form)

        self.login_button = self.register_button = None
        self.login_form = self.register_form = None

    def account_clicked(self):
        if self.login_button or self.register_button:
            for btn in [self.login_button, self.register_button]:
                if btn: destroy(btn)
            for form in [self.login_form, self.register_form]:
                if form: destroy(form)

            self.login_button = self.register_button = None
            self.login_form = self.register_form = None
            return

        self.login_button = Button(
            text="Login",
            scale=(1.5, 0.4),
            position=(1.8, 1.1),
            parent=self,
            color=color.clear,
            text_size=.5,
            z=-1,
            on_click=self.show_login_form
        )

        self.register_button = Button(
            text="Registrar",
            scale=(1.5, 0.4),
            position=(1.8, 0.6), 
            parent=self,
            color=color.clear,
            text_size=.5,
            z=-1,
            on_click=self.show_register_form
        )

    def show_login_form(self):
        if self.register_form:
            destroy(self.register_form)
            self.register_form = None

        if not self.login_form:
            self.login_form = LoginForm(parent=self)

    def show_register_form(self):
        if self.login_form:
            destroy(self.login_form)
            self.login_form = None

        if not self.register_form:
            self.register_form = RegisterForm(parent=self)

    def close(self):
        for btn in [self.login_button, self.register_button]:
            if btn: destroy(btn)

        for form in [self.login_form, self.register_form]:
            if form: destroy(form)

        if self.on_close:
            self.on_close()
        destroy(self)