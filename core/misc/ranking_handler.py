from ursina import *
from core.api.api_requests import APIClient
import threading

class RankingHandler:
    def __init__(self, parent, player, shop_background, api_client):
        self.parent = parent
        self.player = player
        self.shop_background = shop_background
        self.api_client = api_client
        self.ranking_entities = []
        
    def show_ranking(self):
        self.parent.hide_options()
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
        self.parent.return_to_options()
    
    def clear_ranking(self):
        for entity in self.ranking_entities:
            destroy(entity)
        self.ranking_entities.clear()