# main_menu.py
from ursina import *

class MainMenu(Entity):
    def __init__(self, start_game_callback):
        super().__init__()
        self.start_game_callback = start_game_callback

        self.menu_bg = Entity(model='quad', scale=(2, 1), color=color.black, z=1, parent=self)

        self.title = Text(text='The Ivory Tower', scale=2, y=0.3, parent=self)

        self.start_button = Button(
            text='Iniciar Jogo',
            scale=(3, 1),
            y=0,
            color=color.azure,
            on_click=self.start_game,
            parent=self
        )

        self.disable()

    def start_game(self):
        self.disable()
        self.start_game_callback()
