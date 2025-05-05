from ursina import *
import random

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
        self.active = True
        self.timer = 10
        self.projectiles = []

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

        self.spawn_timer = 0.5
        self.spawn_cooldown = 0

        # Hitbox de debug
        self.hitbox_debug = Entity(
            model='quad',
            color=color.azure,
            scale=self.player.sprite.scale,
            position=self.player.sprite.position,
            wireframe=True,
            z=-0.5  # Atrás do player
        )

        self.walk_frames_right = [f'../assets/Player/PlayerMovement/Walk/Right/move_right_{i}' for i in range(8)]
        self.walk_frames_left = [f'../assets/Player/PlayerMovement/Walk/Left/move_left_{i}' for i in range(8)]
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_speed = 0.1
        self.facing = 'right'

        self.player.sprite.collider = BoxCollider(
            self.player.sprite,
            center=Vec3(0, -0.2, 0),  
            size=Vec3(0.8, 0.8, 1)  
        )
        self.hitbox_debug.scale = (0.8, 0.8)
        self.hitbox_debug.position = self.player.sprite.position + Vec3(0, -0.2, 0)

    def update(self):
        if not self.active:
            return

        self.timer -= time.dt
        if self.timer <= 0:
            self.end_bossfight(success=True)

        # Spawning de projéteis
        self.spawn_cooldown -= time.dt
        if self.spawn_cooldown <= 0:
            self.spawn_projectile()
            self.spawn_cooldown = self.spawn_timer

        for proj in self.projectiles:
            proj.y -= 5 * time.dt
            if proj.y < -5:
                destroy(proj)
                self.projectiles.remove(proj)
            else:
                result = proj.intersects(self.player.sprite)
                if result.hit:
                    self.end_bossfight(success=False)

        move = Vec2(
            held_keys['d'] - held_keys['a'],
            held_keys['w'] - held_keys['s']
        )
        new_x = self.player.sprite.x + move.x * time.dt * self.speed
        new_y = self.player.sprite.y + move.y * time.dt * self.speed

        if not self.arena_fill or not self.arena_fill.enabled:
            return  

        half_width = self.arena_fill.scale_x / 2
        half_height = self.arena_fill.scale_y / 2

        min_x = self.arena_fill.x - half_width + self.player.sprite.scale_x / 2
        max_x = self.arena_fill.x + half_width - self.player.sprite.scale_x / 2
        min_y = self.arena_fill.y - half_height + self.player.sprite.scale_y / 2
        max_y = self.arena_fill.y + half_height - self.player.sprite.scale_y / 2


        self.player.sprite.x = clamp(new_x, min_x, max_x)
        self.player.sprite.y = clamp(new_y, min_y, max_y)

        if self.has_dash_powerup and not self.dashing and self.dash_cooldown_timer <= 0:
            if held_keys['e'] and move != Vec2(0, 0):
                self.dashing = True
                self.dash_timer = self.dash_duration
                self.dash_cooldown_timer = self.dash_cooldown
                self.dash_direction = move.normalized()

        if self.dashing:
            dash_move = self.dash_direction * self.dash_speed * time.dt
            dash_x = self.player.sprite.x + dash_move.x
            dash_y = self.player.sprite.y + dash_move.y
            self.player.sprite.x = clamp(dash_x, min_x, max_x)
            self.player.sprite.y = clamp(dash_y, min_y, max_y)

            self.dash_timer -= time.dt
            if self.dash_timer <= 0:
                self.dashing = False

        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= time.dt

        # Animação de andar
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

        self.hitbox_debug.position = self.player.sprite.position


    def spawn_projectile(self):
        arena_x_min = self.arena_fill.x - self.arena_fill.scale_x / 2
        arena_x_max = self.arena_fill.x + self.arena_fill.scale_x / 2
        x = random.uniform(arena_x_min, arena_x_max)
        proj = Entity(model='circle', color=color.white, scale=0.5, position=(x, 5), collider='box')
        proj.z = self.player.sprite.z
        self.projectiles.append(proj)

    def end_bossfight(self, success):
        self.active = False
        for proj in self.projectiles:
            destroy(proj)
        self.projectiles.clear()
        destroy(self.arena_fill)
        destroy(self.boss_entity)
        destroy(self.border_top)
        destroy(self.border_bottom)
        destroy(self.border_left)
        destroy(self.border_right)
        destroy(self.background)

        if success:
            self.on_win()
        else:
            self.on_fail()

        self.hitbox_debug.position = self.player.sprite.position