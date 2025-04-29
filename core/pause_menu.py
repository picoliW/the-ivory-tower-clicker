from ursina import *

class PauseMenu(Entity):
    def __init__(self):
        super().__init__()
        self.enabled = False
        
        self.background = Entity(
            parent=self,
            model='quad',
            color=color.black66,
            scale=(999, 999),
            z=1
        )

        self.menu_background = Panel(
            parent=self,
            model=Quad(radius=0.05), 
            color=color.gray,
            scale=(2, 3),
            z=0.5
        )
        
        self.text_size = 0.4 

        self.resume_button = Button(
            parent=self,
            text='Resume',
            color=color.azure,
            scale=(1.2, 0.6),
            y=0.7,
            text_size=self.text_size,  
            on_click=self.close
        )
        
        self.quit_button = Button(
            parent=self,
            text='Quit',
            color=color.red,
            scale=(1.2, 0.6),
            y=-0.7,
            text_size=self.text_size, 
            on_click=application.quit
        )
    
    def open(self):
        self.enabled = True
        mouse.locked = False
    
    def close(self):
        self.enabled = False
        mouse.locked = False
        mouse.visible = True