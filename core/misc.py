from ursina import *
from core.api.api_requests import APIClient
import os
import json
from core.achievements import AchievementManager

class MiscOptions(Entity):
    def __init__(self, player, shop_background):
        super().__init__()
        self.player = player
        self.shop_background = shop_background  
        self.option_buttons = []
        self.option_icons = []
        self.ranking_entities = []  
        self.achievement_entities = []
        self.default_font = 'arial.ttf'
        self.api_client = APIClient()
        
    def show_options(self):
        if self.option_buttons:
            for btn in self.option_buttons:
                btn.enabled = True
            for icon in self.option_icons:
                icon.enabled = True
            return
            
        options = [
            [
                {"name": "", "icon": "ranking_icon.png", "action": self.show_ranking},
                {"name": "", "icon": "config_icon.png", "action": self.show_config}
            ],
            [
                {"name": "", "icon": "stats_icon.png", "action": self.show_stats},
                {"name": "", "icon": "achievements_icon.png", "action": self.show_achievements}
            ]
        ]
        
        positions = [
            [(-0.25, 0.1), (0.25, 0.1)],  
            [(-0.25, -0.1), (0.25, -0.1)]  
        ]
        
        for row in range(2):
            for col in range(2):
                option = options[row][col]
                pos = positions[row][col]
                
                btn = Button(
                    parent=self.shop_background,
                    text=option["name"],
                    position=pos,
                    scale=(0.25, 0.1),
                    color=color.orange,
                    origin=(0, 0),
                    z=-0.4,
                )
                btn.on_click = option["action"]
                self.option_buttons.append(btn)
                
                icon = Entity(
                    parent=btn,
                    model='quad',
                    texture=f'../assets/misc_icons/{option["icon"]}',
                    scale=(0.5, 1),
                    position=0,
                    z=-0.5,
                )
                self.option_icons.append(icon)
    
    def hide_options(self):
        for btn in self.option_buttons:
            btn.enabled = False
        for icon in self.option_icons:
            icon.enabled = False
    
    def show_ranking(self):
        self.hide_options()
        self.clear_ranking()
        
        loading_text = Text(
            parent=self.shop_background,
            text="Carregando ranking...",
            position=(0, 0),
            scale=1,
            color=color.white,
            z=-0.5
        )
        self.ranking_entities.append(loading_text)
        
        import threading
        threading.Thread(target=self._fetch_and_display_ranking, daemon=True).start()

    def _fetch_and_display_ranking(self):
        success, response = self.api_client.get_players_ranking()
        
        invoke(self._update_ranking_display, success, response)
    
    def _update_ranking_display(self, success, response):
        self.clear_ranking()
        
        if not success:
            error_msg = Text(
                parent=self.shop_background,
                text=f"Erro: {response}",
                position=(0, 0),
                scale=0.8,
                color=color.red,
                z=-0.5
            )
            self.ranking_entities.append(error_msg)
            self._add_back_button()
            return
            
        players = response.get('players', [])
        
        if not players:
            no_data_msg = Text(
                parent=self.shop_background,
                text="Nenhum dado de ranking disponível",
                position=(0, 0),
                scale=0.8,
                color=color.yellow,
                z=-0.5
            )
            self.ranking_entities.append(no_data_msg)
            self._add_back_button()
            return
        
        sorted_players = sorted(players, key=lambda x: x.get('gold', 0), reverse=True)
        
        title = Text(
            parent=self.shop_background,
            text="Ranking de Jogadores",
            position=(0, 0.3),
            scale=1.5,
            origin=(0, 0),
            color=color.gold,
            z=-0.5
        )
        self.ranking_entities.append(title)
        
        headers = Text(
            parent=self.shop_background,
            text="Pos.  Nickname          Gold",
            position=(0, 0.2),
            scale=1,
            origin=(0, 0),
            color=color.white,
            z=-0.5
        )
        self.ranking_entities.append(headers)
        
        for i, player in enumerate(sorted_players[:10]):
            pos = i + 1 
            nickname = player.get('nickname', 'Desconhecido')
            gold = player.get('gold', 0)
            
            player_text = Text(
                parent=self.shop_background,
                text=f"{pos:2d}. {nickname[:15]:15s} {gold:10,d}",
                position=(0, 0.1 - i*0.07),
                scale=0.8,
                origin=(0, 0),
                color=color.white if pos % 2 == 1 else color.light_gray,
                z=-0.5
            )
            self.ranking_entities.append(player_text)
            
            if player.get('id') == getattr(self.player, 'user_id', None):
                player_text.color = color.green
                player_text.scale *= 1.1
        
        self._add_back_button()
    
    def _add_back_button(self):
        back_button = Button(
            parent=self.shop_background,
            position=(0.39, -0.45),  
            scale=(0.15, 0.08),
            color=color.clear,
            on_click=self._return_to_options,
            z=-0.5
        )
        
        back_icon = Entity(
            parent=back_button,
            model='quad',
            texture='../assets/misc_icons/back_icon.png',  
            scale=(0.9, 1.3),
            z=-0.6
        )
        
        back_label = Text(
            parent=back_button,
            text="Voltar",
            y=-0.5,
            scale=1,
            color=color.white
        )
        
        self.ranking_entities.extend([back_button, back_icon, back_label])
    
    def _return_to_options(self):
        self.clear_ranking()
        self.show_options()
    
    def clear_ranking(self):
        for entity in self.ranking_entities:
            destroy(entity)
        self.ranking_entities.clear()
    
    def show_config(self):
        print("Mostrando configurações")
    
    def show_stats(self):
        print("Mostrando estatísticas")
    
    def show_achievements(self):
        self.hide_options()
        self.clear_achievements()

        self.achievement_manager = AchievementManager()
        DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
        achievement_path = os.path.join(DATA_DIR, 'achievements.json')
        
        try:
            if not self.achievement_manager.load_from_json(achievement_path):
                raise Exception("Falha ao carregar arquivo de achievements")
            
            self.achievement_manager.check_all_conditions(
                self.player,
                getattr(self.player, 'enemy_manager', None)
            )

            loading_text = Text(
                parent=self.shop_background,
                text="Carregando conquistas...",
                position=(0, 0),
                scale=1.5,
                color=color.white,
                z=-0.5
            )
            self.achievement_entities.append(loading_text)
            
            invoke(self._display_achievements, delay=0.1)
            
        except Exception as e:
            self._show_achievements_error(f"Erro: {str(e)}")

    def _display_achievements(self):
        self.clear_achievements()
        
        title = Text(
            parent=self.shop_background,
            text="CONQUISTAS",
            position=(0, 0.4),
            scale=2.0,
            origin=(0, 0),
            color=color.gold,
            z=-0.5
        )
        self.achievement_entities.append(title)

        # Botão de voltar
        back_button = Button(
            parent=self.shop_background,
            text='Voltar',
            position=(0.7, 0.4),
            scale=(0.15, 0.07),
            color=color.dark_gray,
            on_click=self._return_from_achievements,
            z=-0.5
        )
        self.achievement_entities.append(back_button)

        # Mostra todas as conquistas juntas, sem separação
        for i, achievement in enumerate(self.achievement_manager.achievements):
            self._create_achievement_card(achievement, 0.25 - i*0.15, achievement.unlocked)

    def _create_achievement_card(self, achievement, y_pos, unlocked):
        # Cor baseada no status de desbloqueio (mais sutil)
        bg_color = color.rgba(50, 205, 50, 150) if unlocked else color.rgba(169, 169, 169, 150)
        
        panel = Entity(
            parent=self.shop_background,
            model='quad',
            color=bg_color,
            position=(0, y_pos),
            scale=(0.8, 0.13),
            origin=(0, 0),
            z=-0.5
        )
        self.achievement_entities.append(panel)

        # Ícone
        icon_texture = achievement.icon_path if os.path.exists(achievement.icon_path) else 'white_cube'
        icon = Entity(
            parent=panel,
            model='quad',
            texture=icon_texture,
            position=(-0.4, 0),
            scale=(0.08, 0.08),
            color=color.white if unlocked else color.gray,
            z=-0.6
        )
        if not unlocked:
            icon.alpha = 0.6
        self.achievement_entities.append(icon)

        name_text = Text(
            parent=panel,
            text=achievement.name,
            position=(-0.35, 0.04),
            scale=(1.5, 4.3),
            color=color.white if unlocked else color.light_gray,
            origin=(-0.5, 0),
            z=-0.6
        )
        self.achievement_entities.append(name_text)

        desc_text = Text(
            parent=panel,
            text=achievement.description,
            position=(-0.35, -0.08),
            scale=(1.5, 4.3),
            color=color.white,
            origin=(-0.5, 0),
            z=-0.6
        )
        self.achievement_entities.append(desc_text)

        if unlocked:
            status_icon = Entity(
                parent=panel,
                model='quad',
                texture='checkmark',
                position=(0.35, 0),
                scale=(0.05, 0.05),
                color=color.gold,
                z=-0.6
            )
            self.achievement_entities.append(status_icon)

        border = Entity(
            parent=panel,
            model=Quad(radius=0.02),
            color=color.clear,
            scale=(1.02, 1.02),
            origin=(0, 0),
            z=-0.55
        )
        border.color = color.gold if unlocked else color.gray
        self.achievement_entities.append(border)

    def _return_from_achievements(self):
        self.clear_achievements()
        self.show_options()  

    def _show_achievements_error(self, error_msg):
        self.clear_achievements()
        
        error_panel = Entity(
            parent=self.shop_background,
            model='quad',
            color=color.dark_red,
            position=(0, 0),
            scale=(0.7, 0.3),
            z=-0.5
        )
        self.achievement_entities.append(error_panel)
        
        Text(
            parent=error_panel,
            text="Erro ao carregar conquistas",
            position=(0, 0.05),
            scale=1.2,
            color=color.white,
            z=-0.6
        )
        
        Text(
            parent=error_panel,
            text=error_msg,
            position=(0, -0.05),
            scale=0.8,
            color=color.white,
            z=-0.6
        )
        
        back_button = Button(
            parent=self.shop_background,
            text='Voltar',
            position=(0, -0.2),
            scale=(0.15, 0.07),
            color=color.dark_gray,
            on_click=self._return_from_achievements,
            z=-0.5
        )
        self.achievement_entities.append(back_button)

    def clear_achievements(self):
        for entity in self.achievement_entities:
            try:
                destroy(entity)
            except:
                continue
        self.achievement_entities.clear()