from ursina import *

class Player:
    def __init__(self):
        self.damage = 1
        self.gold = 0
        self.gold_per_second = 0
        self.floor = 1
        self.dash_unlocked = False
        
        # Criação do sprite do jogador
        self.sprite = Entity(
            model='quad',
            texture='assets/player',
            scale=(1, 1.5),
            position=(-5, 0),
            collider='box'
        )
        
        # Temporizador para gold passivo
        self.gold_timer = 0
        
    def update(self):
        # Ganho passivo de gold
        self.gold_timer += time.dt
        if self.gold_timer >= 1:
            self.gold += self.gold_per_second
            self.gold_timer = 0
            
    def attack(self, enemy):
        if enemy.take_damage(self.damage):
            pass 
            
    def upgrade_damage(self, amount, cost):
        if self.gold >= cost:
            self.gold -= cost
            self.damage += amount
            return True
        return False
        
    def upgrade_gold_per_second(self, amount, cost):
        if self.gold >= cost:
            self.gold -= cost
            # Se gold_per_second for 0, define como 1 (primeira compra)
            if self.gold_per_second == 0:
                self.gold_per_second = 1
            self.gold_per_second += amount
            return True
        return False
        
    def unlock_dash(self, cost):
        if not self.dash_unlocked and self.gold >= cost:
            self.gold -= cost
            self.dash_unlocked = True
            return True
        return False