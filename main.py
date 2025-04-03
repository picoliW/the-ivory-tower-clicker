from ursina import *
from player import Player
from enemy import EnemyManager
from shop import Shop
from ui import UI
from background import Background

app = Ursina()

window.title = 'The Ivory Tower'
window.borderless = False
window.fullscreen = True
window.exit_button.visible = True
window.size = (1920, 1080) 

def update():
    player.update()
    enemy_manager.update()
    ui.update()

def input(key):
    if key == 'left mouse down':
        for enemy in enemy_manager.enemies:
            if enemy.hovered:
                player.attack(enemy)
                break

player = Player()
enemy_manager = EnemyManager(player)
shop = Shop(player)
ui = UI(player, enemy_manager, shop)
background = Background()


app.run()