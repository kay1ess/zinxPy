

class RouterAlreadyExists(Exception):
    """路由id已经存在"""


class HandlerNotExists(Exception):
    """路由id不存在"""


class ConnectionNotExists(Exception):
    """链接不存在"""


class NotAllowConnection(Exception):
    """不允许连接"""
