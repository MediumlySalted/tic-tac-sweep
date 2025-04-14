import tkinter as tk
import threading
from PIL import Image, ImageTk
from tictacsweep import Minesweeper, TicTacToe
from assets import GAME_FONT, COLORS
from matchmaker import Match, Matchmaker

class Game(tk.Tk):
    def __init__(self): 
        tk.Tk.__init__(self)
        self.matchmaker = Matchmaker()

        self.geometry("1024x768")
        self.title('Tic-Tac-Sweep')
        self.config(background=COLORS['background'])

        # Main container frame for all menus
        game_frame = tk.Frame(self, width=1024, height=768, background=COLORS['background'])
        game_frame.place(x=0, y=0, width=1024, height=786) 

        # Populates pages with the different menu classes after loading them
        self.pages = {}
        for F in (MainMenu, SinglePlayer, MultiPlayer, ServerListDisplay, Instructions):
            frame = F(game_frame, self)
            self.pages[F] = frame
            frame.place(x=0, y=0, width=1024, height=786)

        self.show_page(MainMenu)

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
            command=lambda : controller.show_page(SinglePlayer),
            highlightthickness=0
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
            command=lambda : controller.show_page(ServerListDisplay),
            highlightthickness=0
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
            command=lambda : controller.show_page(Instructions),
            highlightthickness=0
        )
        how_to_play_btn.place(
            relx=.135,
            rely=.465,
            relwidth=.35,
            relheight=.1
        )

        quit_btn = tk.Button(
            self,
            text="Quit",
            font=(GAME_FONT, 32),
            fg=COLORS["background"].dark(),
            activeforeground=COLORS["background"].dark(),
            background=COLORS['purple btn'],
            activebackground=COLORS['purple btn'].dark(),
            borderwidth=0,
            compound="center",
            command=controller.quit,
            highlightthickness=0
        )
        quit_btn.place(
            relx=.515,
            rely=.465,
            relwidth=.35,
            relheight=.1
        )


class SinglePlayer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=COLORS['background'])
        self.controller = controller
        self.top_bar = TopBar(self, "Single Player")
        self.top_bar.place(relx=0, rely=0, relwidth=1, relheight=.1)
        self.game = None

        self.create_side_bar_elements()
        self.minefield_frame = tk.Frame(
            self,
            bg=COLORS['background'].dark(.6),
            borderwidth=5
        )
        self.minefield_frame.place(relx=.35, rely=.15, relwidth=.6, relheight=.8)

    def create_side_bar_elements(self):
        self.side_bar = tk.Frame(self, background=COLORS['background'].dark())
        self.side_bar.place(relx=.05, rely=.15, relwidth=.25, relheight=.8)

        self.start_btn = ButtonIcon(self.side_bar, 'assets/start.png', hover_scale=1.1,
                                    command=self.start_game)
        self.start_btn.place(relx=.9, rely=.1, anchor='center')
        
        self.stop_btn = ButtonIcon(self.side_bar, 'assets/stop.png', hover_scale=1.1,
                                   command=self.stop_game)
        self.stop_btn.place(relx=.09, rely=.1, anchor='center')

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
        self.start_btn.change_image('assets/reset.png')
        self.start_btn.command = self.reset_game
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
        self.start_btn.change_image('assets/start.png')
        self.start_btn.command = self.start_game
        if self.game: self.game.game_state = 'Stopped'
        self.timer.configure(text=f'00:00.0')
        self.bomb_count.configure(text='0')
        for widget in self.minefield_frame.winfo_children():
            widget.destroy()

    def update_info(self):
        if self.game.game_state not in {'Win', 'Lose', 'Stopped'}: # Game still going
            self.time += 1
            self.timer.configure(text=f'{self.time // 600:02}:{(self.time // 10) % 60:02}.{self.time % 10}')
            self.controller.after(100, self.update_info)

    def reset_game(self):
        self.stop_game()
        self.controller.after(100, self.start_game)

    def back(self):
        self.stop_game()
        self.controller.show_page(MainMenu)


