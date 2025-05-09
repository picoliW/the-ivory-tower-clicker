from ursina import *

class OptionsMenu(Entity):
    def __init__(self, on_close=None):
        super().__init__()
        self.on_close = on_close
        self.login_button = None
        self.register_button = None

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
        print("Abrindo configurações...")

    def account_clicked(self):
        print("Abrindo conta...")
        
        if self.login_button:
            destroy(self.login_button)
            destroy(self.register_button)
            self.login_button = None
            self.register_button = None
            return
            
        self.login_button = Button(
            text="Login",
            scale=(1.5, 0.4),
            position=(1.8, 1.1),
            parent=self,
            color=color.clear,
            text_size=.5,
            z=-1
        )
        
        self.register_button = Button(
            text="Registrar",
            scale=(1.5, 0.4),
            position=(1.8, 0.6), 
            parent=self,
            color=color.clear,
            text_size=.5,
            z=-1
        )

    def close(self):
        if self.login_button:
            destroy(self.login_button)
        if self.register_button:
            destroy(self.register_button)
            
        if self.on_close:
            self.on_close()
        destroy(self)