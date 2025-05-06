from ursina import *

class MainMenu(Entity):
    def __init__(self, start_game_callback):
        super().__init__()
        self.start_game_callback = start_game_callback

        self.menu_bg = Entity(model='quad', scale=(20, 20), color=color.black, z=1, parent=self)

        self.start_button = Button(
            text='Iniciar Jogo',
            scale=(2.2, .7),
            y=-3,
            x=-4,
            color=color.azure,        
            text_color=color.white,
            on_click=self.start_game,
            parent=self
        )

        self.start_button.text_entity.scale = (4, 9)

        self.game_logo = Entity(
            parent=self,
            model='quad',
            texture='../assets/game_logo.png', 
            scale=(6, 5),  
            position=(0, 2.5) 
        )

        self.dev_logo = Entity(
            parent=self,
            model='quad',
            texture='../assets/dev_logo.png', 
            scale=(2, 1),  
            position=(6.4, -3.7) 
        )

        self.disable()

    def start_game(self):
        self.disable()
        self.start_game_callback()
