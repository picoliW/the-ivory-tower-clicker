# main_menu.py
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

        self.disable()

    def start_game(self):
        self.disable()
        self.start_game_callback()
