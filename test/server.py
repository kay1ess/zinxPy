import sys


sys.path.append("D:\\PycharmProjects\\practice")

if __name__ == "__main__":
    from zinxPy.net.server import Server
    server = Server("zinxPy0.1", "127.0.0.1", 9999)
    server.serve()
