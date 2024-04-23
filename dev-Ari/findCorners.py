
#!/usr/bin/env python
#The line above tells Linux that this file is a Python script,
#and that the OS should use the Python interpreter in /usr/bin/env
#to run it. Don't forget to use "chmod +x [filename]" to make
#this script executable.

#Import the rospy package. For an import to work, it must be specified
#in both the package manifest AND the Python file in which it is used.
import rospy
import tf2_ros
import sys
import Quaternions
import numpy as np

from geometry_msgs.msg import Point

#Define the method which contains the main functionality of the node.
def findCorners(ar_frame_corner1, ar_frame_corner2):
  """
  Locates the position of a provided piece

  Inputs:
  - ar_frame_corner1: the tf frame of the AR tag on a given corner1
  - ar_frame_corner2: the tf frame of the AR tag on a given corner2

  """

  ################################### YOUR CODE HERE ##############

  #Create a publisher and a tf buffer, which is primed with a tf listener
  pub = rospy.Publisher('/corners_locations', [Point, Point], queue_size=10)
  tfBuffer = tf2_ros.Buffer()
  tfListener = tf2_ros.TransformListener(tfBuffer)
  
  # Create a timer object that will sleep long enough to result in
  # a 10Hz publishing rate
  r = rospy.Rate(10) # 10hz

  # Loop until the node is killed with Ctrl-C
  while not rospy.is_shutdown():
    try:
      ar_corner1_trans = tfBuffer.lookup_transform("usb_cam", ar_frame_corner1, rospy.Time())
      ar_corner2_trans = tfBuffer.lookup_transform("usb_cam", ar_frame_corner2, rospy.Time())
      
      #TODO MODIFY THIS OFFSET
      # Process trans to get your state error
      offset_x = None
      offset_y = None
      offset_z = None

      input_x = ar_corner1_trans.transform.translation.x + offset_x
      input_y = ar_corner1_trans.transform.translation.y + offset_y
      input_z = ar_corner1_trans.transform.translation.z + offset_z

      input_vector = np.array([input_x, input_y, input_z, 1]).T

      gripper_trans = tfBuffer.lookup_transform("joint1", "gripper_base", rospy.Time())
      t_x = gripper_trans.transform.translation.x
      t_y = gripper_trans.transform.translation.y
      t_z = gripper_trans.transform.translation.z

      q_x = gripper_trans.transform.rotation.x
      q_y = gripper_trans.transform.rotation.y
      q_z = gripper_trans.transform.rotation.z
      q_w = gripper_trans.transform.rotation.w
      q = [q_w, q_x, q_y, q_z]

      rot_matrix = Quaternions.quaternion_rotation_matrix(q)
      transform_matrix = np.zeros((4, 4))
      for i in range(3):
          for j in range(3):
            transform_matrix[i][j] = rot_matrix[i][j]
      
      transform_matrix[0][3] = t_x
      transform_matrix[1][3] = t_y
      transform_matrix[2][3] = t_z
      transform_matrix[3][3] = 1
      
      piece_location1 = (transform_matrix @ input_vector)
      piece1 = Point()
      piece1.x = piece_location1[0]
      piece1.y = piece_location1[1]
      piece1.z = piece_location1[2]


      input_x = ar_corner2_trans.transform.translation.x + offset_x
      input_y = ar_corner2_trans.transform.translation.y + offset_y
      input_z = ar_corner2_trans.transform.translation.z + offset_z

      input_vector = np.array([input_x, input_y, input_z, 1]).T

      piece_location2 = (transform_matrix @ input_vector)
      piece2 = Point()
      piece2.x = piece_location2[0]
      piece2.y = piece_location2[1]
      piece2.z = piece_location2[2]

      #################################### end your code ###############

      pub.publish([piece_location1, piece_location2])
    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
      print("error: ", e)
      pass
      # Use our rate object to sleep until it is time to publish again
      r.sleep()

      
# This is Python's sytax for a main() method, which is run by default
# when exectued in the shell
if __name__ == '__main__':
  # Check if the node has received a signal to shut down
  # If not, run the talker method

  #Run this program as a new node in the ROS computation graph 
  #called /turtlebot_controller.
  rospy.init_node('piece_locator3', anonymous=True)

  try:
    findPiece(sys.argv[1])
  except rospy.ROSInterruptException:
    pass