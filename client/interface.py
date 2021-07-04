from tkinter import *
from tkinter import font
from functools import WRAPPER_ASSIGNMENTS, partial
import os

class GameInterface:
    def __init__(self, chat):
        self.title = 'Game, mungkin'
        self.state = False
        self.chat = chat
        # self.chat.welcome_page()

        self.tkWindow = Tk()
        self.tkWindow.title(self.title)
        if os.name == 'nt':
            self.tkWindow.state('zoomed')
        else:
            self.tkWindow.attributes('-zoomed', True)

        self.tkWindow.resizable(False, False)
        self.tkWindow.bind("<F11>", self.toggle_fullscreen)
        self.tkWindow.bind("<Escape>", self.end_fullscreen)
        
        self.frame = Frame(self.tkWindow)
        self.frame.pack(side=TOP)

        self.special_button = Button(self.frame, text="Home", command=self.set_auth_interface)
        self.special_button.pack()
        
        self.tkWindow.update()
        self.width= self.tkWindow.winfo_width()
        self.height= self.tkWindow.winfo_height()

        self.main_frame = Frame(self.tkWindow, bg="green", width=self.width)
        self.main_frame.update()
        self.game_frame = Frame(self.main_frame, bg="black")
        self.chat_frame = Frame(self.main_frame, bg="red")
        self.auth_frame = Frame(self.tkWindow, bg="grey", width=self.width)

        self.chat_text = None

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
        button_main = Button(self.auth_frame, text="ke main frame", command=self.set_main_interface)
        button_register = Button(self.auth_frame, text="Register", command=self.set_register_interface)
        button_login = Button(self.auth_frame, text="Login", command=self.set_login_interface)
        button_main.pack()
        button_register.pack()
        button_login.pack()
        self.auth_frame.pack(fill= BOTH, expand=True)
        
    def set_main_interface(self):
        self.forget_current_frame()
        self.current_frame = self.main_frame

        self.current_frame.columnconfigure(0, weight=4)
        self.current_frame.columnconfigure(1, weight=1)
        self.current_frame.rowconfigure(0, weight=1)
        self.game_frame.grid(row=0, column=0, sticky="nsew")
        self.chat_frame.grid(row=0, column=1, sticky="nsew")

        self.show_chat_interface(self.chat_frame)

        button_auth = Button(self.game_frame, text="ke auth frame", command=self.set_auth_interface)
        button_auth.pack()

        self.main_frame.pack(fill= BOTH, expand=True)

    def set_register_interface(self):
        self.forget_current_frame()
        register_frame = Frame(self.tkWindow, bg="grey", width=self.width)
        self.current_frame = register_frame
        register_frame.pack(fill= BOTH, expand=True)
        #label
        register_label = Label(register_frame, text="Register")
        register_label.grid(column=0,row=0)
        #username
        username_label = Label(register_frame, text="Username")
        username_label.grid(column=0,row=1)
        username_entry = Entry(register_frame, bd=5)
        username_entry.grid(column=1,row=1)
        #name
        name_label = Label(register_frame, text="Nama")
        name_label.grid(column=0,row=2)
        name_entry = Entry(register_frame, bd=5)
        name_entry.grid(column=1,row=2)
        #password
        password_label = Label(register_frame, text="Password")
        password_label.grid(column=0,row=3)
        password_entry = Entry(register_frame, bd=5, show="*")
        password_entry.grid(column=1,row=3)
        #button
        submit_button = Button(register_frame, text="Submit")
        submit_button.grid(column=0, row=4)

    def set_login_interface(self):
        self.forget_current_frame()
        login_frame = Frame(self.tkWindow, bg="grey", width=self.width)
        self.current_frame = login_frame
        login_frame.pack(fill= BOTH, expand=True)
        #label
        login_label = Label(login_frame, text="login")
        login_label.grid(column=0,row=0)
        #username
        username_label = Label(login_frame, text="Username")
        username_label.grid(column=0,row=1)
        username_entry = Entry(login_frame, bd=5)
        username_entry.grid(column=1,row=1)
        #name
        name_label = Label(login_frame, text="Nama")
        name_label.grid(column=0,row=2)
        name_entry = Entry(login_frame, bd=5)
        name_entry.grid(column=1,row=2)
        #password
        password_label = Label(login_frame, text="Password")
        password_label.grid(column=0,row=3)
        password_entry = Entry(login_frame, bd=5, show="*")
        password_entry.grid(column=1,row=3)
        #button
        submit_button = Button(login_frame, text="Submit")
        submit_button.grid(column=0, row=4)

        
    def forget_current_frame(self):
        for widgets in self.current_frame.winfo_children():
            if widgets == self.chat_frame or widgets == self.game_frame:
                for widget in widgets.winfo_children():
                    widget.destroy()
                continue
            widgets.destroy()
        try:
            self.current_frame.pack_forget()
        except Exception:
            self.current_frame.grid_forget()

    def show_chat_interface(self, parent_frame):
        frame = Frame(parent_frame, bg="grey")
        frame.pack(fill=BOTH, expand=True)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=4)
        frame.rowconfigure(1, weight=1)

        message_frame = Frame(frame)
        message_frame.grid(row=0, column=0, padx=0)

        message_label = Label(message_frame, text="Chat", font=font.Font(size=16, weight='bold'))
        message_label.pack()
        scrollbar = Scrollbar(message_frame)
        scrollbar.pack( side = RIGHT, fill = Y )

        mylist = Text(message_frame, yscrollcommand = scrollbar.set, wrap=WORD, width=35, height=40, bd=5)
        for line in range(100):
            mylist.insert(END, "This is line numberadfadfasdf " + str(line) + "\n")

        mylist.pack(side=LEFT, fill= BOTH, expand=True)
        scrollbar.config( command = mylist.yview )
        
        #input frame
        input_frame = Frame(frame)
        input_frame.grid(row=1, column=0, padx=0)
        input_frame.columnconfigure(0, weight=3)
        input_frame.columnconfigure(1, weight=1)
            #entry  #button
        entry = Entry(input_frame, bd=5)
        entry.grid(row=0, column=0)
        button = Button(input_frame, text="Send", command=partial(
            self.new_line,
            mylist
        ))
        button.grid(row=0, column=1)

    def new_line(self, mylist):
        mylist.insert(END, "newlinenewlinenewlinenewlinenewlinenewlinenewline\n")
        mylist.yview(END)

    def show_chat(self):
        return
    def show_image(self):
        return
    def show_message(self):
        return
    def show_friends(self):
        return
    def clear_message(self):
        return
    def show_alert(self):
        return
    def show_lie_modal(self):
        return
    def show_waiting_modal(self):
        return
    def show_rooms(self):
        return
    def show_game_room(self):
        return
    def show_grid(self):
        return
    def place_ship(self):
        return
    def show_shot_alert(self):
        return
    def update(self):
        return

if __name__ == '__main__':
    chat = 'hehe'
    w = GameInterface(chat)
    w.tkWindow.mainloop()        