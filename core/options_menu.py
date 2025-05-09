from ursina import *

class OptionsMenu(Entity):
    def __init__(self, on_close=None):
        super().__init__()
        self.on_close = on_close

        self.background = Entity(
            parent=self,
            model='quad',
            color=color.gray,
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
            scale=(.5, .3),
            position=(-2, 1),
            parent=self,
            color=color.clear,
            on_click=self.settings_clicked,
            text_size=0.5,
            z=-1
        )

        self.x_icon = Entity(
            parent=self.settings_button,
            model='quad',
            texture='../assets/config_icons/config.png', 
            scale=(.1, .1),  
            z=-0.1,  
        )

        self.account_button = Button(
            text='Conta',
            scale=(1.8, 0.5),
            position=(2, 1),
            parent=self,
            color=color.orange,
            on_click=self.account_clicked,
            text_size=0.5,
            z=-1
        )

        self.close_button = Button(
            scale=(0.8, 0.3),
            position=(3.15, 2.25),
            parent=self,
            color=color.clear,
            on_click=self.close,
            text_size=0.5,
            z=-1
        )

        self.x_icon = Entity(
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

    def close(self):
        if self.on_close:
            self.on_close()
        destroy(self)
