from ursina import *
from core.api.api_requests import APIClient
import threading

class StatsHandler:
    def __init__(self, parent, player, shop_background, api_client):
        self.parent = parent
        self.player = player
        self.shop_background = shop_background
        self.api = api_client
        self.stats_entities = []
        self.stats_data = None
        
    def show_stats(self):
        self.parent.hide_options()
        self.clear_stats()
        
        loading_text = Text(
            parent=self.shop_background,
            text="Carregando estatísticas...",
            position=(0, 0),
            scale=1,
            color=color.white,
            z=-0.5
        )
        self.stats_entities.append(loading_text)
        
        threading.Thread(target=self._fetch_and_display_stats, daemon=True).start()

    def _fetch_and_display_stats(self):
        success, response = self.api.get_player_stats(self.player.user_id)
        invoke(self._update_stats_display, success, response)
    
    def _update_stats_display(self, success, response):
        self.clear_stats()
        
        if not success:
            print(f"Erro ao carregar estatísticas: {response}")
            self.stats_data = {
                'enemies_defeated': getattr(self.player, 'enemies_defeated', 0),
                'items_purchased': getattr(self.player, 'items_purchased', 0),
                'armor_upgrades': getattr(self.player, 'armor_upgrades', 0),
                'floors_reached': getattr(self.player, 'floor', 1),
                'gold_earned': getattr(self.player, 'total_gold_earned', self.player.gold)
            }
        else:
            self.stats_data = response.get('stats', {})
        
        title = Text(
            parent=self.shop_background,
            text='Estatísticas do Jogador',
            y=0.3,
            scale=1.5,
            origin=(0, 0),
            color=color.orange,
            z=-0.5
        )
        self.stats_entities.append(title)
        
        stats_list = [
            f"Inimigos derrotados: {self.stats_data.get('enemies_defeated', 0)}",
            f"Itens comprados: {self.stats_data.get('items_purchased', 0)}",
            f"Melhorias de armadura: {self.stats_data.get('armor_upgrades', 0)}",
            f"Andares alcançados: {self.stats_data.get('floors_reached', 1)}",
            f"Ouro total ganho: {self.stats_data.get('gold_earned', 0)}",
            f"Dano: {self.player.damage}",
            f"Ouro por segundo: {self.player.gold_per_second}",
            f"DPS: {self.player.dps}"
        ]
        
        for i, stat_text in enumerate(stats_list):
            stat_entity = Text(
                parent=self.shop_background,
                text=stat_text,
                y=0.2 - i * 0.07,
                scale=1,
                origin=(0, 0),
                color=color.white,
                z=-0.5
            )
            self.stats_entities.append(stat_entity)
        
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
        
        self.stats_entities.extend([back_button, back_icon, back_label])
    
    def _return_to_options(self):
        self.clear_stats()
        self.parent.return_to_options()
    
    def clear_stats(self):
        for entity in self.stats_entities:
            destroy(entity)
        self.stats_entities.clear()