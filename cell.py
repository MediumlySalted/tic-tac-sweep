import assets
import random
from tkinter import Button

game_font = assets.game_font
colors = assets.colors

class Minefield:
    def __init__(self, game_frame):
        self.game_frame = game_frame
        self.cells = [[] for _ in range(9)]

    def create_minefield(self):
        for i in range(9):
            for j in range(9):
                bomb = False
                if random.randrange(8) == 1: bomb = True
                cell = Cell(self, self.game_frame, (j, i), bomb)
                cell.cell_btn.place(
                    relx=j/9,
                    rely=i/9,
                    relwidth=1/9,
                    relheight=1/9
                )
                self.cells[i].append(cell)


class Cell:
    def __init__(self, minefield, game_frame, pos, is_bomb):
        self.minefield = minefield
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.is_bomb = is_bomb
        self.is_swept = False
        self.is_flagged = False

        self.cell_btn = Button(
            game_frame,
            background=colors['cell'],
            activebackground=colors['cell'].dark(),
            borderwidth=1,
            relief='ridge'
        )
        self.cell_btn.bind('<Button-1>', self.sweep)
        self.cell_btn.bind('<Button-3>', self.flag)

    def sweep(self, event=None):
        self.is_swept = True
        if self.is_bomb:
            self.cell_btn.configure(background=colors['red x'])
        else:
            self.cell_btn.configure(background=colors['white'])
            num_bombs = self.num_surrounding_cells()
            if num_bombs == 0:
                for i in range(-1,2):
                    for j in range(-1,2):
                        check_x = self.x_pos + j
                        check_y = self.y_pos + i
                        if (check_x >= 0 and check_x <= 8) and (check_y >= 0 and check_y <= 8):
                            cell = self.minefield.cells[check_y][check_x]
                            if not cell.is_swept: cell.sweep()

            else: self.cell_btn.configure(text=str(num_bombs), font=(game_font, 24))

    def flag(self, event=None):
        pass

    def end_game(self):
        pass

    def num_surrounding_cells(self):
        num = 0
        for i in range(-1,2):
            for j in range(-1,2):
                check_x = self.x_pos + j
                check_y = self.y_pos + i
                if (check_x >= 0 and check_x <= 8) and (check_y >= 0 and check_y <= 8):
                    if self.minefield.cells[check_y][check_x].is_bomb:
                        num += 1

        return num