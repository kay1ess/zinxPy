#### zinxPy简介

> 基于python的tcp框架， 主要参考golang的[Zinx](https://github.com/aceld/zinx)框架进行实现，本项目主要用于学习， 同时也欢迎贡献代码。

#### 主要功能

1. 提供基于线程的链接管理
2. tcp拆包封包
3. tcp路由

#### get start

server.py
``` python
from zinxPy.server import Server
server = Server()

@server.router(1)
class MyRouter(BaseRouter):

    def before_handle(self, request):
        print("=================before handle=====================")

    def handle(self, request):
        print("receive msg:", request.msg.data.decode())
        request.conn.send_msg(101, "ping ping".encode())

    def after_handle(self, request):
        print("=================after handle======================")

server.serve()
```

client.py
``` python
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))
msg = Message(1, "hello".encode())
client.send(pack(msg))
client.close()
```

##### 配置文件

config.json
``` json

{
    "host": "0.0.0.0",    # 监听地址
    "port": 9999,         # 监听端口
    "name": "zinxPy",     # 服务器名
    "max_conn": 100,      # 最大连接数  
    "max_package_size": 1024  # tcp包最大长度
}
```
