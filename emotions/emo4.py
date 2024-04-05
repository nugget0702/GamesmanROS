from pymycobot.mycobot import MyCobot
import time

#emotion: laugh by opening and closing gripper
def do_something():
    mc.send_angles([92.72,(-31.02),24.87,(-35.41),10.54,56.33],20)
    time.sleep(1)
    for count in range(2):
        mc.set_gripper_state(0,25)
        time.sleep(2)
        mc.set_gripper_state(1,25)
        time.sleep(2)

    
mc = MyCobot('/dev/ttyAMA0', 1000000)
do_something()
