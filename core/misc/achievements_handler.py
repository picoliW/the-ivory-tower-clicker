from ursina import *
import os
from core.misc.achievements import AchievementManager

class AchievementsHandler:
    def __init__(self, parent, player, shop_background):
        self.parent = parent
        self.player = player
        self.shop_background = shop_background
        self.achievement_entities = []
        
    def show_achievements(self):
        self.parent.hide_options()
        self.clear_achievements()

        self.achievement_manager = AchievementManager(self.player.user_id)
        
        loading_text = Text(
            parent=self.shop_background,
            text="Loading achievements...",
            position=(0, 0),
            scale=1.5,
            color=color.white,
            z=-0.5
        )
        self.achievement_entities.append(loading_text)
        
        try:
            if not self.achievement_manager.load_from_server():
                raise Exception("Failed to load achievements from server")
            
            enemy_manager = getattr(self.player, 'enemy_manager', None)
            self.achievement_manager.check_all_conditions(
                self.player,
                enemy_manager
            )

            invoke(self._display_achievements, delay=0.1)
            
        except Exception as e:
            self._show_achievements_error(f"Error: {str(e)}")

    def _display_achievements(self):
        self.clear_achievements()
        
        title = Text(
            parent=self.shop_background,
            text="ACHIEVEMENTS",
            position=(0, 0.4),
            scale=2.0,
            origin=(0, 0),
            color=color.gold,
            z=-0.5
        )
        self.achievement_entities.append(title)

        back_button = Button(
            parent=self.shop_background,
            text='Back',
            position=(0.7, 0.4),
            scale=(0.15, 0.07),
            color=color.dark_gray,
            on_click=self._return_from_achievements,
            z=-0.5
        )
        self.achievement_entities.append(back_button)

        self._add_back_button()

        visible_achievements = [a for a in self.achievement_manager.achievements 
                          if not a.claimed or not a.unlocked]

        for i, achievement in enumerate(visible_achievements):
            self._create_achievement_card(achievement, 0.25 - i*0.15, achievement.unlocked)

    def _add_back_button(self):
        back_button = Button(
            parent=self.shop_background,
            position=(0.39, -0.45),  
            scale=(0.15, 0.08),   
            color=color.clear,
            on_click=self._return_from_achievements,
            z=-0.5
        )
        
        back_icon = Entity(
            parent=back_button,
            model='quad',
            texture='../assets/misc_icons/back_icon.png',
            scale=(0.9, 1.3),
            z=-0.6
        )
        
        self.achievement_entities.extend([back_button, back_icon, back_label])

    def _create_achievement_card(self, achievement, y_pos, unlocked):
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

        print(f"Tentando carregar ícone em: {achievement.icon_path}")
        print(f"Arquivo existe? {os.path.exists(achievement.icon_path)}")
        try:
            icon_texture = load_texture(achievement.icon_path)
            if icon_texture:
                icon = Entity(
                    parent=panel,
                    model='quad',
                    texture=icon_texture,
                    position=(-0.43, 0),
                    scale=(0.13, 0.6),
                    color=color.white if unlocked else color.gray,
                    z=-0.6
                )
            else:
                raise Exception("Texture não carregada")
        except:
            print(f"Falha ao carregar textura: {achievement.icon_path}")
            icon = Entity(
                parent=panel,
                model='quad',
                texture='white_cube',
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

        if unlocked and not achievement.claimed:
            claim_button = Button(
                parent=panel,
                text='Claim',
                position=(0.35, 0),
                scale=(0.15, 0.3),
                color=color.green,
                on_click=Func(self._claim_achievement, achievement, y_pos),
                z=-0.6,
                enabled=True
            )

            self.achievement_entities.append(claim_button)
        elif unlocked:
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

    def _claim_achievement(self, achievement, y_pos):
        if achievement.claim():  
            reward = achievement.reward  
            self.player.gold += reward
            
            reward_text = Text(
                parent=self.shop_background,
                text=f"+{reward} gold!",
                position=(0.35, y_pos),
                scale=1,
                color=color.gold,
                z=-0.4
            )
            self.achievement_entities.append(reward_text)
            destroy(reward_text, delay=1)
            
            invoke(self._display_achievements, delay=1.1)

    def _return_from_achievements(self):
        self.clear_achievements()
        self.parent.return_to_options()

    def _show_achievements_error(self, error_msg):
        self.clear_achievements()
        
        error_panel = Entity(
            parent=self.shop_background,
            model='quad',
            color=color.red,
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