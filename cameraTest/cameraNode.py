#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError
import cv2

def publish_video_and_info():
    # Initialize ROS node
    rospy.init_node('video_publisher', anonymous=True)
    # Create publishers for both Image and CameraInfo topics
    image_pub = rospy.Publisher("/camera_raw", Image, queue_size=10)
    info_pub = rospy.Publisher("/camera_info", CameraInfo, queue_size=10)
    # Initialize the bridge between ROS and OpenCV
    bridge = CvBridge()

    # Capture video from the default camera
    cap = cv2.VideoCapture(0)

    # Check if video capture is opened successfully
    if not cap.isOpened():
        rospy.logerr("Error opening video stream or file")
        return

    # Placeholder for CameraInfo - adjust these values
    camera_info = CameraInfo()
    camera_info.header.frame_id = "camera_link"
    camera_info.width = 1280  # Adjust according to your camera's resolution
    camera_info.height = 720  # Adjust according to your camera's resolution
    # Note: Properly fill other fields such as D (distortion coefficients),
    # K (camera matrix), R (rectification matrix), P (projection matrix) based on your camera's calibration

    # Set the loop rate
    rate = rospy.Rate(10)  # 10hz

    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if ret:
            try:
                # Convert the OpenCV image to a ROS message
                ros_image = bridge.cv2_to_imgmsg(frame, "bgr8")
                ros_image.header.stamp = rospy.Time.now()  # Synchronize timestamp
                camera_info.header.stamp = ros_image.header.stamp
            except CvBridgeError as e:
                rospy.logerr(e)

            # Publish the ROS messages
            image_pub.publish(ros_image)
            info_pub.publish(camera_info)
        else:
            rospy.loginfo("Frame capture failed")

        rate.sleep()

    # Release the video capture object
    cap.release()

if __name__ == '__main__':
    try:
        publish_video_and_info()
    except rospy.ROSInterruptException:
        pass
