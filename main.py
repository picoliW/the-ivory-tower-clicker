from ursina import *
from core.entities.player import Player
from core.entities.enemy import EnemyManager
from core.shop.shop import Shop
from core.ui import UI
from core.background import Background
from screeninfo import get_monitors
from core.menus.pause_menu import PauseMenu
from core.bossfight.start_bossfight import Start_bossfight
from core.menus.main_menu import MainMenu
from core.scenes.splash_screen import SplashScreen
from core.scenes.loading_screen import LoadingScreen
from core.scenes.first_time_scene import FirstTimeScene
from ursina import Text
Text.default_font = 'assets/fonts/Roboto-Regular.ttf'
Text.default_resolution = 48

app = Ursina()

monitor = get_monitors()[0]
window.title = 'The Ivory Tower'
window.borderless = True
window.fullscreen = False
window.size = (monitor.width, monitor.height)

game_started = False
player = None
shop = None
background = None
enemy_manager = None
ui = None
pause_menu = None
start_bossfight = None

start_in_bossfight = False 

def start_game(user_id=None, player_data=None):
    splash_screen.disable()
    main_menu.disable()

    def load_game():
        global game_started, player, shop, background, enemy_manager, ui, pause_menu, start_bossfight

        game_started = True
        player = Player(user_id, player_data)

        if start_in_bossfight:
            setup_main_game()
            start_bossfight.start_bossfight()  
        elif player.gold == 0:
            first_time_scene = FirstTimeScene(on_complete=lambda: [
                setup_main_game(),
                first_time_scene.disable()
            ], player=player)
        else:
            setup_main_game()
    
    def setup_main_game():
        global shop, background, enemy_manager, ui, pause_menu, start_bossfight
        shop = Shop(player)
        background = Background()
        enemy_manager = EnemyManager(player, background)
        ui = UI(player, enemy_manager)
        pause_menu = PauseMenu()
        start_bossfight = Start_bossfight(player, enemy_manager, ui)

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

    if background:
        background.update()
    if start_bossfight:
        start_bossfight.update()
    if ui:
        ui.update()
    if enemy_manager:
        enemy_manager.update()
    if hasattr(player, 'achievement_manager'):
        player.achievement_manager.update(player, enemy_manager)

def input(key):
    if not game_started:
        return

    if key == 'left mouse down' and (not pause_menu or not pause_menu.enabled):
        if enemy_manager:
            for enemy in enemy_manager.enemies:
                if enemy.hovered and enemy.is_colliding:
                    player.attack(enemy)
                    
                    if player.golden_touch.add_gold_on_click():
                        ui.gold_value_text.text = str(player.gold)
                    break

    if key == 'escape':
        if pause_menu:  
            if pause_menu.enabled:
                pause_menu.close()
            else:
                pause_menu.open()

app.run()
