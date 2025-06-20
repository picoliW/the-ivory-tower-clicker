from ursina import *
from core.abilities.dashability import DashAbility
from core.abilities.goldentouch import GoldenTouch

class UI:
    def __init__(self, player, enemy_manager):
        self.player = player
        self.enemy_manager = enemy_manager

        self.create_main_ui()
        self.create_hud_ui()
        self.create_golden_touch_button()
        self.create_run_button()

    def disable_ui(self):
        self.floor_text.enabled = False
        self.gold_text.enabled = False
        self.enemy_count_text.enabled = False
        self.gold_bg.enabled = False
        self.gold_label.enabled = False
        self.gold_coin_img.enabled = False
        self.gold_value_text.enabled = False
        self.golden_touch_button.enabled = False
        self.run_button.enabled = False

    def enable_ui(self):
        self.floor_text.enabled = True
        self.gold_text.enabled = False  
        self.enemy_count_text.enabled = True
        self.gold_bg.enabled = True
        self.gold_label.enabled = True
        self.gold_coin_img.enabled = True
        self.gold_value_text.enabled = True
        self.golden_touch_button.enabled = True
        self.run_button.enabled = True

    def create_main_ui(self):
        self.floor_text = Text(
            text=f'Floor: {self.player.floor}', 
            #position=(-0.6, 0.45), XERECA
            position=(-0.6, 0.45), 
            scale=1.5,
            z=-0.1
        )
        self.gold_text = Text(
            text=f'Gold: {self.player.gold}', 
            position=(-0.8, 0.4), 
            scale=1.5,
            z=-0.2
        )
        self.enemy_count_text = Text(
            text=f'Enemies: {self.enemy_manager.enemies_defeated}/5', 
            #position=(-0.6, 0.35),  XERECA
            position=(-0.6, 0.35), 
            scale=1.5,
            z=-0.1
        )

    def create_hud_ui(self):
        self.gold_bg = Panel(
            scale=(0.45, 0.08),
            position=(0, 0.40), 
            texture='white_cube',
            texture_scale=(1, 1),
            color=color.gray,
            z=-0.1
        )

        self.gold_label = Text(
            text='Gold:',
            parent=self.gold_bg,
            position=(-0.23, 0),
            scale=(3, 15),
            origin=(0, 0),
            color=color.gold,
            bold=True,
            z=-0.2
        )

        self.gold_coin_img = Entity(
            parent=self.gold_bg,
            model='quad',
            texture="../assets/gold_coin.png",
            position=(-0.4, 0),
            scale=(0.15, 0.65),
            origin=(0, 0),
        )

        self.gold_value_text = Text(
            text=str(self.player.gold),
            parent=self.gold_bg,
            position=(0, 0),
            scale=(3, 15),
            origin=(0, 0),
            color=color.gold,
            z=-0.2
        )

        self.gold_text.enabled = False

    def create_golden_touch_button(self):
        self.golden_touch_button = Button(
            text='Golden Touch!',
            # position=(-.8, -0.3),  XERECA
            position=(-.6, -0.3),  
            scale=(0.1, 0.1)
        )
        self.golden_touch = GoldenTouch(self.golden_touch_button, self.player)
        setattr(self.player, 'golden_touch', self.golden_touch)
    

    def create_run_button(self):
        self.run_button = Button(
            text='Run!',
            # position=(-.8, -0.42),  XERECA
            position=(-.6, -0.42),
            scale=(0.1, 0.1)
        )
        self.dash_ability = DashAbility(self.run_button)

    def update(self):
        self.floor_text.text = f'Floor: {self.player.floor}'
        self.gold_value_text.text = str(self.player.gold)
        self.enemy_count_text.text = f'Enemies: {self.enemy_manager.enemies_defeated}/5'
        self.dash_ability.update()
        self.golden_touch.update()
