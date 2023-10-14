from pymycobot.mycobot import MyCobot

board_size = 250
dim = 3


def play(before, after):
    mc = MyCobot("/dev/ttyAMA0", 1000000)
    
    square_length = 250/3

    x = (before[0] - 1) * square_length
    y = (before[1] - 1) * square_length
    z = 150

    rx = 170
    ry = 5
    rz = -50

    mc.send_coords([x, y, z, rx, ry, rz], 20)
    mc.send_coords([x, y, z, 100, rx, ry, rz], 20)

    mc.set_gripper_state(0, 20)

    if after == None:
        after = [4.5, 1.5]

    x = (after[0] - 1) * square_length
    y = (after[1] - 1) * square_length
    z = 150

    mc.send_coords([x, y, z, rx, ry, rz], 20)
    mc.send_coords([x, y, z, 100, rx, ry, rz], 20)

    mc.set_gripper_state(1, 20)

    mc.send_coords([0, 100, z, rx, ry, rz], 20)