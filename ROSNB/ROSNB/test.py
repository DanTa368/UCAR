#! /usr/bin/python3

import rospy
import run
import speak
import drop
import asr
import player
import lidar_distance
from threading import Thread
import Judging_crops
import darknet_sdk
import dynamic_reconfigure_sdk
import os

# init
rospy.init_node("main")
# 点位
print("===============start=================")
all_drop = drop.all_drop

#
# # 实例化

walk = run.Run()
talk = speak.Speak()
music = player.Music()
asr = asr.Listen()
darknet = darknet_sdk.DarknetSDK()
lidar_distance = lidar_distance.Lidar_distance()
# t = Thread(music.player())
# t.daemon = True
# talk.speak("小微准备就绪")

# 启动语音唤醒
# asr.get_awake_angle()
#
# asr.start_asr_service()
# #

start = rospy.Time.now().to_sec()
# F-0
F_result = []
walk.run(all_drop["F-0"], "F-0")

try:
    dynamic_reconfigure_sdk.reconfigure({"weight_optimaltime": 5, "max_vel_y": 0})
except:
    print("============调参失败===============")
# F

walk.run(all_drop["F"], "F")
rospy.sleep(0.5)
F_result.extend([i for i in Judging_crops.F_judging_crops(darknet.get_result())])

try:
    dynamic_reconfigure_sdk.reconfigure({"weight_optimaltime": 20, "max_vel_y": 8})
except:
    print("============调参失败===============")

# F-L

walk.run(all_drop["F-L"], "F-L")
rospy.sleep(0.3)
F_result.extend([i for i in Judging_crops.F_judging_crops(darknet.get_result())])

# F-R

walk.run(all_drop["F-R"], "F-R")
F_result.extend([i for i in Judging_crops.F_judging_crops(darknet.get_result())])

# F-R-1


walk.run(all_drop["F-R-1"], "F-R-1")
rospy.sleep(0.3)
F_result.extend([i for i in Judging_crops.F_judging_crops(darknet.get_result())])

# F-R-2
walk.run(all_drop["F-R-2"], "F-R-2")
rospy.sleep(0.3)
F_result.extend([i for i in Judging_crops.F_judging_crops(darknet.get_result())])

try:
    dynamic_reconfigure_sdk.reconfigure({"weight_optimaltime": 5, "max_vel_y": 1})
except:
    print("============调参失败===============")

# F-1
walk.run(all_drop["F-1"], "F-1")
rospy.sleep(0.5)
# F-2

walk.run(all_drop["F-2"], "F-2")
# rospy.sleep(0.5)

try:
    dynamic_reconfigure_sdk.reconfigure({"weight_optimaltime": 25, "max_vel_y": 15})
except:
    print("============调参失败===============")
#
# E-1

# E_result = []
walk.run(all_drop["E-1"], "E-1")
darknet.start_detect()

# E-2
walk.run(all_drop["E-2"], "E-2")
darknet.stop_detect()
E_result = darknet.get_res()
#
#
# D-1
# D_result = []

walk.run(all_drop["D-1"], "D-1")
darknet.start_detect()
# D-2
walk.run(all_drop["D-2"], "D-2")
darknet.stop_detect()
D_result = darknet.get_res()
#
# C-1
# C_result = []
walk.run(all_drop["C-1"], "C-1")
darknet.start_detect()
# C-2
walk.run(all_drop["C-2"], "C-2")
darknet.stop_detect()
C_result = darknet.get_res()
# B-1
# B_result = []
walk.run(all_drop["B-1"], "B-1")
darknet.start_detect()
# B-2
walk.run(all_drop["B-2"], "B-2")
darknet.stop_detect()
B_result = darknet.get_res()
# # # #
# # # # # A
# # # #
walk.run(all_drop["A"], "A")
# # #
# stop
print("================开始停车=====================")
# 向前对准
while lidar_distance.front > 0.390:
    walk.forward()
print(f"=======================前方{lidar_distance.front}=========================")
walk.stop()
# # # 向右对准
while lidar_distance.right > 0.352:
    walk.right()
print(f"=======================右方{lidar_distance.right}=========================")
walk.stop()
end = rospy.Time.now().to_sec()
# # #
print(f"E\n{E_result}")
print(f"D\n{D_result}")
print(f"C\n{C_result}")
print(f"B\n{B_result}")
print(f"F\n{F_result}{Judging_crops.count(F_result)}")
talk.speak(f"用时{(end -start):.2f}秒,"
           f"任务完成,B区域种植的作物为{max(B_result, key=B_result.count)},"
           f"C区域种植的作物为{max(C_result, key=C_result.count)},"
           f"D区域种植的作物为{max(D_result, key=D_result.count)},"
           f"E区域种植的作物为{max(E_result, key=E_result.count)},"
           f"F区域种植的果实为{Judging_crops.F_result(max(F_result, key=F_result.count))},数量为{Judging_crops.count(F_result)}个")
