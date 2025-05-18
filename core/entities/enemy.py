from random import randint
from ursina import *
from ursina.color import rgb
from core.abilities.dashability import DashAbility

class Enemy(Entity):
    def __init__(self, enemy_type, health, position=(2, -2)):
        super().__init__(
            model='quad',
            texture=f'../assets/enemies/enemy_{enemy_type}',
            scale=(1.5, 1.5),
            position=position,
            collider='box'
        )
        self.max_health = health
        self.health = health
        self.type = enemy_type
        self.speed = 1.0 
        self.moving = True
        self.is_colliding = False 

        self.health_bar = Entity(
            parent=self,
            model='quad',
            color=color.red,
            scale=(0.8, 0.1),
            position=(0, 0.7),
            origin=(0, 0))
            
        self.health_bar_bg = Entity(
            parent=self,
            model='quad',
            color=color.dark_gray,
            scale=(0.8, 0.1),
            position=(0, 0.7),
            origin=(0, 0),
            z=0.1)

        try:
            self.death_sound = Audio(f'../assets/sounds/enemySounds/enemy_{self.type}_die.wav', autoplay=False)
        except:
            print(f"Erro ao carregar som para inimigo tipo {self.type}")
            self.death_sound = None

        self.update_health_bar() 

    def update_health_bar(self):
        health_percent = self.health / self.max_health
        self.health_bar.scale_x = 0.8 * health_percent
        
        red_amount = int(255 * (1 - health_percent))
        green_amount = int(255 * health_percent)
        self.health_bar.color = rgb(red_amount, green_amount, 0)

    def take_damage(self, amount):
        self.health -= amount
        self.blink(color.black, duration=0.1)
        
        if self.health <= 0:
            self.health = 0
            self.update_health_bar()
            return True
            
        self.update_health_bar()
        return False

    def die(self):
        if self.death_sound:
            self.death_sound.play()
        destroy(self.health_bar)
        destroy(self.health_bar_bg)
        destroy(self)

    def update(self):
        if self.moving:
            self.x -= self.speed * time.dt


class EnemyManager:
    def __init__(self, player, background):
        self.player = player
        self.background = background
        self.enemies = []
        self.enemies_defeated = 0
        self.current_enemy = None
        self.dps_timer = 0
        self.dps_interval = 1.0
        self.spawn_enemy()

    def hide_enemies(self):
        for enemy in self.enemies:
            enemy.enabled = False

    def show_enemies(self):
        for enemy in self.enemies:
            enemy.enabled = True


    def spawn_enemy(self):
        for enemy in self.enemies:
            if enemy:
                enemy.die()
        self.enemies.clear()
        
        enemy_type = randint(1, 3)
        health = 10 + (self.player.floor * 5)
        
        enemy = Enemy(enemy_type, health, position=(10, -2.6)) 
        enemy.player_ref = self.player  
        self.enemies.append(enemy)
        self.current_enemy = enemy
        self.player.is_colliding_with_enemy = False 
        self.background.should_scroll = True

    def update(self):
        if not self.current_enemy:
            return
        
        self.dps_timer += time.dt
        if self.dps_timer >= self.dps_interval:
            if self.player.dps > 0:
                self.current_enemy.take_damage(self.player.dps)
            self.dps_timer = 0

        if self.current_enemy.moving:
            dash = DashAbility.instance
            speed_multiplier = (2 if dash and dash.active else 1) * self.player.movespeed
            self.current_enemy.x -= self.current_enemy.speed * time.dt * speed_multiplier
            
            self.current_enemy.is_colliding = (
                abs(self.current_enemy.x - self.player.sprite.x) < 1.5 and
                abs(self.current_enemy.y - self.player.sprite.y) < 1
            )
            
            if self.current_enemy.is_colliding:
                self.current_enemy.moving = False
                self.player.is_colliding_with_enemy = True
                self.background.should_scroll = False
            else:
                self.player.is_colliding_with_enemy = False
                self.background.should_scroll = True
                
        if self.current_enemy.health <= 0:
            self.current_enemy.die()  
            self.enemies_defeated += 1
            self.player.gold += 5 + (self.player.floor * 2)
            
            if self.enemies_defeated >= 5:
                self.player.floor += 1
                self.enemies_defeated = 0
                
            self.spawn_enemy()