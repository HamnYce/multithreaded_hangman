import socket
import threading

DEBUG = 1
chats = []
mutex = threading.Lock()
current_word = "test"
players = dict()


class MessagerThread(threading.Thread):
    def __init__(self, client_socket, client_address, client_name):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address
        self.client_name = client_name

        self.msg_location = 0

    def run(self):
        while True:
            while self._more_messages():
                msg = chats[self.msg_location]

                self.client_socket.sendall(bytes(msg, "UTF-8"))

                self.msg_location += 1

    def _more_messages(self):
        return self.msg_location < len(chats)


class ListenerThread(threading.Thread):
    def __init__(self, client_socket, client_address, client_name):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address
        self.client_name = client_name

    def run(self):
        while True:
            msg = self.client_socket.recv(1024).decode()

            with mutex:
                chats.append(f"CM,{msg}")

            if msg == current_word:
                with mutex:
                    chats.append(f"CM,{self.client_name} got the word!")
                    # TODO: replace 10 with proper number of points (based on time? or 6af better?)
                    chats.append(f"PS,{self.client_name}, {10}")


HOST, PORT = "localhost", 9999
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

while True:
    server_socket.listen(1)

    new_client_socket, new_client_address = server_socket.accept()
    new_client_name = new_client_socket.recv(1024).decode()

    if new_client_name in players:
        new_client_socket.close()
        continue

    MessagerThread(new_client_socket, new_client_address, new_client_name).start()
    ListenerThread(new_client_socket, new_client_address, new_client_name).start()

    if DEBUG:
        print(f"name: {new_client_name}, address: {new_client_address}")