class MultiPlayer(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['background'])
        self.controller = controller
        self.game = None
        self.match = None
        self.available_matches = []
        self.stop_searching = None

        self.relwidth = 1024 * .45
        self.relheight = 768 * .6

        self.top_bar = TopBar(self, "Multiplayer")
        self.top_bar.place(relx=0, rely=0, relwidth=1, relheight=.1)

    def refresh_servers(self):
        matches = self.controller.matchmaker.find_servers()
        self.available_matches = matches
        self.controller.pages[ServerListDisplay].update_servers(matches)

    def join_selected_game(self):
        index = self.controller.pages[ServerListDisplay].get_selected_index()
        if index is None:
            return
        
        connection = self.available_matches[index]
        self.join_game(connection)

    def host_game(self):
        self.setup_game()
        self.match = Match(self.game, host=True)
        self.stop_searching = threading.Event()
        threading.Thread(target=self.match.wait_for_player, args=(self.stop_searching,)).start()

    def join_game(self, connection):
        self.setup_game()
        self.match = Match(self.game, connection=connection)

    def setup_game(self):
        self.create_settings_bar()
        self.create_info_bar()
        self.create_minesweeper_frame()
        self.create_tictactoe_frame()
        self.controller.show_page(MultiPlayer)
        self.game = TicTacToe(
            self.tictactoe_frame,
            self.relwidth,
            self.relheight,
            size=self.settings.size,
            bomb_percent=self.settings.bomb_percent
        )

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

    def create_info_bar(self):
        self.info_bar = tk.Frame(self, bg=COLORS['background'].dark())
        self.info_bar.place(relx=.75, rely=.125, relwidth=.45, relheight=.15, anchor='n')
        self.waiting_display = tk.Label(
            self.info_bar,
            text="Waiting for player...",
            font=(GAME_FONT, 32),
            fg=COLORS['yellow txt'],
            bg=COLORS['background'].dark()
        )
        self.waiting_display.place(relx=0.05, rely=0.5, anchor='w')

    def create_minesweeper_frame(self):
        self.minefield_frame = tk.Frame(self, bg=COLORS['background'].dark(.6), borderwidth=5)
        self.minefield_frame.place(relx=.525, rely=.3, width=self.relwidth, height=self.relheight)

    def create_tictactoe_frame(self):
        self.tictactoe_frame = tk.Frame(self, bg=COLORS['background'].dark(.6))
        self.tictactoe_frame.place(relx=.025, rely=.3, width=self.relwidth, height=self.relheight)

    def end_game(self):
        if self.match: 
            self.match.close_connection()
            self.match = None

        if self.game:
            self.game = None
            for widget in [self.settings_bar, self.info_bar, self.minefield_frame, self.tictactoe_frame]:
                if widget:
                    widget.destroy()

    def back(self):
        self.end_game()
        self.controller.show_page(ServerListDisplay)

    def quit(self):
        self.end_game()
        self.controller.quit()


class ServerListDisplay(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, background=COLORS['background'])
        self.controller = controller
        self.selected_server = tk.IntVar(value=0)
        self.entries = []

        self.top_bar = TopBar(self, "Server Browser")
        self.top_bar.place(relx=0, rely=0, relwidth=1, relheight=.1)
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, background=COLORS['background'].dark(), highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, background=COLORS['background'])

        self.scroll_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.place(relx=.1, rely=.15, relwidth=.8, relheight=.7)
        self.scrollbar.place(relx=0.9, rely=0.15, relheight=0.7)

        self.refresh_btn = ButtonIcon(self, 'assets/reset.png', 
                                      command=self.controller.pages[MultiPlayer].refresh_servers,)
        self.refresh_btn.place(relx=0.2, rely=0.9, anchor='center')

        self.join_btn = ButtonIcon(self, 'assets/start.png',
                                   command=self.controller.pages[MultiPlayer].join_selected_game,
        )
        self.join_btn.place(relx=0.5, rely=0.9, anchor='center')

        self.host_btn = tk.Button(
            self,
            text="Host Game", 
            font=(GAME_FONT, 18),
            fg=COLORS["background"].dark(),
            activeforeground=COLORS["background"].dark(),
            background=COLORS['green btn'],
            activebackground=COLORS['green btn'].dark(),
            borderwidth=0,
            compound="center",
            command=self.controller.pages[MultiPlayer].host_game,
            highlightthickness=0
        )
        self.host_btn.place(relx=0.8, rely=0.9, anchor='center')

    def update_servers(self, servers):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.entries.clear()

        for i, server in enumerate(servers):
            btn = tk.Radiobutton(
                self.scroll_frame,
                text=f"{server['name']} ({server['address']}:{server['port']})",
                variable=self.selected_server,  # shared across all buttons
                value=i,
                font=(GAME_FONT, 16),
                fg=COLORS['yellow txt'],
                background=COLORS['background'],
                selectcolor=COLORS['background']
            )
            btn.pack(anchor='w', padx=10, pady=5)
            self.entries.append(btn)

    def get_selected_index(self):
        return self.selected_server.get()

    def back(self):
        self.controller.show_page(MainMenu)

    def quit(self):
        self.controller.quit()


class Instructions(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent, bg=COLORS['background'])

        self.controller = controller
        self.h2p_text = open('instructions.txt', 'r')
        self.top_bar = TopBar(self, "Single Player")
        self.top_bar.place(relx=0, rely=0, relwidth=1, relheight=.1)
        self.text_frame = tk.Frame(self, bg=COLORS['background'])
        self.text_frame.place(relx=0, rely=.1, relwidth=1, relheight=.9)
        self.text = tk.Label(
            self.text_frame,
            text=self.h2p_text.read(),
            wraplength=1024*.9,
            font=(GAME_FONT, 42),
            justify='left',
            fg=COLORS['yellow txt'],
            background=COLORS["background"],
        )
        self.text.place(relx=0.5, rely=0, relwidth=.9, relheight=.9, anchor='n')

    def back(self):
        self.controller.show_page(MainMenu)


