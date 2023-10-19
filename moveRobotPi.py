from pymycobot.mycobot import MyCobot
import time

board_size = 150
dim = 3

#gripper: Open 0, Close 1
def play(before, after):
    mc = MyCobot("/dev/ttyAMA0", 1000000)
    
    square_length = board_size/dim
    
    delay = 3

    x = ((before[0] - 1) * square_length) - 75
    y = ((before[1] - 1) * square_length) + 120
    z = 150

    rx = -170
    ry = -5
    rz = 125

    print("Before: ", x, y, z)

    mc.send_coords([x, y, z, rx, ry, rz], 20)
    time.sleep(delay)
    mc.send_coords([x, y, 100, rx, ry, rz], 20)
    time.sleep(delay)

    mc.set_gripper_state(1, 20)
    time.sleep(delay)

    if after == None:
        after = [4.5, 1.5]

    x = ((after[0] - 1) * square_length) - 75
    y = (after[1] - 1) * square_length + 120
    z = 150

    print("After: ", x, y, z)

    mc.send_coords([x, y, 100, rx, ry, rz], 20)
    time.sleep(delay)
    mc.set_gripper_state(0, 20)
    time.sleep(delay)
    mc.send_coords([x, y, z, rx, ry, rz], 20)
    time.sleep(delay)