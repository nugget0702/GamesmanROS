from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import math
import time

mc = MyCobot('/dev/ttyAMA0',1000000)
rads = [-2.2733737772461615, 0.7847171682458266, 1.5168949721746356, 2.410781516217261, -6.372646103244947e-06, -0.7025809416689617]


deg = [math.degrees(i) for i in rads]

print(deg)

mc.send_radians([0,0,0,0,0,0], 5)
print("Waiting for 5")
time.sleep(5)
print("moving")
mc.send_radians(rads, 10)
print("Waiting for 5")
time.sleep(5)
