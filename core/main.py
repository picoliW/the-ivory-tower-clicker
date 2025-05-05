from ursina import *
from player import Player
from enemy import EnemyManager
from shop import Shop
from ui import UI
from background import Background
from screeninfo import get_monitors
from pause_menu import PauseMenu
from start_bossfight import Start_bossfight

app = Ursina()

monitor = get_monitors()[0]
window.title = 'The Ivory Tower'
window.borderless = True
window.fullscreen = True
window.size = (monitor.width, monitor.height)

player = Player()
enemy_manager = EnemyManager(player)
shop = Shop(player)
ui = UI(player, enemy_manager)
background = Background()
pause_menu = PauseMenu()
start_bossfight = Start_bossfight(player, enemy_manager)

def update():
    background.update()
    start_bossfight.update()
    ui.update()
    enemy_manager.update()

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

app.run()
