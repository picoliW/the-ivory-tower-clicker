from ursina import *
from player import Player
from enemy import EnemyManager
from shop import Shop
from ui import UI
from background import Background
from screeninfo import get_monitors
from bossfight import BossFight
from ursina import Audio
from pause_menu import PauseMenu

app = Ursina()

monitor = get_monitors()[0]
monitor_width = monitor.width
monitor_height = monitor.height

window.title = 'The Ivory Tower'
window.borderless = True
window.fullscreen = True
window.size = (monitor_width, monitor_height)

boss_fight = None
bossfight_win_sound = Audio('../assets/sounds/bossfightSounds/bossfightWin.wav', autoplay=False)

def update():
    global boss_fight

    if boss_fight and boss_fight.active:
        boss_fight.update()
        return

    player.update()
    enemy_manager.update()
    ui.update()

    if player.floor == 2 and not boss_fight:
        def win():
            player.floor += 1
            player.sprite.position = (-5, 0.6)
            bossfight_win_sound.play()
            enemy_manager.show_enemies()
            global boss_fight
            boss_fight = None 

        def fail():
            player.floor -= 1
            player.sprite.position = (-5, 0.6)
            enemy_manager.show_enemies()
            global boss_fight
            boss_fight = None 
        enemy_manager.hide_enemies()
        boss_fight = BossFight(player, on_win=win, on_fail=fail)


def input(key):
    if key == 'left mouse down' and not pause_menu.enabled:
        for enemy in enemy_manager.enemies:
            if enemy.hovered:
                player.attack(enemy)
                break
    if key == 'escape':
        if pause_menu.enabled:
            pause_menu.close()
        else:
            pause_menu.open()


player = Player()
enemy_manager = EnemyManager(player)
shop = Shop(player)
ui = UI(player, enemy_manager)
background = Background()
pause_menu = PauseMenu()


app.run()