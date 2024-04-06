
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
def findPiece(ar_frame):
  """
  Locates the position of a provided piece

  Inputs:
  - ar_frame: the tf frame of the AR tag on a given piece
  """

  ################################### YOUR CODE HERE ##############

  #Create a publisher and a tf buffer, which is primed with a tf listener
  pub = rospy.Publisher('/piece_location_' + ar_frame, Point, queue_size=10)
  tfBuffer = tf2_ros.Buffer()
  tfListener = tf2_ros.TransformListener(tfBuffer)
  
  # Create a timer object that will sleep long enough to result in
  # a 10Hz publishing rate
  r = rospy.Rate(10) # 10hz

  # Loop until the node is killed with Ctrl-C
  while not rospy.is_shutdown():
    try:
      ar_tag_trans = tfBuffer.lookup_transform("joint1", ar_frame, rospy.Time())
      
      #TODO MODIFY THIS OFFSET
      # Process trans to get your state error

      input_x = ar_tag_trans.transform.translation.x
      input_y = ar_tag_trans.transform.translation.y 
      input_z = ar_tag_trans.transform.translation.z
      input_vector = np.array([input_x, input_y, input_z, 1])

      piece = Point()
      piece.x = input_y
      piece.y = input_x
      piece.z = input_z
      #################################### end your code ###############
      pub.publish(piece)
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
  rospy.init_node('piece_locator0', anonymous=True)

  try:
    findPiece(sys.argv[1])
  except rospy.ROSInterruptException:
    pass
