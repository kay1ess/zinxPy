import struct
from .message import Message
from .exceptions import NotAllowConnection


def pack(msg: Message) -> bytes:
    msg_bytes = struct.pack('i', msg.id)
    msg_bytes += struct.pack('i', msg.length)
    msg_bytes += struct.pack(f'{msg.length}s', msg.data)
    return msg_bytes


def unpack(data: bytes) -> Message:
    try:
        msg_id = struct.unpack_from('i', data, offset=0)[0]
        msg_length = struct.unpack_from('i', data, offset=4)[0]
        msg_data = struct.unpack_from(f'{msg_length}s', data, offset=8)[0]
    except Exception:
        raise NotAllowConnection("this connection is not allow to connect")

    msg = Message(msg_id, msg_data)
    return msg