class Settings(tk.Frame):
    def __init__(self, parent, size, bomb_percent, size_range, bomb_percent_range):
        super().__init__(parent, background=COLORS['background'])
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
        self.size_display.place(relx=0.05, rely=0.25, anchor='w')
        self.size_up_btn = ButtonIcon(self, 'assets/up.png',
                                      command=self.size_up)
        self.size_up_btn.place(relx=0.85, rely=0.25, anchor='s')
        self.size_down_btn = ButtonIcon(self, 'assets/down.png',
                                        command=self.size_down)
        self.size_down_btn.place(relx=0.85, rely=0.25, anchor='n')

    def create_bomb_percent_display(self):
        self.bomb_percent_display = tk.Label(
            self,
            text=f'{self.bomb_percent * 100:.0f}%',
            font=(GAME_FONT, 32),
            justify='center',
            fg=COLORS['yellow txt'],
            background=COLORS["background"],
        )
        self.bomb_percent_display.place(relx=0.05, rely=0.75, anchor='w')
        self.bomb_percent_up_btn = ButtonIcon(self, 'assets/up.png',
                                      command=self.bomb_percent_up)
        self.bomb_percent_up_btn.place(relx=0.85, rely=0.75, anchor='s')
        self.bomb_percent_down_btn = ButtonIcon(self, 'assets/down.png',
                                        command=self.bomb_percent_down)
        self.bomb_percent_down_btn.place(relx=0.85, rely=0.75, anchor='n')

    def size_up(self):
        self.size += 1
        if self.size > self.size_range[1]:
            self.size = self.size_range[0]
        self.update_settings()

    def size_down(self):
        self.size -= 1
        if self.size < self.size_range[0]: self.size = self.size_range[1]
        self.update_settings()

    def bomb_percent_up(self):
        self.bomb_percent += 0.01
        if self.bomb_percent > self.bomb_percent_range[1]: self.bomb_percent = self.bomb_percent_range[0]
        self.update_settings()

    def bomb_percent_down(self):
        self.bomb_percent -= 0.01
        if self.bomb_percent < self.bomb_percent_range[0]: self.bomb_percent = self.bomb_percent_range[1]
        self.update_settings()

    def update_settings(self):
        self.size_display.config(text=f'{self.size:02}')
        self.bomb_percent_display.config(text=f'{self.bomb_percent * 100:.0f}%')


class TopBar(tk.Frame):
    def __init__(self, parent, menu_name):
        super().__init__(parent, bg=COLORS['background'].dark())
        self.parent = parent

        # Title label
        title_text = tk.Label(
            self,
            text=menu_name,
            font=(GAME_FONT, 32),
            justify='center',
            fg=COLORS['yellow txt'],
            background=COLORS["background"].dark(),
        )
        title_text.place(relx=0.5, rely=0.5, anchor='center')

        self.back_btn = ButtonIcon(self, 'assets/left.png',
                                   command=self.parent.back)
        self.back_btn.place(relx=0.05, rely=0.5, anchor='center')

        self.quit_btn = ButtonIcon(self, 'assets/quit.png',
                                   command=self.parent.quit)
        self.quit_btn.place(relx=0.95, rely=0.5, anchor='center')


class ButtonIcon(tk.Label):
    def __init__(self, parent, image_path, command=None, scale=1.0,
                 hover_scale=1.15, click_scale=0.95):
        super().__init__(parent, bg=parent["bg"])
        self.command = command
        self.image_path = image_path
        self.scale = scale
        self.hover_scale = hover_scale
        self.click_scale = click_scale

        self.add_image()
        self.bind_button()

    def change_image(self, image_path):
        self.image_path = image_path
        self.add_image()

    def add_image(self):
        self.image = Image.open(self.image_path).convert("RGBA")
        self.tk_image = ImageTk.PhotoImage(self.scale_image(self.image, self.scale))
        self.configure(image=self.tk_image)

    def bind_button(self):
        self.bind("<Enter>", lambda event : self.update_image(self.hover_scale))
        self.bind("<Leave>", lambda event : self.update_image(self.scale))
        self.bind("<ButtonPress-1>", lambda event : self.update_image(self.click_scale))
        self.bind("<ButtonRelease-1>", self.on_release)

    def scale_image(self, image, scale):
        size = (int(image.width * scale), int(image.height * scale))
        scaled = image.resize(size, Image.BILINEAR)
        return scaled

    def update_image(self, scale):
        img = self.scale_image(self.image, scale)
        self.tk_image = ImageTk.PhotoImage(img)
        self.configure(image=self.tk_image)

    def on_release(self, event):
        self.update_image(self.hover_scale)
        if self.command:
            self.command()


if __name__ == "__main__":
    root = Game()
    root.mainloop()
