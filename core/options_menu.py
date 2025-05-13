from ursina import *
from core.auth_forms import LoginForm, RegisterForm

class OptionsMenu(Entity):
    def __init__(self, on_close=None, on_login_success=None):
        super().__init__()
        self.on_close = on_close
        self.on_login_success = on_login_success
        self.login_button = None
        self.register_button = None
        self.login_form = None
        self.register_form = None
        
        self.master_volume = 1.0
        self.music_volume = 1.0
        self.sfx_volume = 1.0
        
        self.master_slider = None
        self.music_slider = None
        self.sfx_slider = None

        self.background = Entity(
            parent=self,
            model='quad',
            color=color.azure,
            scale=(7, 5),
            z=-0.3
        )

        self.settings_button = Button(
            scale=(1.8, .5),
            position=(-1.8, 1.73),
            parent=self,
            color=color.white,
            on_click=self.settings_clicked,
            z=-0.4
        )

        self.settings_icon = Entity(
            parent=self.settings_button,
            model='quad',
            texture='../assets/config_icons/config.png', 
            scale=(.25, .65),  
            z=-0.4 
        )

        self.account_button = Button(
            scale=(1.8, .5),
            position=(1.8, 1.73),
            parent=self,
            color=color.white,
            on_click=self.account_clicked,
            z=-0.4
        )
        
        self.account_icon = Entity(
            parent=self.account_button,
            model='quad',
            texture='../assets/config_icons/account.png', 
            scale=(.3, 1),  
            z=-0.4 
        )

        self.close_button = Button(
            scale=(0.8, 0.3),
            position=(3.15, 2.25),
            parent=self,
            color=color.clear,
            on_click=self.close,
            z=-0.4
        )

        self.close_icon = Entity(
            parent=self.close_button,
            model='quad',
            texture='../assets/config_icons/x.png', 
            scale=(0.6, 0.9),  
            z=-0.4  
        )

    def settings_clicked(self):
        for btn in [self.login_button, self.register_button]:
            if btn: destroy(btn)

        for form in [self.login_form, self.register_form]:
            if form: destroy(form)

        self.login_button = self.register_button = None
        self.login_form = self.register_form = None
        
        for slider in [self.master_slider, self.music_slider, self.sfx_slider]:
            if slider: destroy(slider)
        
        if not self.master_slider:
            self.create_volume_controls()

    def create_volume_controls(self):
        self.master_slider = Slider(
            min=0, 
            max=1, 
            default=self.master_volume,
            dynamic=True,
            position=(-2.1, 0.8),
            parent=self,
            scale=(9, 7),
            on_value_changed=self.update_master_volume,
            z=-0.4
        )
        Text(
            text="Master Volume",
            position=(-.5, 1.1),
            parent=self,
            scale=7.5,
            z=-0.4
        )
        
        self.music_slider = Slider(
            min=0, 
            max=1, 
            default=self.music_volume,
            dynamic=True,
            position=(-2.1, 0.3),
            parent=self,
            scale=(9, 7),
            on_value_changed=self.update_music_volume,
            z=-0.4
        )
        Text(
            text="Music Volume",
            position=(-.5, 0.6),
            parent=self,
            scale=7.5,
            z=-0.4
        )
        
        self.sfx_slider = Slider(
            min=0, 
            max=1, 
            default=self.sfx_volume,
            dynamic=True,
            position=(-2.1, -.2),
            parent=self,
            scale=(9, 7),
            on_value_changed=self.update_sfx_volume,
            z=-0.4
        )
        Text(
            text="SFX Volume",
            position=(-.5, .1),
            parent=self,
            scale=7.5,
            z=-0.4
        )

    def update_master_volume(self):
        self.master_volume = self.master_slider.value

        
    def update_music_volume(self):
        self.music_volume = self.music_slider.value

        
    def update_sfx_volume(self):
        self.sfx_volume = self.sfx_slider.value


    def account_clicked(self):
        if self.login_button or self.register_button:
            for btn in [self.login_button, self.register_button]:
                if btn: destroy(btn)
            for form in [self.login_form, self.register_form]:
                if form: destroy(form)

            self.login_button = self.register_button = None
            self.login_form = self.register_form = None
            return

        self.login_button = Button(
            text="Login",
            scale=(1.5, 0.4),
            position=(1.8, 1.1),
            parent=self,
            color=color.clear,
            text_size=.5,
            z=-0.4,
            on_click=self.show_login_form
        )

        self.register_button = Button(
            text="Register",
            scale=(1.5, 0.4),
            position=(1.8, 0.6), 
            parent=self,
            color=color.clear,
            text_size=.5,
            z=-0.4,
            on_click=self.show_register_form
        )

    def show_login_form(self):
        for btn in [self.login_button, self.register_button]:
            if btn: 
                destroy(btn)
        self.login_button = self.register_button = None

        if self.register_form:
            destroy(self.register_form)
            self.register_form = None

        if not self.login_form:
            self.login_form = LoginForm(parent=self)
            self.login_form.on_login_success = self.handle_login_success

    def show_register_form(self):
        for btn in [self.login_button, self.register_button]:
            if btn: 
                destroy(btn)
        self.login_button = self.register_button = None

        if self.login_form:
            destroy(self.login_form)
            self.login_form = None

        if not self.register_form:
            self.register_form = RegisterForm(parent=self)

    def handle_login_success(self, user_id, player_data):
        self.close()
        if self.on_login_success:
            self.on_login_success(user_id, player_data)

    def close(self):
        for btn in [self.login_button, self.register_button]:
            if btn: destroy(btn)

        for form in [self.login_form, self.register_form]:
            if form: destroy(form)
            
        for slider in [self.master_slider, self.music_slider, self.sfx_slider]:
            if slider: destroy(slider)

        if self.on_close:
            self.on_close() 

        destroy(self)