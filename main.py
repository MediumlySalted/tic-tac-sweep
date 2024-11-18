import tkinter as tk
import threading
from json import dumps, loads
from ctypes import windll, byref, create_unicode_buffer
from tictacsweep import Minesweeper, TicTacToe
from assets import GAME_FONT, COLORS
from matchmaker import Match

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
        tk.Frame.__init__(self, parent, bg=COLORS['background'])

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
        tk.Frame.__init__(self, parent, bg=COLORS['background'])
        self.controller = controller
        self.top_bar = TopBar(self, "Single Player")
        self.top_bar.place(relx=0, rely=0, relwidth=1, relheight=.1)
        self.game = None

        self.create_side_bar_elements()

    def create_side_bar_elements(self):
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

        self.create_info_box_elements()
        self.create_settings_box_elements()

    def create_info_box_elements(self):
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

    def create_settings_box_elements(self):
        self.settings = Settings(
            self.side_bar,
            size=9,
            size_range=(8, 16),
            bomb_percent=0.12,
            bomb_percent_range=(0.1, 0.2)
        )
        self.settings.place(relx=.5, rely=.2, relwidth=.65, relheight=.2, anchor='n')
        self.settings.create_size_display()
        self.settings.create_bomb_percent_display()

    def start_game(self):
        self.start_btn.configure(image=self.reset_icon)
        self.start_btn.configure(command=self.reset_game)
        self.time = 0
        self.game = Minesweeper(
            self.minefield_frame,
            size=self.settings.size,
            bomb_percent=self.settings.bomb_percent
        )
        self.game.create_minefield()
        # Wait 100ms before updating the timer
        self.controller.after(100, self.update_info)

    def stop_game(self):
        self.start_btn.configure(image=self.start_icon)
        self.start_btn.configure(command=self.start_game)
        if self.game: self.game.game_state = 'Stopped'
        self.timer.configure(text=f'00:00.0')
        self.bomb_count.configure(text='0')
        for widget in self.minefield_frame.winfo_children():
            widget.destroy()

    def update_info(self):
        if self.game.game_state == 'Stopped': return
        self.bomb_count.configure(text=self.game.total_bombs - self.game.total_flags)
        if self.game.game_state not in {'Win', 'Lose'}: # Game still going
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
        tk.Frame.__init__(self, parent, bg=COLORS['background'])
        self.controller = controller
        self.top_bar = TopBar(self, "Multiplayer")
        self.top_bar.place(relx=0, rely=0, relwidth=1, relheight=.1)
        self.top_bar.quit_btn.configure(command=self.quit)
        self.relwidth = 1024 * .45
        self.relheight = 768 * .6
        self.game = None
        self.match = None

        self.create_settings_bar()
        self.create_info_bar()
        self.create_minesweeper_elements()
        self.create_tictactoe_elements()

    def create_settings_bar(self):
        self.settings_bar = tk.Frame(self, bg=COLORS['background'].dark())
        self.settings_bar.place(relx=.25, rely=.125, relwidth=.45, relheight=.15, anchor='n')

        self.settings = Settings(
            self.settings_bar,
            size=9,
            size_range=(8, 16),
            bomb_percent=0.12,
            bomb_percent_range=(0.1, 0.2)
        )
        self.settings.place(relx=.05, rely=.5, relwidth=.6, relheight=.8, anchor='w')
        self.settings.create_size_display()
        self.settings.create_bomb_percent_display()

        self.start_icon = tk.PhotoImage(file='assets/start.png')
        self.start_btn = tk.Button(
            self.settings_bar,
            image=self.start_icon,
            background=COLORS['background'].dark(),
            activebackground=COLORS['background'].dark(),
            borderwidth=0,
            compound="center",
            command=self.start_game
        )
        self.start_btn.place(relx=.925, rely=.5, anchor='e')
        self.stop_icon = tk.PhotoImage(file='assets/stop.png')
        self.stop_btn = tk.Button(
            self.settings_bar,
            image=self.stop_icon,
            background=COLORS['background'].dark(),
            activebackground=COLORS['background'].dark(),
            borderwidth=0,
            compound="center",
            command=self.end_game
        )
        self.stop_btn.place(relx=.8, rely=.5, anchor='e')

    def create_info_bar(self):
        self.info_bar = tk.Frame(self, bg=COLORS['background'].dark())
        self.info_bar.place(relx=.75, rely=.125, relwidth=.45, relheight=.15, anchor='n')

    def create_minesweeper_elements(self):
        self.minefield_frame = tk.Frame(
            self,
            bg=COLORS['background'].dark(.6),
            borderwidth=5
        )
        self.minefield_frame.place(relx=.525, rely=.3, width=self.relwidth, height=self.relheight)

    def create_tictactoe_elements(self):
        self.tictactoe_frame = tk.Frame(self, bg=COLORS['background'].dark(.6),)
        self.tictactoe_frame.place(relx=.025, rely=.3, width=self.relwidth, height=self.relheight)

    def start_game(self):
        self.game = TicTacToe(
            self.tictactoe_frame,
            self.relwidth,
            self.relheight,
            size=self.settings.size,
            bomb_percent=self.settings.bomb_percent
        )
        self.match = Match(self.game)
        self.search_dots = 0
        self.searching_display = tk.Label(
            self.info_bar,
            text=f'Searching{self.search_dots //2 * '.'}',
            font=(GAME_FONT, 32),
            justify='center',
            fg=COLORS['yellow txt'],
            background=COLORS["background"],
        )
        self.searching_display.place(relx=.05, rely=.5, anchor='w')
        self.stop_searching = threading.Event()
        match_thread = threading.Thread(target=self.match.find_match, args=(self.stop_searching,))
        match_thread.start()
        self.wait_for_game()

    def wait_for_game(self):
        if self.match:
            if not self.match.connection:
                self.search_dots = (self.search_dots + 1) % 8
                self.searching_display['text'] = f'Searching{self.search_dots // 2 * '.'}'
                self.controller.after(100, self.wait_for_game)
            else: self.game_found()

    def game_found(self):
        self.game.match = self.match
        for widget in self.info_bar.winfo_children():
            widget.destroy()
        self.game.draw_canvas()
        self.game.create_buttons()

    def end_game(self):
        if self.match:
            print("Search ended.")
            self.stop_searching.set()
            self.match.end()
        self.clear_game()

    def back(self):
        self.end_game()
        self.controller.show_page(MainMenu)

    def quit(self):
        self.end_game()
        self.controller.quit()

    def clear_game(self):
        self.game = None
        self.match = None
        for widget in self.minefield_frame.winfo_children():
            widget.destroy()
        for widget in self.tictactoe_frame.winfo_children():
            widget.destroy()
        for widget in self.info_bar.winfo_children():
            widget.destroy()


