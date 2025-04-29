import json
import os

class ShopItem:
    def __init__(self, name, texture, cost, stat_type, stat_value, image_path, description=""):
        self.name = name
        self.texture = texture
        self.cost = cost
        self.stat_type = stat_type
        self.stat_value = stat_value
        self.image_path = image_path
        self.description = description
        self.purchased = False

class ArmorItem:
    def __init__(self, name, texture, base_damage, base_cost, image_path):
        self.name = name
        self.texture = texture
        self.base_damage = base_damage
        self.base_cost = base_cost
        self.image_path = image_path
        self.level = 1
        self.max_level = 100
        self.total_damage_added = 0

    @property
    def current_cost(self):
        return int(self.base_cost * (1.6 ** (self.level - 1)))

    @property
    def current_damage(self):
        return self.base_damage * self.level

    def upgrade(self, player):
        if self.level < self.max_level and player.gold >= self.current_cost:
            player.gold -= self.current_cost
            player.damage += self.base_damage
            self.total_damage_added += self.base_damage
            self.level += 1
            return True
        return False

class Shop:
    DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
    shop_path = os.path.join(DATA_DIR, 'shop_items.json')
    armor_path = os.path.join(DATA_DIR, 'armor_items.json')

    def __init__(self, player, shop_items_path=shop_path, armor_items_path=armor_path):
        self.player = player
        self.available_items = []
        self.all_items = self.load_shop_items(shop_items_path)
        self.armor_list = self.load_armor_items(armor_items_path)
        self.reset_shop()

    def load_shop_items(self, filepath):
        with open(filepath, 'r') as f:
            items_data = json.load(f)
        return [ShopItem(**item) for item in items_data]

    def load_armor_items(self, filepath):
        with open(filepath, 'r') as f:
            armors_data = json.load(f)
        return [ArmorItem(**armor) for armor in armors_data]

    def reset_shop(self):
        self.available_items = [item for item in self.all_items if not item.purchased]

    def buy_item(self, item_index):
        if item_index >= len(self.available_items):
            return False

        item = self.available_items[item_index]

        if self.player.gold >= item.cost:
            self.player.gold -= item.cost
            item.purchased = True

            if item.stat_type == 'damage':
                self.player.damage += item.stat_value
            elif item.stat_type == 'gold_per_second':
                self.player.gold_per_second += item.stat_value
            elif item.stat_type == 'dash':
                self.player.dash_unlocked = True

            self.available_items.pop(item_index)
            return True

        return False
