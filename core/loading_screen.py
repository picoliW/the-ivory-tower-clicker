from ursina import *
import random
import json

class LoadingScreen(Entity):
    def __init__(self, on_complete):
        super().__init__()

        self.bg = Entity(model='quad', color=color.black, scale=(20, 20), z=1, parent=self)

        self.loading_text = Text(
            "Loading...", 
            origin=(-8, 20), 
            scale=7,
            y=0.2, 
            parent=self
        )

        self.spinner_frames = [f'../assets/loading_spinner/frame_{i}.png' for i in range(12)]
        self.current_frame = 0
        self.frame_time = 0
        self.frame_duration = 0.1 

        self.spinner = Entity(
            model='quad',
            texture=self.spinner_frames[self.current_frame],
            scale=.4,
            position=(6.4, -3.7),
            parent=self
        )

        self.gradient_line = Entity(
            model='quad',
            scale=(10, 0.01),  
            position=(-5, -2),
            parent=self
        )

        self.tips = self.load_tips()

        self.tips_text = Text(
            random.choice(self.tips), 
            origin=(1.4, 14), 
            scale=7,
            y=0.2, 
            parent=self
        )
        self.tips_text.color = color.white


        self.timer = 0
        self.duration = random.uniform(2, 4)
        self.on_complete = on_complete

    def load_tips(self):
        try:
            with open('data/tips.json', 'r') as file:
                data = json.load(file)
                return data['tips']
        except FileNotFoundError:
            print("Error: 'tips.json' not found.")
            return []

    def update(self):
        self.frame_time += time.dt
        if self.frame_time >= self.frame_duration:
            self.frame_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.spinner_frames)
            self.spinner.texture = self.spinner_frames[self.current_frame]

        self.timer += time.dt
        if self.timer >= self.duration:
            self.disable()
            if self.on_complete:
                self.on_complete()
