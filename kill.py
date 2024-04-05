from pymycobot.mycobot import MyCobot

from pymycobot.mycobot import MyCobot


mc = MyCobot('/dev/ttyAMA0',1000000)
mc.release_all_servos()
mc.power_off()
