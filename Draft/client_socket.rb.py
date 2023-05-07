import socket
import threading

# TODO: for the word we can link it up with a dictionary and have people guess
#   from the definition of the word

user_name = "James"
PROMPT = f"Next Input>"
chats = []
guess_word = ""
players = dict()


def chat_message(msg):
    chats.append(msg)


def update_word(word):
    global guess_word

    if len(word) != len(guess_word):
        guess_word = word
        return

    for i, (old_c, new_c) in enumerate(zip(guess_word, word)):
        if new_c != '_':
            guess_word[i] = new_c


def player_status(player_name, points_gained):
    if player_name not in players:
        players[player_name] = points_gained
    else:
        players[player_name] += points_gained


def parse_message(msg):
    # TODO: if msg contains player name then output a different message than everybody else
    match msg.split(','):
        case ['CM', msg]:
            chat_message(msg)
        case ['UW', word]:
            update_word(word)
        case ['PS', player_name, points_gained]:
            player_status(player_name, points_gained)


class MessagerThread(threading.Thread):
    def __init__(self, server_socket):
        threading.Thread.__init__(self)
        self.server_socket = server_socket

    def run(self):
        while True:
            msg = input(PROMPT)

            self.server_socket.sendall(bytes(msg, "UTF-8"))


class ListenerThread(threading.Thread):
    def __init__(self, server_socket):
        threading.Thread.__init__(self)
        self.server_socket = server_socket

    def run(self):
        while True:
            msg = self.server_socket.recv(1024).decode()

            parse_message(msg)


HOST, PORT = "0.0.0.0", 9999
new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

new_socket.connect((HOST, PORT))
new_socket.sendall(user_name)

MessagerThread(new_socket).start()
ListenerThread(new_socket).start()
