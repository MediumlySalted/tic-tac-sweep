from assets import GAME_FONT, COLORS
import tkinter as tk

class TicTacToe:
    def __init__(self, game_frame, width, height):
        self.game_frame = game_frame
        self.width = width
        self.height = height

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
        pass


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
        self.tictactoe.check_for_win()
