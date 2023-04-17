import socket
import threading

# TODO: we can add usernames later, structure: '<username>:<msg>'
chat_msgs = []


class ClientListenerThread(threading.Thread):
    def __init__(self, client_socket, client_address):
        threading.Thread.__init__(self)

        self.client_socket = client_socket
        self.client_address = client_address

    def run(self):
        while True:
            res = self.client_socket.recv(1024).decode()
            if res == 'sign out now' or len(res) == 0:
                break

            print(f"{self.client_address} says {res}")

            chat_msgs.append(res)

        self.client_socket.close()
        print(f"Disconnected from client: {self.client_address}")


class ClientMessagerThread(threading.Thread):
    def __init__(self, client_socket, client_address):
        threading.Thread.__init__(self)

        self.client_socket = client_socket
        self.client_address = client_address
        self.msg_i = 0

    def run(self):
        while True:
            if self.msg_i < len(chat_msgs):
                self.client_socket.sendall(bytes(chat_msgs[self.msg_i], 'utf-8'))
                self.msg_i += 1

    def more_chats_available(self):
        return self.msg_i < len(chat_msgs)


HOST, PORT = "0.0.0.0", 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))

print("Chatroom server Starting")
print(f"Server Listening on socket: {HOST}:{PORT}...")
while True:
    server_socket.listen(1)
    new_client_socket, new_client_address = server_socket.accept()
    client_messager_thread = ClientMessagerThread(new_client_socket, new_client_address)
    client_messager_thread.start()
    client_listener_thread = ClientListenerThread(new_client_socket, new_client_address)
    client_listener_thread.start()
    print(f"Attached to client: {new_client_address}")
