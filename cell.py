import assets
from tkinter import Button

colors = assets.colors

class Cell:
    def __init__(self, minefield, is_bomb):
        self.is_bomb = is_bomb
        self.is_swept = False
        self.is_flagged = False

        self.cell_btn = Button(
            minefield,
            background=colors['cell'],
            activebackground=colors['cell'].dark(),
            borderwidth=1,
            relief='ridge'
        )
