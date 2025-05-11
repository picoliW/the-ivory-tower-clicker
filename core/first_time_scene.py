from ursina import *

class FirstTimeScene(Entity):
    def __init__(self, on_complete, player=None):
        super().__init__()
        self.on_complete = on_complete
        self.player = player

        self.background = Entity(model='quad', texture='white_cube', color=color.black, scale=(20, 10), z=1)

        if self.player:
            self.player.sprite.z = 10
        
        self.intro_text = Text("In a pacific time...", y=0.2, origin=(0,0), scale=2, color=color.white)
        self.intro_text.fade_out = False
        self.intro_text.fade_speed = 0.5
        self.intro_text.alpha = 1
        
        self.intro_image = Entity(
            model='quad', 
            texture='../assets/pacific_time.png', 
            scale=(10, 5), 
            color=color.white,
            alpha=0 
        )
        self.image_shown = False
        
        self.skip_button = Button(text="Pular", position=(0,-0.3), scale=(0.2, 0.1), on_click=self.skip)
        
        invoke(self.start_fade_out, delay=2)  
        
    def start_fade_out(self):
        self.intro_text.fade_out = True
        
    def update(self):
        if self.intro_text.fade_out and self.intro_text.alpha > 0:
            self.intro_text.alpha -= time.dt * self.intro_text.fade_speed
            if self.intro_text.alpha <= 0 and not self.image_shown:
                self.show_image()
        
        if hasattr(self, 'intro_image') and self.image_shown:
            if self.intro_image.alpha < 1:
                self.intro_image.alpha += time.dt * 0.5
            else:
                if self.text.alpha < 1:
                    self.text.alpha += time.dt * 0.5
    
    def show_image(self):
        self.image_shown = True
        self.intro_image.alpha = 0 
        invoke(self.start_image_fade_out, delay=3)  
        
    def start_image_fade_out(self):
        if hasattr(self, 'intro_image'):
            self.intro_image.fade_out = True
            self.intro_image.fade_speed = 0.5
            
        if self.intro_image.fade_out and self.intro_image.alpha > 0:
            self.intro_image.alpha -= time.dt * self.intro_image.fade_speed
            
    def skip(self):
        self.background.disable()
        if hasattr(self, 'intro_text'):
            self.intro_text.disable()
        if hasattr(self, 'intro_image'):
            self.intro_image.disable()
        if hasattr(self, 'skip_button'):
            self.skip_button.disable()
        if self.player:
            self.player.sprite.z = 0

        self.on_complete()