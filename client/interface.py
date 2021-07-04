from tkinter import *
from functools import partial

class GameInterface:
    def __init__(self):
        self.chatFrame=None
        self.gameFrame=None
        
        self.title = 'Game, mungkin'
        self.tkWindow = Tk()
        self.tkWindow.title(self.title)
        self.tkWindow.state('zoomed')
        self.tkWindow.resizable(False, False)
        
        self.frame = Frame(self.tkWindow)
        self.frame.pack()
        
        self.state = False
        self.width= self.tkWindow.winfo_screenwidth() 
        self.height= self.tkWindow.winfo_screenheight()

        self.tkWindow.bind("<F11>", self.toggle_fullscreen)
        self.tkWindow.bind("<Escape>", self.end_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.tkWindow.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tkWindow.attributes("-fullscreen", False)
        return "break"
        
        #buat frame auth

        #game frame

    def start(self):
        self.tkWindow.mainloop()
    def set_auth_interface():
        return
    def set_chat_interface():
        return
    def set_game_interface():
        return
    def show_chat():
        return
    def show_image():
        return
    def show_message():
        return
    def show_friends():
        return
    def clear_message():
        return
    def show_alert():
        return
    def show_lie_modal():
        return
    def show_waiting_modal():
        return
    def show_rooms():
        return
    def show_game_room():
        return
    def show_grid():
        return
    def place_ship():
        return
    def show_shot_alert():
        return
    def update():
        return

if __name__ == '__main__':
    w = GameInterface()
    w.tkWindow.mainloop()