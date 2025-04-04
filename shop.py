class ShopItem:
    def __init__(self, name, texture, cost, stat_type, stat_value, description=""):
        self.name = name
        self.texture = texture
        self.cost = cost
        self.stat_type = stat_type 
        self.stat_value = stat_value
        self.description = description
        self.purchased = False

class ArmorItem:
    def __init__(self, name, texture, base_damage, base_cost):
        self.name = name
        self.texture = texture
        self.base_damage = base_damage 
        self.base_cost = base_cost
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
            damage_to_add = self.base_damage  
            player.damage += damage_to_add
            self.total_damage_added += damage_to_add
            self.level += 1
            return True
        return False

class Shop:
    def __init__(self, player):
        self.player = player
        self.available_items = [] 
        self.all_items = [  
            ShopItem("Wooden Sword", "sword_wood", 15, 'damage', 2, "+2 Damage"),
            ShopItem("Iron Sword", "sword_iron", 150, 'damage', 5, "+5 Damage"),
            ShopItem("Steel Sword", "sword_steel", 325, 'damage', 15, "+15 Damage"),
            ShopItem("Small Pouch", "pouch_small", 25, 'gold_per_second', 1, "+1 Gold/s"),
            ShopItem("Coin Purse", "purse_coin", 70, 'gold_per_second', 3, "+3 Gold/s"),
            ShopItem("Treasure Chest", "chest_treasure", 500, 'gold_per_second', 10, "+10 Gold/s"),
            ShopItem("Dash Boots", "boots_dash", 5000, 'dash', 0, "Unlock Dash Ability")
        ]
        self.armor_list = [
            ArmorItem("Wooden Chestplate", "wooden_chestplate", 2, 15),
            ArmorItem("Wooden Shield", "wooden_shield", 5, 300),
            ArmorItem("Wooden Ring", "wooden_ring", 10, 1000),
            ArmorItem("Wooden Boots", "wooden_boots", 20, 2000)
        ]
        self.reset_shop() 
        
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