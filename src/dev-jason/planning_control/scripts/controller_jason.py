#!/usr/bin/env python
from pymycobot.mycobot import MyCobot
import time
import rospy
from mycobot_280pi_moveit.msg import move_piece_msg

#/move_piece
#controller node will subscribe to it
#the planning node will publish to it

global mc

def move_piece_callback(self,msg):
    global mc 
    mc.send_angles(msg.piece_location, msg.movement_speed)
    time.sleep(msg.delay_between_movements)
    mc.set_gripper_state(0, msg.movement_speed)
    time.sleep(msg.delay_between_movements)

    mc.send_angles(msg.piece_destination, msg.movement_speed)
    time.sleep(msg.delay_between_movements)
    mc.set_gripper_state(0, msg.movement_speed)
    time.sleep(msg.delay_between_movements)

def mycobot_controller():
    mc = MyCobot("/dev/ttyAMA0", 1000000)
    rospy.init_node('mycobot_controller_jason', anonymous=True)
    rospy.Subscriber("/move_piece", move_piece_msg, move_piece_callback)
    rospy.spin()

if __name__ == '__main__':
    mycobot_controller()

#create message definition 
#determine the datatype for each message element (piece locaiton, piece destination, movement speed)
#movment speed int8
#piece location (list)