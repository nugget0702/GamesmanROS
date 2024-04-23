import math
import time
from geometry_msgs.msg import PoseStamped, Point, Pose
import rospy


def findCoord(armarker):
    '''
    Takes in armarker 1, 3, 6, or 0 and returns its fuzzy (real) coordinates
    '''
    print(armarker)
    def getCurrentCord(pose):
        print(pose)
        return pose.position

    rospy.Subscriber('/piece_location_' + armarker, Pose, getCurrentCord) 

def readBoard():
    '''
    1. Initializes a boardstate and list of ar_markers: done
    2. Calls FindCoord and stores real/fuzzy values for all the armarkers on the board: 
    3. Converts fuzzy values to ideal values using real_to_ideal (real = fuzzy)
    4. Converts ideal values to indices using getIndex
    5. Updates the Boardstate 
    6. Updates MoveData and A_Turn = True because Human has finished moving 
    '''

    def real_to_ideal(x, y):
        def shift_left(x):
            return (x + 0.075) * 20
        def shift_down(y):
            return (y - 0.1) * 20
        return [shift_left(x), shift_down(y)]
    
    
    def getIndex(x, y):
        x, y = real_to_ideal(x, y)
        y = 3 - y
        x = math.ceil(x)
        y = math.floor(y)
        indice = x + 3*y
        return indice
    
    boardState = '1_---------'
    armarkers = ["ar_marker_0", "ar_marker_1", "ar_marker_3", "ar_marker_6"]
    for armarker in armarkers:
        coord1 = findCoord(armarker)
        index = getIndex(coord1[0], coord1[1])
        boardState[index + 1] = 'x' if armarker in [1,6] else 'o'

    return boardState



while True:

    board = readBoard()
    print(board)

    for i in range(10):
        print(i+1)
        time.sleep(1)