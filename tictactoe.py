from assets import GAME_FONT, COLORS
import tkinter as tk

class TicTacToe:
    def __init__(self, game_frame, width, height):
        self.game_frame = game_frame

        self.game_board = [[] for _ in range(3)]

        # Canvas Drawing
        self.game_canvas = tk.Canvas(
            self.game_frame,
            bg=COLORS['background'].dark(.6),
            highlightthickness=0
        )
        self.game_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.game_canvas.create_line(5, height/3, width-5, height/3, fill=COLORS['background'], width=5)
        self.game_canvas.create_line(5, 2*height/3, width-5, 2*height/3, fill=COLORS['background'], width=5)
        self.game_canvas.create_line(width/3, 5, width/3, height-5, fill=COLORS['background'], width=5)
        self.game_canvas.create_line(2*width/3, 5, 2*width/3, height-5, fill=COLORS['background'], width=5)

        # Buttons
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    game_frame,
                    background=COLORS['background'].dark(.6),
                    activebackground=COLORS['background'].dark(.5),
                    borderwidth=0,
                    compound="center",
                    relief='ridge'
                )
                btn.place(
                    x=j*width/3+10,
                    y=i*height/3+10,
                    width=width/3-20,
                    height=height/3-20
                )