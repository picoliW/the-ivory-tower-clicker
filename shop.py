class Shop:
    def __init__(self, player):
        self.player = player
        self.damage_upgrade_cost = 10
        self.gold_upgrade_cost = 20
        self.dash_cost = 100
        self.gold_upgrade_multiplier = 1  # Novo atributo para controlar o multiplicador
        
    def buy_damage_upgrade(self):
        if self.player.upgrade_damage(1, self.damage_upgrade_cost):
            self.damage_upgrade_cost = int(self.damage_upgrade_cost * 1.5)
            return True
        return False
        
    def buy_gold_upgrade(self):
        # Calcula o novo valor multiplicando por 2
        new_gold_per_second = self.player.gold_per_second * 2 if self.player.gold_per_second > 0 else 2
        
        if self.player.upgrade_gold_per_second(new_gold_per_second - self.player.gold_per_second, self.gold_upgrade_cost):
            self.gold_upgrade_cost = int(self.gold_upgrade_cost * 2.6)  
            self.gold_upgrade_multiplier *= 2
            return True
        return False
        
    def buy_dash(self):
        return self.player.unlock_dash(self.dash_cost)