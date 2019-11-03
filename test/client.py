import sys


sys.path.append("D:\\PycharmProjects\\practice")


import socket
import time
from zinxPy.message import Message
from zinxPy.data_pack import pack, unpack

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))

while True:
    msg = Message(1, "hahah i am zinxPy".encode())
    print("->>>> send msg id:", msg.id)
    print("->>>> send msg data:", msg.data)

    client.send(pack(msg))
    time.sleep(5)
    data = client.recv(1024)
    print("->>>> rece msg id:", unpack(data).id)
    print("->>>> rece msg data:", unpack(data).data.decode())

client.close()
