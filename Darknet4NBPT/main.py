#!/usr/bin/env python3
import os
import darknet
import cv2
import rospy
from nbpt_darknet.srv import *
from threading import Thread
import json

os.chdir("/home/ucar/ucar_ws/src/nbpt_darknet/scripts/")


class Darknet:
    def __init__(self):
        # set param
        self.image_width = 640
        self.image_height = 480
        self.thresh = 0.35
        self.weights_file = "./yolov4-tiny_4MyDataSet_final.weights"
        self.config_file = "./cfg/yolov4-tiny_4MyDataSet.cfg"
        self.data_file = "./data/ucar.data"

        # init network
        self._network, self._class_names, self._class_colors = darknet.load_network(self.config_file, self.data_file,
                                                                                    self.weights_file, batch_size=1)
        self._darknet_width = darknet.network_width(self._network)
        self._darknet_height = darknet.network_height(self._network)
        # inner var
        self._cam = cv2.VideoCapture(0)
        self._cam.set(3, 640)
        self._cam.set(4, 480)
        self._cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        self.state = False
        self._ls = []
        self._result = []

        # init thread
        t = Thread(target=self.detect)
        t.daemon = True
        t.start()

    def detect(self):
        while self._cam.isOpened():
            if not self.state:
                continue
            ret, frame = self._cam.read()
            # cv2.imwrite("/home/ucar/detect_image/" + time.strftime("%HH:%MM:%SS") + ".jpg", frame)
            if not ret:
                break
            frame = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (self._darknet_width, self._darknet_height),
                               interpolation=cv2.INTER_LINEAR)
            img = darknet.make_image(self._darknet_width, self._darknet_height, 3)
            darknet.copy_image_from_bytes(img, frame.tobytes())
            detections = darknet.detect_image(self._network, self._class_names, img, thresh=self.thresh)
            # darknet.print_detections(detections)
            for label, _, _ in detections:
                self._add_times(label)
            darknet.free_image(img)

    def _add_times(self, data):
        self._ls.append(data)

    def _add_without_repeat(self, data):
        if not data in self._result:
            self._result.append(data)

    def get_result(self):
        for i in self._ls:
            if self._ls.count(i) >= 3:
                self._add_without_repeat(i)
        return json.dumps(self._result)

    def clear_result(self):
        self._ls.clear()
        self._result.clear()

    def release(self):
        self._cam.release()


detect_timeout = 15
rotate_freq = 10
rotate_angle = 0.5


def get_result(req):
    # Thread(target=dn.detect).start()
    #
    # rotator = rospy.Publisher("/cmd_vel", Twist)
    # twist = Twist()
    # twist.angular.z = rotate_angle
    #
    # timeout = rospy.Rate(rotate_freq)
    # i = 0
    # tick = detect_timeout / (1 / rotate_freq)
    # while i < tick:
    #     rotator.publish(twist)
    #     timeout.sleep()
    #     i += 1
    # dn.state = False
    return Result_srvResponse(dn.get_result())


def stop_detect(req):
    dn.state = False
    return Stop_srvResponse()


def start_detect(req):
    dn.clear_result()
    dn.state = True
    return Start_srvResponse()


def release(req):
    dn.release()
    return Release_srvResponse()


if __name__ == "__main__":
    rospy.init_node("nbpt_darknet")
    dn = Darknet()

    rospy.Service("nbpt_darknet/getResult", Result_srv, get_result)
    rospy.Service("nbpt_darknet/start", Start_srv, start_detect)
    rospy.Service("nbpt_darknet/stop", Stop_srv, stop_detect)
    rospy.Service("nbpt_darknet/Release", Release_srv, release)
    rospy.spin()
