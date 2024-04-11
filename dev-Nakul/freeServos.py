import pymycobot

mc = pymycobot.MyCobot("/dev/ttyAMA0", baudrate=1000000)

mc.release_all_servos()