import socket
import time


class Server:

    def __init__(self, name: str, ip: str, port: int, tcp_version="tcp4"):
        self.name = name
        self.ip = ip
        self.port = port
        self.tcp_version = tcp_version
        if self.tcp_version == "tcp4":
            family = socket.AF_INET
        elif self.tcp_version == "tcp4":
            family = socket.AF_INET6
        else:
            raise ValueError("tcp_version must be in [tcp4, tcp6]")
        self.server = socket.socket(family=family, type=socket.SOCK_STREAM)

    def start(self):
        print(f"[start server] Server Name: {self.name}")
        print(f"[start server] Server Tcp Ver: {self.tcp_version}")
        print("[start server] zinxPy is starting up...")
        time.sleep(0.5)
        self.server.bind((self.ip, self.port))
        self.server.listen()
        while True:
            conn, r_addr = self.server.accept()
            while True:
                try:
                    data = conn.recv(1024)
                    print("recev data:", data.decode())
                    conn.send(data)
                except ConnectionResetError as err:
                    print(err)
                    break
            conn.close()

    def stop(self):
        pass

    def serve(self):
        self.start()
