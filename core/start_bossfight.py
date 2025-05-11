from core.bossfight import BossFight
from ursina import *

class Start_bossfight:
    def __init__(self, player, enemy_manager):
        self.player = player
        self.enemy_manager = enemy_manager
        self.boss_fight = None
        self.choice_made = False
        self.bossfight_win_sound = Audio('../assets/sounds/bossfightSounds/bossfightWin.wav', autoplay=False)

    def update(self):
        if self.boss_fight and self.boss_fight.active:
            self.boss_fight.update()
            return

        self.player.update()
        self.enemy_manager.update()

        if self.player.floor == 2 and not self.boss_fight:
            self.start_bossfight()

    def start_bossfight(self):
        def win():
            if not self.choice_made: 
                self.show_choice()
            else:
                self.finish_win_sequence()

        def fail():
            self.player.floor -= 1
            self.player.sprite.position = (-5, -2.5)
            self.enemy_manager.show_enemies()
            self.boss_fight = None
            self.choice_made = False  

        self.enemy_manager.hide_enemies()
        self.boss_fight = BossFight(self.player, on_win=win, on_fail=fail)
        self.choice_made = False  

    def show_choice(self):
        self.choice_panel = Panel(
            scale=(1.5, .8),
            position=(0, 0),
            texture='white_cube',
            color=color.rgba(0, 0, 0, 200),
            z=-10
        )
        
        self.choice_text = Text(
            text="Você derrotou o chefe! Escolha uma melhoria:",
            parent=self.choice_panel,
            position=(-0.25, 0.4),
            scale=(1, 2),
        )
        
        self.speed_button = Button(
            text="+ Movespeed / - Damage\n\n(20% Increased MS\n10% Decreased DMG Dealt)",
            parent=self.choice_panel,
            position=(-0.25, 0),
            scale=(0.4, 0.2),
            on_click=self.choose_speed
        )

        self.gradient_line = Entity(
            model='quad',
            scale=(0.01, .5),  
            position= 0,
            parent=self.choice_panel,
        )
        
        self.damage_button = Button(
            text="+ Damage / - Movespeed\n\n(10% Increased DMG Dealt\n20% Decreased MS)",
            parent=self.choice_panel,
            position=(0.25, 0),
            scale=(0.4, 0.2),
            on_click=self.choose_damage
        )

    def choose_speed(self):
        self.player.movespeed *= 1.2 
        self.player.damage *= 0.9     
        self.finish_choice()

    def choose_damage(self):
        self.player.damage *= 1.2     
        self.player.movespeed *= 0.9  
        self.finish_choice()

    def finish_choice(self):
        destroy(self.choice_panel)
        self.choice_made = True
        self.finish_win_sequence()

    def finish_win_sequence(self):
        self.player.floor += 1
        self.player.sprite.position = (-5, -2.5)
        self.bossfight_win_sound.play()
        self.enemy_manager.show_enemies()
        self.boss_fight = None
        self.player.save_data() 
