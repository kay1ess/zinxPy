
from .exceptions import RouterAlreadyExists, HandlerNotExists


class Message:
    def __init__(self, id, data):
        self.id = id
        self.length = len(data)
        self.data = data


class MessageHandler:
    def __init__(self, data: dict):
        self.api = data

    def handle_message(self, request):
        try:
            handler = self.api[request.msg.id]
        except KeyError:
            raise HandlerNotExists("not found the handler by the msg id")
        handler.before_handle(request)
        handler.handle(request)
        handler.after_handle(request)

    def add_router(self, msg_id, router):
        if self.api.get(msg_id) is not None:
            raise RouterAlreadyExists("msg id already is used！！！")
        self.api[msg_id] = router
