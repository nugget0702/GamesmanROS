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
        self.observe = [126.65, 9.31, -80.85, -13.97, 11.95, 88.76]
        self.sub = None

    def pickUp(self, ar_tag_name):
        rospy.init_node('finding_'+ar_tag_name)
        try:
            # Subscribe to the topic "/chatter" with a queue size of 10
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

    def move(self, point, pickUp=True):
        # Wait for the IK service to become available
        print("Inside move")
        rospy.wait_for_service('compute_ik')
        rospy.init_node('service_query')
        # Create the function used to call the service
        compute_ik = rospy.ServiceProxy('compute_ik', GetPositionIK)

        while not rospy.is_shutdown():
            input('Inside Move function, Press [ Enter ]: ')
            
            # Construct the request
            request = GetPositionIKRequest()
            request.ik_request.group_name = "arm_group"

            # If a Sawyer does not have a gripper, replace '_gripper_tip' with '_wrist' instead
            #link = "right_gripper_tip"

            #request.ik_request.ik_link_name = link
            #request.ik_request.attempts = 20
            request.ik_request.pose_stamped.header.frame_id = "g_base"
            
            # Set the desired orientation for the end effector HERE
            request.ik_request.pose_stamped.pose.position.x = point.x
            request.ik_request.pose_stamped.pose.position.y = point.y
            request.ik_request.pose_stamped.pose.position.z = point.z       
            request.ik_request.pose_stamped.pose.orientation.x = 0.0
            request.ik_request.pose_stamped.pose.orientation.y = -1.0
            request.ik_request.pose_stamped.pose.orientation.z = 0.0
            request.ik_request.pose_stamped.pose.orientation.w = 0.0
            
            try:
                # Send the request to the service
                response = compute_ik(request)
                
                # Print the response HERE
                print(response)

                #DEBUG & TODO
                group = MoveGroupCommander("arm_group")

                # Setting position and orientation target
                group.set_pose_target(request.ik_request.pose_stamped)

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

                        print(plan)
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