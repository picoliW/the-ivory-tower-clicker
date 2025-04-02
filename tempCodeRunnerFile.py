from ursina import *
from player import Player
from enemy import EnemyManager
from shop import Shop
from ui import UI

app = Ursina()

# Configurações básicas
window.title = 'Tower Clicker'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False

def update():
    # Atualizações globais do jogo
    player.update()
    enemy_manager.update()
    ui.update()

def input(key):
    if key == 'left mouse down':
        # Verifica se clicou em um inimigo
        for enemy in enemy_manager.enemies:
            if enemy.hovered:
                player.attack(enemy)
                break

# Inicializa os sistemas
player = Player()
enemy_manager = EnemyManager(player)
shop = Shop(player)
ui = UI(player, enemy_manager, shop)

app.run()