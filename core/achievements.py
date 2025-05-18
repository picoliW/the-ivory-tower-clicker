from ursina import *
import json


class Achievement:
    def __init__(self, name, description, condition, icon_path, unlocked=False):
        self.name = name
        self.description = description
        self.condition = condition
        self.icon_path = icon_path
        self.unlocked = unlocked
    
    def check_condition(self, player, enemy_manager=None):
        try:
            eval_globals = {
                'player': player,
                'enemy_manager': enemy_manager
            }
            
            for key in list(eval_globals.keys()):
                if key.startswith('_'):
                    del eval_globals[key]
            
            self.unlocked = eval(self.condition, {}, eval_globals)
            return self.unlocked
        except Exception as e:
            print(f"Erro ao verificar conquista {self.name}: {e}")
            self.unlocked = False
            return False


class AchievementManager:
    def __init__(self):
        self.achievements = []
    
    def load_from_json(self, json_path):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.normpath(os.path.join(current_dir, '..', json_path))
            
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for item in data:
                icon_path = os.path.normpath(os.path.join(current_dir, '..', item['icon']))
                self.achievements.append(
                    Achievement(
                        name=item['name'],
                        description=item['description'],
                        condition=item['condition'],
                        icon_path=icon_path
                    )
                )
            return True
        except Exception as e:
            print(f"Erro ao carregar achievements: {e}")
            return False
    
    def check_all_conditions(self, player, enemy_manager=None):
        for achievement in self.achievements:
            if not achievement.unlocked:
                achievement.check_condition(player, enemy_manager)