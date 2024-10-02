from tkinter import Tk, Button, Label, Frame
from ctypes import windll, byref, create_unicode_buffer

def loadfont(font_path):
    '''
    Makes custom fonts available to the font system as a private
    resource for the application to use.

    font_path (str): file directory for the font. Ex: 'foldername/filename.ttf'
    '''
    if not isinstance(font_path, str):
        raise ValueError("font_path needs to be a string. Ex: 'foldername/filename.ttf'")
    
    path_buffer = create_unicode_buffer(font_path)
    windll.gdi32.AddFontResourceExW(byref(path_buffer), 0x10, 0)


def clear_screen():
    print('Clearing screen...')
    for widget in window.winfo_children():
        widget.destroy()
    print("Screen cleared!")


def go_single_player():
    print("Starting single player..")
    single_player_menu.place(x=0, y=0)
    print("Single player started!")


def go_main_menu():
    print("Going to main menu...")
    main_menu.place(x=0, y=0)
    print("Welcome to Tic Tac Sweep!")



# Main Screen Set-up
root = Tk()
root.geometry("1024x768")
root.title("Tic-Tac-Sweep")
window = Frame(
    root,
    bg = "#645E5B",
    height = 768,
    width = 1024,
)
window.pack()


# Main menu set-up
main_menu = Frame(
    window,
    bg = "#645E5B",
    height = 768,
    width = 1024,
)

title = Frame(
    main_menu,
    width=960,
    height=128,
    bg="#645E5B",
)
title.place(x=32, y=32)

title_text = Label(
    title,
    text="Tic-Tac-Sweep",
    font=(("RuneScape Bold 12"), 52),
    justify='center',
    fg="#D8B600",
    background='#645E5B',
)
title_text.place(x=960/2, y=128/2, anchor='center')

single_player_btn = Button(
    main_menu,
    text="Single Player",
    font=("RuneScape Bold 12", 32),
    fg="#4E4946",
    activeforeground="#4E4946",
    background="#7EA75F",
    activebackground="#6A8A51",
    borderwidth=0,
    compound="center",
    command=go_single_player
)
single_player_btn.place(
    x=128.0,
    y=256.0,
    width=352.0,
    height=80.0
)

multiplayer_btn = Button(
    main_menu,
    text="Multi Player",
    font=("RuneScape Bold 12", 32),
    fg="#4E4946",
    activeforeground="#4E4946",
    background="#A77D5F",
    activebackground="#8D6950",
    borderwidth=0,
    compound="center",
)
multiplayer_btn.place(
    x=512,
    y=256,
    width=352,
    height=80
)

how_to_play_btn = Button(
    main_menu,
    text="How to Play",
    font=("RuneScape Bold 12", 32),
    fg="#4E4946",
    activeforeground="#4E4946",
    background="#A7A05F",
    activebackground="#968F56",
    borderwidth=0,
    compound="center",
)
how_to_play_btn.place(
    x=128,
    y=368,
    width=352,
    height=80
)

profile_btn = Button(
    main_menu,
    text="Profile",
    font=("RuneScape Bold 12", 32),
    fg="#4E4946",
    activeforeground="#4E4946",
    background="#AB73CD",
    activebackground="#9162AD",
    borderwidth=0,
    compound="center",
)
profile_btn.place(
    x=512,
    y=368,
    width=352,
    height=80
)


# Single player set-up
single_player_menu = Frame(
    window,
    bg = "#645E5B",
    height = 768,
    width = 1024,
)


main_menu_btn = Button(

)

go_main_menu()


root.resizable(False, False)
root.mainloop()
