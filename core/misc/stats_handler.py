from ursina import *

class StatsHandler:
    def __init__(self, parent, player, background, api_client):
        self.parent = parent
        self.player = player
        self.background = background
        self.api = api_client
        self.stats_entities = []
        self.stats_data = None
        
    def show_stats(self):
        self.clear_stats()
        
        self.stats_panel = Entity(
            parent=self.background,
            model='quad',
            color=color.dark_gray,
            scale=(0.7, 0.8),
            position=(0, 0),
            z=-0.4
        )
        
        self.stats_title = Text(
            parent=self.stats_panel,
            text='Estatísticas do Jogador',
            y=0.4,
            scale=1.5,
            origin=(0, 0),
            color=color.orange,
            z=-0.5
        )
        
        self.back_button = Button(
            parent=self.stats_panel,
            text='Voltar',
            position=(0, -0.45),
            scale=(0.2, 0.08),
            color=color.gray,
            z=-0.5,
            on_click=self.clear_stats
        )
        
        self.load_stats()
        
    def load_stats(self):
        success, response = self.api.get_player_stats(self.player.user_id)
        
        if success:
            self.stats_data = response.get('stats', {})
            self.display_stats()
        else:
            print(f"Erro ao carregar estatísticas: {response}")
            self.stats_data = {
                'enemies_defeated': getattr(self.player, 'enemies_defeated', 0),
                'items_purchased': getattr(self.player, 'items_purchased', 0),
                'armor_upgrades': getattr(self.player, 'armor_upgrades', 0),
                'floors_reached': getattr(self.player, 'floor', 1),
                'gold_earned': getattr(self.player, 'total_gold_earned', self.player.gold)
            }
            self.display_stats()
    
    def display_stats(self):
        if not self.stats_data:
            return
            
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
                parent=self.stats_panel,
                text=stat_text,
                y=0.3 - i * 0.1,
                scale=1,
                origin=(-0.5, 0),
                color=color.white,
                z=-0.5
            )
            self.stats_entities.append(stat_entity)
    
    def clear_stats(self):
        if hasattr(self, 'stats_panel'):
            destroy(self.stats_panel)
        for entity in self.stats_entities:
            destroy(entity)
        self.stats_entities = []
        self.parent.return_to_options()