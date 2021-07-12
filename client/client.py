import socket
import sys
import threading
import os
import pickle
import ntpath
from getpass import getpass
from tkinter import Tk # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import GameMain

buff_size = 65535
HOST = '127.0.0.1'
PORT = 5000

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect((HOST, PORT))
game = None
    
class Account:
    def __init__ (self, id, name, password):
        self.id = id
        self.name = name
        self.password = password
        self.friend = set()

def clear(args):
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def header_page():
    clear('')
    print('Welcome to Esaiyy Play')
    print('==============================')

def get_request_header(requestType, lenRequest):
    header = b''
    header += requestType.encode('utf-8') + b'\n'
    header += str(lenRequest).encode('utf-8') + b'\n'
    return header

def parseRequest(request):
    splitRequest = (request.split(b'\n', 2))
    requestType = splitRequest[0].decode('utf-8')
    lenData = int(splitRequest[1].decode('utf-8'))
    data = splitRequest[2]
    return requestType, lenData, data

def helper(args):
    print('''Manual for Esaiyy Play\nCommand:
    help - show all command available
    add - add user to friend list
        add [user] - add user to your friend
    friend - show my friend list
    chat - chat to specific user or broadcast
        chat [user] - chat to account user
        chat [bcast] - broadcast chat
    send - send a file
        send [user] - send a file to use
    game - play a battlefield game
        game [create] - create a game room
        game [join] [roomNo] - join to game specific room number
        
    ''')
    return

def friendlist(args):
    dataRequest = pickle.dumps(tuple())
    headerRequest = get_request_header('friendlist', len(dataRequest))
    socket_client.send(headerRequest + dataRequest)
    return

def chat(args):
    data = dict()

    data[0] = args[1] if len(args) > 1 else input('<App>: Send to (use [user_id] or bcast) :\n')
    data[1] = input('<App>: Type your message :\n')

    dataRequest = pickle.dumps((data,))
    headerRequest = get_request_header('chat', len(dataRequest))
    socket_client.send(headerRequest + dataRequest)    
    return

def addfriend(args):
    user_id = args[1] if len(args) > 1 else input('<App>: Add Friend ID :\n')
    dataRequest = pickle.dumps((user_id, ))
    headerRequest = get_request_header('addfriend', len(dataRequest))
    socket_client.send(headerRequest + dataRequest)  
    return

def sendfile(args):
    user_id = args[1] if len(args) > 1 else input('<App>: Send to : (user_id)\n')

    Tk().withdraw()
    filepath = askopenfilename()
    if filepath:
        f = open(filepath, 'rb')
        filename = ntpath.basename(filepath)
        data = f.read()

        dataRequest = pickle.dumps((user_id, filename, data))
        # print(dataRequest)
        headerRequest = get_request_header('sendfile', len(dataRequest))
        socket_client.sendall(headerRequest + dataRequest)
    
    return

def playgame(args):
    # print(roomStatus)
    roomCommand = args[1] if len(args) > 1 else input('<App>: Create or Join room? (create|join)\n')
    if(roomCommand == 'create'):
        dataRequest = pickle.dumps(tuple())
        headerRequest = get_request_header('createRoom', len(dataRequest))
        socket_client.sendall(headerRequest + dataRequest)
    elif (roomCommand == 'join'):
        roomId = args[2] if len(args) > 2 else input('<App>: Input room id:\n')
        dataRequest = pickle.dumps((roomId,))
        headerRequest = get_request_header('joinRoom', len(dataRequest))
        socket_client.sendall(headerRequest + dataRequest)
    return

def commandError(args):
    print('<App>: Command Not Found')

def commandSwitch(args):
    commandAvailable = {
        'help' : helper,
        'friend' : friendlist,
        'add' : addfriend,
        'chat' : chat,
        'send' : sendfile,
        'clear' : clear,
        'game' : playgame,
    }
    args = args.split(' ')
    # args = [''] if len(args) == 0 else args
    commandAvailable.get(args[0], commandError)(args)

