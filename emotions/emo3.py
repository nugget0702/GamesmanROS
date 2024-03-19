from pymycobot.mycobot import MyCobot
import time

#emotion: nod by moving the claw up and down
def do_something():
    mc.send_angles([94.21,(-20.91),24.96,(-90),9.58,57.39],25)
    time.sleep(3)
    for count in range(2):
        mc.send_angles([94.21,(-20.91),24.96,(-29.26),9.58,57.39],28)
        time.sleep(1.5)
        mc.send_angles([94.21,(-20.91),24.96,(-90),9.58,57.39],28)
        time.sleep(1.5)

    
mc = MyCobot('/dev/ttyAMA0', 1000000)
do_something()
