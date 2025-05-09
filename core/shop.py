from ursina import *
import json
import os
from core.shop_items import ShopItem, ArmorItem

class Shop(Entity):
    DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
    shop_path = os.path.join(DATA_DIR, 'shop_items.json')
    armor_path = os.path.join(DATA_DIR, 'armor_items.json')

    def __init__(self, player, shop_items_path=shop_path, armor_items_path=armor_path):
        super().__init__()
        self.player = player
        self.background_enabled = False

        self.item_sprites = []
        self.armor_sprites = []

        self.all_items = self.load_shop_items(shop_items_path)
        self.armor_list = self.load_armor_items(armor_items_path)
        self.available_items = [item for item in self.all_items if not item.purchased]

        self.background = Entity(parent=camera.ui, model='quad', color=color.black66, scale=(0.8,0.8), enabled=False)
        self.title = Text(parent=self.background, text='SHOP', y=0.35, scale=2, origin=(0,0))
        
        self.items_button = Button(text='Items', parent=self.background, position=(-0.2, 0.25), scale=(0.3,0.1), color=color.azure)
        self.armor_button = Button(text='Armor', parent=self.background, position=(0.2, 0.25), scale=(0.3,0.1), color=color.orange)
        
        self.close_button = Button(text='Close', parent=self.background, position=(0, -0.35), scale=(0.3, 0.1), color=color.red)
        
        self.item_list = []

        self.items_button.on_click = self.show_items
        self.armor_button.on_click = self.show_armors
        self.close_button.on_click = self.hide

        self.open_shop_button = Button(
            parent=camera.ui,
            position=(0.63, -0.4),
            scale=(0.13, 0.09), 
            color=color.orange,  
            text='',
            highlight_color=color.orange.tint(-0.2),  
            pressed_color=color.orange.tint(-0.3), 
        )

        self.shop_icon = Entity(
            parent=self.open_shop_button,
            model='quad',
            texture='../assets/shop.png', 
            scale=(0.6, 0.9),  
            z=-0.1,  
        )
        self.open_shop_button.on_click = self.show

    def load_shop_items(self, filepath):
        with open(filepath, 'r') as f:
            items_data = json.load(f)
        return [ShopItem(**item) for item in items_data]

    def load_armor_items(self, filepath):
        with open(filepath, 'r') as f:
            armors_data = json.load(f)
        return [ArmorItem(**armor) for armor in armors_data]

    def show(self):
        self.background.enabled = True
        self.background.enabled = True
        self.show_items()

    def hide(self):
        self.background.enabled = False
        self.background_enabled = False
        self.clear_list()

    def clear_list(self):
        for i in self.item_list:
            destroy(i)
        for s in self.item_sprites:
            destroy(s)
        for s in self.armor_sprites:
            destroy(s)
        self.item_list.clear()
        self.item_sprites.clear()
        self.armor_sprites.clear()
            
    def show_items(self):
        self.clear_list()
        sorted_items = sorted(self.available_items, key=lambda item: item.cost)
        for i, item in enumerate(sorted_items[:3]):
            can_afford = self.player.gold >= item.cost
            b = Button(
                parent=self.background,
                text=f'{item.name}\n{item.description}\n{item.cost} gold',
                y=0.1 - i*0.15,
                scale=(0.6, 0.1),
                color=color.rgb(0, 224, 0) if can_afford else color.black66
            )
            b.on_click = lambda i=i: self.buy_item(self.available_items.index(sorted_items[i]))
            self.item_list.append(b)
            
            sprite = Sprite(
                parent=self.background,
                texture=item.image_path,
                scale=(0.01, 0.011),
                position=(-0.25, 0.1 - i*0.15, 0) 
            )
            self.item_sprites.append(sprite)

        for sprite in self.armor_sprites:
            sprite.z = 10

    def show_armors(self):
        self.clear_list()
        for i, armor in enumerate(self.armor_list[:3]):
            can_afford = self.player.gold >= armor.current_cost
            b = Button(
                parent=self.background,
                text=f'{armor.name}\nLevel {armor.level}\nCost {armor.current_cost}',
                y=0.1 - i*0.15,
                scale=(0.6, 0.1),
                color=color.rgb(0, 224, 0) if can_afford else color.black66
            )
            b.on_click = lambda i=i: self.upgrade_armor(i)
            self.item_list.append(b)

            sprite = Sprite(
                parent=self.background,
                texture=armor.image_path,
                scale=(0.01, 0.01),
                position=(-0.25, 0.1 - i*0.15, 0)  
            )
            self.armor_sprites.append(sprite)

        for sprite in self.item_sprites:
            sprite.z = 10



    def buy_item(self, index):
        if index >= len(self.available_items):
            return
        item = self.available_items[index]
        if self.player.gold >= item.cost:
            self.player.gold -= item.cost
            item.purchased = True
            if item.stat_type == 'damage':
                self.player.damage += item.stat_value
            elif item.stat_type == 'gold_per_second':
                self.player.gold_per_second += item.stat_value
            elif item.stat_type == 'dash':
                self.player.dash_unlocked = True
            self.available_items.pop(index)
            self.show_items()

    def upgrade_armor(self, index):
        armor = self.armor_list[index]
        if armor.upgrade(self.player):
            self.show_armors()
