from pymycobot.mycobot import MyCobot
import time

#emotion: greet by bowing 
def do_something():

    mc.send_angles([94.21,(-19.95),25.4,(-106.69),9.66,57.12],20)
    time.sleep(2)
    mc.send_angles([91.49,(-90.79),25.75,(-24.25),(9.66),59.58],25)
    time.sleep(2)
    mc.send_angles([94.21,(-19.95),25.4,(-106.69),9.66,57.12],20)



mc = MyCobot('/dev/ttyAMA0', 1000000)
do_something()
