from ursina import *

class PauseMenu(Entity):
    def __init__(self):
        super().__init__()
        self.enabled = False
        
        # Fundo semi-transparente
        self.background = Entity(
            parent=self,
            model='quad',
            color=color.black66,
            scale=(999, 999),
            z=1
        )

                # Fundo arredondado cinza (apenas atrás dos botões)
        self.menu_background = Panel(
            parent=self,
            model=Quad(radius=0.05),  # Bordas arredondadas
            color=color.gray,
            scale=(2, 3),
            z=0.5
        )
        
        # Configurações de texto
        self.text_size = 0.4  # Tamanho da fonte aumentado
        
        # Botão Resume
        self.resume_button = Button(
            parent=self,
            text='Resume',
            color=color.azure,
            scale=(1.2, 0.6),
            y=0.7,
            text_size=self.text_size,  # Aplica o tamanho da fonte
            on_click=self.close
        )
        
        # Botão Quit
        self.quit_button = Button(
            parent=self,
            text='Quit',
            color=color.red,
            scale=(1.2, 0.6),
            y=-0.7,
            text_size=self.text_size,  # Aplica o mesmo tamanho de fonte
            on_click=application.quit
        )
    
    def open(self):
        self.enabled = True
        mouse.locked = False
    
    def close(self):
        self.enabled = False
        mouse.locked = True