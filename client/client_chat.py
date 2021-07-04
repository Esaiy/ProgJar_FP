import socket
import sys
import threading
import os
import pickle
import ntpath
import xmlrpc
from getpass import getpass
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from client_account import Account

class Chat:
    def __init__(self):
        self.buff_size = 65535
        self.HOST = '127.0.0.1'
        self.PORT = 5000

        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((self.HOST, self.PORT))

    def clear(args):
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')

    def header_page(self):
        self.clear()
        print('Welcome to Esaiyy Chat')
        print('==============================')

    def get_request_header(self, requestType, lenRequest):
        header = b''
        header += requestType.encode('utf-8') + b'\n'
        header += str(lenRequest).encode('utf-8') + b'\n'
        return header

    def helper(self, args):
        print('''Manual for Esaiyy Chat\nCommand:
        help - show all command available
        add - add user to friend list
            add [user] - add user to your friend
        friend - show my friend list
        chat - chat to specific user or broadcast
            chat [user] - chat to account user
            chat [bcast] - broadcast chat
        send - send a file to friend
        ''')
        return

    def friend_list(self, args):
        dataRequest = pickle.dumps(tuple())
        headerRequest = self.get_request_header('friend_list', len(dataRequest))
        self.socket_client.send(headerRequest + dataRequest)
        return

    def chat(self, args):
        data = dict()

        data[0] = args[1] if len(args) > 1 else input('<App>: Send to (use [user_id] or bcast) :\n')
        data[1] = input('<App>: Type your message :\n')

        dataRequest = pickle.dumps((data,))
        headerRequest = self.get_request_header('chat', len(dataRequest))
        self.socket_client.send(headerRequest + dataRequest)    
        return

    def add_friend(self, args):
        user_id = args[1] if len(args) > 1 else input('<App>: Add Friend ID :\n')
        dataRequest = pickle.dumps((user_id, ))
        headerRequest = self.get_request_header('add_friend', len(dataRequest))
        self.socket_client.send(headerRequest + dataRequest)  
        return

    def send_file(self, args):
        user_id = args[1] if len(args) > 1 else input('<App>: Send to : (user_id)\n')

        Tk().withdraw()
        filepath = askopenfilename()
        f = open(filepath, 'rb')
        filename = ntpath.basename(filepath)
        data = f.read()

        dataRequest = pickle.dumps((user_id, filename, data))
        print(dataRequest)
        headerRequest = self.get_request_header('send_file', len(dataRequest))
        self.socket_client.sendall(headerRequest + dataRequest)
        return

    def command_error(self, args):
        print('<App>: Command Not Found')

    def command_switch(self, args):
        commandAvailable = {
            'help' : self.helper,
            'friend' : self.friend_list,
            'add' : self.add_friend,
            'chat' : self.chat,
            'send' : self.send_file,
            'clear' : self.clear
        }
        args = args.split(' ')
        # args = [''] if len(args) == 0 else args
        commandAvailable.get(args[0], self.command_error)(args)

    def read_message(self):
        while True:
            response = self.socket_client.recv(self.buff_size)
            response = pickle.loads(response)

            if response[0] == 'add_friend':
                if response[1] == 'success':
                    print('<App>: {} now added to your friend list'.format(response[2].id))
                else:
                    print('<App>: Cannot add user!')
                print()

            elif response[0] == 'friend_list':
                print('<App>:\n== Your Friend ==')
                if response[1]:
                    for idx, user in enumerate(response[1]):
                        print('  {}. {}'.format(idx + 1, user))
                else:
                    print('No one in your friend list') 
                print()             
            
            elif response[0] == 'chat':
                if response[1] == 'failed':
                    print("<App>: {}".format(response[2]))
                else:
                    senderid, sendername, message = response[2]
                    print("<{}> {}: {}".format(senderid, sendername, message))
                print()

    def dasboard(self, status, myAccount):
        self.header_page()
        print(status, end='')
        print('Hello, ' + myAccount.name + '\n')
        print('Type "help" to see all available command \n')
        
        thread = threading.Thread(target=self.read_message)
        thread.daemon = True
        thread.start()

        try:
            while True:
                command = input()
                self.command_switch(command)
        except KeyboardInterrupt:
            self.socket_client.close()
            sys.exit()

    def register(self, status):
        try:
            self.header_page()
            print('Register an account\n')
            print(status, end='')

            id = input('Enter username: ')
            name = input('Enter your name: ')
            password = getpass('Enter password: ')
            newAccount = Account(id, name, password)

            dataRequest = pickle.dumps((newAccount,))
            headerRequest = self.get_request_header('register', len(dataRequest))

            self.socket_client.send(headerRequest + dataRequest)
            response = self.socket_client.recv(self.buff_size)
            response = pickle.loads(response)

            if response[0] == 'failed':
                self.register('Account is already Exist\n')
            else:
                self.dasboard('Account Created, you\'re login now\n', response[1])
            return
        except KeyboardInterrupt:
            return self.welcome_page()

    def login(self, status):
        try:
            self.header_page()
            print('Login to chat\n')
            print(status, end='')

            id = input('Enter username: ')
            password = getpass('Enter password: ')

            dataRequest = pickle.dumps((id, password))
            headerRequest = self.get_request_header('login', len(dataRequest))

            self.socket_client.send(headerRequest + dataRequest)
            response = self.socket_client.recv(self.buff_size)
            response = pickle.loads(response)

            if response[0] == 'failed':
                self.login('Login Failed, please check your credential\n')
            else:
                self.dasboard('Login success\n', response[1])
            return
        except KeyboardInterrupt:
            return self.welcome_page()
            
    def welcome_page(self):
        try:
            self.header_page()
            status = ''
            islogin = input('Have an account? (y/n) : ')
            if islogin == 'n':
                self.register(status)
            elif islogin == 'y':
                self.login(status)
            else:
                print('Byee!!')
        except KeyboardInterrupt:
            sys.exit()
