from interface import GameInterface
from client_chat import Chat

if __name__ == '__main__':
    chat = Chat()
    w = GameInterface(chat)
    w.tkWindow.mainloop()