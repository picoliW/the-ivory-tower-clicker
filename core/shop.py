from ursina import *
import json
import os
from core.shop_items import ShopItem, ArmorItem
from core.misc import MiscOptions

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
        self.dps_texts = []

        self.all_items = self.load_shop_items(shop_items_path)
        self.armor_list = self.load_armor_items(armor_items_path)
        self.available_items = [item for item in self.all_items if not item.purchased]

        self.background = Entity(
            parent=camera.ui, 
            model='quad', 
            color=color.black66, 
            position=(.5, 0),
            scale=(0.8, 1), 
            enabled=False,
            z=-0.3
        )
        self.misc_options = MiscOptions(player, self.background)

        self.title = Text(
            parent=self.background, 
            text='SHOP', 
            y=0.35, 
            scale=2, 
            origin=(0,0),
            z=-0.4
        )
        
        self.items_button = Button(
            parent=self.background, 
            position=(0.11, -0.45),
            scale=(0.15, 0.08), 
            color=color.clear
        )
        self.items_icon = Entity(
            parent=self.items_button,
            model='quad',
            texture='../assets/shop_items/open_items_shop.png',
            scale=(0.9, 1.3),
            z=-0.4
        )
        self.items_label = Text(
            parent=self.items_button,
            text='Items',
            y=-0.5,
            scale=1,
            color=color.white
        )
        
        self.armor_button = Button(
            parent=self.background, 
            position=(0.25, -0.45), 
            scale=(0.15, 0.08), 
            color=color.clear
        )
        self.armor_icon = Entity(
            parent=self.armor_button,
            model='quad',
            texture='../assets/shop_items/open_armor_shop.png', 
            scale=(0.9, 1.3),
            z=-0.4
        )
        self.armor_label = Text(
            parent=self.armor_button,
            text='Armor',
            y=-0.5,
            scale=1,
            color=color.white
        )
        
        self.close_button = Button(
            parent=self.background, 
            position=(0.45, 0.445), 
            scale=(0.08, 0.06), 
            color=color.clear
        )
        self.close_icon = Entity(
            parent=self.close_button,
            model='quad',
            texture='../assets/config_icons/x.png', 
            scale=(0.9, 0.9),
            z=-0.4
        )
        self.close_label = Text(
            parent=self.close_button,
            text='Close',
            y=-0.5,
            scale=1,
            color=color.white
        )

        self.options_button = Button(
            parent=self.background, 
            position=(0.39, -0.45), 
            scale=(0.15, 0.08), 
            color=color.clear
        )
        self.options_icon = Entity(
            parent=self.options_button,
            model='quad',
            texture='../assets/shop_items/misc.png', 
            scale=(0.9, 1.3),
            z=-0.4
        )
        self.options_label = Text(
            parent=self.options_button,
            text='Options',
            y=-0.5,
            scale=1,
            color=color.white
        )
        
        self.item_list = []

        self.items_button.on_click = self.show_items
        self.armor_button.on_click = self.show_armors
        self.close_button.on_click = self.hide
        self.options_button.on_click = self.show_misc_options

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
        self.open_shop_button.enabled = False        
        self.show_items()

    def hide(self):
        self.background.enabled = False
        self.open_shop_button.enabled = True
        self.clear_list()
        self.misc_options.hide_options() 

    def clear_list(self):
        for i in self.item_list:
            destroy(i)
        for s in self.item_sprites:
            destroy(s)
        for s in self.armor_sprites:
            destroy(s)
        for t in self.dps_texts:  
            destroy(t)
        self.item_list.clear()
        self.item_sprites.clear()
        self.armor_sprites.clear()
        self.dps_texts.clear() 
            
    def show_items(self):
        self.clear_list()
        self.misc_options.hide_options() 
        sorted_items = sorted(self.available_items, key=lambda item: item.cost)
        for i, item in enumerate(sorted_items[:4]):
            can_afford = self.player.gold >= item.cost
            b = Button(
                parent=self.background,
                text=f'{item.name}\n{item.description}\n{item.cost} gold',
                position=(0, 0.25 - i*0.15),
                scale=(0.6, 0.1),
                color=color.rgb(0, 224, 0) if can_afford else color.black66,
                z=-0.4
            )
            b.on_click = lambda i=i: self.buy_item(self.available_items.index(sorted_items[i]))
            self.item_list.append(b)
            
            sprite = Sprite(
                parent=self.background,
                texture=item.image_path,
                scale=(0.01, 0.01),
                position=(-0.22, 0.25 - i*0.15),
                z=-0.5
            )
            self.item_sprites.append(sprite)

        for sprite in self.armor_sprites:
            sprite.z = 10

    def show_armors(self):
        self.clear_list()
        self.misc_options.hide_options() 
        for i, armor in enumerate(self.armor_list[:4]):
            can_afford = self.player.gold >= armor.current_cost
            
            b = Button(
                parent=self.background,
                text=f'{armor.name}\nLevel {armor.level}\nCost {armor.current_cost}',
                position=(0, 0.25 - i*0.15),
                scale=(0.6, 0.1),
                color=color.rgb(0, 224, 0) if can_afford else color.black66,
                z=-0.4
            )
            b.on_click = lambda i=i: self.upgrade_armor(i)
            self.item_list.append(b)

            sprite = Sprite(
                parent=self.background,
                texture=armor.image_path,
                scale=(0.01, 0.01),
                position=(-0.22, 0.25 - i*0.15),
                z=-0.5
            )
            self.armor_sprites.append(sprite)

            dps_text = Text(
                parent=self.background,
                text=f'+{armor.base_dps} DPS\nPer\nLevel',
                position=(0.35, 0.25 - i*0.15),  
                origin=(0, 0),  
                scale=(0.7, 0.7), 
                color=color.green,
                z=-0.4
            )
            self.dps_texts.append(dps_text)

        for sprite in self.item_sprites:
            sprite.z = 10

    def show_misc_options(self):
        self.clear_list()
        self.misc_options.show_options()

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
