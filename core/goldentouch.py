from ursina import *
import time

class GoldenTouch:
    instance = None

    def __init__(self, button: Button, player, duration=10, cooldown=20, gold_per_click=1):
        GoldenTouch.instance = self

        self.duration = duration
        self.cooldown = cooldown
        self.gold_per_click = gold_per_click
        self.active = False
        self.on_cooldown = False
        self.activation_time = 0
        self.button = button
        self.player = player

        self.button.text = ''
        self.button.icon = '../assets/powerups/golden_touch.png'  
        self.button.icon.scale = (1, 1)
        self.set_button_color(color.gold)

        self.button.tooltip = Tooltip('Golden Touch!')
        self.button.tooltip.enabled = False

        self.button.on_click = self.toggle

    def toggle(self):
        if not self.active and not self.on_cooldown:
            self.activate()

    def activate(self):
        self.active = True
        self.activation_time = time.time()
        self.button.icon = '../assets/powerups/golden_touch.png' 
        self.button.icon.scale = (1, 1)
        self.set_button_color(color.yellow)
        invoke(self.deactivate, delay=self.duration)

    def deactivate(self):
        self.active = False
        self.on_cooldown = True
        self.activation_time = time.time()
        self.set_button_color(color.gray)
        self.button.icon = '../assets/powerups/golden_touch.png' 
        self.button.icon.scale = (1, 1)
        invoke(self.reset_cooldown, delay=self.cooldown)

    def reset_cooldown(self):
        self.on_cooldown = False
        self.set_button_color(color.gold)
        self.button.icon = '../assets/powerups/golden_touch.png' 
        self.button.icon.scale = (1, 1)

    def add_gold_on_click(self):
        if self.active:
            self.player.gold += self.gold_per_click
            return True
        return False

    def update(self):
        current_time = time.time()
        remaining = 0
        if self.on_cooldown:
            remaining = self.cooldown - (current_time - self.activation_time)
        elif self.active:
            remaining = self.duration - (current_time - self.activation_time)
        
        if remaining > 0:
            self.button.tooltip.text = f'{remaining:.1f}s'
        else:
            self.button.tooltip.text = 'Golden Touch!'

    def set_button_color(self, color_value):
        self.button.color = color_value
        self.button.highlight_color = color_value.tint(-0.2)
        self.button.pressed_color = color_value.tint(-0.3)