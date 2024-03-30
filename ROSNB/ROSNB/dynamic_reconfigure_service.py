#! /usr/bin/python2
import rospy
from dynamic_reconfigure.client import Client
import socket
import signal
import sys
import json


def callback(data):
    server.sendto(json.dumps(data).encode(), ("127.0.0.1", 8889))
    print("============successful=============")


def stop(*args):
    global running_flag
    running_flag = False
    server.close()
    client.close()
    sys.exit(0)

print("============starting=============")
running_flag = True
rospy.init_node("dynamic_reconfigure_service")
client = Client("/move_base/TebLocalPlannerROS", timeout=10, config_callback=callback)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.bind(("127.0.0.1", 8888))

signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)
while running_flag:
    try:
        config = json.loads(server.recv(1024).decode())
        client.update_configuration(config)
    except socket.timeout:
        pass
