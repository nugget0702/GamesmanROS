import pymycobot

observe = [126.65, 9.31, -80.85, -13.97, 11.95, 88.76]

mc = pymycobot.MyCobot("/dev/ttyAMA0", baudrate=1000000)
mc.send_angles(observe, 20)