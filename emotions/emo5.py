from pymycobot.mycobot import MyCobot
import time

#emotion: wave hands
def do_something():
    for count in range(2):
        mc.send_angles([0,0,(-0.17),90,13.79,(-42.89)],25)
        time.sleep(1)
        mc.send_angles([0,25,(-0.17),90,13.79,(-42.89)],25)
        time.sleep(1.2)
        mc.send_angles([0,-35,(-0.17),90,13.79,(-42.89)],25)
        time.sleep(1.45)
    mc.send_angles([0,0,(-0.17),90,13.79,(-42.89)],25)

mc = MyCobot('/dev/ttyAMA0', 1000000)
do_something()
