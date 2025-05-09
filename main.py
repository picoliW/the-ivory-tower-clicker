from ursina import *
from core.player import Player
from core.enemy import EnemyManager
from core.shop import Shop
from core.ui import UI
from core.background import Background
from screeninfo import get_monitors
from core.pause_menu import PauseMenu
from core.start_bossfight import Start_bossfight
from core.main_menu import MainMenu
from core.splash_screen import SplashScreen
from core.loading_screen import LoadingScreen

app = Ursina()

monitor = get_monitors()[0]
window.title = 'The Ivory Tower'
window.borderless = False
window.fullscreen = True
window.size = (monitor.width, monitor.height)

game_started = False

def start_game():
    splash_screen.disable()
    main_menu.disable()

    def load_game():
        global game_started, player, shop, background, enemy_manager, ui, pause_menu, start_bossfight

        game_started = True
        player = Player()
        shop = Shop(player)
        background = Background()
        enemy_manager = EnemyManager(player, background)
        ui = UI(player, enemy_manager)
        pause_menu = PauseMenu()
        start_bossfight = Start_bossfight(player, enemy_manager)

    loading_screen = LoadingScreen(on_complete=load_game)

splash_screen = SplashScreen()

main_menu = MainMenu(start_game)
main_menu.disable()

def show_main_menu():
    splash_screen.fade_out(on_complete=main_menu.enable)
    
invoke(show_main_menu, delay=3)

def update():
    if not game_started:
        return

    background.update()
    start_bossfight.update()
    ui.update()
    enemy_manager.update()
    

def input(key):
    if not game_started:
        return

    if key == 'left mouse down' and not pause_menu.enabled:
        for enemy in enemy_manager.enemies:
            if enemy.hovered and enemy.is_colliding:
                player.attack(enemy)
                break
    if key == 'escape':
        if pause_menu.enabled:
            pause_menu.close()
        else:
            pause_menu.open()

app.run()
