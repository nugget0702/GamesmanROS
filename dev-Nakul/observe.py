import pymycobot

observe = [131.13, 5.53, -50.53, -37.08, 13.27, 91.93]

mc = pymycobot.MyCobot("/dev/ttyAMA0", baudrate=1000000)
mc.send_angles(observe, 20)