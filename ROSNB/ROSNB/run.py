#! /usr/bin/python3

import math
import rospy
import actionlib
from actionlib_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionGoal
from geometry_msgs.msg import Twist, PoseStamped, PoseWithCovarianceStamped


class Run:

    def __init__(self):
        # Init navigation
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)

        self.cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

        action_within_time = self.move_base.wait_for_server()

        self._robot_pose = {"x": 0.00, "y": 0.00}
        self._goal_pose = {"x": 0.00, "y": 0.00}
        self._amcl_pose_subscriber = rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, self._set_robot_pose)
        # self._goal_pose_subscipber = rospy.Subscriber("/move_base/goal", MoveBaseActionGoal, self._set_goal_pose)
        self.first = True
        self.go_A = False

    def run(self, drop, name):
        print(f"前往{name}点")
        self.first = True
        self._set_goal_pose(drop)
        goal = MoveBaseGoal()

        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = drop["x"]
        goal.target_pose.pose.position.y = drop["y"]
        goal.target_pose.pose.position.z = 0.00
        goal.target_pose.pose.orientation.x = 0.00
        goal.target_pose.pose.orientation.y = 0.00
        goal.target_pose.pose.orientation.z = drop["z"]
        goal.target_pose.pose.orientation.w = drop["w"]

        self.move_base.send_goal(goal)

        while self.get_goal_distance() > 0.48:
            if self.first:
                print(f"前往{name}点中")
                self.first = False
            rospy.sleep(0.2)
        print(f"===============到达{name}点===============")
        return True

        # print("点位已发送")

    def get_goal_result(self):
        finished_result = self.move_base.wait_for_result()

        if not finished_result:
            self.move_base.cancel_goal()
            # rospy.loginfo("Timed out achieving goal")
            return False
        else:
            # We made it!
            state = self.move_base.get_state()
            if state == GoalStatus.SUCCEEDED:
                # rospy.loginfo("Goal succeeded!")
                return True
            else:
                self.move_base.cancel_goal()
                return False

    def rotate(self):
        print("================开始旋转===================")
        rate = rospy.Rate(10)
        twist = Twist()
        twist.angular.z = -1.0
        _start = rospy.Time.now()
        while not rospy.is_shutdown():
            self.cmd_vel.publish(twist)
            rate.sleep()
            _end = rospy.Time.now() - _start
            if _end.to_sec() >= 0.9:
                print("===================旋转完成================")
                break

    def rotate_left(self):
        print("================开始旋转===================")
        rate = rospy.Rate(10)
        twist = Twist()
        twist.angular.z = 1.0
        _start = rospy.Time.now()
        while not rospy.is_shutdown():
            self.cmd_vel.publish(twist)
            rate.sleep()
            _end = rospy.Time.now() - _start
            if _end.to_sec() >= 0.7:
                print("===================旋转完成================")
                break
    def cross_bridge(self):
        # print("============过桥===============")
        twist = Twist()
        twist.linear.x = 3.0
        self.cmd_vel.publish(twist)

    def forward(self):
        # print("=========================向前=======================")
        twist = Twist()
        twist.linear.x = 0.25
        self.cmd_vel.publish(twist)

    def right(self):
        # print("=======================向右=====================")
        twist = Twist()
        twist.linear.y = -0.15
        self.cmd_vel.publish(twist)

    def stop(self):
        print("======================停止==========================")
        self.move_base.cancel_goal()

    def reset_pose(self, pose):
        # print("=================调整位置==========================")
        twist = Twist()
        twist.linear.y = 0
        if pose > 1.30:
            twist.linear.y = -0.15
            self.cmd_vel.publish(twist)
        elif pose < 1.14:
            twist.linear.y = 0.15
            self.cmd_vel.publish(twist)
        else:
            return True

    def reset_orient(self):
        rospy.set_param("/")

    def _set_goal_pose(self, goal):
        self._goal_pose["x"] = goal["x"]
        self._goal_pose["y"] = goal["y"]
        print("goal_pose已更性")

    def _set_robot_pose(self, pose: PoseWithCovarianceStamped):
        self._robot_pose["x"] = pose.pose.pose.position.x
        self._robot_pose["y"] = pose.pose.pose.position.y

    def get_goal_pose(self):
        return f"_goal_pose_x=={self._goal_pose['x']}----------------_goal_pose_y={self._goal_pose['y']}"

    def get_robot_pose(self):
        return f"_robot_pose_x=={self._robot_pose['x']}-------------------_robot_pose_y{self._robot_pose['y']}"

    def get_goal_distance(self):
        distance = math.sqrt(math.pow(self._robot_pose["x"] - self._goal_pose["x"], 2) + math.pow(
            self._robot_pose["y"] - self._goal_pose["y"], 2))
        # print(f"goal_distance=={distance}========{self.get_goal_pose()}=============={self.get_robot_pose()}\n{rospy.get_param('/move_base/TebLocalPlannerROS/weight_optimaltime')}")
        return distance
