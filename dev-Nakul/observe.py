import pymycobot

observe = [132.89, 15.55, -40.51, -45.79, 10.45, 95]

mc = pymycobot.MyCobot("/dev/ttyAMA0", baudrate=1000000)
mc.send_angles(observe, 20)