#!/usr/bin/env python
import math
import rospy
from moveit_msgs.srv import GetPositionIK, GetPositionIKRequest, GetPositionIKResponse
from geometry_msgs.msg import PoseStamped, Point, Pose
from std_msgs.msg import String
from moveit_commander import MoveGroupCommander
import numpy as np
from numpy import linalg
import sys
import pymycobot
import time


class Acutate:
    #TODO Double Check
    def __init__(self):
        self.mc = pymycobot.MyCobot("/dev/ttyAMA0", baudrate=1000000)
        self.lift = [109.51, 25.31, -73.47, -19.16, 5.8, 69.34]
        self.observe = [131.13, 5.53, -50.53, -37.08, 13.27, 91.93]
        self.sub = None
        self.pub = rospy.Publisher('/piece', String, queue_size=10)

        self.board_size = 150
        self.dim = 3
        self.scaling = self.board_size/self.dim
        self.x_offset = self.board_size/2
        self.y_offset = 100
        self.place_z = 150

        # Wait for the IK service to become available
        rospy.wait_for_service('compute_ik')
        rospy.init_node('service_query', anonymous=True)
        # Create the function used to call the service

        # Construct the request
        self.request = GetPositionIKRequest()
        self.request.ik_request.group_name = "arm_group"

        # If a Sawyer does not have a gripper, replace '_gripper_tip' with '_wrist' instead
        #link = "right_gripper_tip"

        #request.ik_request.ik_link_name = link
        #request.ik_request.attempts = 20
        self.request.ik_request.pose_stamped.header.frame_id = "joint1"

    def pickUp(self, ar_tag_name):
        try:
            print("Inside pickUP : ", ar_tag_name)
            self.pub.publish(ar_tag_name)
            rospy.sleep(1.0)
            self.mc.send_angles(self.observe, 20)
            rospy.sleep(1.0)

            self.sub = rospy.Subscriber('/piece_location_' + ar_tag_name, Pose, self.move)
        except:
            print("Could not locate piece : " + ar_tag_name)
            return
        
    def place(self, end_coord):
        pose = Pose()
        pose.position.x = (((end_coord[0] - 1) * self.scaling) - self.x_offset) / 1000
        pose.position.y = (((end_coord[1] - 1) * self.scaling) + self.y_offset) / 1000
        pose.position.z = self.place_z / 1000

        pose.orientation.x = 0
        pose.orientation.y = 1
        pose.orientation.z = 0
        pose.orientation.w = 0

        #TODO findPoint
        #point = findPoint(self, end_coord)
        print("Inside Place: ", pose)
        self.move(pose, pickUp=False)

    def move(self, pose, pickUp=True):
        print("Inside Move: ", pose)
        input('Inside Move function, Press [ Enter ]: ')
        # Set the desired orientation for the end effector HERE
        self.request.ik_request.pose_stamped.pose = pose
        try:
            #DEBUG & TODO
            group = MoveGroupCommander("arm_group")

            # Setting position and orientation target
            group.set_pose_target(self.request.ik_request.pose_stamped)

            # Plan IK
            plan = group.plan()
            user_input = input("Enter 'y' if the trajectory looks safe on RVIZ")
            
            # Execute IK if safe
            if user_input == 'y':                    
                if pickUp:
                    print("Inside Pickup")

                    #Open the right gripper
                    print('Opening...')
                    self.mc.set_gripper_state(0, 20)
                    time.sleep(1)
                    print('Done!')

                    data = plan[1].joint_trajectory.points[-1].positions

                    data_list = []
                    for index, value in enumerate(data):
                        radians_to_angles = round(math.degrees(value), 2)
                        data_list.append(radians_to_angles)
                    rospy.loginfo(rospy.get_caller_id() + "%s", data_list)
                    self.mc.send_angles(data_list, 25)
                    time.sleep(3)

                    # Close the right gripper
                    print('Closing...')
                    self.mc.set_gripper_state(1, 20)
                    time.sleep(1)

                    self.mc.send_angles(self.lift, 20)
                    time.sleep(3)
                else:
                    print("Inside Place")

                    data = plan[1].joint_trajectory.points[-1].positions

                    data_list = []
                    for index, value in enumerate(data):
                        radians_to_angles = round(math.degrees(value), 2)
                        data_list.append(radians_to_angles)
                    rospy.loginfo(rospy.get_caller_id() + "%s", data_list)
                    self.mc.send_angles(data_list, 25)
                    time.sleep(3)

                    # Open the right gripper
                    print('Opening...')
                    self.mc.set_gripper_state(0, 20)
                    time.sleep(1)
                    print('Done!')

                    self.mc.send_angles(self.observe, 20)
                    time.sleep(3)

                    # Close the right gripper
                    print('Closing...')
                    self.mc.set_gripper_state(1, 20)
                    time.sleep(1)

        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)