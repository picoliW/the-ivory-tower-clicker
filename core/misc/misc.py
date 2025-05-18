from ursina import *
from core.api.api_requests import APIClient
import os
from core.misc.ranking_handler import RankingHandler
from core.misc.achievements_handler import AchievementsHandler

class MiscOptions(Entity):
    def __init__(self, player, shop_background):
        super().__init__()
        self.player = player
        self.shop_background = shop_background  
        self.option_buttons = []
        self.option_icons = []
        self.default_font = 'arial.ttf'
        self.api_client = APIClient()
        
        self.ranking_handler = RankingHandler(self, player, shop_background, self.api_client)
        self.achievements_handler = AchievementsHandler(self, player, shop_background)
        
    def show_options(self):
        if self.option_buttons:
            for btn in self.option_buttons:
                btn.enabled = True
            for icon in self.option_icons:
                icon.enabled = True
            return
            
        options = [
            [
                {"name": "", "icon": "ranking_icon.png", "action": self.ranking_handler.show_ranking},
                {"name": "", "icon": "config_icon.png", "action": self.show_config}
            ],
            [
                {"name": "", "icon": "stats_icon.png", "action": self.show_stats},
                {"name": "", "icon": "achievements_icon.png", "action": self.achievements_handler.show_achievements}
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
    
    def show_config(self):
        print("Mostrando configurações")
    
    def show_stats(self):
        print("Mostrando estatísticas")
    
    def return_to_options(self):
        self.show_options()