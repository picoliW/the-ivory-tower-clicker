from ursina import *

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
        self.scroll_speed = 0.06
        self.should_scroll = True

    def update(self):
        if self.should_scroll:
            self.offset += time.dt * self.scroll_speed
            self.texture_offset = (self.offset % 1, 0)

        window_ratio = window.aspect_ratio
        base_height = 12.5
        self.scale = (base_height * window_ratio, base_height)
