from ursina import *

class UI:
    def __init__(self, player, enemy_manager, shop):
        self.player = player
        self.enemy_manager = enemy_manager
        self.shop = shop
        
        # Elementos da UI
        self.floor_text = Text(text=f'Floor: {self.player.floor}', position=(-0.8, 0.45), scale=1.5)
        self.gold_text = Text(text=f'Gold: {self.player.gold}', position=(-0.8, 0.4), scale=1.5)
        self.enemy_count_text = Text(text=f'Enemies: {self.enemy_manager.enemies_defeated}/5', position=(-0.8, 0.35), scale=1.5)
        
        # Botões da loja
        self.damage_button = Button(text=f'Upgrade Damage ({self.shop.damage_upgrade_cost} gold)', position=(0.6, 0.3), scale=(0.3, 0.1))
        self.damage_button.on_click = self.upgrade_damage
        
        self.gold_button = Button(text=f'Upgrade Gold/s ({self.shop.gold_upgrade_cost} gold)', position=(0.6, 0.2), scale=(0.3, 0.1))
        self.gold_button.on_click = self.upgrade_gold
        
        self.dash_button = Button(text=f'Unlock Dash ({self.shop.dash_cost} gold)', position=(0.6, 0.1), scale=(0.3, 0.1))
        self.dash_button.on_click = self.buy_dash
        
        
    def update(self):
        # Atualiza textos
        self.floor_text.text = f'Floor: {self.player.floor}'
        self.gold_text.text = f'Gold: {self.player.gold}'
        self.enemy_count_text.text = f'Enemies: {self.enemy_manager.enemies_defeated}/5'
        
        # Atualiza botões
        self.damage_button.text = f'Upgrade Damage ({self.shop.damage_upgrade_cost} gold)'
        self.gold_button.text = f'Upgrade Gold/s ({self.shop.gold_upgrade_cost} gold)'
        self.dash_button.text = f'Unlock Dash ({self.shop.dash_cost} gold)'
        self.dash_button.disabled = self.player.dash_unlocked
                
    def upgrade_damage(self):
        self.shop.buy_damage_upgrade()
        
    def upgrade_gold(self):
        self.shop.buy_gold_upgrade()
        
    def buy_dash(self):
        self.shop.buy_dash()