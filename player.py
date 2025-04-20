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
            scale=(2.4, 2),
            position=(-5, 0.6),
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
        if hasattr(enemy, 'take_damage'):
            enemy.take_damage(self.damage)