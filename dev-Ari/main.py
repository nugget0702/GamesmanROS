import requests
import moveRobot
from follow_display import robot

URL = "https://nyc.cs.berkeley.edu/universal/v1/"

# Don't TOUCH Code blocks below!
######################### Get All Games #####################################
games_data = requests.get(url=URL).json()
print(games_data)
for i in range(len(games_data)):
    print(i, " : ", games_data[i]['name'])
user_game = int(input("Pick the index of the game you want to play: "))

URL = URL + games_data[user_game]["name"].lower() + '/'
#############################################################################


############## Get Variant and Starting Positon #############################
variants_data = requests.get(url=URL).json()['variants']
for j in range(len(variants_data)):
    print(j, " : ", variants_data[j]["id"])
user_variant = int(input("Pick the index of the variant you want to play: "))
variant = variants_data[user_variant]["id"]
URL = URL + variant + '/'
variants_data = requests.get(url=URL).json()
starting_position = variants_data["startPosition"]
##############################################################################


############################# Meta Data  #####################################
Static_URL = URL + "/positions/?p="
theme = list(variants_data["imageAutoGUIData"]["themes"].keys())[0]
centers = variants_data["imageAutoGUIData"]["themes"][theme]["centers"]
###############################################################################

# Input: starting position string and ending position string
# Output: List of start coord and end cood [[x1, y1], [x2, y2]]


def position_to_coord(start, end):
    start_cord = None
    end_cord = None

    start = start[2:]
    end = end[2:]

    if len(start) != len(end):
        print("error")
        exit()
    else:
        for i in range(len(start)):
            if start[i] != end[i]:
                if start[i] == "-":
                    end_cord = centers[i]
                else:
                    start_cord = centers[i]
        return [start_cord, end_cord]


# Input: starting coord and ending coord
# Output: List of start position string and end position string ["RA_3_3_000", "RA_3_3_01230"]
def coor_to_position(postion, start, end):
    start_index = centers.index(start)
    end_index = centers.index(end)

    return postion[:start_index] + postion[end_index] + postion[start_index+1:end_index] + postion[start_index] + postion[end_index+1:]

###############################################################################
################################################################################


# Work here!
Dynamic_URL = Static_URL + starting_position

# List of available moves from starting position
moves_data = requests.get(url=Dynamic_URL).json()['moves']


def pick_best_position(moves):
    position_values = {}
    for i in range(len(moves)):
        if moves[i]['moveValue'] not in position_values:
            position_values[moves[i]['moveValue']] = [moves[i]['position']]
        else:
            position_values[moves[i]['moveValue']].append(moves[i]['position'])

    if 'win' in position_values and len(position_values['win']) > 0:
        return position_values['win'][0]
    elif 'draw' in position_values and len(position_values['draw']) > 0:
        return position_values['draw'][0]
    elif 'lose' in position_values and len(position_values['lose']) > 0:
        return position_values['lose'][0]
    else:
        print('error: in pick_best_postion')
        exit()

pieces = {str(c) : "" for c in centers}

#Initialize Board Pieces
#TODO
pieces["[0.5, 1.5]"] = "ar_marker_0"
pieces["[0.5, 2.5]"] = "ar_marker_3"
pieces["[1.5, 3.5]"] = "ar_marker_1"
pieces["[2.5, 3.5]"] = "ar_marker_6"

A_turn = True
while (len(moves_data) > 0):
    if A_turn:
        new_position = pick_best_position(moves_data)
        move_coords = position_to_coord(starting_position, new_position)
        start_coord, end_coord = (str(move_coords[0]), str(move_coords[1]))

        ar_tag_piece = pieces[start_coord]
        pieces[end_coord] = ar_tag_piece
        pieces[start_coord] = ""

        print("A : ", start_coord, end_coord, ar_tag_piece)
        flag = False
        while not flag:
            user = input("Enter y and Press ENTER: ")
            flag = user == 'y'
        
        robot.pickUp(ar_tag_piece)
        robot.place(move_coords[1])

        Dynamic_URL = Static_URL + new_position
        moves_data = requests.get(url=Dynamic_URL).json()['moves']
        starting_position = new_position
        A_turn = False
    else:
        new_position = pick_best_position(moves_data)
        move_coords = position_to_coord(starting_position, new_position)
        start_coord, end_coord = (str(move_coords[0]), str(move_coords[1]))

        ar_tag_piece = pieces[start_coord]
        pieces[end_coord] = ar_tag_piece
        pieces[start_coord] = ""

        print("B : ", move_coords, ar_tag_piece)
        flag = False
        while not flag:
            user = input("Enter y and Press ENTER: ")
            flag = user == 'y'
        
        robot.pickUp(ar_tag_piece)
        robot.place(move_coords[1])
        
        Dynamic_URL = Static_URL + new_position
        moves_data = requests.get(url=Dynamic_URL).json()['moves']
        starting_position = new_position
        A_turn = True
