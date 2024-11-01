import tkinter as tk
from ctypes import windll, byref, create_unicode_buffer
from minesweeper import Minefield
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
        for F in (MainMenu, SPMenu):
            frame = F(game_frame, self)
            self.pages[F] = frame 
            frame.place(x=0, y=0, width=1024, height=786) 

        self.show_page(MainMenu)

    # Displays the current page
    def show_page(self, page_class):
        print(f"\nDisplaying {page_class.__name__} page")
        page = self.pages[page_class]
        page.tkraise()
    
    def quit(self):
        print("\nExiting Game...")
        self.destroy()
        print("Done!")


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

        # TOP BAR ELEMENTS
        self.top_bar = tk.Frame(
            self,
            bg=COLORS['background'].dark()
        )
        self.top_bar.place(relx=0, rely=0, relwidth=1, relheight=.1)

        title_text = tk.Label(
            self.top_bar,
            text="Single Player",
            font=(GAME_FONT, 32),
            justify='center',
            fg=COLORS['yellow txt'],
            background=COLORS["background"].dark(),
        )
        title_text.place(relx=.5, rely=.5, anchor='center')

        self.back_icon = tk.PhotoImage(file='assets/left.png')
        self.back_btn = tk.Button(
            self.top_bar,
            image=self.back_icon,
            background=COLORS['background'].dark(),
            activebackground=COLORS['background'].dark(),
            borderwidth=0,
            compound="center",
            command=self.back
        )
        self.back_btn.place(relx=.025, rely=0.5, anchor='w')

        self.quit_icon = tk.PhotoImage(file='assets/quit.png')
        self.quit_btn = tk.Button(
            self.top_bar,
            image=self.quit_icon,
            background=COLORS['background'].dark(),
            activebackground=COLORS['background'].dark(),
            borderwidth=0,
            compound="center",
            command=self.controller.quit
        )
        self.quit_btn.place(relx=.975, rely=0.5, anchor='e')

        self.side_bar = tk.Frame(
            self,
            background=COLORS['background'].dark()
        )
        self.side_bar.place(relx=.05, rely=.15, relwidth=.25, relheight=.8)

        self.start_icon = tk.PhotoImage(file='assets/start.png')
        self.start_btn = tk.Button(
            self.side_bar,
            image=self.start_icon,
            background=COLORS['background'].dark(),
            activebackground=COLORS['background'].dark(),
            borderwidth=0,
            compound="center",
            command=self.start_game
        )
        self.start_btn.place(relx=.95, rely=.05, anchor='ne')

        self.stop_icon = tk.PhotoImage(file='assets/stop.png')
        self.stop_btn = tk.Button(
            self.side_bar,
            image=self.stop_icon,
            background=COLORS['background'].dark(),
            activebackground=COLORS['background'].dark(),
            borderwidth=0,
            compound="center",
            command=self.end_game
        )
        self.stop_btn.place(relx=.025, rely=.05, anchor='nw')

        self.timer_frame = tk.Frame(
            self.side_bar,
            bg=COLORS['background'],
        )
        self.timer_frame.place(relx=.5, rely=.025, relwidth=.65, relheight=.1, anchor='n')

        self.timer = tk.Label(
            self.timer_frame,
            text='00:00.0',
            font=(GAME_FONT, 32),
            justify='center',
            fg=COLORS['yellow txt'],
            background=COLORS["background"],
        )
        self.timer.place(relx=.05, rely=.5, anchor='w')
        
        self.minefield_frame = tk.Frame(
            self,
            bg=COLORS['background'].dark(.6),
            borderwidth=5
        )
        self.minefield_frame.place(relx=.35, rely=.15, relwidth=.6, relheight=.8)

    def start_game(self):
        self.start_btn.configure(state='disabled')
        self.time = 0
        self.game = Minefield(self.minefield_frame)
        self.game.create_minefield()
        self.controller.after(100, self.update_timer)

    def end_game(self):
        print("\nEnding Game...")
        self.start_btn.configure(state='active')
        self.game.game_over = True
        self.reset_timer()
        for widget in self.minefield_frame.winfo_children():
            widget.destroy()
        print("Done!")

    def update_timer(self):
        self.time += 1
        self.timer.configure(text=f'{self.time // 600:02}:{(self.time // 10) % 60:02}.{self.time % 10}')
        if not self.game.game_over: self.controller.after(100, self.update_timer)

    def reset_timer(self):
        self.controller.after(100, lambda: self.timer.configure(text=f'00:00.0'))

    def back(self):
        self.end_game()
        self.controller.show_page(MainMenu)


class MPMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


class H2PMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


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
