from ursina import *
from dashability import DashAbility

class Background(Entity):
    def __init__(self, texture='../assets/bg.png'):
        window_ratio = window.aspect_ratio  
        base_height = 12.5  
        base_width = base_height * window_ratio

        super().__init__(
            model='quad',
            texture=texture,
            scale=(base_width, base_height),
            position=(0, 0),
            z=10,
            texture_scale=(1, 1),
            name='background'
        )

        self.texture.filtering = None
        self.texture.wrap = 'repeat'
        self.offset = 0
        self.base_scroll_speed = 0.06
        self.should_scroll = True

    def update(self):
        if self.should_scroll:
            dash = DashAbility.instance  
            speed_multiplier = 2 if dash and dash.active else 1
            current_speed = self.base_scroll_speed * speed_multiplier
            self.offset += time.dt * current_speed
            self.texture_offset = (self.offset % 1, 0)

        window_ratio = window.aspect_ratio
        base_height = 12.5
        self.scale = (base_height * window_ratio, base_height)
