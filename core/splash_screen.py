# splash_screen.py
from ursina import *

class SplashScreen(Entity):
    def __init__(self):
        super().__init__()

        self.logo = Entity(
            parent=self,
            model='quad',
            texture='../assets/splash_screen.png',
            position=(0, 0, -10),
            scale=(1.5, 0.75),
            color=color.white
        )
