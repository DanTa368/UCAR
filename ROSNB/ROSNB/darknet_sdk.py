import socket
from threading import Thread
from typing import List

import rospy
import Judging_crops
from darknet_result import DarknetResult
import run
import json


class DarknetSDK:
    def __init__(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect(("127.0.0.1", 8848))
        self._result: List[DarknetResult] = list()
        self._running_flag = True
        self._detect_flag = True
        self._res = list()
        Thread(target=self._receive, daemon=True).start()

    def _receive(self):
        while self._running_flag:
            result: List[DarknetResult] = list()
            data = self._client.recv(1024)
            try:
                for i in json.loads(data):
                    result.append(DarknetResult(i))
            except Exception as e:
                print(e)
                continue
            self._result.clear()
            self._result.extend(result)

    def get_result(self) -> List[DarknetResult]:
        return self._result

    def start_detect(self):
        print("start detect")
        self._res.clear()
        self._detect_flag = True

        def _run():
            while self._detect_flag:
                # print(f"======get_result==={self.get_result()}")
                for j in Judging_crops.judging_crops(self.get_result()):
                    self._res.append(j)
                    rospy.sleep(0.01)

        Thread(target=_run, daemon=True).start()

    def start_F_detect(self):
        print("start detect")
        self._res.clear()
        self._detect_flag = True

        def _run():
            while self._detect_flag:
                # print(f"======get_result==={self.get_result()}")
                for j in self.get_result():
                    self._res.append(j)
                    rospy.sleep(0.01)

        Thread(target=_run, daemon=True).start()

    def stop_detect(self):
        self._detect_flag = False

    def get_res(self):
        ls = list()
        for i in self._res:
            ls.append(i)
        return ls


if __name__ == '__main__':
    darknet = DarknetSDK()
    darknet.start_detect()
    rospy.init_node("a")
    run = run.Run()
    while True:
        time1 = rospy.Time.now().to_sec()
        run.right()
        if (int(rospy.Time.now().to_sec()) - int(time1)) > 0.5:
            break
    darknet.stop_detect()
    res = darknet.get_res()
    print(res)
