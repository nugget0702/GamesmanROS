#!/usr/bin/env python
import rospy
from moveit_msgs.srv import GetPositionIK, GetPositionIKRequest, GetPositionIKResponse
from geometry_msgs.msg import PoseStamped
from moveit_commander import MoveGroupCommander
import numpy as np
from numpy import linalg
import sys

from intera_interface import gripper as robot_gripper



def main():
    # Wait for the IK service to become available
    rospy.wait_for_service('compute_ik')
    
    rospy.init_node('right_gripper')

    # Set up the right gripper
    right_gripper = robot_gripper.Gripper('right_gripper')

    # Calibrate the gripper (other commands won't work unless you do this first)
    print('Calibrating...')
    right_gripper.calibrate()
    rospy.sleep(2.0)
    #rospy.init_node('service_query')

    # Create the function used to call the service
    compute_ik = rospy.ServiceProxy('compute_ik', GetPositionIK)
    while not rospy.is_shutdown():
        input('Press [ Enter ]: ')
        
        # Construct the request
        request = GetPositionIKRequest()
        request.ik_request.group_name = "right_arm"

        # If a Sawyer does not have a gripper, replace '_gripper_tip' with '_wrist' instead
        link = "right_gripper_tip"

        request.ik_request.ik_link_name = link
        # request.ik_request.attempts = 20
        request.ik_request.pose_stamped.header.frame_id = "base"
        
        # Set the desired orientation for the end effector HERE
        flag = True
        gripper_flag = True 
        if flag:
            request.ik_request.pose_stamped.pose.position.x = 0.5
            request.ik_request.pose_stamped.pose.position.y = 0.5
            request.ik_request.pose_stamped.pose.position.z = 0     
            request.ik_request.pose_stamped.pose.orientation.x = 1.0
            request.ik_request.pose_stamped.pose.orientation.y = 0.0
            request.ik_request.pose_stamped.pose.orientation.z = 0.0
            request.ik_request.pose_stamped.pose.orientation.w = 0.0
            flag = False
        else:
            request.ik_request.pose_stamped.pose.position.x = 0.760
            request.ik_request.pose_stamped.pose.position.y = 0.227
            request.ik_request.pose_stamped.pose.position.z = -0.130        
            request.ik_request.pose_stamped.pose.orientation.x = 0.0
            request.ik_request.pose_stamped.pose.orientation.y = 1.0
            request.ik_request.pose_stamped.pose.orientation.z = 0.0
            request.ik_request.pose_stamped.pose.orientation.w = 0.0

        
        try:
            # Send the request to the service
            response = compute_ik(request)
            
            # Print the response HERE
            print(response)
            group = MoveGroupCommander("right_arm")

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
                if gripper_flag:
                    # Open the right gripper
                    print('Opening...')
                    right_gripper.open()
                    rospy.sleep(1.0)
                    print('Done!')

                    group.execute(plan[1])

                    # Close the right gripper
                    print('Closing...')
                    right_gripper.close()
                    rospy.sleep(1.0)
                else:
                    group.execute(plan[1])

                    # Open the right gripper
                    print('Opening...')
                    right_gripper.open()
                    rospy.sleep(1.0)
                    print('Done!')

                gripper_flag = not gripper_flag

            
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)

# Python's syntax for a main() method
if __name__ == '__main__':
    main()
