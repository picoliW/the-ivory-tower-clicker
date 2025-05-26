import requests
from ursina import *
import json
import os

class Achievement:
    def __init__(self, id, name, description, condition_text, icon_path, reward=0, unlocked=False, completed=False, player_id=None):
        self.id = id
        self.name = name
        self.description = description
        self.condition = condition_text
        self.icon_path = icon_path
        self.reward = reward
        self.unlocked = unlocked
        self.completed = completed
        self.player_id = player_id

    @property
    def claimed(self):
        return self.completed

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
            print(f"Error checking achievement {self.name}: {e}")
            self.unlocked = False
            return False

    def claim(self):
        if self.unlocked and not self.completed and self.player_id:
            try:
                response = requests.post(
                    "http://localhost:3000/auth/claim-achievement",
                    json={
                        "userId": self.player_id,
                        "achievementId": self.id
                    }
                )
                if response.json().get('success'):
                    self.completed = True
                    return True
            except Exception as e:
                print(f"Error claiming achievement: {e}")
        return False

class AchievementManager:
    def __init__(self, player_id=None):
        self.achievements = []
        self.player_id = player_id

    def load_from_server(self):
        if not self.player_id:
            return False
        try:
            response = requests.get(f"http://localhost:3000/auth/achievements/{self.player_id}")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.achievements.clear()
                    for item in data['achievements']:
                        achievement = Achievement(
                            id=item['id'],
                            name=item['name'],
                            description=item['description'],
                            condition_text=item['condition_text'],
                            icon_path=item['icon_path'],
                            reward=item.get('reward', 0),
                            unlocked=item.get('unlocked', False),
                            completed=item.get('completed', False),
                            player_id=self.player_id
                        )
                        self.achievements.append(achievement)
                    return True
        except Exception as e:
            print(f"Error loading achievements from server: {e}")
        return False

    def load_from_json(self):
        try:
            DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
            json_path = os.path.join(DATA_DIR, 'achievements.json')


            if not os.path.exists(json_path):
                return False

            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.achievements.clear()
                for item in data.get('achievements', []):
                    print(f"[DEBUG] Lendo conquista: {item['name']}")
                    achievement = Achievement(
                        id=item['id'],
                        name=item['name'],
                        description=item['description'],
                        condition_text=item['condition_text'],
                        icon_path=item['icon_path'],
                        reward=item.get('reward', 0),
                        unlocked=False,
                        completed=False,
                        player_id=None
                    )
                    self.achievements.append(achievement)

                return True

        except Exception as e:
            return False


    def check_all_conditions(self, player, enemy_manager=None):
        if not self.player_id:
            for achievement in self.achievements:
                achievement.check_condition(player, enemy_manager)
            return

        try:
            player_data = {
                'damage': player.damage,
                'gold': player.gold,
                'gold_per_second': player.gold_per_second,
                'floor': player.floor,
                'dash_unlocked': player.dash_unlocked,
                'movespeed': player.movespeed,
                'dps': player.dps
            }
            enemy_data = {
                'enemies_defeated': enemy_manager.enemies_defeated if enemy_manager else 0
            }
            response = requests.post(
                "http://localhost:3000/auth/check-achievements",
                json={
                    "userId": self.player_id,
                    "playerData": {
                        **player_data,
                        "enemyManager": enemy_data
                    }
                }
            )
            if response.status_code == 200:
                self.load_from_server()
        except Exception as e:
            print(f"Error checking achievements on server: {e}")
