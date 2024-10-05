import tkinter as tk
import colorsys
from ctypes import windll, byref, create_unicode_buffer

GAME_FONT = "RuneScape Bold 12"
background_color = colorsys.hsv_to_rgb

class Color:
    def __init__(self, h, s, v):
        self.hue = h / 360
        self.saturation = s / 100
        self.value = v / 100

        self.rgb = colorsys.hsv_to_rgb(self.hue, self.saturation, self.value)

    def darken(self):
        pass


class Game(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.geometry("1024x768")
        self.title = 'Tic-Tac-Sweep'
        self.config(background=background_color)

        # Menu Frames
        self.main_menu = tk.Frame(
            self,
            bg=background_color,
            height=768,
            width=1024,
        )
        self.sp_menu = tk.Frame(
            self,
            bg=background_color,
            height=768,
            width=1024,
        )
        self.mp_menu = tk.Frame(
            self,
            bg=background_color,
            height=768,
            width=1024,
        )
        self.h2p_menu = tk.Frame(
            self,
            bg=background_color,
            height=768,
            width=1024,
        )
        self.profile_menu = tk.Frame(
            self,
            bg=background_color,
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
            bg="#645E5B",
        )
        title.place(x=32, y=32)
        title_text = tk.Label(
            self.main_menu,
            text="Tic-Tac-Sweep",
            font=(GAME_FONT, 52),
            justify='center',
            fg="#D8B600",
            background='#645E5B',
        )
        title_text.place(x=960/2, y=128/2, anchor='center')

        # Button Widgets
        single_player_btn = tk.Button(
            self.main_menu,
            text="Single Player",
            font=(GAME_FONT, 32),
            fg="#4E4946",
            activeforeground="#4E4946",
            background="#7EA75F",
            activebackground="#6A8A51",
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
            font=(GAME_FONT, 32),
            fg="#4E4946",
            activeforeground="#4E4946",
            background="#A77D5F",
            activebackground="#8D6950",
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
            font=(GAME_FONT, 32),
            fg="#4E4946",
            activeforeground="#4E4946",
            background="#A7A05F",
            activebackground="#968F56",
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
            font=(GAME_FONT, 32),
            fg="#4E4946",
            activeforeground="#4E4946",
            background="#AB73CD",
            activebackground="#9162AD",
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
            bg=''
        )
        information_bar.place(x=0, y=0, relheight=.1, relwidth=1)

    def load_mp_menu(self):
        pass

    def load_h2p_menu(self):
        pass

    def load_profile_menu(self):
        pass

    # Functions for displaying menu frames
    def go_main_menu(self):
        self.clear_menu()
        print("Displaying main menu...")
        self.main_menu.pack()
        print("Done!")

    def play_sp(self):
        self.clear_menu()
        print("Displaying Single Player Menu...")
        self.sp_menu.pack()
        print("Done!")

    def play_mp(self):
        pass

    def go_h2p_menu(self):
        pass

    def go_profile_menu(self):
        pass

    def clear_menu(self):
        print('Clearing screen...')
        for child in self.winfo_children():
            print(f'Destroying {child}')
            child.pack_forget()
        print("Screen cleared!")



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