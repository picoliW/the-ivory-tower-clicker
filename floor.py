from ursina import *

class Floor(Entity):
    def __init__(self, texture='floor.png'):
        super().__init__(
            model='quad',
            texture=texture,
            scale=(camera.aspect_ratio * 12, 12),  # Cobre toda a tela
            position=(0, -1.5),
            z=1,  # Coloca atrás de todos os elementos
            texture_scale=(1, 1)  # Não repete a textura
        )
        # Garante que a textura não fique esticada
        self.texture.filtering = None
        self.texture.wrap = 'clamp'