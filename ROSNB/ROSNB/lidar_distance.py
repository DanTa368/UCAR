#! /usr/bin/pytohn3

import rospy
from sensor_msgs.msg import LaserScan


class Lidar_distance:

    def __init__(self):
        self.front = 1.0
        self.right = 1.0
        sub = rospy.Subscriber("/scan", LaserScan, self._set_distance)
        print("==================lidar_distance_init==============")

    def _set_distance(self, data: LaserScan):
        ls = data.ranges
        # print(ls[377], ls[189])
        # 0.377         0.462
        self.front = ls[167]
        self.right = ls[83]
        # print("=======================雷达数据已更新==================")
