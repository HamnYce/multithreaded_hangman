# TODO: we need 2 threads running for this, with the same server socket. one thread is always listening
#   while the other thread is always waiting for user input & sending
#   these 2 threads will communicate with the server this way
#   TCP is friggin awesome cause its bidirectional

import socket
import threading
PROMPT = "next msg: "
still_talking = True


class SpeakerThread(threading.Thread):
    def __init__(self, server_socket):
        self.server_socket = server_socket
        threading.Thread.__init__(self)

    def run(self):
        while True:
            msg = input("next msg: ")
            print("\b" * len("next msg: "), end="")
            if msg == "sign out":
                break
            self.server_socket.sendall(bytes(msg, "utf-8"))

        global still_talking
        still_talking = False

        self.server_socket.close()


class ListenerThread(threading.Thread):
    def __init__(self, server_socket):
        self.server_socket = server_socket
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if not still_talking:
                break
            res = self.server_socket.recv(1024).decode()
            print(res)


HOST, PORT = "0.0.0.0", 9999

new_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
new_server_socket.connect((HOST, PORT))

SpeakerThread(new_server_socket).start()
ListenerThread(new_server_socket).start()

