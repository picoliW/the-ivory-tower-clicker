from ursina import *
import random
import math

class BossFight(Entity):
    def __init__(self, player, ui, on_win, on_fail): 
        super().__init__()

        self.player = player
        self.ui = ui 
        self.on_win = on_win
        self.on_fail = on_fail

        self.dash_speed = 15
        self.dash_duration = 0.2
        self.dash_cooldown = 1.5
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        self.dashing = False
        self.has_dash_powerup = True  
        self.dash_direction = Vec2(0, 0)
        self.active = True
        self.timer = 999999
        self.speed = 5
        
        self.player_max_health = 3
        self.player_health = self.player_max_health
        self.player_invincible = False
        self.player_invincible_time = 1.0
        self.player_invincible_timer = 0
        
        self.projectiles = []
        self.player_projectiles = []
        
        self.boss_max_health = 15
        self.boss_health = self.boss_max_health
        self.boss_speed = 1.5
        self.boss_direction = 1
        self.boss_move_timer = 0
        self.boss_move_duration = 2
        
        self.attack_pattern = 0
        self.attack_timer = 0
        self.attack_cooldown = 5
        self.is_attacking = False  
        self.attack_duration = 0
        self.current_attack_time = 0

        self.initialize_arena()
        self.setup_animations()
        self.setup_colliders()
        self.setup_health_bar()

    def setup_animations(self):
        self.walk_frames_right = [f'../assets/Player/PlayerMovement/Walk/Right/move_right_{i}' for i in range(8)]
        self.walk_frames_left = [f'../assets/Player/PlayerMovement/Walk/Left/move_left_{i}' for i in range(8)]
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_speed = 0.1
        self.facing = 'right'

    def setup_colliders(self):
        self.player.sprite.collider = BoxCollider(
            self.player.sprite,
            center=Vec3(0, -0.2, 0),  
            size=Vec3(0.8, 0.8, 1)  
        )

    def setup_health_bar(self):
        if hasattr(self, 'health_bar') and self.health_bar:
            destroy(self.health_bar)
        if hasattr(self, 'health_bar_bg') and self.health_bar_bg:
            destroy(self.health_bar_bg)
            
        self.health_bar_bg = Entity(
            parent=camera.ui,
            model='quad',
            color=color.dark_gray,
            scale=(0.4, 0.03),
            position=(0, 0.4),
            z=-10
        )
        
        self.health_bar = Entity(
            parent=camera.ui,
            model='quad',
            color=color.red,
            scale=(0.4, 0.03),
            position=(0, 0.4),
            z=-10
        )
        
        self.update_health_bar()

    def update_health_bar(self):
        if not hasattr(self, 'health_bar') or not self.health_bar:
            return
            
        health_percentage = self.boss_health / self.boss_max_health
        self.health_bar.scale_x = 0.4 * health_percentage
        
        self.health_bar.x = -0.2 * (1 - health_percentage)

    def player_take_damage(self):
        if self.player_invincible:
            return
            
        self.player_health = 0
        self.player_invincible = True
        self.player_invincible_timer = self.player_invincible_time
        
        self.end_bossfight(success=False)

    def initialize_arena(self):
        self.background = Entity(
            model='quad', 
            color=color.black, 
            scale=(camera.aspect_ratio * 20, 20),
            z=10  
        )

        offset_y = -1 
        w, h = 10, 5
        thickness = 0.05

        self.arena_fill = Entity(
            model='quad', 
            color=color.black33,  
            scale=(w, h), 
            y=offset_y, 
            z=1
        )

        self.boss_entity = Entity(
            model='quad',
            texture='../assets/bosses/boss1', 
            scale=(3.5, 3), 
            position=(0, offset_y + h/2 + 1.5),
            z=0.8,
            collider='box'
        )
        
        self.border_top = Entity(model='quad', color=color.white, scale=(w, thickness), y=h/2 + offset_y, z=0.5)
        self.border_bottom = Entity(model='quad', color=color.white, scale=(w, thickness), y=-h/2 + offset_y, z=0.5)
        self.border_left = Entity(model='quad', color=color.white, scale=(thickness, h), x=-w/2, y=offset_y, z=0.5)
        self.border_right = Entity(model='quad', color=color.white, scale=(thickness, h), x=w/2, y=offset_y, z=0.5)

        #self.player.sprite.position = (0, offset_y - h/2 + 1.5)
        self.player.sprite.position = (0, offset_y - h/2 + 0.45)
        self.player.sprite.z = 0.6

    def update(self):
        if not self.active:
            return

        if not hasattr(self, 'arena_fill') or not self.arena_fill or not self.arena_fill.enabled:
            return

        if self.player_invincible:
            self.player_invincible_timer -= time.dt
            if self.player_invincible_timer <= 0:
                self.player_invincible = False

        self.timer -= time.dt
        if self.timer <= 0:
            self.end_bossfight(success=True)

        if hasattr(self, 'boss_entity') and self.boss_entity and self.boss_entity.enabled:
            self.update_boss_movement()
            self.update_attack_system() 
        
        self.update_boss_projectiles()
        self.update_player_projectiles()
        self.update_player_movement()

    def update_boss_movement(self):
        if not hasattr(self, 'boss_entity') or not self.boss_entity:
            return

        self.boss_move_timer += time.dt
        if self.boss_move_timer >= self.boss_move_duration:
            self.boss_move_timer = 0
            self.boss_direction *= -1
            self.boss_move_duration = random.uniform(1.5, 3)
        
        arena_half_width = self.arena_fill.scale_x / 2
        boss_half_width = self.boss_entity.scale_x / 2
        arena_x_min = self.arena_fill.x - arena_half_width + boss_half_width
        arena_x_max = self.arena_fill.x + arena_half_width - boss_half_width
        
        new_x = self.boss_entity.x + self.boss_speed * self.boss_direction * time.dt
        self.boss_entity.x = clamp(new_x, arena_x_min, arena_x_max)

    def update_attack_system(self):
        if self.is_attacking:
            self.current_attack_time += time.dt
            if self.current_attack_time >= self.attack_duration:
                self.is_attacking = False
                self.current_attack_time = 0
                self.attack_timer = 0 
        else:
            self.attack_timer += time.dt
            if self.attack_timer >= self.attack_cooldown:
                self.start_new_attack_pattern()
    
    def start_new_attack_pattern(self):
        self.is_attacking = True
        self.attack_pattern = random.randint(0, 2)
        
        if self.attack_pattern == 0: 
            self.attack_duration = 2.5
            self.pattern_spiral()
        elif self.attack_pattern == 1: 
            self.attack_duration = 3.0
            self.pattern_rain()
        else:  
            self.attack_duration = 3.5
            self.pattern_wave()
        
        self.attack_cooldown = self.attack_duration + random.uniform(3, 5) 

    def pattern_spiral(self):
        for i in range(8): 
            angle = i * math.pi / 4
            delay = i * 0.15  
            invoke(self.create_spiral_projectile, angle, delay=delay)

    def create_spiral_projectile(self, angle):
        if not hasattr(self, 'boss_entity') or not self.boss_entity or not self.active:
            return

        proj = Entity(
            model='circle', 
            color=color.red, 
            scale=0.3, 
            position=self.boss_entity.position,
            z=self.player.sprite.z,
            collider='box'
        )
        
        direction = Vec2(math.cos(angle), math.sin(angle)).normalized()
        proj.direction = direction
        proj.speed = 2.5  
        self.projectiles.append(proj)

    def pattern_rain(self):
        for i in range(8): 
            x = random.uniform(
                self.arena_fill.x - self.arena_fill.scale_x/2,
                self.arena_fill.x + self.arena_fill.scale_x/2
            )
            delay = i * 0.2 
            invoke(self.create_rain_projectile, x, delay=delay)

    def create_rain_projectile(self, x):
        if not hasattr(self, 'arena_fill') or not self.arena_fill or not hasattr(self, 'boss_entity') or not self.boss_entity or not self.active:
            return

        proj = Entity(
            model='circle', 
            color=color.yellow, 
            scale=0.4, 
            position=(x, self.boss_entity.y),
            z=self.player.sprite.z,
            collider='box'
        )
        proj.speed = 5
        self.projectiles.append(proj)

    def pattern_wave(self):
        for i in range(5):  
            delay = i * 0.7  
            invoke(self.create_wave_projectiles, i, delay=delay)

    def create_wave_projectiles(self, wave_num):
        if not hasattr(self, 'arena_fill') or not self.arena_fill or not hasattr(self, 'boss_entity') or not self.boss_entity:
            return
            
        for i in range(5):
            x = lerp(
                self.arena_fill.x - self.arena_fill.scale_x/2,
                self.arena_fill.x + self.arena_fill.scale_x/2,
                i/4
            )
            proj = Entity(
                model='circle', 
                color=color.blue, 
                scale=0.3, 
                position=(x, self.boss_entity.y),
                z=self.player.sprite.z,
                collider='box'
            )
            proj.speed = 4
            proj.wave_offset = wave_num * 0.8  
        
            self.projectiles.append(proj)

    def update_boss_projectiles(self):
        for proj in self.projectiles[:]:
            if not proj or not proj.enabled:
                continue

            if hasattr(proj, 'direction'):  
                proj.x += proj.direction.x * proj.speed * time.dt
                proj.y += proj.direction.y * proj.speed * time.dt
            elif hasattr(proj, 'wave_offset'): 
                proj.y -= proj.speed * time.dt
                proj.x += math.sin((proj.y + proj.wave_offset) * 3) * 0.5 * time.dt
            else: 
                proj.y -= proj.speed * time.dt
            
            if (proj.y < -5 or proj.x < -10 or proj.x > 10):
                destroy(proj)
                if proj in self.projectiles:
                    self.projectiles.remove(proj)
                continue

            if hasattr(self, 'player') and hasattr(self.player, 'sprite') and self.player.sprite:
                if not hasattr(proj, 'collider'):
                    proj.collider = 'box'  
                
                if hasattr(self.player.sprite, 'collider') and self.player.sprite.collider:
                    if proj.intersects(self.player.sprite):
                        destroy(proj)
                        if proj in self.projectiles:
                            self.projectiles.remove(proj)
                        
                        self.player_take_damage()
                        return

    def update_player_projectiles(self):
        if mouse.left and len(self.player_projectiles) == 0: 
            self.create_player_projectile()
        
        for proj in self.player_projectiles[:]:
            if not proj or not proj.enabled:
                continue

            proj.y += 10 * time.dt 
            
            if hasattr(self, 'boss_entity') and self.boss_entity:
                result = proj.intersects(self.boss_entity)
                if result.hit:
                    destroy(proj)
                    if proj in self.player_projectiles:
                        self.player_projectiles.remove(proj)
                    
                    self.boss_health -= 1
                    self.update_health_bar()
                    
                    self.boss_entity.color = color.red
                    invoke(setattr, self.boss_entity, 'color', color.white, delay=0.2)
                    
                    if self.boss_health <= 0:
                        self.end_bossfight(success=True)
                    return  
            
            if proj.y > 5:
                destroy(proj)
                if proj in self.player_projectiles:
                    self.player_projectiles.remove(proj)

    def create_player_projectile(self):
        if not hasattr(self, 'player') or not hasattr(self.player, 'sprite'):
            return

        proj = Entity(
            model='quad',
            texture='white_cube',
            color=color.green,
            scale=(0.3, 0.6),
            position=self.player.sprite.position,
            rotation_z=-90,
            z=0.8,
            collider='box'
        )
        self.player_projectiles.append(proj)
        proj.collider.visible = True

    def update_player_movement(self):
        if not hasattr(self, 'player') or not hasattr(self.player, 'sprite'):
            return

        move = Vec2(
            held_keys['d'] - held_keys['a'],
            0 
        )
        new_x = self.player.sprite.x + move.x * time.dt * self.speed
        new_y = self.player.sprite.y 

        if not hasattr(self, 'arena_fill') or not self.arena_fill:
            return

        half_width = self.arena_fill.scale_x / 2
        player_half_width = self.player.sprite.scale_x / 2

        min_x = self.arena_fill.x - half_width + player_half_width
        max_x = self.arena_fill.x + half_width - player_half_width

        self.player.sprite.x = clamp(new_x, min_x, max_x)

        if self.player.dash_unlocked and not self.dashing and self.dash_cooldown_timer <= 0:
            if held_keys['e'] and move != Vec2(0, 0):
                self.dashing = True
                self.dash_timer = self.dash_duration
                self.dash_cooldown_timer = self.dash_cooldown
                self.dash_direction = move.normalized()

        if self.dashing:
            dash_move = self.dash_direction * self.dash_speed * time.dt
            dash_x = self.player.sprite.x + dash_move.x
            self.player.sprite.x = clamp(dash_x, min_x, max_x)

            self.dash_timer -= time.dt
            if self.dash_timer <= 0:
                self.dashing = False

        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= time.dt

        moving = move.x != 0
        if move.x < 0:
            self.facing = 'left'
        elif move.x > 0:
            self.facing = 'right'

        if moving:
            self.frame_timer += time.dt
            if self.frame_timer >= self.frame_speed:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_right)
                self.frame_timer = 0

                if self.facing == 'right':
                    self.player.sprite.texture = self.walk_frames_right[self.current_frame]
                else:
                    self.player.sprite.texture = self.walk_frames_left[self.current_frame]
        else:
            self.current_frame = 0
            if self.facing == 'right':
                self.player.sprite.texture = self.walk_frames_right[0]
            else:
                self.player.sprite.texture = self.walk_frames_left[0]

    def end_bossfight(self, success):
        self.active = False
        self.player.sprite.position = Vec3(-5, -2.5, 0)
        
        for proj in self.projectiles[:]:
            if proj:
                destroy(proj)
        self.projectiles.clear()
        
        for proj in self.player_projectiles[:]:
            if proj:
                destroy(proj)
        self.player_projectiles.clear()
        
        entities_to_destroy = [
            'arena_fill', 'boss_entity', 'border_top', 
            'border_bottom', 'border_left', 'border_right', 'background',
            'health_bar', 'health_bar_bg'
        ]
        
        for attr in entities_to_destroy:
            if hasattr(self, attr) and getattr(self, attr):
                destroy(getattr(self, attr))
                setattr(self, attr, None)



        if success:
            self.on_win()
        else:
            self.on_fail()