from ursina import *

class UI:
    def __init__(self, player, enemy_manager, shop):
        self.player = player
        self.enemy_manager = enemy_manager
        self.shop = shop
        self.shop_visible = False
        self.shop_scroll_position = 0
        
        self.create_main_ui()
        self.create_shop_ui()
        self.set_shop_visibility(False)
        
    def create_main_ui(self):
        self.floor_text = Text(text=f'Floor: {self.player.floor}', position=(-0.8, 0.45), scale=1.5)
        self.gold_text = Text(text=f'Gold: {self.player.gold}', position=(-0.8, 0.4), scale=1.5)
        self.enemy_count_text = Text(text=f'Enemies: {self.enemy_manager.enemies_defeated}/5', position=(-0.8, 0.35), scale=1.5)
        
        # Botão da loja
        self.shop_button = Button(
            text='Shop',
            position=(0.7, 0.4),
            scale=(0.2, 0.08),
            color=color.orange,
            on_click=self.toggle_shop
        )
        
    def create_shop_ui(self):
        # Fundo da loja (popup)
        self.shop_background = Panel(
            scale=(0.8, 0.8),
            position=(0, 0),
            texture='white_cube',
            texture_scale=(1, 1),
            color=color.dark_gray,
            z=-1
        )
        
        # Título da loja
        self.shop_title = Text(
            text='SHOP',
            position=(0, 0.35),
            scale=2,
            origin=(0, 0),
            background=True
        )
        
        # Botões de scroll
        self.scroll_up_btn = Button(
            parent=self.shop_background,
            texture='assets/arrow_up',
            position=(0.7, 0.25),
            scale=(0.1, 0.05),
            on_click=self.scroll_up
        )
        
        self.scroll_down_btn = Button(
            parent=self.shop_background,
            texture='assets/arrow_down',
            position=(0.7, -0.25),
            scale=(0.1, 0.05),
            on_click=self.scroll_down
        )
        
        self.shop_items_ui = []
        for i in range(4): 
            y_pos = 0.35 - (i * 0.18) 
            
            # Container do item
            item_bg = Entity(
                parent=self.shop_background,
                model='quad',
                color=color.rgba(0, 0, 0, 255),
                scale=(0.7, 0.15),
                position=(0, y_pos),
                origin=(0, 0),
                enabled=False  
            )
            
            # Imagem do item
            item_icon = Entity(
                parent=item_bg,
                model='quad',
                scale=(0.4, 1.0),
                position=(-0.35, 0),
                origin=(0, 0))
            
            # Nome e preço
            item_name = Text(
                parent=item_bg,
                position=(-0.1, 0.03),
                scale=1,
                origin=(-0.5, 0))
            
            # Descrição do efeito
            item_effect = Text(
                parent=item_bg,
                position=(0.1, -0.03),
                scale=1,
                origin=(-0.5, 0),
                color=color.yellow)
            
            # Botão de compra
            buy_btn = Button(
                parent=item_bg,
                text='BUY',
                position=(0.35, 0),
                scale=(0.2, 0.08),
                color=color.green.tint(-0.2))
            
            self.shop_items_ui.append({
                'background': item_bg,
                'icon': item_icon,
                'name': item_name,
                'effect': item_effect,
                'button': buy_btn
            })
        
        self.close_btn = Button(
            parent=self.shop_background,
            text='CLOSE',
            position=(0, -0.4),
            scale=(0.2, 0.08),
            color=color.red.tint(-0.2),
            on_click=self.toggle_shop
        )
        
        self.update_visible_items()
        
    def scroll_up(self):
        if self.shop_scroll_position > 0:
            self.shop_scroll_position -= 1
            self.update_visible_items()
    
    def scroll_down(self):
        if self.shop_scroll_position + 4 < len(self.shop.items):
            self.shop_scroll_position += 1
            self.update_visible_items()
    
    def update_visible_items(self):
        self.scroll_up_btn.enabled = (self.shop_scroll_position > 0)
        self.scroll_down_btn.enabled = (self.shop_scroll_position + 4 < len(self.shop.items))
        
        for i in range(4):
            item_ui = self.shop_items_ui[i]
            item_index = self.shop_scroll_position + i
            
            if item_index < len(self.shop.items):
                item = self.shop.items[item_index]
                
                item_ui['background'].enabled = True
                
                item_ui['icon'].texture = f'assets/{item.texture}'
                item_ui['name'].text = f"{item.name} ({item.cost}g)"
                item_ui['effect'].text = item.description
                item_ui['button'].on_click = Func(self.buy_item, item_index)
                item_ui['button'].disabled = item.purchased or self.player.gold < item.cost
                item_ui['button'].color = color.green if not item.purchased and self.player.gold >= item.cost else color.gray
            else:
                item_ui['background'].enabled = False
    
    def buy_item(self, item_index):
        if self.shop.buy_item(item_index):
            # Feedback visual
            self.shop_items_ui[item_index - self.shop_scroll_position]['button'].color = color.gray
            self.shop_items_ui[item_index - self.shop_scroll_position]['button'].disabled = True
            self.shop_items_ui[item_index - self.shop_scroll_position]['button'].blink(color.green)
            
            self.update_gold_text()
            self.update_visible_items()
    
    def set_shop_visibility(self, visible):
        self.shop_visible = visible
        self.shop_background.enabled = visible
        self.shop_title.enabled = visible
        self.close_btn.enabled = visible
        self.scroll_up_btn.enabled = visible
        self.scroll_down_btn.enabled = visible
        
        if visible:
            self.update_visible_items()
        else:
            for item_ui in self.shop_items_ui:
                item_ui['background'].enabled = False
    
    def toggle_shop(self):
        self.set_shop_visibility(not self.shop_visible)
        if self.shop_visible:
            self.shop_scroll_position = 0
            self.update_visible_items()
    
    def update_gold_text(self):
        self.gold_text.text = f'Gold: {self.player.gold}'
    
    def update(self):
        self.floor_text.text = f'Floor: {self.player.floor}'
        self.gold_text.text = f'Gold: {self.player.gold}'
        self.enemy_count_text.text = f'Enemies: {self.enemy_manager.enemies_defeated}/5'
        
        if self.shop_visible:
            self.update_visible_items()