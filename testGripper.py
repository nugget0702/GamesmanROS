from pymycobot.mycobot import MyCobot
import time

mc = MyCobot('/dev/ttyAMA0',1000000)
print(mc.get_gripper_value())
