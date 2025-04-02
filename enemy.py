from random import randint
from ursina import *
from ursina.color import rgb

class Enemy(Entity):
    def __init__(self, enemy_type, health, position=(2, 0)):
        super().__init__(
            model='quad',
            texture=f'assets/enemy_{enemy_type}',
            scale=(1.5, 1.5),
            position=position,
            collider='box'
        )
        self.max_health = health
        self.health = health
        self.type = enemy_type
        
        self.health_bar = Entity(
            parent=self,
            model='quad',
            color=color.red,
            scale=(0.8, 0.1),
            position=(0, 0.7),
            origin=(0, 0)
        )
            
        # Fundo da barra de vida
        self.health_bar_bg = Entity(
            parent=self,
            model='quad',
            color=color.dark_gray,
            scale=(0.8, 0.1),
            position=(0, 0.7),
            origin=(0, 0),
            z=0.1
        )
            
        # Texto da vida
        self.health_text = Text(
            parent=self,
            text=f"{self.health}/{self.max_health}",
            position=(0, 0.7),
            origin=(0, 0),
            scale=1.5,
            background=True,
            background_color=color.black
        )
            
        self.update_health_bar()
        
    def update_health_bar(self):
        # Atualiza a largura da barra de vida
        health_percent = self.health / self.max_health
        self.health_bar.scale_x = 0.8 * health_percent
        
        # Atualiza a cor (verde para alta vida, vermelho para baixa)
        # Substitui color.lerp por uma função manual
        red_amount = int(255 * (1 - health_percent))
        green_amount = int(255 * health_percent)
        self.health_bar.color = rgb(red_amount, green_amount, 0)
        
        # Atualiza o texto
        self.health_text.text = f"{int(self.health)}/{int(self.max_health)}"
        
        # Centraliza o texto na barra
        self.health_text.position = (0.4 - (0.4 * health_percent), 0.7)
        
    def take_damage(self, amount):
        self.health -= amount
        self.blink(color.white, duration=0.1) 
        self.shake(duration=0.2, magnitude=0.1) 
        if self.health <= 0:
            self.health = 0
            self.update_health_bar()
            return True  # Inimigo derrotado
            
        self.update_health_bar()
        # Efeito visual ao levar dano
        self.blink(color.white, duration=0.1)
        return False  # Inimigo ainda vivo

    def die(self):
        """Lidar com a morte do inimigo"""
        destroy(self.health_bar)
        destroy(self.health_bar_bg)
        destroy(self.health_text)
        destroy(self)

class EnemyManager:
    def __init__(self, player):
        self.player = player
        self.enemies = []
        self.enemies_defeated = 0
        self.current_enemy = None
        self.spawn_enemy()
        
    def spawn_enemy(self):
        # Remove inimigos antigos
        for enemy in self.enemies:
            if enemy:
                enemy.die()
        self.enemies.clear()
        
        # Cria um novo inimigo
        enemy_type = randint(1, 3)
        health = 10 + (self.player.floor * 5)
        
        enemy = Enemy(enemy_type, health)
        self.enemies.append(enemy)
        self.current_enemy = enemy
        
    def update(self):
        if self.current_enemy and self.current_enemy.health <= 0:
            self.enemies_defeated += 1
            self.player.gold += 5 + (self.player.floor * 2)
            
            if self.enemies_defeated >= 5:
                self.player.floor += 1
                self.enemies_defeated = 0
                
            self.spawn_enemy()