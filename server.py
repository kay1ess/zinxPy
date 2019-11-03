import socket
import time
from .connection import Connection, ConnectionManager
from .message import MessageHandler
from .config import default_config, reload
import threading
import ctypes
import inspect


class Server:

    def __init__(self, fp=None, tcp_version="tcp4", daemon=True):
        self.daemon = daemon
        self.threads = None
        if fp is None:
            global_config = default_config
        else:
            global_config = reload(fp)
        try:
            self.name = global_config["name"]
            self.ip = global_config["host"]
            self.port = global_config["port"]
            self.max_conn = global_config["max_conn"]
        except KeyError:
            print("config error, please check the config file")
            return
        self.tcp_version = tcp_version
        self.on_connection_start = None
        self.on_connection_stop = None
        self.conn_manager = ConnectionManager()
        self.msg_handler = MessageHandler({})


        if self.tcp_version == "tcp4":
            family = socket.AF_INET
        elif self.tcp_version == "tcp4":
            family = socket.AF_INET6
        else:
            raise ValueError("tcp_version must be in [tcp4, tcp6]")
        self.server = socket.socket(family=family, type=socket.SOCK_STREAM)

    def add_router(self, msg_id, router):
        self.msg_handler.add_router(msg_id, router)

    def process_request_thread(self):
        while True:
            conn, r_addr = self.server.accept()
            conn_id = threading.current_thread().ident
            c = Connection(self, conn, conn_id, r_addr)
            self.conn_manager.add(c)
            c.start()

    def start(self):
        print(f"[start server] Server Name: {self.name}")
        print(f"[start server] Server Tcp Ver: {self.tcp_version}")
        print("[start server] zinxPy is starting up...")
        time.sleep(0.5)

        self.server.bind((self.ip, self.port))
        self.server.setblocking(True)
        self.server.listen()
        print("start listening...")
        while True:
            try:
                t = threading.Thread(target=self.process_request_thread)
                t.daemon = self.daemon
                if self.threads is None:
                    self.threads = []
                if len(self.threads) < self.max_conn:
                    self.threads.append(t)
                    t.start()
            except KeyboardInterrupt:
                self.stop()
                break
            time.sleep(3)

    def stop(self):
        print("[stop server] zinxPy stopping...")
        try:
            if self.threads:
                for t in self.threads:
                    _async_raise(t.ident, SystemExit)
            self.server.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        print("[EXIT] Bye Bye")

    def serve(self):
        self.start()


# user c-api to shutdown the threads
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(
        exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