class H2PMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


class TopBar(tk.Frame):
    def __init__(self, parent, menu_name):
        tk.Frame.__init__(self, parent, bg=COLORS['background'].dark())
        self.parent = parent

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


class Settings(tk.Frame):
    def __init__(self, parent, size, bomb_percent, size_range, bomb_percent_range):
        tk.Frame.__init__(self, parent, background=COLORS['background'])
        self.size = size
        self.bomb_percent = bomb_percent
        self.size_range = size_range
        self.bomb_percent_range = bomb_percent_range
        self.up_icon = tk.PhotoImage(file='assets/up.png')
        self.down_icon = tk.PhotoImage(file='assets/down.png')

    def create_size_display(self):
        self.size_display = tk.Label(
            self,
            text=f'{self.size:02}',
            font=(GAME_FONT, 32),
            justify='center',
            fg=COLORS['yellow txt'],
            background=COLORS["background"],
        )
        self.size_display.place(relx=.05, rely=.25, anchor='w')
        self.size_up_btn = tk.Button(
            self,
            image=self.up_icon,
            background=COLORS['background'],
            borderwidth=0,
            compound="center",
            command=self.size_up
        )
        self.size_up_btn.place(relx=.95, rely=.25, anchor='se')
        self.size_down_btn = tk.Button(
            self,
            image=self.down_icon,
            background=COLORS['background'],
            borderwidth=0,
            compound="center",
            command=self.size_down
        )
        self.size_down_btn.place(relx=.95, rely=.25, anchor='ne')

    def create_bomb_percent_display(self):
        self.bomb_percent_display = tk.Label(
            self,
            text=f'{self.bomb_percent * 100:.0f}%',
            font=(GAME_FONT, 32),
            justify='center',
            fg=COLORS['yellow txt'],
            background=COLORS["background"],
        )
        self.bomb_percent_display.place(relx=.05, rely=.75, anchor='w')
        self.bomb_percent_up_btn = tk.Button(
            self,
            image=self.up_icon,
            background=COLORS['background'],
            borderwidth=0,
            compound="center",
            command=self.bomb_percent_up
        )
        self.bomb_percent_up_btn.place(relx=.95, rely=.75, anchor='se')
        self.bomb_percent_down_btn = tk.Button(
            self,
            image=self.down_icon,
            background=COLORS['background'],
            borderwidth=0,
            compound="center",
            command=self.bomb_percent_down
        )
        self.bomb_percent_down_btn.place(relx=.95, rely=.75, anchor='ne')

    def size_up(self):
        self.size += 1
        if self.size > self.size_range[1]: self.size -= self.size_range[1] - self.size_range[0] + 1
        self.update_settings()

    def size_down(self):
        self.size -= 1
        if self.size < self.size_range[0]: self.size += self.size_range[1] - self.size_range[0] + 1
        self.update_settings()

    def bomb_percent_up(self):
        self.bomb_percent += 0.01
        if self.bomb_percent > self.bomb_percent_range[1]:
            self.bomb_percent -= self.bomb_percent_range[1] - self.bomb_percent_range[0] + 0.01
        self.update_settings()

    def bomb_percent_down(self):
        self.bomb_percent -= 0.01
        if self.bomb_percent < self.bomb_percent_range[0]:
            self.bomb_percent += self.bomb_percent_range[1] - self.bomb_percent_range[0] + 0.01
        self.update_settings()

    def update_settings(self):
        self.size_display['text'] = f'{self.size:02}'
        self.bomb_percent_display['text'] = f'{self.bomb_percent * 100:.0f}%'

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
