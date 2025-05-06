from ursina import *

class MainMenu(Entity):
    def __init__(self, start_game_callback):
        super().__init__()
        self.start_game_callback = start_game_callback

        window_ratio = window.aspect_ratio

        base_height = 10
        base_width = base_height * window_ratio

        self.frames = [load_texture(f'../assets/background_video/frame_{i}.png') for i in range(56)]
        self.frame_index = 0
        self.is_forward = True
        self.frame_timer = 0
        self.frame_delay = 0.1

        self.bg_music = Audio('../assets/sounds/main_menu_song.mp3', loop=True, autoplay=False)
        self.music_fade_out_start = 5  
        self.is_fading_out = False

        self.menu_bg = Entity(
            model='quad',
            scale=(base_width, base_height),
            texture=self.frames[0],
            z=1,
            parent=self
        )

        self.start_button = Button(
            text='Start Game',
            scale=(2.2, .7),
            position=(0, 1),
            color=color.clear,        
            text_color=color.white,
            on_click=self.start_game,
            parent=self
        )
        self.start_button.text_entity.scale = (6, 13)
        self.apply_hover_effect(self.start_button)

        self.options_button = Button(
            text='Options',
            scale=(2.2, .7),
            position=(0, .5),
            color=color.clear,
            text_color=color.white,
            on_click=self.open_options,
            parent=self
        )
        self.options_button.text_entity.scale = (6, 13)
        self.apply_hover_effect(self.options_button)

        self.quit_button = Button(
            text='Quit',
            scale=(2.2, .7),
            position=(0, -1),
            color=color.clear,
            text_color=color.white,
            on_click=application.quit,
            parent=self
        )
        self.quit_button.text_entity.scale = (6, 13)
        self.apply_hover_effect(self.quit_button)

        self.game_logo = Entity(
            parent=self,
            model='quad',
            texture='../assets/game_logo.png',
            scale=(6, 5),
            position=(0, 2.5)
        )

        self.dev_logo = Entity(
            parent=self,
            model='quad',
            texture='../assets/dev_logo.png',
            scale=(2, 1),
            position=(6.4, -3.7)
        )

        self.disable()
        self.update = self.animate_background

    def animate_background(self):
        self.frame_timer += time.dt
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.menu_bg.texture = self.frames[self.frame_index]

            if self.is_forward:
                self.frame_index += 1
                if self.frame_index >= len(self.frames):
                    self.frame_index = len(self.frames) - 2
                    self.is_forward = False
            else:
                self.frame_index -= 1
                if self.frame_index < 0:
                    self.frame_index = 1
                    self.is_forward = True
        
        if self.bg_music.playing:
            remaining_time = self.bg_music.length - self.bg_music.time
            if remaining_time < self.music_fade_out_start and not self.is_fading_out:
                self.is_fading_out = True
            
            if self.is_fading_out:
                fade_amount = remaining_time / self.music_fade_out_start
                self.bg_music.volume = max(0, fade_amount)
                
                if remaining_time <= 0:
                    self.bg_music.stop()
                    self.bg_music.play()
                    self.bg_music.volume = 1
                    self.is_fading_out = False

    def enable(self):
        super().enable()
        self.bg_music.play()
        self.bg_music.volume = 1
        self.is_fading_out = False

    def disable(self):
        super().disable()
        self.bg_music.stop()

    def start_game(self):
        self.disable()
        self.start_game_callback()

    def open_options(self):
        print("Abrir menu de opções (futuro)")

    def apply_hover_effect(self, button):
        original_scale = Vec3(6, 13, 1)
        hover_scale = original_scale * 1.1
        original_color = color.white
        hover_color = color.azure

        def update_hover():
            if button.hovered:
                button.text_entity.scale = lerp(button.text_entity.scale, hover_scale, 8 * time.dt)
                button.text_entity.color = hover_color
            else:
                button.text_entity.scale = lerp(button.text_entity.scale, original_scale, 8 * time.dt)
                button.text_entity.color = original_color

        button.update = update_hover

