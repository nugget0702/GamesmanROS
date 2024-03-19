from pymycobot.mycobot import MyCobot
import time

# board_size = 150
# dim = 3

mapping = {}

mapping["[3.5, 1.5]"] = [98.52, 12.65, -128.93, 26.01, 10.89, 58.35]
mapping["[2.5, 1.5]"] = [113.37, 12.21, -127.52, 24.34, 13.18, 76.46]
mapping["[1.5, 1.5]"] = [134.12, 10.72, -128.32, 28.38, 10.63, 93.25]
mapping["[1.5, 2.5]"] = [123.31, -17.13, -95.36, 19.86, 11.42, 87.09]
mapping["[2.5, 2.5]"] = [110.3, -13.53, -103.97, 27.68, 11.16, 72.94]
mapping["[3.5, 2.5]"] = [98.17, -13.62, -103.97, 28.3, 9.31, 58.27]
mapping["[3.5, 3.5]"] = [98.17, -34.1, -73.91, 21.09, 8.7, 57.21]
mapping["[2.5, 3.5]"] = [106.87, -33.83, -73.91, 20.39, 11.33, 68.55]
mapping["[1.5, 3.5]"] = [118.91, -41.48, -59.15, 10.63, 10.28, 80.06]
mapping["lift"] = [109.51, 25.31, -73.47, -19.16, 5.8, 69.34]
mapping["[4.5, 1.5]"] = [81.29, -25.75, -86.3, 22.93, 10.72, 45.87]

#gripper: Open 0, Close 1
def play(before, after):
    mc = MyCobot("/dev/ttyAMA0", 1000000)    
    delay = 3

    mc.send_angles(mapping["lift"], 20)
    time.sleep(delay)
    mc.set_gripper_state(0, 20)
    time.sleep(delay)

    mc.send_angles(mapping[str([before[0] + 1, before[1]])], 20)
    time.sleep(delay)
    mc.set_gripper_state(1, 20)
    time.sleep(delay)
    mc.send_angles(mapping["lift"], 20)
    time.sleep(delay)

    if after == None:
        after = [4.5, 1.5]

    mc.send_angles(mapping[str([after[0] + 1, after[1]])], 20)
    time.sleep(delay)
    mc.set_gripper_state(0, 20)
    time.sleep(delay)
    mc.send_angles(mapping["lift"], 20)
    time.sleep(delay)