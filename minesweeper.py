from assets import GAME_FONT, COLORS
import random
import tkinter as tk

class Minefield:
    def __init__(self, game_frame):
        self.game_frame = game_frame
        self.cells = [[] for _ in range(9)]
        self.game_over = False
        self.total_bombs = 0
        self.total_flags = 0
        self.cells_left = 9 * 9

    def create_minefield(self):
        for i in range(9):
            for j in range(9):
                bomb = False
                if random.randrange(8) == 1:
                    bomb = True
                    self.total_bombs += 1
                cell = Cell(self, self.game_frame, (j, i), bomb)
                cell.cell_btn.place(
                    relx=j/9,
                    rely=i/9,
                    relwidth=1/9,
                    relheight=1/9
                )
                self.cells[i].append(cell)

    def reveal(self):
        for i in range(9):
            for j in range(9):
                cell =  self.cells[i][j]
                if not cell.is_swept: cell.sweep()

    def check_for_win(self):
        if self.cells_left == self.total_bombs == self.total_flags:
            self.game_over = 'Win'
            self.reveal()


class Cell:
    def __init__(self, minefield, game_frame, pos, is_bomb):
        self.minefield = minefield
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.is_bomb = is_bomb
        self.is_swept = False
        self.is_flagged = False


        self.cell_btn = tk.Button(
            game_frame,
            background=COLORS['cell'],
            activebackground=COLORS['cell'].dark(),
            borderwidth=1,
            compound="center",
            relief='ridge'
        )
        self.cell_btn.bind('<Button-1>', self.sweep)
        self.cell_btn.bind('<Button-3>', self.flag)
        self.bomb_icon = tk.PhotoImage(file='assets/bomb.png')
        self.flag_icon = tk.PhotoImage(file='assets/flag.png')

    def sweep(self, event=None):
        if not self.is_swept: self.minefield.cells_left -= 1
        self.is_swept = True
        if self.is_bomb:
            if not self.minefield.game_over: self.minefield.game_over = 'Lose'
            if self.minefield.game_over == 'Lose': self.cell_btn.configure(background=COLORS['red x'], image=self.bomb_icon)
            if self.minefield.game_over == 'Win': self.cell_btn.configure(background=COLORS['green'], image=self.bomb_icon)
            self.minefield.reveal()
        else:
            self.cell_btn.configure(background=COLORS['white'])
            surrounding_bombs = self.surrounding_cells()[0]
            surrounding_flags = self.surrounding_cells()[1]
            if surrounding_bombs - surrounding_flags == 0:
                for i in range(-1,2):
                    for j in range(-1,2):
                        check_x = self.x_pos + j
                        check_y = self.y_pos + i
                        if (check_x >= 0 and check_x <= 8) and (check_y >= 0 and check_y <= 8):
                            cell = self.minefield.cells[check_y][check_x]
                            if not cell.is_swept and not cell.is_flagged:
                                cell.sweep()

            self.minefield.check_for_win()
            if surrounding_bombs > 0: self.cell_btn.configure(text=str(surrounding_bombs), font=(GAME_FONT, 24))

    def flag(self, event=None):
        if not self.is_swept:
            if not self.is_flagged:
                self.is_flagged = True
                self.minefield.total_flags += 1
                self.cell_btn.configure(image=self.flag_icon)
            else:
                self.is_flagged = False
                self.minefield.total_flags -= 1
                self.cell_btn.configure(image='')
            self.minefield.check_for_win()

    def surrounding_cells(self):
        bombs = 0
        flags = 0
        for i in range(-1,2):
            for j in range(-1,2):
                check_x = self.x_pos + j
                check_y = self.y_pos + i
                if (check_x >= 0 and check_x <= 8) and (check_y >= 0 and check_y <= 8):
                    if self.minefield.cells[check_y][check_x].is_bomb:
                        bombs += 1
                    if self.minefield.cells[check_y][check_x].is_flagged:
                        flags += 1

        return (bombs, flags)