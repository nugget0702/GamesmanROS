# GamesmanROS
Welcome to GamesCrafters Robotics!

This is our official codebase for OXSI, the GamesCrafters Robot!

# Intro
The objective of this project is to utilize the already existing GamesmanUNI interface to interact physically with games. Using the system with perfect-play information, we encode a robot to play any game perfectly with a human. This project utilizes Vision, Inverse Kinematics, Control, and Path Planning, to precisely pick-and-place pieces on a game board.

**The robot**

We are using the [_mycobot280pi_](https://shop.elephantrobotics.com/products/mycobot-pi-worlds-smallest-and-lightest-six-axis-collaborative-robot) robot from [Elephant Robotics](https://shop.elephantrobotics.com/products). 

**List of supported games:**

* Dodgem

*	Dao

* Connect-4 (In progress)

*	Fox-and-Hounds (In progress)


# Running the Robot

**Run the following commands, each in a seperate terminal.**

* The default serial port name of mycobot 280-Pi version is "/dev/ttyAMA0", and the baud rate is 1000000.

	`rosrun mycobot_280pi follow_display_gripper.py _port:=/dev/ttyAMA0 _baud:=1000000`
  
* Launch RViz to visualize current state of the robot
  
  `roslaunch mycobot_280pi mycobot_follow_gripper.launch`



