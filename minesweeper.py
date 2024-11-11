from assets import GAME_FONT, COLORS
import random
import tkinter as tk

class Minefield:
    def __init__(self, game_frame):
        self.game_frame = game_frame
        self.game_over = False
        self.size = 9 # Recommended range [8, 16]
        self.bomb_percent = .12 # Recommended range [0.10, 0.20]
        self.total_bombs = int(self.size**2 * self.bomb_percent)
        self.total_flags = 0
        self.cells_left = self.size**2
    
        self.create_minefield()

        
    def create_minefield(self):
        # 2d array of minefield
        self.cells = [[] for _ in range(self.size)]
        bombs = random.sample(range(self.size**2), self.total_bombs)
        for i in range(self.size):
            for j in range(self.size):
                bomb = (i*self.size + j) in bombs
                cell = Cell(self, self.game_frame, (j, i), bomb)
                cell.cell_btn.place(
                    relx=j/self.size,
                    rely=i/self.size,
                    relwidth=1/self.size,
                    relheight=1/self.size
                )
                self.cells[i].append(cell)

    def reveal(self):
        for i in range(self.size):
            for j in range(self.size):
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

    def sweep(self, rec=False, event=None):
        if not self.is_swept: self.minefield.cells_left -= 1
        self.is_swept = True
        if self.is_bomb:
            if not self.minefield.game_over: self.minefield.game_over = 'Lose'
            if self.minefield.game_over == 'Lose': self.cell_btn.configure(background=COLORS['red x'], image=self.bomb_icon)
            if self.minefield.game_over == 'Win': self.cell_btn.configure(background=COLORS['green'], image=self.bomb_icon)
            self.minefield.reveal()
        else:
            if self.is_flagged: return
            self.cell_btn.configure(background=COLORS['white'])
            surrounding_bombs, surrounding_flags = self.surrounding_cells()

            # Sweep surrounding cells
            if surrounding_bombs == 0: rec = True
            if surrounding_bombs - surrounding_flags == 0 and rec:
                for i in range(max(0, self.y_pos-1), min(self.y_pos+2, self.minefield.size)):
                    for j in range(max(0, self.x_pos-1), min(self.x_pos+2, self.minefield.size)):
                        cell = self.minefield.cells[i][j]
                        if not cell.is_swept and not cell.is_flagged:
                            cell.sweep()

            self.minefield.check_for_win()
            if surrounding_bombs > 0: self.cell_btn.configure(text=str(surrounding_bombs), font=(GAME_FONT, 24))

    def flag(self, event=None):
        if self.is_swept: return
        if not self.is_flagged:
            self.minefield.total_flags += 1
            self.cell_btn.configure(image=self.flag_icon)
        else:
            self.minefield.total_flags -= 1
            self.cell_btn.configure(image='')
        self.is_flagged = not self.is_flagged
        self.minefield.check_for_win()

    def surrounding_cells(self):
        bombs = 0
        flags = 0
        for i in range(max(0, self.y_pos-1), min(self.y_pos+2, self.minefield.size)):
            for j in range(max(0, self.x_pos-1), min(self.x_pos+2, self.minefield.size)):
                if self.minefield.cells[i][j].is_bomb:
                    bombs += 1
                if self.minefield.cells[i][j].is_flagged:
                    flags += 1

        return (bombs, flags)
