from ursina import *
import random

class BossFight(Entity):
    def __init__(self, player, on_win, on_fail):
        super().__init__()
        self.player = player
        self.on_win = on_win
        self.on_fail = on_fail

        self.active = True
        self.timer = 10
        self.projectiles = []

        # Área da bossfight
        self.area = Entity(model='quad', color=color.black, scale=(16, 9), z=1)

        self.player.sprite.position = (0, -3)

        # Ativar movimentação manual
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

        self.walk_frames_right = [f'assets/Player/PlayerMovement/Right/move_right_{i}' for i in range(8)]
        self.walk_frames_left = [f'assets/Player/PlayerMovement/Left/move_left_{i}' for i in range(8)]
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_speed = 0.1
        self.facing = 'right'



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

        # Atualizar projéteis
        for proj in self.projectiles:
            proj.y -= 5 * time.dt
            if proj.y < -5:
                destroy(proj)
                self.projectiles.remove(proj)
            elif proj.intersects(self.player.sprite).hit:
                self.end_bossfight(success=False)

        move = Vec2(
            held_keys['d'] - held_keys['a'],
            held_keys['w'] - held_keys['s']
        )
        self.player.sprite.x += move.x * time.dt * self.speed
        self.player.sprite.y += move.y * time.dt * self.speed

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


    def spawn_projectile(self):
        x = random.uniform(-7, 7)
        proj = Entity(model='circle', color=color.white, scale=0.5, position=(x, 5), collider='box')
        self.projectiles.append(proj)

    def end_bossfight(self, success):
        self.active = False
        for proj in self.projectiles:
            destroy(proj)
        self.projectiles.clear()
        destroy(self.area)

        if success:
            self.on_win()
        else:
            self.on_fail()

        self.hitbox_debug.position = self.player.sprite.position

