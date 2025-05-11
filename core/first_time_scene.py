from ursina import *

class FirstTimeScene(Entity):
    def __init__(self, on_complete, player=None):
        super().__init__()
        self.on_complete = on_complete
        self.player = player

        self.background = Entity(model='quad', texture='white_cube', color=color.black, scale=(20, 10), z=1)

        if self.player:
            self.player.sprite.z = 10
        
        # First text
        self.intro_text = Text("In a pacific time...", y=0.2, origin=(0,0), scale=2, color=color.white)
        self.intro_text.fade_out = False
        self.intro_text.fade_speed = 0.5
        self.intro_text.alpha = 1
        
        # First image
        self.intro_image = Entity(
            model='quad', 
            texture='../assets/pacific_time.png', 
            scale=(10, 5), 
            color=color.white,
            alpha=0,
            z=0.5
        )
        
        # Second text
        self.second_text = Text(
            "But things have changed...", 
            y=0.2, 
            origin=(0,0), 
            scale=2, 
            color=color.white,
            alpha=0,
            z=0.6
        )
        
        # Second image
        self.second_image = Entity(
            model='quad',
            texture='../assets/things_changed.png', 
            scale=(10, 5),
            color=color.white,
            alpha=0,
            z=0.5
        )
        
        # Third text
        self.third_text = Text(
            "Now he's going to risk it all, to rescue his all",
            y=0.2,
            origin=(0,0),
            scale=2,
            color=color.white,
            alpha=0,
            z=0.6
        )
        
        # Third image
        self.third_image = Entity(
            model='quad',
            texture='../assets/risk_it_all.png',
            scale=(10, 5),
            color=color.white,
            alpha=0,
            z=0.5
        )
        
        self.current_stage = 0
        self.skip_button = Button(text="Pular", position=(0,-0.3), scale=(0.2, 0.1), on_click=self.skip, z=0.7)
        
        invoke(self.start_fade_out, delay=2)
        
    def start_fade_out(self):
        self.intro_text.fade_out = True
        
    def update(self):
        if self.current_stage == 0:  # First text fading out
            if self.intro_text.fade_out and self.intro_text.alpha > 0:
                self.intro_text.alpha -= time.dt * self.intro_text.fade_speed
                if self.intro_text.alpha <= 0:
                    self.current_stage = 1
                    self.intro_image.alpha = 0  # Start showing first image
                    invoke(self.start_image_fade_out, delay=3)  # Schedule its fade out
        
        elif self.current_stage == 1:  # First image fading in
            if self.intro_image.alpha < 1:
                self.intro_image.alpha += time.dt * 0.5
        
        elif self.current_stage == 1.5:  # First image fading out
            if hasattr(self.intro_image, 'fade_out') and self.intro_image.alpha > 0:
                self.intro_image.alpha -= time.dt * 0.5
                if self.intro_image.alpha <= 0:
                    self.current_stage = 2
                    self.second_text.alpha = 0  # Start showing second text
                    invoke(self.start_second_text_fade_out, delay=3)  # Schedule its fade out
        
        elif self.current_stage == 2:  # Second text fading in
            if self.second_text.alpha < 1:
                self.second_text.alpha += time.dt * 0.5
        
        elif self.current_stage == 2.5:  # Second text fading out
            if hasattr(self.second_text, 'fade_out') and self.second_text.alpha > 0:
                self.second_text.alpha -= time.dt * 0.5
                if self.second_text.alpha <= 0:
                    self.current_stage = 3
                    self.second_image.alpha = 0  # Start showing second image
                    invoke(self.start_second_image_fade_out, delay=3)  # Schedule its fade out
        
        elif self.current_stage == 3:  # Second image fading in
            if self.second_image.alpha < 1:
                self.second_image.alpha += time.dt * 0.5
        
        elif self.current_stage == 3.5:  # Second image fading out
            if hasattr(self.second_image, 'fade_out') and self.second_image.alpha > 0:
                self.second_image.alpha -= time.dt * 0.5
                if self.second_image.alpha <= 0:
                    self.current_stage = 4
                    self.third_text.alpha = 0  # Start showing third text
                    invoke(self.start_third_text_fade_out, delay=3)  # Schedule its fade out
        
        elif self.current_stage == 4:  # Third text fading in
            if self.third_text.alpha < 1:
                self.third_text.alpha += time.dt * 0.5
        
        elif self.current_stage == 4.5:  # Third text fading out
            if hasattr(self.third_text, 'fade_out') and self.third_text.alpha > 0:
                self.third_text.alpha -= time.dt * 0.5
                if self.third_text.alpha <= 0:
                    self.current_stage = 5
                    self.third_image.alpha = 0  # Start showing third image
        
        elif self.current_stage == 5:  # Third image fading in
            if self.third_image.alpha < 1:
                self.third_image.alpha += time.dt * 0.5
            elif not hasattr(self.third_image, 'fade_out'):
                invoke(self.start_third_image_fade_out, delay=3)
        
        elif self.current_stage == 5.5:  # Third image fading out
            if hasattr(self.third_image, 'fade_out') and self.third_image.alpha > 0:
                self.third_image.alpha -= time.dt * 0.5
                if self.third_image.alpha <= 0:
                    self.complete_scene()
    
    def start_image_fade_out(self):
        self.intro_image.fade_out = True
        self.current_stage = 1.5
    
    def start_second_text_fade_out(self):
        self.second_text.fade_out = True
        self.current_stage = 2.5
    
    def start_second_image_fade_out(self):
        self.second_image.fade_out = True
        self.current_stage = 3.5
    
    def start_third_text_fade_out(self):
        self.third_text.fade_out = True
        self.current_stage = 4.5
    
    def start_third_image_fade_out(self):
        self.third_image.fade_out = True
        self.current_stage = 5.5
    
    def complete_scene(self):
        self.skip()
    
    def skip(self):
        self.background.disable()
        if hasattr(self, 'intro_text'):
            self.intro_text.disable()
        if hasattr(self, 'intro_image'):
            self.intro_image.disable()
        if hasattr(self, 'second_text'):
            self.second_text.disable()
        if hasattr(self, 'second_image'):
            self.second_image.disable()
        if hasattr(self, 'third_text'):
            self.third_text.disable()
        if hasattr(self, 'third_image'):
            self.third_image.disable()
        if hasattr(self, 'skip_button'):
            self.skip_button.disable()
        if self.player:
            self.player.sprite.z = 0
        self.on_complete()