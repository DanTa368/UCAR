#! /usr/bin/python3

import rospy
from xf_mic_tts_offline.srv import *
from std_msgs.msg import *

class Speak:
    def __init__(self):
        # Init Service
        rospy.wait_for_service("/xf_mic_tts_offline_node/play_txt_wav")
        self.ts = rospy.ServiceProxy("/xf_mic_tts_offline_node/play_txt_wav", Play_TTS_srv)
        #message
        # self.message = "Hello Hello"


    def speak(self,message):
        # self.message = ""
        self.ts.call(message, "xiaoyan")

