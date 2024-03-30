#! /usr/bin/python3
import select

import rospy
from xf_mic_asr_offline.srv import *
from std_msgs.msg import *
from geometry_msgs.msg import Twist
import speak


class Listen:

    def __init__(self):
        # Wait Service
        rospy.wait_for_service("/xf_asr_offline_node/get_offline_recognise_result_srv")
        rospy.wait_for_service("/xf_mic_tts_offline_node/play_txt_wav")
        # Init Service Proxy
        self._asr = rospy.ServiceProxy("/xf_asr_offline_node/get_offline_recognise_result_srv", Get_Offline_Result_srv)
        # Parking Assist
        self._cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

        self.talk = speak.Speak()

        self.asr_first = True
        self.asr_second = False
        self._asr_trigger = None
        self.sub = None

    def get_awake_angle(self):
        return rospy.wait_for_message("/mic/awake/angle", Int32)

    def _asr_callback(self, angle):
        self.talk.speak("我在")
        asr_result = self._asr.call(1, 50, 5)
        asr_result_text = asr_result.text
        twist = Twist()
        rate = rospy.Rate(10)
        time1 = rospy.Time.now()
        if "移动" in asr_result_text:
            self.talk.speak("好的")
            return
        if "转" in asr_result_text:
            print("===================================转弯============================================")
            if "左" in asr_result_text:
                print("==============================左转==============================================")
                twist.angular.z = 1.0
            elif "右" in asr_result_text:
                print("============================右转============================================")
                twist.angular.z = -1.0
            else:
                print("===============================没听清==========================================")
                self.talk.speak("没听清")
        else:
            print("=================================移动=============================================")
            if "前" in asr_result_text:
                twist.linear.x = 1.0
            elif "后" in asr_result_text:
                twist.linear.x = -1.0
            elif "左" in asr_result_text:
                twist.linear.y = 1.0
            elif "右" in asr_result_text:
                twist.linear.y = -1.0
            else:
                self.talk.speak("好的")
        while not rospy.is_shutdown():
            self._cmd_vel.publish(twist)
            rate.sleep()
            time_diff = (rospy.Time.now() - time1).to_sec()
            print(f"======================time_diff=====>{time_diff}===============================")
            if time_diff > 1.5:
                break
        return

    def start_asr_service(self):
        self.sub = rospy.topics.Subscriber("/mic/awake/angle", Int32, callback=self._asr_callback)

    # rospy.spin()
    def stop_asr_service(self):
        if not self._asr_trigger is None:
            self._asr_trigger.unregister()
