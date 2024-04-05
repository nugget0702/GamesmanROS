from pymycobot.mycobot import MyCobot
from pymycobot.genre import Coord
import time



mc = MyCobot("/dev/ttyAMA0", 1000000)
mc.send_angles([0,0,0,0,0,0], 20)
mc.set_gripper_state(0, 20)
