import sys
import random


sys.path.append("D:\\PycharmProjects\\practice")


from zinxPy.server import Server
from zinxPy.router import BaseRouter


class MyRouter(BaseRouter):

    def before_handle(self, request):
        print("=================before handle=====================")

    def handle(self, request):
        print("receive msg:", request.msg.data.decode())
        request.conn.send_msg(101, "ping ping".encode())

    def after_handle(self, request):
        print("=================after handle=======================")


class Disconnection(BaseRouter):
    """用于断开指定的链接"""

    def handle(self, request):
        print("ready to disconnect the client")
        cur_connid = request.conn.conn_id
        pool = request.conn.conn_manager.connection_pool
        print("pool:", request.conn.conn_manager.connection_pool)
        sample = []
        for id in pool.keys():
            if id != cur_connid:
                sample.append(id)
        print(sample)
        if sample:
            closed_connid = random.choice(list(sample))
            request.conn.conn_manager.delete(closed_connid)
            print(closed_connid)


def start():
    print("on start")


def stop():
    print("on stop")


if __name__ == "__main__":
    fp = open("config.json", encoding="utf-8")
    server = Server(fp)
    server.add_router(1, MyRouter())
    server.add_router(2, Disconnection())
    server.on_connection_start = start
    server.on_connection_stop = stop
    server.serve()
