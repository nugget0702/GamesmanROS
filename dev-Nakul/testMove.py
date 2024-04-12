import moveRobot
from geometry_msgs.msg import PoseStamped, Point, Pose

acutation = moveRobot.Acutate()

piece_pose = Pose()
piece_pose.position.x = -0.002
piece_pose.position.y = 0.17
piece_pose.position.z = 0.17
piece_pose.orientation.x = 0
piece_pose.orientation.y = -1
piece_pose.orientation.z = 0
piece_pose.orientation.w = 0

acutation.move(piece_pose)