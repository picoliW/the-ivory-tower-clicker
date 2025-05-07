import time
from ursina import *

class DashAbility:
    instance = None  

    def __init__(self, button: Button, duration=5, cooldown=10):
        DashAbility.instance = self  

        self.duration = duration
        self.cooldown = cooldown
        self.active = False
        self.on_cooldown = False
        self.activation_time = 0
        self.button = button

        self.button.text = 'Run!'
        self.button.color = color.lime
        self.button.highlight_color = color.lime.tint(-0.2)
        self.button.pressed_color = color.lime.tint(-0.3)
        self.button.on_click = self.toggle

    def toggle(self):
        if not self.active and not self.on_cooldown:
            self.activate()

    def activate(self):
        self.active = True
        self.activation_time = time.time()
        self.button.color = color.orange
        invoke(self.deactivate, delay=self.duration)
        print("Speed boost activated!")

    def deactivate(self):
        self.active = False
        self.on_cooldown = True
        self.activation_time = time.time()
        self.button.color = color.gray
        invoke(self.reset_cooldown, delay=self.cooldown)
        print("Speed boost ended. Cooldown started.")

    def reset_cooldown(self):
        self.on_cooldown = False
        self.button.color = color.lime
        print("Speed boost ready again!")

    def update(self):
        current_time = time.time()
        if self.on_cooldown:
            remaining = self.cooldown - (current_time - self.activation_time)
            self.button.text = f'{remaining:.1f}s' if remaining > 0 else 'Run!'
        elif self.active:
            remaining = self.duration - (current_time - self.activation_time)
            self.button.text = f'{remaining:.1f}s' if remaining > 0 else 'Run!'
        else:
            self.button.text = 'Run!'
