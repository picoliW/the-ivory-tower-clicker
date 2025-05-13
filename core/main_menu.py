from ursina import *
from core.options_menu import OptionsMenu

class MainMenu(Entity):
    def __init__(self, start_game_callback):
        super().__init__()
        self.start_game_callback = start_game_callback

        self.hover_sound = Audio('../assets/sounds/hover_sound.mp3', autoplay=False)
        self.hover_sound.volume = 1
        self.click_sound = Audio('../assets/sounds/click_sound.mp3', autoplay=False)
        self.click_sound.volume = 1

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
            z=-0.1,
            parent=self
        )

        self.copyright_text = Text(
            text="© 2025 LEG Studios. The Ivory Tower™ is a trademark of LEG.\nAll rights reserved.",
            origin=(0, 14),
            color=color.white,
            scale=5.5,
            parent=self,
            z=-0.2
        )

        self.start_button = Button(
            text='Start Game',
            scale=(2.2, .7),
            position=(0, 1),
            color=color.clear,        
            text_color=color.white,
            on_click=Func(self.play_click_sound),
            parent=self,
            z=-0.2
        )
        self.start_button.on_click = Sequence(  
            Func(self.play_click_sound),
            Func(self.start_game)
        )
        self.start_button.text_entity.scale = (6, 13)
        self.apply_hover_effect(self.start_button)

        self.options_button = Button(
            text='Options',
            scale=(2.2, .7),
            position=(0, .5),
            color=color.clear,
            text_color=color.white,
            on_click=Func(self.play_click_sound), 
            parent=self,
            z=-0.2
        )
        self.options_button.on_click = Sequence(  
            Func(self.play_click_sound),
            Func(self.open_options)
        )
        self.options_button.text_entity.scale = (6, 13)
        self.apply_hover_effect(self.options_button)

        self.quit_button = Button(
            text='Quit',
            scale=(2.2, .7),
            position=(0, -1),
            color=color.clear,
            text_color=color.white,
            on_click=Func(self.play_click_sound),
            parent=self,
            z=-0.2
        )
        self.quit_button.on_click = Sequence( 
            Func(self.play_click_sound),
            Func(application.quit)
        )
        self.quit_button.text_entity.scale = (6, 13)
        self.apply_hover_effect(self.quit_button)

        self.game_logo = Entity(
            parent=self,
            model='quad',
            texture='../assets/logos/game_logo.png',
            scale=(6, 5),
            position=(0, 2.5),
            z=-0.2
        )

        self.dev_logo = Entity(
            parent=self,
            model='quad',
            texture='../assets/logos/dev_logo.png',
            scale=(2, 1),
            position=(6.4, -3.7),
            z=-0.2
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
        if not hasattr(self, 'options_popup') or not self.options_popup:
            self.options_popup = OptionsMenu(
                on_close=self.clear_options_popup,
                on_login_success=self.handle_login_success  
            )
            destroy(self.start_button)
            destroy(self.quit_button)
            
    def handle_login_success(self, user_id, player_data):
        self.start_game_callback(user_id, player_data)

    def clear_options_popup(self):
        self.options_popup = None

        if not self.start_button:  
            self.start_button = Button(
                text='Start Game',
                scale=(2.2, .7),
                position=(0, 1),
                color=color.clear,
                text_color=color.white,
                parent=self,
                z=-0.2
            )
            self.start_button.on_click = Sequence(
                Func(self.play_click_sound),
                Func(self.start_game)
            )
            self.start_button.text_entity.scale = (6, 13)
            self.apply_hover_effect(self.start_button)

        if not self.quit_button:
            self.quit_button = Button(
                text='Quit',
                scale=(2.2, .7),
                position=(0, -1),
                color=color.clear,
                text_color=color.white,
                parent=self,
                z=-0.2
            )
            self.quit_button.on_click = Sequence(
                Func(self.play_click_sound),
                Func(application.quit)
            )
            self.quit_button.text_entity.scale = (6, 13)
            self.apply_hover_effect(self.quit_button)
        else:  
            self.start_button.enable()
            self.quit_button.enable()

    def apply_hover_effect(self, button):
        original_scale = Vec3(6, 13, 1)
        hover_scale = original_scale * 1.1
        original_color = color.white
        hover_color = color.azure
        was_hovered = False 

        def update_hover():
            nonlocal was_hovered
            
            if button.hovered:
                button.text_entity.scale = lerp(button.text_entity.scale, hover_scale, 8 * time.dt)
                button.text_entity.color = hover_color
                
                if not was_hovered:
                    self.hover_sound.play()
                    was_hovered = True
            else:
                button.text_entity.scale = lerp(button.text_entity.scale, original_scale, 8 * time.dt)
                button.text_entity.color = original_color
                was_hovered = False

        button.update = update_hover

    def play_click_sound(self):
        self.click_sound.play()
