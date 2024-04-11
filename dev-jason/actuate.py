# !/usr/bin/env python
import rospy
# The desired final position
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point
from moveit_commander import MoveGroupCommander
#import sys

# This and the end_callback passe in the newest data into the combined function so that both
# data can be used for path planning and actuation
def current_callback():
    return

def end_callback():
    return

def bind_callback_data():
    return

# Given: current_joint_configuration and final position for the end effector

def listener():
    
    rospy.Subscriber("/joint_states", JointState, current_callback)

    rospy.Subscriber("/end_position", Point, end_callback)
    
    rospy.spin()

    return

if __name__ == '__main__':

    # Initialize the subscriber node that listens for the current and end positions
    rospy.init_node('moveit_actuation_listener')

    # Call the listener
    listener()



