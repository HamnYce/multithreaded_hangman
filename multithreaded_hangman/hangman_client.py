import socket

# Homemade Protocols / Signals
# e.g. EC,SC,GW etc. can be found in hangman_server.py

HOST, PORT = '0.0.0.0', 9999


def is_valid_letter(letter):
    return not (len(letter) != 1 or ord(letter) < ord('a') or ord(letter) > ord('z'))


class ClientClass:
    def __init__(self, server_host, server_port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.attempt_connect(server_host, server_port)

        # NOTE: will be set in the introduction
        self.name = None
        # NOTE: updated after every WG signal
        self.lives = 10
        # NOTE: updated after every CG signal
        self.correct = set()
        # NOTE: updated after every WG signal
        self.incorrect = set()

        self.word = None

    def start(self):
        self.introduction()

        self.game_loop()

        self.server_socket.close()

    def introduction(self):
        self.msg_server("NC")

        res = self.recv_server().split(",")

        # if 'error connection' signal then shutdown the program
        # or implement try again function on both sides
        if res[0] == "EC":
            print(res[1])
            self.server_socket.close()
            raise AssertionError("Connection Error, Please rerun the program")
        elif res[0] == "SC":
            self.name = res[1]
            self.word = ['_'] * int(res[2])
        else:
            raise AssertionError("Unknown error please rerun program")

    def game_loop(self):
        while True:
            print(self.game_status())
            letter = input("input the letter you want to guess\n")

            if not is_valid_letter(letter):
                print("Please enter a valid letter, a-z or A-Z")
                continue

            if self.is_guessed_letter(letter):
                print("That letter has already been guessed!")
                continue

            self.msg_server(letter)
            res = self.recv_server()

            match res.split(','):
                case ["GO", word] | ["GL", word]:
                    print(f"Game over, the word was {''.join(word)}!")
                    return
                case ["GW"]:
                    print(f"Game won!!, you found out the word was {''.join(self.word)}")
                    return
                case ["CG", *indexes]:
                    print("Correct Guess!")
                    self.correct.add(letter)
                    self.update_word(letter, indexes)
                case ["IG"]:
                    print("Incorrect Guess!")
                    self.incorrect.add(letter)
                    self.lives -= 1
                case _:
                    print(f"Res '{res}'")
                    raise AssertionError("Unknown error please rerun program")

    def update_word(self, letter, indexes):
        for i in indexes:
            self.word[int(i)] = letter

    def is_guessed_letter(self, letter):
        return letter in self.correct

    def msg_server(self, msg):
        self.server_socket.sendall(bytes(msg, 'utf-8'))

    def recv_server(self):
        return self.server_socket.recv(1024).decode()

    def attempt_connect(self, server_host, server_port):
        self.server_socket.connect((server_host, server_port))

    def game_status(self):
        game_stats = \
            f"""
word status: {''.join(self.word)}
name: {self.name}
correct: {self.correct}
wrong: {self.incorrect}
lives: {self.lives}"""
        return game_stats

client = ClientClass(HOST, PORT)
client.start()
