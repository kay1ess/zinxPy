import sys


sys.path.append("D:\\PycharmProjects\\practice")


from zinxPy.data_pack import pack, unpack
from zinxPy.message import Message


msg_id = 2
msg_data = "delete".encode()


def test_pack():
    msg = Message(msg_id, msg_data)
    return pack(msg)


def test_unpack():
    ret = unpack(test_pack())
    print(ret.data)
    print(ret)


test_unpack()
