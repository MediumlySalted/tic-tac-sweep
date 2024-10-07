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
        self.cell_btn.bind('<Button-1>', self.sweep)
        self.cell_btn.bind('<Button-3>', self.flag)

    def sweep(self, left_click):
        if self.is_bomb: self.end_game()
        num_surrounding_cells = self.num_surrounding_cells()
        if num_surrounding_cells > 0: self.cell_btn.configure(text=str(num_surrounding_cells))
        self.cell_btn.configure(background=colors['white'])

    def flag(self, right_click):
        pass

    def end_game(self):
        pass

    def num_surrounding_cells(self):
        return 0