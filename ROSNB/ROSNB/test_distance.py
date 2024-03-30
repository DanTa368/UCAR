import lidar_distance
import rospy

rospy.init_node("a")
lidar_distance = lidar_distance.Lidar_distance()
# 1.36 1.24
while True:
    print(f"====================={lidar_distance.right}=====================")