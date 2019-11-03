import sys
import random


sys.path.append("D:\\PycharmProjects\\practice")


import socket
import time
from zinxPy.message import Message
from zinxPy.data_pack import pack, unpack

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))

msg = Message(2, "delete".encode())
client.send(pack(msg))

client.close()
