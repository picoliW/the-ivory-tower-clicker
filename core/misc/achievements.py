from ursina import *
import json

class Achievement:
    def __init__(self, name, description, condition, icon_path, reward=0, unlocked=False, claimed=False):
        self.name = name
        self.description = description
        self.condition = condition
        self.icon_path = icon_path
        self.reward = reward
        self.unlocked = unlocked
        self.claimed = claimed
    
    def check_condition(self, player, enemy_manager=None):
        try:
            eval_globals = {
                'player': player,
                'enemy_manager': enemy_manager
            }
            
            for key in list(eval_globals.keys()):
                if key.startswith('_'):
                    del eval_globals[key]
            
            if 'enemy_manager' in self.condition and enemy_manager is None:
                return False
                
            self.unlocked = eval(self.condition, {}, eval_globals)
            return self.unlocked
        except Exception as e:
            print(f"Erro ao verificar conquista {self.name}: {e}")
            self.unlocked = False
            return False
        
    def claim(self):
        if self.unlocked and not self.claimed:
            self.claimed = True
            return True
        return False

class AchievementManager:
    def __init__(self):
        self.achievements = []
    
    def load_from_json(self, json_path):
        try:
            json_dir = os.path.dirname(os.path.abspath(json_path))
            
            project_root = os.path.normpath(os.path.join(json_dir, '..'))
            
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for item in data:
                icon_path = item['icon_path']
                icon_path = os.path.normpath(icon_path).replace(os.sep, '/')
                print(f"Carregando ícone: {icon_path}") 
                
                self.achievements.append(
                    Achievement(
                        name=item['name'],
                        description=item['description'],
                        condition=item['condition'],
                        icon_path=icon_path,
                        reward=item.get('reward', 0)  
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