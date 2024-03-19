from pymycobot.mycobot import MyCobot
import time

#emotion: no by shaking the claw
def do_something():
    for count in range(2):
        mc.send_angles([91.49,(-31.55),25.75,(-82.96),11.07,59.58],25)
        time.sleep(1)
        mc.send_angles([91.49,(-31.55),25.75,(-82.96),(-19.77),59.58],25)
        time.sleep(1)
        mc.send_angles([91.49,(-31.55),25.75,(-82.96),39.72,59.58],25)
        time.sleep(1.45)
    mc.send_angles([91.49,(-31.55),25.75,(-82.96),11.07,59.58],25)

mc = MyCobot('/dev/ttyAMA0', 1000000)
do_something()
