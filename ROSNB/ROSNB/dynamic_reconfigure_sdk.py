import rospy
from dynamic_reconfigure.client import Client
import socket
import signal
import sys
import json

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("127.0.0.1", 8889))


def reconfigure(param: dict):
    client.sendto(json.dumps(param).encode(), ("127.0.0.1", 8888))
    return


# if __name__ == '__main__':
#     print(reconfigure({"acc_lim_x": 15}))
