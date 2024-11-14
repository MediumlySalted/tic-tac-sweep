from assets import GAME_FONT, COLORS
import random
import tkinter as tk

class Minesweeper:
    def __init__(self, game_frame, mp=False, ttt_button=None):
        self.game_frame = game_frame
        self.mp = mp
        self.ttt_button = ttt_button
        self.game_state = False
        self.size = 9 # Recommended range [8, 16]
        self.bomb_percent = .12 # Recommended range [0.10, 0.20]
        self.total_bombs = int(self.size**2 * self.bomb_percent)
        self.total_flags = 0
        self.cells_left = self.size**2
        self.bomb_icon = tk.PhotoImage(file='assets/bomb.png')
        self.flag_icon = tk.PhotoImage(file='assets/flag.png')

    def create_minefield(self):
        self.game_state = True
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
            self.game_state = 'Win'
            self.reveal()
            if self.mp:
                self.ttt_button.mark('Win')


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

    def sweep(self, rec=False, event=None):
        if self.is_flagged and self.minefield.game_state != 'Lose': return
        if not self.is_swept: self.minefield.cells_left -= 1
        self.is_swept = True
        if self.is_bomb:
            if self.minefield.game_state == 'Win':
                self.cell_btn.configure(background=COLORS['green'], image=self.minefield.bomb_icon)
            else: self.minefield.game_state = 'Lose'
            if self.minefield.game_state == 'Lose': self.cell_btn.configure(background=COLORS['red x'], image=self.minefield.bomb_icon)
            self.minefield.reveal()
        else:
            self.cell_btn.configure(background=COLORS['white'])
            surrounding_bombs, surrounding_flags = self.surrounding_cells()
            # Sweep surrounding cells
            if surrounding_bombs == 0: rec = True
            if surrounding_bombs - surrounding_flags <= 0 and rec:
                for i in range(max(0, self.y_pos-1), min(self.y_pos+2, self.minefield.size)):
                    for j in range(max(0, self.x_pos-1), min(self.x_pos+2, self.minefield.size)):
                        cell = self.minefield.cells[i][j]
                        if not cell.is_swept and not cell.is_flagged:
                            cell.sweep()

            if surrounding_bombs > 0 and not self.is_flagged: self.cell_btn.configure(text=str(surrounding_bombs), font=(GAME_FONT, 24))
            if self.is_flagged: self.cell_btn.configure(text='X', font=(GAME_FONT, 32), fg=COLORS['red x'], image='')
            self.minefield.check_for_win()

    def flag(self, event=None):
        if self.is_swept: return
        if not self.is_flagged:
            self.minefield.total_flags += 1
            self.cell_btn.configure(image=self.minefield.flag_icon)
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


class TicTacToe:
    def __init__(self, game_frame, width, height):
        self.game_frame = game_frame
        self.width = width
        self.height = height

        self.game_state = None
        self.game_board = [[] for _ in range(3)]
        self.turn = True

        self.draw_canvas()
        self.create_buttons()

    def draw_canvas(self):
        game_canvas = tk.Canvas(
            self.game_frame,
            bg=COLORS['background'].dark(.6),
            highlightthickness=0
        )
        game_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        game_canvas.create_line(5, self.height/3, self.width-5, self.height/3, fill=COLORS['background'], width=5)
        game_canvas.create_line(5, 2*self.height/3, self.width-5, 2*self.height/3, fill=COLORS['background'], width=5)
        game_canvas.create_line(self.width/3, 5, self.width/3, self.height-5, fill=COLORS['background'], width=5)
        game_canvas.create_line(2*self.width/3, 5, 2*self.width/3, self.height-5, fill=COLORS['background'], width=5)

    def create_buttons(self):
        for i in range(3):
            for j in range(3):
                btn = TTTButton(self)
                btn.btn.place(
                    x=j*self.width/3+10,
                    y=i*self.height/3+10,
                    width=self.width/3-20,
                    height=self.height/3-20
                )
                self.game_board[i].append(btn)

    def check_for_win(self):
        # Check rows & cols
        for i in range(3):
            row_check = self.game_board[i][0].btn['text']
            if row_check and all(row_check == self.game_board[i][j].btn['text'] for j in range(1, 3)): return row_check
            col_check = self.game_board[0][i].btn['text']
            if col_check and all(col_check == self.game_board[j][i].btn['text'] for j in range(1, 3)): return col_check

        # Check diagonals
        nw_to_se_check = self.game_board[0][0].btn['text']
        if nw_to_se_check and all(nw_to_se_check == self.game_board[i][i].btn['text'] for i in range(1, 3)): return nw_to_se_check
        ne_to_sw_check = self.game_board[0][-1].btn['text']
        if ne_to_sw_check and all(ne_to_sw_check == self.game_board[i][-i].btn['text'] for i in range(1, 3)): return ne_to_sw_check


class TTTButton:
    def __init__(self, tictactoe):
        self.tictactoe = tictactoe
        self.marked = False
        self.btn = tk.Button(
            self.tictactoe.game_frame,
            text=None,
            font=(GAME_FONT, 48),
            background=COLORS['background'].dark(.6),
            activebackground=COLORS['background'].dark(.5),
            borderwidth=0,
            command=self.start_ms_game
        )
        self.ms_game = None

    def start_ms_game(self):
        if self.marked: return
        if self.tictactoe.turn: self.btn.configure(text='X', fg=COLORS['yellow txt'])
        if not self.tictactoe.turn: self.btn.configure(text='O', fg=COLORS['yellow txt'])
        for widget in self.tictactoe.game_frame.master.minefield_frame.winfo_children():
            widget.destroy()
        self.ms_game = Minesweeper(self.tictactoe.game_frame.master.minefield_frame, mp=True, ttt_button=self)
        self.ms_game.create_minefield()

    def mark(self, state):
        if state == 'Win':
            self.marked = True
            turn = self.tictactoe.turn
            if turn: self.btn.configure(text='X', fg=COLORS['green'])
            if not turn: self.btn.configure(text='O', fg=COLORS['red x'])
            self.tictactoe.turn = not turn
            self.tictactoe.game_state = self.tictactoe.check_for_win()
        if self.ms_game.game_state == 'Lose':
            self.tictactoe.game_state = None
            if self.tictactoe.turn: self.btn.configure(text=None)
            if not self.tictactoe.turn: self.btn.configure(text=None)
