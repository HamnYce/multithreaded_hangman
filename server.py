import socket
import threading
from random import sample
from random import randint

# Homemade Protocols:
# NC <- new connection
# SC <- successful connection
# EC <- error connection
# GS <- game status
# GO <- game over (user entered 'exit')
# GW <- win game
# GL <- lose game
# AG <- already guessed
# CG <- correctly guessed
# IG <- incorrectly guessed
# EG <- error guessed

with open('common_words.txt') as word_file:
    words = word_file.read().splitlines()
    words = sample(words, 100)

word = words[0].lower()
# NOTE: we do this for comparison later on. There is 100% a better way to do this but this works for now
word_set = set(word)

users = dict()


def new_user():
    return {'correct': set(), 'wrong': set(), 'lives': 10}


def game_status(user):
    word_left = ''.join(map(lambda c: c if c in user['correct'] else '_', word))
    return f"GS,{word_left},{user['lives']}"


class ClientThread(threading.Thread):

    def __init__(self, client_socket, client_address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address
        self.name = sample(words, 1)[0] + str(randint(1, 100))

        print("New connection added: ", client_address)

    def run(self):
        print("Connected to : ", self.client_address)

        # client is waiting for game status after this call
        if self.introduction():
            users[self.name] = new_user()
        else:
            return

        print(f"word: {word}")

        # game loop
        self.game_loop()

        self.client_socket.close()
        del users[self.name]
        print(f"Client,{self.name}, at {self.client_address} disconnected...")

    def msg_client(self, msg):
        self.client_socket.sendall(bytes(msg, 'utf-8'))

    def recv_client(self):
        res = self.client_socket.recv(1024)
        return res.decode()

    def introduction(self):
        intro = self.recv_client()
        print(self.client_address + intro)

        if intro == "NC":
            self.msg_client(f"SC,{self.name}")

            return True
        else:
            self.msg_client("EC,send 'I'm new'")
            self.client_socket.close()
            return False

    def game_loop(self):
        while True:
            data = self.csocket.recv(2048)
            rand_word = sample(x, 1)[0]

            msg = data.decode()

            if msg == 'bye' or not msg:
                break

            print("from client", msg)
            self.csocket.send(bytes(rand_word, 'utf-8'))
            # self.csocket.send(bytes(msg, 'UTF-8'))

        print("Client at ", clientAddress, " disconnected...")


HOST = "0.0.0.0"
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))

print("Server started")
print("Waiting for client request..")

while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
