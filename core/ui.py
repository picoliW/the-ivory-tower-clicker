from ursina import *
from dashability import DashAbility

class UI:
    def __init__(self, player, enemy_manager):
        self.player = player
        self.enemy_manager = enemy_manager

        self.create_main_ui()
        self.create_hud_ui()
        self.create_run_button()

    def create_main_ui(self):
        self.floor_text = Text(text=f'Floor: {self.player.floor}', position=(-0.8, 0.45), scale=1.5)
        self.gold_text = Text(text=f'Gold: {self.player.gold}', position=(-0.8, 0.4), scale=1.5)
        self.enemy_count_text = Text(text=f'Enemies: {self.enemy_manager.enemies_defeated}/5', position=(-0.8, 0.35), scale=1.5)

    def create_hud_ui(self):
        self.gold_bg = Panel(
            scale=(0.45, 0.08),
            position=(0, 0.40), 
            texture='white_cube',
            texture_scale=(1, 1),
            color=color.rgba(50, 50, 50, 200),
            z=-1
        )

        self.gold_label = Text(
            text='Gold:',
            parent=self.gold_bg,
            position=(-0.23, 0),
            scale=(3, 15),
            origin=(0, 0),
            color=color.gold,
            bold=True,
        )

        self.gold_coin_img = Entity(
            parent=self.gold_bg,
            model='quad',
            texture="../assets/gold_coin.png",
            position=(-0.4, 0),
            scale=(0.15, 0.65),
            origin=(0, 0)
        )

        self.gold_value_text = Text(
            text=str(self.player.gold),
            parent=self.gold_bg,
            position=(0, 0),
            scale=(3, 15),
            origin=(0, 0),
            color=color.white
        )

        self.gold_text.enabled = False

    def create_run_button(self):
        self.run_button = Button(
            text='Run!',
            position=(0.80, -0.4),
            scale=(0.10, 0.10)
        )
        self.dash_ability = DashAbility(self.run_button)

    def update(self):
        self.floor_text.text = f'Floor: {self.player.floor}'
        self.gold_value_text.text = str(self.player.gold)
        self.enemy_count_text.text = f'Enemies: {self.enemy_manager.enemies_defeated}/5'
        self.dash_ability.update()
