#! /usr/bin/python3

import rospy
import run
import speak
import drop
import asr
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
asr = asr.Listen()
darknet = darknet_sdk.DarknetSDK()
lidar_distance = lidar_distance.Lidar_distance()

# 启动语音唤醒
asr.get_awake_angle()

asr.start_asr_service()
#
rospy.sleep(10)

start = rospy.Time.now().to_sec()
# F-0
F_result = []
walk.run(all_drop["F-0"], "F-0")
# F-0-1
walk.run(all_drop["F-0-1"], "F-0-1")
try:
    dynamic_reconfigure_sdk.reconfigure({"weight_optimaltime": 7, "max_vel_y": 3})
except:
    print("============调参失败===============")
# F
darknet.start_F_detect()
walk.run(all_drop["F"], "F")
# rospy.sleep(0.5)
# F_result.extend([i for i in Judging_crops.F_judging_crops(darknet.get_result())])

try:
    dynamic_reconfigure_sdk.reconfigure({"weight_optimaltime": 18, "max_vel_y": 10})
except:
    print("============调参失败===============")

# F_result.extend([i for i in Judging_crops.F_judging_crops(darknet.get_result())])
# F-L

walk.run(all_drop["F-L"], "F-L")
# rospy.sleep(0.5)
# F_result.extend([i for i in Judging_crops.F_judging_crops(darknet.get_result())])

# F-R

walk.run(all_drop["F-R"], "F-R")
# rospy.sleep(0.5)
# F_result.extend([i for i in Judging_crops.F_judging_crops(darknet.get_result())])

# F-R-1


walk.run(all_drop["F-R-1"], "F-R-1")
# rospy.sleep(0.3)
# F_result.extend([i for i in Judging_crops.F_judging_crops(darknet.get_result())])

# F-R-2
walk.run(all_drop["F-R-2"], "F-R-2")
# rospy.sleep(0.3)
# F_result.extend([i for i in Judging_crops.F_judging_crops(darknet.get_result())])
darknet.stop_detect()
F_result = darknet.get_res()
try:
    dynamic_reconfigure_sdk.reconfigure({"weight_optimaltime": 8, "max_vel_y": 5, "max_vel_x": 1})
except:
    print("============调参失败===============")

# F-1
walk.run(all_drop["F-1"], "F-1")
rospy.sleep(0.8)
# F-2

walk.run(all_drop["F-2"], "F-2")
# rospy.sleep(0.5)

try:
    dynamic_reconfigure_sdk.reconfigure({"weight_optimaltime": 40, "max_vel_y": 16, "acc_lim_x": 0.5, "max_vel_x": 10})
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
darknet.start_detect()
walk.run(all_drop["D-1"], "D-1")
# D-2
walk.run(all_drop["D-2"], "D-2")
darknet.stop_detect()
D_result = darknet.get_res()
#
# C-1
# C_result = []
darknet.start_detect()
walk.run(all_drop["C-1"], "C-1")
# C-2
walk.run(all_drop["C-2"], "C-2")
darknet.stop_detect()
C_result = darknet.get_res()
# B-1
# B_result = []
darknet.start_detect()
walk.run(all_drop["B-1"], "B-1")

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
while lidar_distance.front > 0.459:
    walk.forward()
print(f"=======================前方{lidar_distance.front}=========================")
walk.stop()
# # # 向右对准
while lidar_distance.right > 0.375:
    walk.right()
print(f"=======================右方{lidar_distance.right}=========================")
walk.stop()
end = rospy.Time.now().to_sec()
# # #
print(f"E\n{E_result}")
print(f"D\n{D_result}")
print(f"C\n{C_result}")
print(f"B\n{B_result}")
print(f"F\n{F_result}")
print(f"用时{(end - start):.2f}秒")
All_result = []


def result_no_repeat(_result):
    try:
        _result = max(_result, key=_result.count)
        for i in All_result:
            if _result == i:
                _result = []
        All_result.append(_result)
    except:
        pass
    return _result


E_result = result_no_repeat(E_result)
D_result = result_no_repeat(D_result)
C_result = result_no_repeat(C_result)
B_result = result_no_repeat(B_result)
# try:
#     E_result = max(E_result, key=E_result.count)
#     All_result.append(E_result)
# except:
#     pass
# try:
#     D_result = max(D_result, key=D_result.count)
#     All_result.append(D_result)
#     for i in All_result:
#         if D_result == i:
#             D_result = []
# except:
#     pass
# try:
#     C_result = max(C_result, key=C_result.count)
#     All_result.append(C_result)
#
# except:
#     pass
# try:
#     B_result = max(B_result, key=B_result.count)
#     All_result.append(B_result)
# except:
#     pass
room_results = {
    "B": B_result,
    "C": C_result,
    "D": D_result,
    "E": E_result
}


def guess_crop(room_results):
    crops = ["小麦", "水稻", "玉米", "黄瓜"]
    missing_rooms = []

    for room, result in room_results.items():
        if result == []:
            missing_rooms.append(room)

    if len(missing_rooms) == 0:
        print("所有房间结果均已有值，无需猜测。")
        return room_results

    for room in missing_rooms:
        # 获取已知结果的房间列表
        known_rooms = [r for r in room_results if r != room and room_results[r] != []]

        # 获取已知结果的作物列表
        known_crops = [room_results[r] for r in known_rooms]

        # 猜测缺失房间的结果
        guessed_result = max(set(crops) - set(known_crops), key=known_crops.count)
        room_results[room] = guessed_result
        print(f"猜测 {room} 的作物是: {guessed_result}")

    return room_results


room_results = guess_crop(room_results)

print(room_results)

count = int(Judging_crops.count(F_result)[0])

talk.speak(
    f"任务完成,B区域种植的作物为{room_results.get('B')},"
    f"C区域种植的作物为{room_results.get('C')},"
    f"D区域种植的作物为{room_results.get('D')},"
    f"E区域种植的作物为{room_results.get('E')},"
    f"F区域种植的果实为{Judging_crops.F_result(Judging_crops.count(F_result)[1])},数量为{count}个")
