import socket
import pickle
from sys import platform
import threading
import random

from pygame.event import peek

buff_size = 65535
HOST = '0.0.0.0'
PORT = 5000
clients = {}

class AccountManager():
    def __init__ (self):
        self.account = {}
        self.online = {}
    def check_account(self, id):
        return self.account.get(id, None)

    def add_account(self, account):
        check = self.check_account(account.id)
        if check == None:
            self.account[account.id] = account
            return self.account[account.id]
        else:
            return None

    def check_online(self, account):
        if type(account) == Account:
            return self.online.get(account.id, None)
        elif type(account) == str:
            return self.online.get(account, None)
        
    def add_online(self, account, socket_client, address_client):
        if not(self.check_online(account)):
            self.online[account.id] = (socket_client, address_client)
            return account
        return None
        
    def set_disconnected(self, account):
        print("Account " + account.id + " disconnected")
        del self.online[account.id]

class RoomManager():
    def __init__(self):
        self.room = {}
        self.gameManager = {}
    def create_room(self, account):
        while True:
            id = random.randint(10000,99999)
            if self.room.get(id, None) == None:
                self.room[id] = [account]
                break
        print(id)
        return id
    def join_room(self, account, id):
        print(type(id))
        print(self.room)
        print(self.room.get(id))
        if self.room.get(id):
            if len(self.room[id]) == 2:
                return 'failed'
            self.room[id].append(account)
            self.playgame(id)
            return 'success'
        else:
            return 'failed'
    def playgame(self, id):
        self.gameManager[id] = GameManager(self.room[id])
        return
    def finished(self, id):
        del self.gameManager[id]
        del self.room[id]

class GameManager():
    def __init__(self, room):
        self.room = room
        self.player1 = (room[0], accountManager.check_online(room[0])[0])
        self.player2 = (room[1], accountManager.check_online(room[1])[0])
    def sendPlay(self):
        response = dict()
        responseData = pickle.dumps(response)
        responseHeader = get_response_header('play', len(responseData))
        self.player1[1].sendall(responseHeader + responseData)
        self.player2[1].sendall(responseHeader + responseData)
        return
    def defBoard(self, account, board):
        print(board)
        if account == self.room[0]:
            self.board1 = board
            self.counter1 = 14
        else:
            self.board2 = board
            self.counter2 = 14
    def atkBoard(self, account, row, col):
        if account == self.room[0]:
            if self.board2[row][col] < 2:
                self.counter2 -= self.board2[row][col] 
                self.board2[row][col] += 2
                self.sendBoard(self.player2[1], self.board2, 'def')
                self.sendBoard(self.player1[1], self.board2, 'atk')  
            if self.counter2 == 0:
                self.sendResult(self.player1[0])
                
        else:
            if self.board1[row][col] < 2:
                self.counter1 -= self.board2[row][col] 
                self.board1[row][col] += 2
                self.sendBoard(self.player1[1], self.board1, 'def')
                self.sendBoard(self.player2[1], self.board1, 'atk')  
            if self.counter1 == 0:
                self.sendResult(self.player2[0])

    def sendBoard(self, socket_cli, board, status):
        response = dict()
        response[1] = status
        response[2] = board
        responseData = pickle.dumps(response)
        responseHeader = get_response_header('updateBoard', len(responseData))
        socket_cli.sendall(responseHeader + responseData)
    
    def sendResult(self, winner):
        response = dict()
        response[1] = winner.id
        responseData = pickle.dumps(response)
        responseHeader = get_response_header('stop', len(responseData))
        self.player1[1].sendall(responseHeader + responseData)
        self.player2[1].sendall(responseHeader + responseData)

            
class Account():
    def __init__ (self, id, name, password):
        self.id = id
        self.name = name
        self.password = password
        self.friend = set()
    def get_friendlist(self):
        return self.friend
    def check_friend(self, account):
        return account in self.friend

def get_response_header(requestType, lenRequest):
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

