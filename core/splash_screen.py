from ursina import *

class SplashScreen(Entity):
    def __init__(self):
        super().__init__()

        self.bg = Entity(model='quad', scale=(20, 20), color=color.black, z=1, parent=self)

        self.logo = Entity(
            parent=self,
            model='quad',
            texture='../assets/logos/dev_logo.png',
            position=(0, 0, -10),
            scale=(3, 2),
            color=color.white
        )

        self.bg.color = color.black
        self.logo.color = color.white

        self.fading_out = False
        self.fade_speed = 2
        self.on_fade_out_complete = None  

    def fade_out(self, on_complete=None):
        self.fading_out = True
        self.on_fade_out_complete = on_complete

    def update(self):
        if self.fading_out:
            self.logo.color = lerp(self.logo.color, color.clear, time.dt * self.fade_speed)

            if self.logo.color.a < 0.05:
                self.disable()
                self.fading_out = False
                if self.on_fade_out_complete:
                    self.on_fade_out_complete()
