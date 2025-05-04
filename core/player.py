from ursina import *

class Player:
    def __init__(self):
        self.damage = 1
        self.gold = 0
        self.gold_per_second = 0
        self.floor = 1
        self.dash_unlocked = False

        self.run_textures = [
            load_texture(f'../assets/Player/PlayerMovement/Run/Right/run_right_{i}') for i in range(8)
        ]
        self.run_index = 0
        self.run_timer = 0
        self.run_frame_duration = 0.1  # ajuste a velocidade da animação

        self.sprite = Entity(
            model='quad',
            texture=self.run_textures[0],  
            scale=(2, 1.6),
            position=(-5, -2),
            collider='box'
        )

        # Temporizador para gold passivo
        self.gold_timer = 0

        self.attack_textures = [
            load_texture(f'../assets/Player/AttackAnimations/AttackRight/attack_right_{i}') for i in range(6)
        ]
        self.is_attacking = False

    def play_idle_animation(self):
        self.run_timer += time.dt
        if self.run_timer >= self.run_frame_duration:
            self.run_index = (self.run_index + 1) % len(self.run_textures)
            self.sprite.texture = self.run_textures[self.run_index]
            self.run_timer = 0

    def play_attack_animation(self):
        if self.is_attacking:
            return

        self.is_attacking = True

        all_frames = self.attack_textures + self.attack_textures[-2::-1]
        tempo_por_frame = 0.05

        for i, texture in enumerate(all_frames):
            invoke(setattr, self.sprite, 'texture', texture, delay=tempo_por_frame * i)

        duracao_total = tempo_por_frame * len(all_frames)

        def reset_texture():
            self.is_attacking = False
            self.run_index = 0
            self.sprite.texture = self.run_textures[self.run_index]

        invoke(reset_texture, delay=duracao_total)

    def update(self):
        self.gold_timer += time.dt
        if self.gold_timer >= 1:
            self.gold += self.gold_per_second
            self.gold_timer = 0

        if not self.is_attacking:
            self.play_idle_animation()

    def attack(self, enemy):
        if hasattr(enemy, 'take_damage'):
            enemy.take_damage(self.damage)
        self.play_attack_animation()


