from ursina import *

class Background(Entity):
    def __init__(self, texture='bg.png'):
        super().__init__(
            model='quad',
            texture=texture,
            scale=(camera.aspect_ratio * 12.5, 12.5),  # Cobre toda a tela
            position=(0, 0),
            z=10, 
            texture_scale=(1, 1),  
            name='background'
        )
        self.texture.filtering = None
        self.texture.wrap = 'clamp'