def commandHandler(socket_client, address_client):
    currentAccount = None
    myRoom = None
    while True:
        request = socket_client.recv(buff_size)
        if request:
            requestType, lenData, data = parseRequest(request)
            # print(requestType, lenData)
            dataRemain = lenData - len(data)
            
            while dataRemain > 0:
                request = socket_client.recv(buff_size)
                data += request
                dataRemain -= len(request)

            data = pickle.loads(data)

            if requestType == 'register' :
                currentAccount = accountManager.add_account(data[0])
                response = dict()
                if currentAccount:
                    response[0] = 'success'
                    response[1] = currentAccount
                    print("user {} has been created".format(currentAccount.id))
                    accountManager.add_online(currentAccount, socket_client, address_client)
                else:
                    response[0] = 'failed'
                socket_client.send(pickle.dumps(response))
                
            elif requestType == 'login' :
                currentAccount = accountManager.check_account(data[0])
                response = dict()
                if currentAccount and not(accountManager.check_online(currentAccount)) and data[1] == currentAccount.password:
                    response[0] = 'success'
                    response[1] = currentAccount
                    print("{} is online".format(currentAccount.id))
                    accountManager.add_online(currentAccount, socket_client, address_client)
                else:
                    response[0] = 'failed'
                    print("Failed login for user {}".format(data[0]))
                    currentAccount = None    
                socket_client.send(pickle.dumps(response))

            elif requestType == 'friendlist':
                response = dict()
                response[1] = currentAccount.get_friendlist()
                responseData = pickle.dumps(response)
                responseHeader = get_response_header(requestType, len(responseData))
                print('Request friend list for user {}'.format(currentAccount.id))
                print(responseHeader + responseData)
                socket_client.sendall(responseHeader + responseData)

            elif requestType == 'addfriend':
                userTarget = accountManager.check_account(data[0])
                response = dict()
           
                if userTarget and not(userTarget == currentAccount):
                    currentAccount.friend.add(userTarget.id)
                    response[1] = 'success'
                    response[2] = userTarget
                else:
                    response[1] = 'failed'

                responseData = pickle.dumps(response)
                responseHeader = get_response_header(requestType, len(responseData))
                socket_client.sendall(responseHeader + responseData)

            elif requestType == 'chat' :
                requestData = data[0]
                destination = requestData[0]
                message = requestData[1]
                
                response = dict()
                if destination == 'bcast' : 
                    send_broadcast(currentAccount, message, socket_client)
                else:
                    send_message(currentAccount, destination, message, socket_client) 
            
            elif requestType == 'sendfile':
                destination = data[0]
                filename = data[1]
                filedata = data[2]
                send_file(currentAccount, destination, filename, filedata, socket_client)

            elif requestType == 'createRoom':
                roomId = roomManager.create_room(currentAccount)
                response = dict()
                response[1] = 'success'
                response[2] = 'Created Room with id ' + str(roomId)
                myRoom = roomId
                print(roomId)

                responseData = pickle.dumps(response)
                responseHeader = get_response_header(requestType, len(responseData))
                socket_client.sendall(responseHeader + responseData)
            
            elif requestType == 'joinRoom':
                roomId = int(data[0])
                response[1] = roomManager.join_room(currentAccount, roomId)
                print(roomId, response[1])
                if response[1] == 'success':
                    response[2] = 'Success joined room ' + str(roomId)
                    myRoom = roomId
                    gm = roomManager.gameManager[roomId]
                    gm.sendPlay()
                else:
                    response[2] = 'Room not found'
                
                responseData = pickle.dumps(response)
                responseHeader = get_response_header(requestType, len(responseData))
                socket_client.sendall(responseHeader + responseData)

            elif requestType == 'defBoard':
                board = data[0]
                gm = roomManager.gameManager[roomId]
                gm.defBoard(currentAccount, board)

            elif requestType == 'atkBoard':
                row = data[0]
                col = data[1]
                gm = roomManager.gameManager[roomId]
                gm.atkBoard(currentAccount, col, row)

        else:
            if currentAccount:
                accountManager.set_disconnected(currentAccount)
            break
    return

def send_broadcast(currentAccount, message, socket_client):
    for destination in currentAccount.friend:
        send_message(currentAccount, destination, message, socket_client)
    return

def send_file(currentAccount, destination, filename, filedata, socket_client):
    response = dict()
    requestType = 'sendfile'
    if not(destination == currentAccount.id):
        if(currentAccount.check_friend(destination)):
            checkDestination = accountManager.check_online(destination)
            if checkDestination:
                dest_socket, _ = checkDestination
                response[1] = 'success'
                response[2] = (currentAccount.id, currentAccount.name, filename, filedata)
                responseData = pickle.dumps(response)
                responseHeader = get_response_header(requestType, len(responseData))
                dest_socket.sendall(responseHeader + responseData)
                return
            else:
                response[2] = destination + ' is not online'
        else:
            response[2] = destination + ' is not your friend'
    else:
        response[2] = 'Cannot sent file to yourself'

    response[1] = 'failed'
    responseData = pickle.dumps(response)
    responseHeader = get_response_header(requestType, len(responseData))
    socket_client.sendall(responseHeader + responseData)
    return

def send_message(currentAccount, destination, message, socket_client):
    response = dict()
    requestType = 'chat'
    if not(destination == currentAccount.id):
        if(currentAccount.check_friend(destination)):
            checkDestination = accountManager.check_online(destination)
            if checkDestination:
                dest_socket, _ = checkDestination
                response[1] = 'success'
                response[2] = (currentAccount.id, currentAccount.name, message)
                responseData = pickle.dumps(response)
                responseHeader = get_response_header(requestType, len(responseData))
                dest_socket.sendall(responseHeader + responseData)
                return
            else:
                response[2] = destination + ' is not online'
        else:
            response[2] = destination + ' is not your friend'
    else:
        response[2] = 'Cannot sent message to yourself'
    
    response[1] = 'failed'
    responseData = pickle.dumps(response)
    responseHeader = get_response_header(requestType, len(responseData))
    socket_client.sendall(responseHeader + responseData)
    return

try:
    accountManager = pickle.load(open('accountmanager.pkl', 'rb'))
except:
    accountManager = AccountManager()

roomManager = RoomManager()
def main():
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((HOST, PORT))
    socket_server.listen(5)
    
    print('Server started')
    try:
        while True:
            socket_client, address_client = socket_server.accept()

            thread_client = threading.Thread(target=commandHandler, args=(socket_client, address_client))
            thread_client.start()
    except KeyboardInterrupt:
        pickle.dump(accountManager, open('accountmanager.pkl', 'wb'))

if __name__ == '__main__':
    main()