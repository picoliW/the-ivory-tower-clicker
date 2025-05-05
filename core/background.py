from ursina import *

class Background(Entity):
    def __init__(self, texture='../assets/bg.png'):
        super().__init__(
            model='quad',
            texture=texture,
            scale=(22, 12.5),
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
