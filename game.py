import tkinter as tk
from ctypes import windll, byref, create_unicode_buffer
from minesweeper import Minefield
from tictactoe import TicTacToe
from assets import GAME_FONT, COLORS

class Game(tk.Tk):
    def __init__(self): 
        tk.Tk.__init__(self)

        self.geometry("1024x768")
        self.title('Tic-Tac-Sweep')
        self.config(background=COLORS['background'])

        # Main container for all page frames
        game_frame = tk.Frame(self, width=1024, height=768, background=COLORS['background'])
        game_frame.place(x=0, y=0, width=1024, height=786) 

        # Populates pages with the different page classes after loading them
        self.pages = {}
        for F in (MainMenu, SPMenu, MPMenu):
            frame = F(game_frame, self)
            self.pages[F] = frame 
            frame.place(x=0, y=0, width=1024, height=786) 

        self.show_page(MainMenu)

    # Displays the current page
    def show_page(self, page_class):
        page = self.pages[page_class]
        page.tkraise()
    
    def quit(self):
        self.destroy()


class MainMenu(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        self.configure(bg=COLORS['background'])

        # Title Widgets
        title_text = tk.Label(
            self,
            text="Tic-Tac-Sweep",
            font=(GAME_FONT, 52),
            justify='center',
            fg=COLORS['yellow txt'],
            background=COLORS["background"],
        )
        title_text.place(relx=.5, rely=.15, anchor='center')

        # Button Widgets
        single_player_btn = tk.Button(
            self,
            text="Single Player",
            font=(GAME_FONT, 32),
            fg=COLORS["background"].dark(),
            activeforeground=COLORS["background"].dark(),
            background=COLORS['green btn'],
            activebackground=COLORS['green btn'].dark(),
            borderwidth=0,
            compound="center",
            command=lambda : controller.show_page(SPMenu)
        )
        single_player_btn.place(
            relx=.135,
            rely=.325,
            relwidth=.35,
            relheight=.1
        )

        multiplayer_btn = tk.Button(
            self,
            text="Multi Player",
            font=(GAME_FONT, 32),
            fg=COLORS["background"].dark(),
            activeforeground=COLORS["background"].dark(),
            background=COLORS['red btn'],
            activebackground=COLORS['red btn'].dark(),
            borderwidth=0,
            compound="center",
            command=lambda : controller.show_page(MPMenu)
        )
        multiplayer_btn.place(
            relx=.515,
            rely=.325,
            relwidth=.35,
            relheight=.1
        )

        how_to_play_btn = tk.Button(
            self,
            text="How to Play",
            font=(GAME_FONT, 32),
            fg=COLORS["background"].dark(),
            activeforeground=COLORS["background"].dark(),
            background=COLORS['yellow btn'],
            activebackground=COLORS['yellow btn'].dark(),
            borderwidth=0,
            compound="center",
        )
        how_to_play_btn.place(
            relx=.135,
            rely=.465,
            relwidth=.35,
            relheight=.1
        )

        profile_btn = tk.Button(
            self,
            text="Quit",
            font=(GAME_FONT, 32),
            fg=COLORS["background"].dark(),
            activeforeground=COLORS["background"].dark(),
            background=COLORS['purple btn'],
            activebackground=COLORS['purple btn'].dark(),
            borderwidth=0,
            compound="center",
            command=controller.quit
        )
        profile_btn.place(
            relx=.515,
            rely=.465,
            relwidth=.35,
            relheight=.1
        )


class SPMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.configure(bg=COLORS['background'])
        self.top_bar = TopBar(self, "Single Player").place(relx=0, rely=0, relwidth=1, relheight=.1)
        self.game = None

        # SIDE BAR ELEMENTS
        self.side_bar = tk.Frame(
            self,
            background=COLORS['background'].dark()
        )
        self.side_bar.place(relx=.05, rely=.15, relwidth=.25, relheight=.8)

        self.start_icon = tk.PhotoImage(file='assets/start.png')
        self.reset_icon = tk.PhotoImage(file='assets/reset.png')
        self.start_btn = tk.Button(
            self.side_bar,
            image=self.start_icon,
            background=COLORS['background'].dark(),
            activebackground=COLORS['background'].dark(),
            borderwidth=0,
            compound="center",
            command=self.start_game
        )
        self.start_btn.place(relx=.97, rely=.05, anchor='ne')

        self.stop_icon = tk.PhotoImage(file='assets/stop.png')
        self.stop_btn = tk.Button(
            self.side_bar,
            image=self.stop_icon,
            background=COLORS['background'].dark(),
            activebackground=COLORS['background'].dark(),
            borderwidth=0,
            compound="center",
            command=self.stop_game
        )
        self.stop_btn.place(relx=.025, rely=.05, anchor='nw')

        self.info_box = tk.Frame(
            self.side_bar,
            bg=COLORS['background'],
        )
        self.info_box.place(relx=.5, rely=.025, relwidth=.65, relheight=.15, anchor='n')

        self.timer = tk.Label(
            self.info_box,
            text='00:00.0',
            font=(GAME_FONT, 32),
            justify='center',
            fg=COLORS['yellow txt'],
            background=COLORS["background"],
        )
        self.timer.place(relx=.05, rely=.25, anchor='w')

        self.bomb_icon = tk.PhotoImage(file='assets/bomb.png')
        self.bomb_label = tk.Label(
            self.info_box,
            image=self.bomb_icon,
            background=COLORS['background'],
            borderwidth=0,
            compound="center",
        )
        self.bomb_label.place(relx=.25, rely=.75, anchor='w')
        self.bomb_count = tk.Label(
            self.info_box,
            text='0',
            font=(GAME_FONT, 32),
            justify='center',
            fg=COLORS['yellow txt'],
            background=COLORS["background"],
        )
        self.bomb_count.place(relx=.75, rely=.75, anchor='e')

        # GAME ELEMENTS
        self.minefield_frame = tk.Frame(
            self,
            bg=COLORS['background'].dark(.6),
            borderwidth=5
        )
        self.minefield_frame.place(relx=.35, rely=.15, relwidth=.6, relheight=.8)

    def start_game(self):
        self.start_btn.configure(image=self.reset_icon)
        self.start_btn.configure(command=self.reset_game)
        self.time = 0
        self.game = Minefield(self.minefield_frame)
        # Wait 100ms before updating the timer
        self.controller.after(100, self.update_info)

    def stop_game(self):
        self.start_btn.configure(image=self.start_icon)
        self.start_btn.configure(command=self.start_game)
        if self.game: self.game.game_over = 'Stopped'
        self.timer.configure(text=f'00:00.0')
        self.bomb_count.configure(text='0')
        for widget in self.minefield_frame.winfo_children():
            widget.destroy()

    def update_info(self):
        if self.game.game_over == 'Stopped': return
        self.bomb_count.configure(text=self.game.total_bombs - self.game.total_flags)
        if not self.game.game_over: # Game still going
            self.time += 1
            self.timer.configure(text=f'{self.time // 600:02}:{(self.time // 10) % 60:02}.{self.time % 10}')
            self.controller.after(100, self.update_info)

    def reset_game(self):
        self.stop_game()
        self.controller.after(100, self.start_game)

    def back(self):
        self.stop_game()
        self.controller.show_page(MainMenu)


class MPMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.configure(bg=COLORS['background'])
        TopBar(self, "Multiplayer").place(relx=0, rely=0, relwidth=1, relheight=.1)
        self.game = None

        # GAME ELEMENTS
        width = 1024 * .45
        height = 768 * .6
        self.tictactoe_frame = tk.Frame(self, bg=COLORS['background'].dark(.6),)
        self.tictactoe_frame.place(relx=.025, rely=.15, width=width, height=height)

        TicTacToe(self.tictactoe_frame, width, height)
        
    def back(self):
        self.controller.show_page(MainMenu)


class H2PMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


class TopBar(tk.Frame):
    def __init__(self, parent, menu_name):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.configure(bg=COLORS['background'].dark())

        # TOP BAR ELEMENTS
        title_text = tk.Label(
            self,
            text=menu_name,
            font=(GAME_FONT, 32),
            justify='center',
            fg=COLORS['yellow txt'],
            background=COLORS["background"].dark(),
        )
        title_text.place(relx=.5, rely=.5, anchor='center')

        self.back_icon = tk.PhotoImage(file='assets/left.png')
        self.back_btn = tk.Button(
            self,
            image=self.back_icon,
            background=COLORS['background'].dark(),
            activebackground=COLORS['background'].dark(),
            borderwidth=0,
            compound="center",
            command=self.parent.back
        )
        self.back_btn.place(relx=.025, rely=0.5, anchor='w')

        self.quit_icon = tk.PhotoImage(file='assets/quit.png')
        self.quit_btn = tk.Button(
            self,
            image=self.quit_icon,
            background=COLORS['background'].dark(),
            activebackground=COLORS['background'].dark(),
            borderwidth=0,
            compound="center",
            command=self.parent.controller.quit
        )
        self.quit_btn.place(relx=.975, rely=0.5, anchor='e')


def load_font(font_path):
    '''
    Makes custom fonts available to the font system as a private
    resource for the application to use.

    font_path (str): file directory for the font. Ex: 'foldername/filename.ttf'
    '''
    if not isinstance(font_path, str):
        raise ValueError("font_path needs to be a string. Ex: 'foldername/filename.ttf'")
    
    path_buffer = create_unicode_buffer(font_path)
    windll.gdi32.AddFontResourceExW(byref(path_buffer), 0x10, 0)


if __name__ == "__main__":
    load_font("assets/RuneScape-Bold-12.ttf")
    root = Game()
    root.mainloop()
