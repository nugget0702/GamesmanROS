import moveRobot
from geometry_msgs.msg import PoseStamped, Point

acutation = moveRobot.Acutate()

point = Point()
point.x = 0.0
point.y = 0.18
point.z = 0.2

acutation.move(point, True)