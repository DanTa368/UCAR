#! /usr/bin/python3
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
import rospy
from threading import Thread


def set_joy(joy: Joy):
    print(joy)
    x = joy.axes[1]
    y = joy.axes[0]
    th = joy.axes[3]
    twist.linear.x = x * 0.5
    twist.linear.y = y * 0.5
    twist.angular.z = th


def sender():
    while True:
        cmd_publisher.publish(twist)
        sleeper.sleep()


rospy.init_node("joy_controller")
twist = Twist()
cmd_publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
joy_subscriber = rospy.Subscriber("/joy", Joy, callback=set_joy)
sleeper = rospy.Rate(20)

if __name__ == '__main__':
    Thread(target=sender, daemon=True).start()
    rospy.spin()
