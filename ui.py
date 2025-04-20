from ursina import *

class UI:
    def __init__(self, player, enemy_manager, shop):
        self.player = player
        self.enemy_manager = enemy_manager
        self.shop = shop
        self.shop_visible = False
        self.shop_scroll_position = 0
        self.shop_tab = 'items'
        
        self.create_main_ui()
        self.create_hud_ui() 
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
            texture="assets/gold_coin.png",
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
        
    def create_shop_ui(self):
        self.shop_background = Panel(
            scale=(0.8, 0.95),
            position=(0, 0),
            texture='white_cube',
            texture_scale=(1, 1),
            color=color.dark_gray,
            z=-1
        )

        self.tab_items_btn = Button(
            parent=self.shop_background,
            text='Items',
            position=(-0.3, 0.42),
            scale=(0.2, 0.08),
            color=color.blue,
            on_click=Func(self.set_shop_tab, 'items')
        )

        self.tab_armor_btn = Button(
            parent=self.shop_background,
            text='Armor',
            position=(0.3, 0.42),
            scale=(0.2, 0.08),
            color=color.blue,
            on_click=Func(self.set_shop_tab, 'armor')
        )
        
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
            y_pos = 0.26 - (i * 0.18) 
            
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
                scale=(0.2, 0.9),
                position=(-0.35, 0),
                origin=(0, 0))
            
            # Nome e preço
            item_name = Text(
                parent=item_bg,
                position=(0, 0.20),
                scale=(1.5, 7),
                origin=(0, 0))
            
            # Descrição do efeito
            item_effect = Text(
                parent=item_bg,
                position=(0, 0),
                scale=(1.5, 7),
                origin=(0, 0),
                color=color.yellow)
            
            # Botão de compra
            buy_btn = Button(
                parent=item_bg,
                text='BUY',
                position=(0.35, 0),
                scale=(0.2, 0.35),
                color=color.green.tint(-0.2))
            
            self.shop_items_ui.append({
                'background': item_bg,
                'icon': item_icon,
                'name': item_name,
                'effect': item_effect,
                'button': buy_btn
            })
        self.armor_items_ui = []
        for i in range(4): 
            y_pos = 0.26 - (i * 0.18)
            
            armor_bg = Entity(
                parent=self.shop_background,
                model='quad',
                color=color.rgba(0, 0, 0, 255),
                scale=(0.7, 0.15),
                position=(0, y_pos),
                origin=(0, 0),
                enabled=False
            )
            
            armor_icon = Entity(
                parent=armor_bg,
                model='quad',
                scale=(0.2, 0.9),
                position=(-0.35, 0),
                origin=(0, 0)
            )
            
            armor_name = Text(
                parent=armor_bg,
                position=(0, 0.20),
                scale=(1.5, 7),
                origin=(0, 0)
            )
            
            armor_stats = Text(
                parent=armor_bg,
                position=(0, 0),
                scale=(1.5, 7),
                origin=(0, 0),
                color=color.yellow
            )
            
            upgrade_btn = Button(
                parent=armor_bg,
                text='UPGRADE',
                position=(0.35, 0),
                scale=(0.2, 0.35),
                color=color.green.tint(-0.2)
            )
            
            self.armor_items_ui.append({
                'background': armor_bg,
                'icon': armor_icon,
                'name': armor_name,
                'stats': armor_stats,
                'button': upgrade_btn
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

    def select_armor_type(self, index):
        if self.shop.armor.select_armor(index):
            for i, btn in enumerate(self.armor_select_buttons):
                btn.color = color.blue if i == index else color.gray
            self.update_armor_ui()

    def set_shop_tab(self, tab_name):
        self.shop_tab = tab_name
        self.update_shop_display()

    def update_shop_display(self):
        if self.shop_tab == 'items':
            for armor_ui in self.armor_items_ui:
                armor_ui['background'].enabled = False
            self.update_visible_items()
        else:
            for item_ui in self.shop_items_ui:
                item_ui['background'].enabled = False
            self.update_visible_armors()
    
    def update_armor_ui(self):
        armor = self.shop.armor
        self.armor_icon.texture = f"assets/shop_items/{armor.texture}"
        
        info = f"""
        {armor.name}
        Damage: +{armor.damage}
        Next Level Cost: {armor.cost}g
        """
        self.armor_info_text.text = info
        
        can_upgrade = armor.current_level < armor.max_level and self.player.gold >= armor.cost
        self.upgrade_btn.color = color.green if can_upgrade else color.gray
        self.upgrade_btn.disabled = not can_upgrade

    def upgrade_armor(self, armor_index):
        if armor_index < len(self.shop.armor_list):
            armor = self.shop.armor_list[armor_index]
            if armor.upgrade(self.player):  
                self.update_gold_text()
                self.update_visible_armors()
                self.armor_items_ui[armor_index]['button'].blink(color.green)
                print(f"Player damage increased to: {self.player.damage}") 
        
    def scroll_up(self):
        if self.shop_tab == 'items' and self.shop_scroll_position > 0:
            self.shop_scroll_position -= 1
            self.update_visible_items()
        elif self.shop_tab == 'armor' and self.shop_scroll_position > 0:
            self.shop_scroll_position -= 1
            self.update_visible_armors()

    def scroll_down(self):
        max_scroll = 0
        if self.shop_tab == 'items':
            max_scroll = max(0, len(self.shop.available_items) - 4)
        elif self.shop_tab == 'armor':
            max_scroll = max(0, len(self.shop.armor_list) - 4)  
        
        if self.shop_scroll_position < max_scroll:
            self.shop_scroll_position += 1
            if self.shop_tab == 'items':
                self.update_visible_items()
            else:
                self.update_visible_armors()

    def update_visible_items(self):
        self.scroll_up_btn.enabled = (self.shop_scroll_position > 0)
        max_scroll = max(0, len(self.shop.available_items) - 4)
        self.scroll_down_btn.enabled = (self.shop_scroll_position < max_scroll)
        
        for i in range(4):
            item_ui = self.shop_items_ui[i]
            item_index = self.shop_scroll_position + i
            
            if item_index < len(self.shop.available_items):
                item = self.shop.available_items[item_index]
                
                item_ui['background'].enabled = True
                item_ui['icon'].texture = f'assets/shop_items/{item.texture}'
                item_ui['name'].text = f"{item.name} ({item.cost}g)"
                item_ui['effect'].text = item.description
                item_ui['button'].on_click = Func(self.buy_item, item_index)
                item_ui['button'].disabled = self.player.gold < item.cost
                item_ui['button'].color = color.green if self.player.gold >= item.cost else color.gray
            else:
                item_ui['background'].enabled = False   

    def update_visible_armors(self):
        for i in range(4):
            armor_ui = self.armor_items_ui[i]
            if i < len(self.shop.armor_list):  
                armor = self.shop.armor_list[i]  
                
                armor_ui['background'].enabled = True
                armor_ui['icon'].texture = f'assets/shop_items/{armor.texture}'
                armor_ui['name'].text = f"{armor.name} (Lv. {armor.level})"
                armor_ui['stats'].text = f"+{armor.base_damage} Damage\nCost: {armor.current_cost}g"
                
                can_upgrade = armor.level < armor.max_level and self.player.gold >= armor.current_cost
                armor_ui['button'].on_click = Func(self.upgrade_armor, i)
                armor_ui['button'].disabled = not can_upgrade
                armor_ui['button'].color = color.green if can_upgrade else color.gray
            else:
                armor_ui['background'].enabled = False

    def buy_item(self, item_index):
        if self.shop.buy_item(item_index):
            self.update_gold_text()
            self.shop_scroll_position = max(0, min(self.shop_scroll_position, len(self.shop.available_items) - 4))
            self.update_visible_items()
            
            for i in range(4):
                current_index = self.shop_scroll_position + i
                if current_index < len(self.shop.available_items):
                    self.shop_items_ui[i]['button'].blink(color.green)
    
    def set_shop_visibility(self, visible):
        self.shop_visible = visible
        self.shop_background.enabled = visible
        self.close_btn.enabled = visible
        self.scroll_up_btn.enabled = visible
        self.scroll_down_btn.enabled = visible
        
        if visible:
            self.update_visible_items()
            self.update_shop_display()
        else:
            for item_ui in self.shop_items_ui:
                item_ui['background'].enabled = False
    
    def toggle_shop(self):
        self.set_shop_visibility(not self.shop_visible)
        if self.shop_visible:
            self.shop_scroll_position = 0
            self.update_visible_items()
    
    def update_gold_text(self):
        gold_str = str(self.player.gold)
        if len(gold_str) > 6:  
            gold_str = f"{self.player.gold/1000000:.1f}M" 
        self.gold_value_text.text = gold_str
        self.gold_value_text.scale *= 1.2
        invoke(setattr, self.gold_value_text, 'scale', (3, 15), delay=0.1)
    
    def update(self):
        self.floor_text.text = f'Floor: {self.player.floor}'
        self.gold_value_text.text = str(self.player.gold)
        self.enemy_count_text.text = f'Enemies: {self.enemy_manager.enemies_defeated}/5'
        
        if self.shop_visible:
            if self.shop_tab == 'items':
                self.update_visible_items()
            else:
                self.update_visible_armors()