
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
import tf

from geometry_msgs.msg import Point, PointStamped, Quaternion, QuaternionStamped, Pose
from std_msgs.msg import Header

#Define the method which contains the main functionality of the node.
def findPiece(ar_frame):
  """
  Locates the position of a provided piece

  Inputs:
  - ar_frame: the tf frame of the AR tag on a given piece
  """

  ################################### YOUR CODE HERE ##############

  #Create a publisher and a tf buffer, which is primed with a tf listener
  pub = rospy.Publisher('/piece_location_' + ar_frame, Pose, queue_size=10)
  tfBuffer = tf2_ros.Buffer()
  tfListener = tf2_ros.TransformListener(tfBuffer)


  tf_listener = tf.TransformListener()
  tfbr = tf.TransformBroadcaster()

  # Create a timer object that will sleep long enough to result in
  # a 10Hz publishing rate
  r = rospy.Rate(10) # 10hz

  # Loop until the node is killed with Ctrl-C
  while not rospy.is_shutdown():
    try:
      cam_to_base_trans = tfBuffer.lookup_transform("joint1", "usb_cam", rospy.Time())
      ar_tag_trans = tfBuffer.lookup_transform("usb_cam", ar_frame, rospy.Time())

      #TODO MODIFY THIS OFFSET
      # Process trans to get your state error
      cam_trans_x = cam_to_base_trans.transform.translation.x
      cam_trans_y = cam_to_base_trans.transform.translation.y
      cam_trans_z = cam_to_base_trans.transform.translation.z

      cam_rot_x = cam_to_base_trans.transform.rotation.x
      cam_rot_y = cam_to_base_trans.transform.rotation.y
      cam_rot_z = cam_to_base_trans.transform.rotation.z
      cam_rot_w = cam_to_base_trans.transform.rotation.w

      input_x = ar_tag_trans.transform.translation.x
      input_y = ar_tag_trans.transform.translation.y 
      input_z = ar_tag_trans.transform.translation.z

      tfbr.sendTransform((cam_trans_x, cam_trans_y, cam_trans_z),
                        (0, 0, 0, 1),
                        rospy.Time.now(),
                        "aligned_usb_cam",
                        "joint1")
      tfbr.sendTransform((input_x, -input_y+0.05, 0),
                        (0, 0, 0, 1),
                        rospy.Time.now(),
                        "marker0 " + ar_frame,
                        "aligned_usb_cam")
      
      ar_tag_trans = tfBuffer.lookup_transform("aligned_usb_cam", "marker0 " + ar_frame, rospy.Time())

      #TODO MODIFY THIS OFFSET
      # Process trans to get your state error

      input_x = ar_tag_trans.transform.translation.x
      input_y = ar_tag_trans.transform.translation.y 
      input_z = ar_tag_trans.transform.translation.z


      piece = Point()
      piece.x = input_x
      piece.y = input_y
      piece.z = input_z

      orientation = Quaternion()
      orientation.x = ar_tag_trans.transform.rotation.x
      orientation.y = ar_tag_trans.transform.rotation.y
      orientation.z = ar_tag_trans.transform.rotation.z
      orientation.w = ar_tag_trans.transform.rotation.w


      tf_listener.waitForTransform("joint1", "aligned_usb_cam", rospy.Time(), rospy.Duration(10.0))
      center_in_base = tf_listener.transformPoint("joint1", PointStamped(header=Header(stamp=rospy.Time(), frame_id="aligned_usb_cam"), point=piece))
      orientation_in_base = tf_listener.transformQuaternion("joint1", QuaternionStamped(header=Header(stamp=rospy.Time(), frame_id="usb_cam"), quaternion=orientation))

      piece_pose = Pose()
      piece_pose.position.x = center_in_base.point.x
      piece_pose.position.y = center_in_base.point.y
      piece_pose.position.z = center_in_base.point.z
      piece_pose.orientation.x = orientation_in_base.quaternion.x
      piece_pose.orientation.y = orientation_in_base.quaternion.y
      piece_pose.orientation.z = orientation_in_base.quaternion.z
      piece_pose.orientation.w = orientation_in_base.quaternion.w


      #################################### end your code ###############
      pub.publish(piece_pose)
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
