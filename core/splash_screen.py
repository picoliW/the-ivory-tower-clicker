from ursina import *

class SplashScreen(Entity):
    def __init__(self):
        super().__init__()

        self.bg = Entity(model='quad', scale=(20, 20), color=color.black, z=1, parent=self)

        self.logo = Entity(
            parent=self,
            model='quad',
            texture='../assets/dev_logo.png',
            position=(0, 0, -10),
            scale=(3, 2),
            color=color.white
        )