def read_message(myaccount):
    while True:
        response = socket_client.recv(buff_size)
        responseType, lenData, data = parseRequest(response)
        # print(responseType)
        dataRemain = lenData - len(data)
        while dataRemain > 0:
            response = socket_client.recv(buff_size)
            data += response
            dataRemain -= len(response)

        data = pickle.loads(data)

        if responseType == 'addfriend':
            if data[1] == 'success':
                print('<App>: {} now added to your friend list'.format(data[2].id))
            else:
                print('<App>: Cannot add user!')
            print()

        elif responseType == 'friendlist':
            print('<App>:\n== Your Friend ==')
            if data[1]:
                for idx, user in enumerate(data[1]):
                    print('  {}. {}'.format(idx + 1, user))
            else:
                print('No one in your friend list') 
            print()             
        
        elif responseType == 'chat':
            if data[1] == 'failed':
                print("<App>: {}".format(data[2]))
            else:
                senderid, sendername, message = data[2]
                print("<{}> {}: {}".format(senderid, sendername, message))
            print()

        elif responseType == 'sendfile':
            if data[1] == 'failed':
                print("<App>: {}".format(data[2]))
            else:
                senderid, sendername, filename, filedata = data[2]
                print("<App>: <{}> {} send you a file ".format(senderid, sendername))
                
                dir = os.listdir(os.getcwd())
                if not(myaccount.id in dir):
                    os.mkdir(myaccount.id)

                f = open(myaccount.id + '/' + filename, 'wb')
                f.write(filedata)
                f.close()                
            print()

        elif responseType == 'createRoom':
            if data[1] == 'failed':
                print("<App>: {}".format(data[2]))
            else:
                print("<App>: {}".format(data[2]))
                hehe = True
        
        elif responseType == 'joinRoom':
            if data[1] == 'failed':
                print("<App>: {}".format(data[2]))
            else:
                print("<App>: {}".format(data[2]))
                room = 1

        elif responseType == 'play':
            game = GameMain.Game(socket_client, myaccount.id)
            game.start()

        elif responseType == 'updateBoard':
            if data[1] == 'atk':
                game.updateAtkBoard(data[2])
            else:
                game.updateDefBoard(data[2])

        elif responseType == 'stop':
            game.setAttackTime(False)
            game.join()
            print('<App>: {} Win the game'.format(data[1]))
            if(data[1] != myaccount.id):
                print('You Lose')
            print()

def dasboard(status, myAccount):
    header_page()
    print(status, end='')
    print('Hello, ' + myAccount.name + '\n')
    print('Type "help" to see all available command \n')
    
    thread = threading.Thread(target=read_message, args=(myAccount,))
    thread.daemon = True
    thread.start()

    try:
        while True:
            command = input()
            commandSwitch(command)
    except KeyboardInterrupt:
        socket_client.close()
        sys.exit()

def register(status):
    try:
        header_page()
        print('Register an account\n')
        print(status, end='')

        id = input('Enter username: ')
        name = input('Enter your name: ')
        password = getpass('Enter password: ')
        newAccount = Account(id, name, password)


        dataRequest = pickle.dumps((newAccount,))
        headerRequest = get_request_header('register', len(dataRequest))

        socket_client.send(headerRequest + dataRequest)
        response = socket_client.recv(buff_size)
        response = pickle.loads(response)

        if response[0] == 'failed':
            register('Account is already Exist\n')
        else:
            dasboard('Account Created, you\'re login now\n', response[1])
        return
    except KeyboardInterrupt:
        return welcome_page()

def login(status):
    try:
        header_page()
        print('Login to chat\n')
        print(status, end='')

        id = input('Enter username: ')
        password = getpass('Enter password: ')

        dataRequest = pickle.dumps((id, password))
        headerRequest = get_request_header('login', len(dataRequest))

        socket_client.send(headerRequest + dataRequest)
        response = socket_client.recv(buff_size)
        response = pickle.loads(response)

        if response[0] == 'failed':
            login('Login Failed, please check your credential\n')
        else:
            dasboard('Login success\n', response[1])
        return
    except KeyboardInterrupt:
        return welcome_page()
        
def welcome_page():
    try:
        header_page()
        status = ''
        islogin = input('Have an account? (y/n) : ')
        if islogin == 'n':
            register(status)
        elif islogin == 'y':
            login(status)
        else:
            print('Byee!!')
    except KeyboardInterrupt:
        sys.exit()

def main():  
    welcome_page()

if __name__ == '__main__':
    main()