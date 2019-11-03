from .message import Message


class Request:

    def __init__(self, conn, msg: Message):
        self.conn = conn
        self.msg = msg
