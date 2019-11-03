from .request import Request
from .message import Message
from .data_pack import pack, unpack
from .exceptions import ConnectionNotExists, NotAllowConnection
import threading


class Connection:

    def __init__(self, server, conn, conn_id, remote_ip):
        self.server = server
        self.conn = conn
        self.is_closed = False
        self.conn_id = conn_id
        self.remote_ip = remote_ip
        self.conn_manager = self.server.conn_manager

    def start(self):
        print("[start connection] connection is starting up...")
        print(f"[connection] connection_id:{self.conn_id}")

        if self.server.on_connection_start is not None and callable(
                self.server.on_connection_start()
                ):
            self.server.on_connection_start()
        self.start_reader()

    def start_reader(self):
        while True:
            try:
                data = self.conn.recv(1024)
                msg = unpack(data)
                req = Request(self, msg)
                self.server.msg_handler.handle_message(req)
            except (ConnectionResetError, NotAllowConnection):
                cur_thread = threading.current_thread()
                if cur_thread in self.server.threads:
                    self.server.threads.remove(cur_thread)
                self.conn_manager.delete(self.conn_id)
                break

    def start_writer(self):
        pass

    def stop(self):
        print("[stop connection] connection is stopping...")
        self.is_closed = True
        if self.server.on_connection_stop is not None and callable(
                self.server.on_connection_stop()
                ):
            self.server.on_connection_stop()
        cur_thread = threading.current_thread()
        if cur_thread.is_alive():
            from .server import _async_raise
            self.conn_manager.delete(self.conn_id)
            _async_raise(cur_thread.ident, SystemExit)

    def send_msg(self, id, data: bytes):
        if self.is_closed:
            print("[ERROR]the connection is closed")
            raise ConnectionError("the connection is closed")
        msg_bytes = pack(Message(id, data))
        self.conn.send(msg_bytes)


class ConnectionManager:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(ConnectionManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.lock = threading.Lock()
        self.connection_pool = {}

    def add(self, conn: Connection):
        with self.lock:
            self.connection_pool[conn.conn_id] = conn

    def delete(self, conn_id):
        with self.lock:
            del(self.connection_pool[conn_id])
            from .server import _async_raise
            _async_raise(conn_id, SystemExit)

    def get_connection(self, connid):
        try:
            return self.connection_pool[connid]
        except KeyError:
            raise ConnectionNotExists("the connections are not found")

    def len(self):
        return len(self.connection_pool)

    def clear_all(self):
        with self.lock:
            for id, conn in self.connection_pool:
                conn.stop()
                del(self.connection_pool[id])

    def __len__(self):
        return self.len()
