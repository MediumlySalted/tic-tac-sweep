import tkinter as tk
import random
import settings
import assets
from cell import Cell
from ctypes import windll, byref, create_unicode_buffer

game_font = assets.game_font
colors = assets.colors

class Game(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.geometry("1024x768")
        self.title = 'Tic-Tac-Sweep'
        self.config(background=colors['background'])

        # Menu Frames
        self.main_menu = tk.Frame(
            self,
            bg=colors['background'],
            height=768,
            width=1024,
        )
        self.sp_menu = tk.Frame(
            self,
            bg=colors['background'],
            height=768,
            width=1024,
        )
        self.mp_menu = tk.Frame(
            self,
            bg=colors['background'],
            height=768,
            width=1024,
        )
        self.h2p_menu = tk.Frame(
            self,
            bg=colors['background'],
            height=768,
            width=1024,
        )
        self.profile_menu = tk.Frame(
            self,
            bg=colors['background'],
            height=768,
            width=1024,
        )

        self.load_all_widgets()
        self.go_main_menu()

    # Functions for building widgets
    def load_all_widgets(self):
        self.load_main_menu()
        self.load_sp_menu()

    def load_main_menu(self):
        '''
        Function to load all widgets relating to the main menu screen. 
        Contains: Title frame & text + 4 Buttons (sp, mp, h2p, profile)
        '''
        # Title Widgets
        title = tk.Frame(
            self.main_menu,
            width=960,
            height=128,
            bg=colors["background"],
        )
        title.place(x=32, y=32)
        title_text = tk.Label(
            self.main_menu,
            text="Tic-Tac-Sweep",
            font=(game_font, 52),
            justify='center',
            fg=colors['yellow txt'],
            background=colors["background"],
        )
        title_text.place(x=960/2, y=128/2, anchor='center')

        # Button Widgets
        single_player_btn = tk.Button(
            self.main_menu,
            text="Single Player",
            font=(game_font, 32),
            fg=colors["background"].dark(),
            activeforeground=colors["background"].dark(),
            background=colors['green btn'],
            activebackground=colors['green btn'].dark(),
            borderwidth=0,
            compound="center",
            command=self.play_sp
        )
        single_player_btn.place(
            x=128.0,
            y=256.0,
            width=352.0,
            height=80.0
        )

        multiplayer_btn = tk.Button(
            self.main_menu,
            text="Multi Player",
            font=(game_font, 32),
            fg=colors["background"].dark(),
            activeforeground=colors["background"].dark(),
            background=colors['red btn'],
            activebackground=colors['red btn'].dark(),
            borderwidth=0,
            compound="center",
            command=self.play_mp
        )
        multiplayer_btn.place(
            x=512,
            y=256,
            width=352,
            height=80
        )

        how_to_play_btn = tk.Button(
            self.main_menu,
            text="How to Play",
            font=(game_font, 32),
            fg=colors["background"].dark(),
            activeforeground=colors["background"].dark(),
            background=colors['yellow btn'],
            activebackground=colors['yellow btn'].dark(),
            borderwidth=0,
            compound="center",
            command=self.h2p_menu
        )
        how_to_play_btn.place(
            x=128,
            y=368,
            width=352,
            height=80
        )

        profile_btn = tk.Button(
            self.main_menu,
            text="Profile",
            font=(game_font, 32),
            fg=colors["background"].dark(),
            activeforeground=colors["background"].dark(),
            background=colors['purple btn'],
            activebackground=colors['purple btn'].dark(),
            borderwidth=0,
            compound="center",
            command=self.go_profile_menu
        )
        profile_btn.place(
            x=512,
            y=368,
            width=352,
            height=80
        )

    def load_sp_menu(self):
        '''
        Loads all single player widgets.
        Contains: Information bar
        '''
        information_bar = tk.Frame(
            self.sp_menu,
            bg=colors['background'].dark()
        )
        information_bar.place(x=0, y=0, relheight=.1, relwidth=1)

        title_text = tk.Label(
            information_bar,
            text="Single Player",
            font=(game_font, 32),
            justify='center',
            fg=colors['yellow txt'],
            background=colors["background"].dark(),
        )
        title_text.place(relx=.5, rely=.5, anchor='center')

        self.back_icon = tk.PhotoImage(file='assets/left.png')
        back_button = tk.Button(
            information_bar,
            image=self.back_icon,
            background=colors['background'].dark(),
            activebackground=colors['background'].dark(),
            borderwidth=0,
            compound="center",
            command=self.go_main_menu
        )
        back_button.place(relx=.01, rely=0.1, relheight=.8, relwidth=.05)

        self.quit_icon = tk.PhotoImage(file='assets/quit.png')
        quit_button = tk.Button(
            information_bar,
            image=self.quit_icon,
            background=colors['background'].dark(),
            activebackground=colors['background'].dark(),
            borderwidth=0,
            compound="center",
            command=self.quit
        )
        quit_button.place(relx=.925, rely=0.1, relheight=.8, relwidth=.05)

        minefield = tk.Frame(
            self.sp_menu,
            bg=colors['background'].dark(.6),
            borderwidth=5
        )
        minefield.place(
            relx=.35,
            rely=.15,
            relheight=.8,
            relwidth=.6,
        )

        self.create_minefield(minefield)

    def load_mp_menu(self):
        pass

    def load_h2p_menu(self):
        pass

    def load_profile_menu(self):
        pass

    # Functions for displaying menu frames
    def go_main_menu(self):
        self.clear_menu()
        print("\nDisplaying main menu...")
        self.main_menu.pack()
        print("Done!")

    def play_sp(self):
        self.clear_menu()
        print("\nDisplaying Single Player Menu...")
        self.sp_menu.pack()
        print("Done!")

    def play_mp(self):
        pass

    def go_h2p_menu(self):
        pass

    def go_profile_menu(self):
        pass

    def create_minefield(self, minefield_frame):
        minefield = [[] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                bomb = False
                if random.randrange(8) == 1: bomb = True
                cell = Cell(minefield_frame, bomb)
                cell.cell_btn.place(
                    relx=j/9,
                    rely=i/9,
                    relwidth=1/9,
                    relheight=1/9
                )
                minefield[i].append(cell)

    def clear_menu(self):
        print('\nClearing screen...')
        for child in self.winfo_children():
            child.pack_forget()
        print("Done!")

    def quit(self):
        print("\nExiting Game...")
        self.destroy()
        print("Done!")


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

def main():
    load_font("assets/RuneScape-Bold-12.ttf")
    root = Game()
    root.mainloop()


if __name__ == "__main__":
    main()
