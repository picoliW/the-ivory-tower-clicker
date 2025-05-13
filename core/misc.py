from ursina import *
from core.api.api_requests import APIClient

class MiscOptions(Entity):
    def __init__(self, player, shop_background):
        super().__init__()
        self.player = player
        self.shop_background = shop_background  
        self.option_buttons = []
        self.option_icons = []
        self.ranking_entities = []  
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
        print("Mostrando achievements")