import rospy
import tf
from ar_track_alvar_msgs.msg import AlvarMarkers

def callback(data):
    br = tf.TransformBroadcaster()
    for marker in data.markers:
        # The received pose of the AR tag
        position = marker.pose.pose.position
        orientation = marker.pose.pose.orientation
        
        # Define a rotation of 90 degrees around the Z-axis
        quaternion_rotation = tf.transformations.quaternion_from_euler(0, 0, 1.5708) # 1.5708 radians = 90 degrees
        
        # Multiply the received orientation by the rotation
        # Assuming the received orientation is also a quaternion
        new_orientation = tf.transformations.quaternion_multiply([orientation.x, orientation.y, orientation.z, orientation.w], quaternion_rotation)
        
        # Now broadcast this new transformation
        br.sendTransform((position.x, position.y, position.z),
                         new_orientation,
                         rospy.Time.now(),
                         "modified_ar_tag_" + str(marker.id),
                         "usb_cam") # Assuming the camera frame is the parent frame

if __name__ == '__main__':
    rospy.init_node('modify_ar_tag_axis')
    rospy.Subscriber("/ar_pose_marker", AlvarMarkers, callback)
    rospy.spin()