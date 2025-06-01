from ursina import *
import random
from math import sin, cos, pi

class BossFight(Entity):
    def __init__(self, player, on_win, on_fail):
        super().__init__()
        self.player = player
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
        
        self.jump_height = 1.5
        self.jump_duration = 0.5
        self.jump_gravity = 9.8 * 2
        self.is_jumping = False
        self.jump_velocity = 0
        self.grounded = True
        
        self.active = True
        self.timer = 15 
        self.projectiles = []
        self.boss_health = 100
        self.attack_patterns = []
        self.current_pattern = 0
        self.pattern_timer = 0
        self.pattern_duration = 7  
        self.patterns_executed = 0  
        self.max_patterns = 2  
        self.attack_cooldown = 1.2  
        self.attack_timer = 0  

        self.setup_arena()
        self.setup_animations()
        self.setup_attack_patterns()

    def setup_arena(self):
        self.background = Entity(
            model='quad', 
            color=color.black, 
            scale=(camera.aspect_ratio * 20, 20),
            z=10  
        )

        offset_y = -1 

        self.arena_fill = Entity(
            model='quad', 
            color=color.black33,  
            scale=(10, 5), 
            y=offset_y, 
            z=1
        )

        thickness = 0.05
        w, h = 10, 5

        self.boss_entity = Entity(
            model='quad',
            texture='../assets/bosses/boss1', 
            scale=(3.5, 3), 
            position=(0, offset_y + h/2 + 1.5),
            z=0.8
        )
        
        self.border_top = Entity(model='quad', color=color.white, scale=(w, thickness), y=h/2 + offset_y, z=0.5)
        self.border_bottom = Entity(model='quad', color=color.white, scale=(w, thickness), y=-h/2 + offset_y, z=0.5)
        self.border_left = Entity(model='quad', color=color.white, scale=(thickness, h), x=-w/2, y=offset_y, z=0.5)
        self.border_right = Entity(model='quad', color=color.white, scale=(thickness, h), x=w/2, y=offset_y, z=0.5)

        self.player.sprite.position = (0, offset_y - h/2 + 1.5)
        self.player.sprite.z = 0.6

        self.speed = 5

        self.player.sprite.collider = BoxCollider(
            self.player.sprite,
            center=Vec3(0, -0.2, 0),  
            size=Vec3(0.8, 0.8, 1)  
        )

    def setup_animations(self):
        self.walk_frames_right = [f'../assets/Player/PlayerMovement/Walk/Right/move_right_{i}' for i in range(8)]
        self.walk_frames_left = [f'../assets/Player/PlayerMovement/Walk/Left/move_left_{i}' for i in range(8)]
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_speed = 0.1
        self.facing = 'right'
        self.moving = False

    def setup_attack_patterns(self):
        self.attack_patterns.append({
            'name': 'circle_wave',
            'cooldown': 0.5,  
            'timer': 0,
            'function': self.pattern_circle_wave,
            'executed': False
        })
        
        self.attack_patterns.append({
            'name': 'targeted',
            'cooldown': 0.5,  
            'timer': 0,
            'function': self.pattern_targeted,
            'executed': False
        })

    def update(self):
        if not self.active:
            return
        
        if not hasattr(self, 'arena_fill') or not self.arena_fill:
            return

        self.timer -= time.dt
        if self.timer <= 0:
            self.end_bossfight(success=True)

        self.handle_player_movement()
        self.handle_jumping()
        self.handle_attack_patterns()
        self.update_projectiles()
        self.update_animations()

    def handle_player_movement(self):
        if not hasattr(self, 'arena_fill') or not self.arena_fill:
            return
            
        move = Vec2(
            held_keys['d'] - held_keys['a'],
            0  
        )
        
        self.moving = move.x != 0
        
        if move.x < 0:
            self.facing = 'left'
        elif move.x > 0:
            self.facing = 'right'

        if not self.dashing:
            new_x = self.player.sprite.x + move.x * time.dt * self.speed
            
            half_width = self.arena_fill.scale_x / 2
            min_x = self.arena_fill.x - half_width + self.player.sprite.scale_x / 2
            max_x = self.arena_fill.x + half_width - self.player.sprite.scale_x / 2

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
            
            half_width = self.arena_fill.scale_x / 2
            min_x = self.arena_fill.x - half_width + self.player.sprite.scale_x / 2
            max_x = self.arena_fill.x + half_width - self.player.sprite.scale_x / 2
            
            self.player.sprite.x = clamp(dash_x, min_x, max_x)

            self.dash_timer -= time.dt
            if self.dash_timer <= 0:
                self.dashing = False

        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= time.dt

        if held_keys['space'] and self.grounded and not self.is_jumping:
            self.is_jumping = True
            self.grounded = False
            self.jump_velocity = (2 * self.jump_height * self.jump_gravity) ** 0.5

    def handle_jumping(self):
        if not hasattr(self, 'arena_fill') or not self.arena_fill:
            return

        ground_level = self.arena_fill.y - (self.arena_fill.scale_y/2) + (self.player.sprite.scale_y/2)
        
        if self.is_jumping or not self.grounded:
            self.jump_velocity -= self.jump_gravity * time.dt
            self.player.sprite.y += self.jump_velocity * time.dt
            
            if self.player.sprite.y <= ground_level:
                self.player.sprite.y = ground_level  
                self.is_jumping = False
                self.grounded = True
                self.jump_velocity = 0

    def update_animations(self):
        if self.moving:
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

    def handle_attack_patterns(self):
        if self.patterns_executed >= self.max_patterns:
            return
            
        self.pattern_timer += time.dt
        
        if self.pattern_timer >= self.pattern_duration:
            self.pattern_timer = 0
            self.current_pattern = (self.current_pattern + 1) % len(self.attack_patterns)
            self.clear_projectiles()
            self.patterns_executed += 1
            self.attack_timer = 0  
            
            if self.patterns_executed >= self.max_patterns:
                return
        
        self.attack_timer += time.dt
        if self.attack_timer >= self.attack_cooldown:
            self.attack_timer = 0
            pattern = self.attack_patterns[self.current_pattern]
            pattern['function']()  

    def update_projectiles(self):
        for proj in self.projectiles[:]:
            if hasattr(proj, 'velocity'):
                proj.x += proj.velocity.x * time.dt
                proj.y += proj.velocity.y * time.dt
            
            if hasattr(proj, 'lifetime'):
                proj.lifetime -= time.dt
                if proj.lifetime <= 0:
                    destroy(proj)
                    self.projectiles.remove(proj)
                    continue
            
            if (proj.y < -5 or proj.y > 5 or 
                proj.x < -5 or proj.x > 5):
                destroy(proj)
                self.projectiles.remove(proj)
            else:
                result = proj.intersects(self.player.sprite)
                if result.hit:
                    self.end_bossfight(success=False)
                    break

    def clear_projectiles(self):
        for proj in self.projectiles[:]:  
            if proj: 
                destroy(proj)
        self.projectiles = []  

    def pattern_circle_wave(self):
        num_projectiles = 12
        for i in range(num_projectiles):
            angle = (i / num_projectiles) * 2 * pi
            proj = Entity(
                model='circle', 
                color=color.yellow, 
                scale=0.4, 
                position=self.boss_entity.position, 
                collider='box'
            )
            proj.z = self.player.sprite.z
            
            speed = 2
            proj.velocity = Vec3(cos(angle) * speed, sin(angle) * speed, 0)
            proj.lifetime = 4.0
            
            self.projectiles.append(proj)

    def pattern_targeted(self):
        predicted_x = self.player.sprite.x
        predicted_y = self.player.sprite.y
        
        predicted_x += random.uniform(-1, 1)
        predicted_y += random.uniform(-0.5, 0.5)
        
        direction = Vec3(predicted_x - self.boss_entity.x, 
                         predicted_y - self.boss_entity.y, 
                         0).normalized()
        
        proj = Entity(
            model='sphere', 
            color=color.blue, 
            scale=0.35, 
            position=self.boss_entity.position, 
            collider='box'
        )
        proj.z = self.player.sprite.z
        proj.velocity = direction * 6  
        proj.lifetime = 2.5
        self.projectiles.append(proj)

    def end_bossfight(self, success):
        self.active = False  
        self.clear_projectiles()
        
        entities_to_destroy = [
            'arena_fill', 'boss_entity', 'border_top',
            'border_bottom', 'border_left', 'border_right', 'background'
        ]
        
        for attr in entities_to_destroy:
            if hasattr(self, attr) and getattr(self, attr):
                destroy(getattr(self, attr))
                setattr(self, attr, None)
        
        if success:
            self.on_win()
        else:
            self.on_fail()