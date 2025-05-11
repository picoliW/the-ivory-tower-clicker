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
    def __init__(self, name, texture, base_dps, base_cost, image_path):
        self.name = name
        self.texture = texture
        self.base_dps = base_dps  
        self.base_cost = base_cost
        self.image_path = image_path
        self.level = 1
        self.max_level = 100
        self.total_dps_added = 0

    @property
    def current_cost(self):
        return int(self.base_cost * (1.2 ** (self.level - 1)))

    @property
    def current_dps(self):
        return self.base_dps * self.level

    def upgrade(self, player):
        if self.level < self.max_level and player.gold >= self.current_cost:
            player.gold -= self.current_cost
            player.dps += self.base_dps  
            self.total_dps_added += self.base_dps
            self.level += 1
            return True
        return False
