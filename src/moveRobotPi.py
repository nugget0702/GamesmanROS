from pymycobot.mycobot import MyCobot
from pymycobot.genre import Coord
import time

board_size = 150
dim = 3

#gripper: Open 0, Close 1
def play(before, after):
    mc = MyCobot("/dev/ttyAMA0", 1000000)
    mc.power_on()
    square_length = board_size/dim
    
    delay = 2
    speed = 30

    gripper_delay = 3
    gripper_speed = 30

    x = ((before[0] - 1) * square_length) - 75
    y = ((before[1] - 1) * square_length) + 105
    z = 185

    rx = 171
    ry = 7
    rz = -52

    pickup_z = 150

    print("Before: ", x, y, z)
    mc.set_gripper_state(0, gripper_speed)
    time.sleep(gripper_delay)

    mc.send_coords([x, y, z, rx, ry, rz], speed, 0)
    time.sleep(delay)

    mc.send_coords([x, y, pickup_z, rx, ry, rz], speed, 0)
    time.sleep(delay)
    
    mc.set_gripper_state(1, gripper_speed)
    time.sleep(gripper_delay)

    mc.send_coords([x, y, z, rx, ry, rz], speed, 0)
    time.sleep(delay)

    if after == None:
        after = [4.5, 1.5]

    x = ((after[0] - 1) * square_length) - 75
    y = ((after[1] - 1) * square_length) + 110

    print("After: ", x, y, z)

    mc.send_coords([x, y, z, rx, ry, rz], speed, 0)
    time.sleep(delay)
    
    mc.send_coords([x, y, pickup_z, rx, ry, rz], speed, 0)
    time.sleep(delay)

    mc.set_gripper_state(0, gripper_speed)
    time.sleep(gripper_delay)

    mc.send_coords([x, y, z, rx, ry, rz], speed, 0)
    time.sleep(delay)
