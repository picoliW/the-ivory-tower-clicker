from bossfight import BossFight
from ursina import Audio

class Start_bossfight:
    def __init__(self, player, enemy_manager):
        self.player = player
        self.enemy_manager = enemy_manager
        self.boss_fight = None
        self.bossfight_win_sound = Audio('../assets/sounds/bossfightSounds/bossfightWin.wav', autoplay=False)

    def update(self):
        if self.boss_fight and self.boss_fight.active:
            self.boss_fight.update()
            return

        self.player.update()
        self.enemy_manager.update()

        if self.player.floor == 2 and not self.boss_fight:
            self.start_bossfight()

    def start_bossfight(self):
        def win():
            self.player.floor += 1
            self.player.sprite.position = (-5, -2.5)
            self.bossfight_win_sound.play()
            self.enemy_manager.show_enemies()
            self.boss_fight = None

        def fail():
            self.player.floor -= 1
            self.player.sprite.position = (-5, -2.5)
            self.enemy_manager.show_enemies()
            self.boss_fight = None

        self.enemy_manager.hide_enemies()
        self.boss_fight = BossFight(self.player, on_win=win, on_fail=fail)
