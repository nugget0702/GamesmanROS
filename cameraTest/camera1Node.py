import rospy
from sensor_msgs.msg import Image, PointCloud2

'''
Republishes on the Raspberry Pi some of the topics populated by the Jetson Nano.
This enables the external computer to read these topics.
'''


def send_image(msg):
        '''
        Input:
           msg: Image
        '''
        pub = rospy.Publisher('/camera/raw_image_feed', Image, queue_size=1)
        pub.publish(msg)


# def send_left_undistorted(msg):
#         '''
#         Input:
#            msg: Image
#         '''
#         #print('Image received')
#         pub = rospy.Publisher('/camera14/left_undist_image_feed', Image, queue_size=1)
#         pub.publish(msg)


# def send_right_undistorted(msg):
#         '''
#         Input:
#            msg: Image
#         '''
#         pub = rospy.Publisher('camera14/right_undist_image_feed', Image, queue_size=1)
#         pub.publish(msg)


# def send_pointcloud(msg):
#         '''
#         Input:
#            msg: PointCloud2
#         '''
#         #print('pointcloud received')
#         pub = rospy.Publisher('/camera1/point_cloud', PointCloud2, queue_size=1)
#         pub.publish(msg)



if __name__=='__main__':

        rospy.init_node("camera_relay_node", anonymous=True)

        rospy.Subscriber("/camera/front", Image, send_image)

        rospy.spin()