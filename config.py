import json

default_config = {
    "host": "0.0.0.0",
    "port": 9999,
    "name": "zinx",
    "max_conn": 100,
    "max_package_size": 1024
}


def reload(fp):
    return json.load(fp)
