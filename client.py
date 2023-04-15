import socket

HOST, PORT = "0.0.0.0", 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

client.sendall(bytes("This is from Client", "UTF-8"))

out_data = ""
while True:
    in_data = client.recv(1024)
    print("From Server :", in_data.decode())

    while not len(out_data):
        out_data = input()

    client.sendall(bytes(out_data, 'UTF-8'))

    if out_data == "bye":
        break
    out_data = ''

client.close()
