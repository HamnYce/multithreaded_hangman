import socket
import threading
from random import sample
from random import randint

# Homemade Protocols / Signals:
# # NC <- new connection
# # SC <- successful connection, comes with name and word length
# # EC <- error connection
# # GO <- game over (user entered 'exit')
# # GW <- win game
# # GL <- lose game
# # GE <- end game
# # CG <- correctly guessed
# # IG <- incorrectly guessed

with open("multithreaded_hangman/common_words.txt") as word_file:
    words = word_file.read().splitlines()
    words = sample(words, 100)

word = words[0].lower()
# NOTE: we do this for comparison later on. There is 100% a better way to do this but this works for now
word_set = set(word)
users = dict()


# FIXME: might need to have the ip address be an input because
#  it will be different everytime we connect to stuff

def new_user():
    return {"correct": set(), "wrong": set(), "lives": 10}


def word_indexes(letter):
    return map(lambda t: str(t[0]), filter(lambda t: t[1] == letter, enumerate(word)))


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

    def introduction(self):
        intro = self.recv_client()
        print(self.client_address)

        if intro == "NC":
            self.msg_client(f"SC,{self.name},{len(word)}")

            return True
        else:
            self.msg_client("EC,send 'I'm new'")
            self.client_socket.close()
            return False

    def game_loop(self):
        while True:
            letter = self.recv_client().lower()
            print(f"letter {letter}")

            if letter == "EG":
                self.msg_client(f"GO,{word}")
                return
            elif letter in word:
                users[self.name]["correct"].add(letter)

                if users[self.name]["correct"] == word_set:
                    self.msg_client("GW")
                    return
                self.msg_client("CG," + ','.join(word_indexes(letter)))
            else:
                users[self.name]["wrong"].add(letter)
                users[self.name]["lives"] -= 1

                if not users[self.name]["lives"]:
                    self.msg_client(f"GL,{word}")
                    return

                self.msg_client("IG")

    def msg_client(self, msg):
        self.client_socket.sendall(bytes(msg, "utf-8"))

    def recv_client(self):
        res = self.client_socket.recv(1024)
        return res.decode()


HOST, PORT = "0.0.0.0", 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))

print("Server started")
print("Waiting for client request..")

while True:
    # enables the server to accept connections
    server.listen(1)

    # accepts an incoming connection.
    # socket must be bound (socket.bind())
    # returns (conn, address), where conn is the new socket object
    # (just like server's socket object but for the client)
    # and address of the bound socket on the other side (the client)
    new_client_socket, new_client_address = server.accept()

    # creates a new thread object in the MAIN thread
    new_thread = ClientThread(new_client_socket, new_client_address)

    # calls ClientThread.run() in a new thread
    new_thread.start()
