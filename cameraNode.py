#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

def publish_video():
    # Initialize ROS node
    rospy.init_node('video_publisher', anonymous=True)
    # Create a publisher object
    image_pub = rospy.Publisher("/video_stream", Image, queue_size=10)
    # Initialize the bridge between ROS and OpenCV
    bridge = CvBridge()

    # Capture video from the default camera
    cap = cv2.VideoCapture(0)

    # Check if the video capture is opened successfully
    if not cap.isOpened():
        rospy.logerr("Error opening video stream or file")
        return

    # Set the loop rate
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if ret:
            try:
                # Convert the OpenCV image to a ROS message
                ros_image = bridge.cv2_to_imgmsg(frame, "bgr8")
            except CvBridgeError as e:
                rospy.logerr(e)

            # Publish the ROS message
            image_pub.publish(ros_image)
        else:
            rospy.loginfo("Frame capture failed")

        rate.sleep()

    # Release the video capture object
    cap.release()

if __name__ == '__main__':
    try:
        publish_video()
    except rospy.ROSInterruptException:
        pass
