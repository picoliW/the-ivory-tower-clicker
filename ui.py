from ursina import *

class UI:
    def __init__(self, player, enemy_manager, shop):
        self.player = player
        self.enemy_manager = enemy_manager
        self.shop = shop
        self.shop_visible = False
        
        # Elementos da UI principal
        self.floor_text = Text(text=f'Floor: {self.player.floor}', position=(-0.8, 0.45), scale=1.5)
        self.gold_text = Text(text=f'Gold: {self.player.gold}', position=(-0.8, 0.4), scale=1.5)
        self.enemy_count_text = Text(text=f'Enemies: {self.enemy_manager.enemies_defeated}/5', position=(-0.8, 0.35), scale=1.5)
        
        # Botão para abrir/fechar a loja
        self.shop_button = Button(text='Shop', position=(0.7, 0.4), scale=(0.2, 0.08))
        self.shop_button.on_click = self.toggle_shop
        
        # Elementos da loja (inicialmente invisíveis)
        self.create_shop_ui()
        self.set_shop_visibility(False)
        
    def create_shop_ui(self):
        # Fundo da loja
        self.shop_background = Entity(
            model='quad',
            color=color.dark_gray,
            scale=(0.7, 0.8),
            position=(0, 0),
            z=-1
        )
        
        # Título da loja
        self.shop_title = Text(
            text='SHOP',
            position=(0, 0.35),
            scale=2,
            origin=(0, 0),
            z=-1
        )
        
        # Botões da loja
        self.damage_button = Button(
            text=f'Upgrade Damage ({self.shop.damage_upgrade_cost} gold)',
            position=(0, 0.1),
            scale=(0.4, 0.1))
        self.damage_button.on_click = self.upgrade_damage
        
        self.gold_button = Button(
            text=f'Upgrade Gold/s ({self.shop.gold_upgrade_cost} gold)',
            position=(0, -0.05),
            scale=(0.4, 0.1))
        self.gold_button.on_click = self.upgrade_gold
        
        self.dash_button = Button(
            text=f'Unlock Dash ({self.shop.dash_cost} gold)',
            position=(0, -0.2),
            scale=(0.4, 0.1))
        self.dash_button.on_click = self.buy_dash
        
        # Botão para fechar a loja
        self.close_shop_button = Button(
            text='Close',
            position=(0, -0.35),
            scale=(0.2, 0.08),
            color=color.red)
        self.close_shop_button.on_click = self.toggle_shop
        
    def set_shop_visibility(self, visible):
        self.shop_visible = visible
        self.shop_background.enabled = visible
        self.shop_title.enabled = visible
        self.damage_button.enabled = visible
        self.gold_button.enabled = visible
        self.dash_button.enabled = visible
        self.close_shop_button.enabled = visible
        
    def toggle_shop(self):
        self.set_shop_visibility(not self.shop_visible)
        
    def update(self):
        # Atualiza textos da UI principal
        self.floor_text.text = f'Floor: {self.player.floor}'
        self.gold_text.text = f'Gold: {self.player.gold}'
        self.enemy_count_text.text = f'Enemies: {self.enemy_manager.enemies_defeated}/5'
        
        # Atualiza textos dos botões da loja (mesmo quando invisíveis)
        self.damage_button.text = f'Upgrade Damage ({self.shop.damage_upgrade_cost} gold)'
        self.gold_button.text = f'Upgrade Gold/s ({self.shop.gold_upgrade_cost} gold)'
        self.dash_button.text = f'Unlock Dash ({self.shop.dash_cost} gold)'
        self.dash_button.disabled = self.player.dash_unlocked
                
    def upgrade_damage(self):
        if self.shop.buy_damage_upgrade():
            # Feedback visual
            self.damage_button.blink(color.green)
        
    def upgrade_gold(self):
        if self.shop.buy_gold_upgrade():
            self.gold_button.blink(color.green)
        
    def buy_dash(self):
        if self.shop.buy_dash():
            self.dash_button.blink(color.green)