from assets import GAME_FONT, COLORS
import tkinter as tk

class TicTacToe:
    def __init__(self, game_frame, width, height):
        self.game_frame = game_frame
        self.width = width
        self.height = height

        self.game_state = True
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
        self.btn = tk.Button(
            self.tictactoe.game_frame,
            text=None,
            font=(GAME_FONT, 48),
            background=COLORS['background'].dark(.6),
            activebackground=COLORS['background'].dark(.5),
            borderwidth=0,
            command=self.mark
        )

    def mark(self):
        if self.btn['text']: return
        turn = self.tictactoe.turn
        if turn: self.btn.configure(text='X')
        if not turn: self.btn.configure(text='O')
        self.tictactoe.turn = not turn
        self.tictactoe.game_state = self.tictactoe.check_for_win()
