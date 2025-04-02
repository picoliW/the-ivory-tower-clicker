class ShopItem:
    def __init__(self, name, texture, cost, stat_type, stat_value, description=""):
        self.name = name
        self.texture = texture
        self.cost = cost
        self.stat_type = stat_type 
        self.stat_value = stat_value
        self.description = description
        self.purchased = False

class Shop:
    def __init__(self, player):
        self.player = player
        self.items = [
            ShopItem(
                "Wooden Sword", 
                "sword_wood", 
                15, 
                'damage', 
                2,
                "+2 Damage"
            ),
            ShopItem(
                "Iron Sword", 
                "sword_iron", 
                50, 
                'damage', 
                5,
                "+5 Damage"
            ),
            ShopItem(
                "Steel Sword", 
                "sword_steel", 
                150, 
                'damage', 
                15,
                "+15 Damage"
            ),
            ShopItem(
                "Small Pouch", 
                "pouch_small", 
                25, 
                'gold_per_second', 
                1,
                "+1 Gold/s"
            ),
            ShopItem(
                "Coin Purse", 
                "purse_coin", 
                75, 
                'gold_per_second', 
                3,
                "+3 Gold/s"
            ),
            ShopItem(
                "Treasure Chest", 
                "chest_treasure", 
                250, 
                'gold_per_second', 
                10,
                "+10 Gold/s"
            ),
            ShopItem(
                "Dash Boots", 
                "boots_dash", 
                120, 
                'dash', 
                0,
                "Unlock Dash Ability"
            )
        ]
        
    def buy_item(self, item_index):
        item = self.items[item_index]
        
        if item.purchased:
            return False
            
        if self.player.gold >= item.cost:
            self.player.gold -= item.cost
            item.purchased = True
            
            if item.stat_type == 'damage':
                self.player.damage += item.stat_value
            elif item.stat_type == 'gold_per_second':
                self.player.gold_per_second += item.stat_value
            elif item.stat_type == 'dash':
                self.player.dash_unlocked = True
                
            return True
        return False