from pymycobot.mycobot import MyCobot
import time

# board_size = 150
# dim = 3

mapping = {}

mapping["[3.5, 1.5]"] = [99.05, 3.6, -133.94, 38.49, 8.96, 76.02]
mapping["[2.5, 1.5]"] = [113.73, 7.2, -139.3, 42.09, 13.35, 85.95]
mapping["[1.5, 1.5]"] = [132.18, 5.09, -139.13, 45.87, 13, 105.55]
mapping["[1.5, 2.5]"] = [122.08, -18.28, -114.69, 47.37, 12.74, 96.06]
mapping["[2.5, 2.5]"] = [109.51, -19.16, -112.32, 42.89, 12.04, 83.67]
mapping["[3.5, 2.5]"] = [91.75, -23.46, -103.79, 37.88, 16.08, 65.56]
mapping["[3.5, 3.5]"] = [93.77, -44.47, -67.76, 23.29, 13.09, 67.5]
mapping["[2.5, 3.5]"] = [103.44, -41.04, -75.05, 28.3, 15.2, 80.24]
mapping["[1.5, 3.5]"] = [113.37, -42.18, -74.97, 31.46, 17.05, 87.62]
mapping["lift"] = [109.51, 25.31, -73.47, -19.16, 5.8, 69.34]
mapping["[4.5, 1.5]"] = [66.09, -27.5, -75.05, 14.5, 12.48, 37.79]

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

    if after[0] + 1 == 4.5 or after[1] == 0.5:
        after = [4.5, 1.5]

    mc.send_angles(mapping[str([after[0] + 1, after[1]])], 20)
    time.sleep(delay)
    mc.set_gripper_state(0, 20)
    time.sleep(delay)
    mc.send_angles(mapping["lift"], 20)
    time.sleep(delay)