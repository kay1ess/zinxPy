import socket
import time


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))

while True:

    msg = "hello zinxPy"
    client.send(msg.encode())
    time.sleep(1)
    data = client.recv(1024)
    print("rece data:", data.decode())

client.close()
