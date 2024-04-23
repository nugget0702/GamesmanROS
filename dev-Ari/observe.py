import pymycobot

observe = [139.3, -0.17, -46.23, -37.88, 10.45, 113.55]

mc = pymycobot.MyCobot("/dev/ttyAMA0", baudrate=1000000)
mc.send_angles(observe, 20)