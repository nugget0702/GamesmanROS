#!/usr/bin/env python
import rospy
from moveit_msgs.srv import GetPositionIK, GetPositionIKRequest, GetPositionIKResponse
from geometry_msgs.msg import PoseStamped, Point
from moveit_commander import MoveGroupCommander
import numpy as np
from numpy import linalg
import sys
import pymycobot


class Acutate:
    #TODO Double Check
    def __init__(self):
        self.mc = pymycobot.MyCobot("/dev/ttyAMA0", baudrate=1000000)
        self.lift = [109.51, 25.31, -73.47, -19.16, 5.8, 69.34]
        self.observe = [131.13, 5.53, -50.53, -37.08, 13.27, 91.93]
        self.sub = None

        # Wait for the IK service to become available
        rospy.wait_for_service('compute_ik')
        rospy.init_node('service_query')
        # Create the function used to call the service
        self.compute_ik = rospy.ServiceProxy('compute_ik', GetPositionIK)

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
            self.mc.send_angles(self.observe, 20)
            rospy.sleep(2.0)

            self.sub = rospy.Subscriber('/piece_location_' + ar_tag_name, Point, self.move, queue_size=10)
        except:
            print("Could not locate piece : " + ar_tag_name)
            return
        
    def place(self, end_coord):
        #TODO findPoint
        point = findPoint(self, end_coord)
        self.move(point, pickUp=False)

    def move(self, pose, pickUp=True):
        print("Inside Move: ", pose)
        while not rospy.is_shutdown():
            input('Inside Move function, Press [ Enter ]: ')
            # Set the desired orientation for the end effector HERE
            self.request.ik_request.pose_stamped.pose = pose

            try:
                # Send the request to the service
                response = self.compute_ik(self.request)
                
                # Print the response HERE
                print(response)

                #DEBUG & TODO
                group = MoveGroupCommander("arm_group")

                # Setting position and orientation target
                group.set_pose_target(self.request.ik_request.pose_stamped)

                # TRY THIS
                # Setting just the position without specifying the orientation
                #group.set_position_target([0.5, 0.5, 0.0])

                # Plan IK
                plan = group.plan()
                user_input = input("Enter 'y' if the trajectory looks safe on RVIZ")
                
                # Execute IK if safe
                if user_input == 'y':                    
                    if pickUp:
                        print("Inside Pickup")

                        # Open the right gripper
                        print('Opening...')
                        self.mc.set_gripper_state(0, 20)
                        rospy.sleep(1.0)
                        print('Done!')

                        
                        group.execute(plan[1])

                        # Close the right gripper
                        print('Closing...')
                        self.mc.set_gripper_state(1, 20)
                        rospy.sleep(1.0)

                        self.mc.send_angles(self.lift, 20)
                    else:
                        print("Inside Place")

                        group.execute(plan[1])

                        # Open the right gripper
                        print('Opening...')
                        self.mc.set_gripper_state(0, 20)
                        rospy.sleep(1.0)
                        print('Done!')

                        self.mc.send_angles(self.lift)

                        # Close the right gripper
                        print('Closing...')
                        self.mc.set_gripper_state(1, 20)
                        rospy.sleep(1.0)

            except rospy.ServiceException as e:
                print("Service call failed: %s"%e)