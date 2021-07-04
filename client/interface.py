from tkinter import *
from functools import partial

class GameInterface:
    def __init__(self, chat):
        self.title = 'Game, mungkin'
        self.state = False
        self.chat = chat

        self.tkWindow = Tk()
        self.tkWindow.title(self.title)
        self.tkWindow.state('zoomed')
        self.tkWindow.resizable(False, False)
        self.tkWindow.bind("<F11>", self.toggle_fullscreen)
        self.tkWindow.bind("<Escape>", self.end_fullscreen)
        
        self.frame = Frame(self.tkWindow)
        self.frame.pack()
        
        self.width= self.tkWindow.winfo_screenwidth() 
        self.height= self.tkWindow.winfo_screenheight()

        self.main_frame = Frame(self.tkWindow, bg="grey", width=self.width)
        self.chat_frame = Frame(self.main_frame, bg="grey", width=self.width/4)
        self.game_frame = Frame(self.main_frame, bg="grey", width=self.width/4*3)
        self.auth_frame = Frame(self.tkWindow, bg="grey", width=self.width)

        self.current_frame = self.auth_frame
        self.set_auth_interface()


    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.tkWindow.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tkWindow.attributes("-fullscreen", False)
        return "break"

    def set_auth_interface(self):
        self.forget_current_frame()
        self.current_frame = self.auth_frame
        button = Button(self.auth_frame, text="ke main frame", command=self.set_main_interface)
        button.pack()
        self.auth_frame.pack(fill= BOTH, expand=True)
        
    def set_main_interface(self):
        self.forget_current_frame()
        self.current_frame = self.main_frame
        self.game_frame.pack(side=LEFT, fill= BOTH, expand=True)
        self.chat_frame.pack(side=LEFT, fill= BOTH, expand=True)
        button = Button(self.game_frame, text="ke auth frame", command=self.set_auth_interface)
        button.pack()
        self.main_frame.pack(fill= BOTH, expand=True)
        
    def forget_current_frame(self):
        for widgets in self.current_frame.winfo_children():
            if widgets == self.chat_frame or widgets == self.game_frame:
                for widget in widgets.winfo_children():
                    widget.destroy()
                continue
            widgets.destroy()
        self.current_frame.pack_forget()

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