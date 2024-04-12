import moveRobot
from geometry_msgs.msg import PoseStamped, Point

acutation = moveRobot.Acutate()

point = Point()
point.x = -0.057
point.y = 0.130
point.z = 0.171

acutation.move(point, True)