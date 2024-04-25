import requests
# import moveRobotPi
# from test import newCenters, board_size, findScaler

URL = "https://nyc.cs.berkeley.edu/universal/v1/"

# Don't TOUCH Code blocks below!
######################### Get All Games #####################################
games_data = requests.get(url=URL).json()
print(games_data)
for i in range(len(games_data)):
    print(i, " : ", games_data[i]['id'])
user_game = int(input("Pick the index of the game you want to play: "))
URL = URL + games_data[user_game]['id'] + '/'
#############################################################################


########################## Get Variant #######################################
variants_data = requests.get(url=URL).json()['variants']
for j in range(len(variants_data)):
    print(j, " : ", variants_data[j]["id"])
user_variant = int(input("Pick the index of the variant you want to play: "))
variant = variants_data[user_variant]["id"]
##############################################################################


################# Get Starting Positon and Meta Data  #######################
Static_URL = URL + variant
static_data = requests.get(url=Static_URL).json()
theme = list(static_data["imageAutoGUIData"]["themes"].keys())[0]
centers = static_data["imageAutoGUIData"]["themes"][theme]["centers"]
starting_position = static_data["startPosition"]
###############################################################################

# Input: starting position string and ending position string
# Output: List of start coord and end cood [[x1, y1], [x2, y2]]

# In the server, the first coord val is row and second val is column
# Both 6x6 and 6x7 connect4 are supported by this implementation

connect4_col_coord_map = {0.5: 1, 1.5: 2, 2.5: 3, 3.5: 4, 4.5: 5, 5.5: 6, 6.5: 7}
connect4_row_coord_map = {1.5: 6, 2.5: 5, 3.5: 4, 4.5: 3, 5.5: 2, 6.5: 1}

def connect4_position_to_coord(start, end):
    moves = []
    # For connect 4, you are always grabbing a new piece, similar to the grabbing new piece part of achi.
    start_cord = "grab_new_piece"
    end_cord = None

    start = start[2:]
    end = end[2:]

    if len(start) != len(end) or start == end:
        print("error: invalid connect4_position_to_coord inputs")
        exit()
    else:
        if variant == 0:
            for i in range(len(start)):
                if start[i] != end[i]:
                    if start[i] != "-" and end[i] != "-":
                        moves.append([centers[i], [-1, -1]])
                        end_cord = [connect4_col_coord_map[centers[i][0]], connect4_row_coord_map[centers[i][1]]]
                    elif start[i] == "-":
                        end_cord = [connect4_col_coord_map[centers[i][0]], connect4_row_coord_map[centers[i][1]]] 
                    else:
                        start_cord = [connect4_col_coord_map[centers[i][0]], connect4_row_coord_map[centers[i][1]]]
            moves.append([start_cord, end_cord])
        else:
            for i in range(len(start)):
                if start[i] != end[i]:
                    if start[i] != "-" and end[i] != "-":
                        moves.append([centers[i], [-1, -1]])
                        end_cord = [connect4_col_coord_map[centers[i][0]], connect4_row_coord_map[centers[i][1]]]
                    elif start[i] == "-":
                        end_cord = [connect4_col_coord_map[centers[i][0]], connect4_row_coord_map[centers[i][1]]] 
                    else:
                        start_cord = [connect4_col_coord_map[centers[i][0]], connect4_row_coord_map[centers[i][1]]]
            moves.append([start_cord, end_cord])
        return moves


# Input: starting coord and ending coord
# Output: List of start position string and end position string ["RA_3_3_000", "RA_3_3_01230"]
def coor_to_position(postion, start, end):
    start_index = centers.index(start)
    end_index = centers.index(end)

    return postion[:start_index] + postion[end_index] + postion[start_index+1:end_index] + postion[start_index] + postion[end_index+1:]

###############################################################################
################################################################################


# Work here!
Static_URL = Static_URL + "/positions/?p="
Dynamic_URL = Static_URL + starting_position

# List of available moves from starting position
moves_data = requests.get(url=Dynamic_URL).json()['moves']
print(moves_data)


def pick_best_position_achi(moves):
    position_values = {}
    for i in range(len(moves)):
        if moves[i]['moveValue'] not in position_values:
            position_values[moves[i]['moveValue']] = [moves[i]['position']]
        else:
            position_values[moves[i]['moveValue']].append(moves[i]['position'])

    if 'win' in position_values and len(position_values['win']) > 0:
        print("best position: " + position_values['win'][0])
        return position_values['win'][0]
    elif 'draw' in position_values and len(position_values['draw']) > 0:
        return position_values['draw'][0]
    elif 'lose' in position_values and len(position_values['lose']) > 0:
        return position_values['lose'][0]
    else:
        print('error: in pick_best_postion')
        exit()

turn_num = 0
A_turn = True
while (len(moves_data) > 0):
    turn_num += 1
    print("This is move " + str(turn_num))
    if A_turn:
        new_position = pick_best_position_achi(moves_data)
        print(starting_position)
        print(new_position)
        move_coords = connect4_position_to_coord(starting_position, new_position)

        print("A : ", move_coords)
        flag = False
        while not flag:
            user = input("Enter y and Press ENTER: ")
            flag = user == 'y'

        for move in move_coords:
            # Need to make sure that move[0] = "grab_new_piece" is properly handled
            # moveRobotPi.play(move[0], move[1])
            pass

        Dynamic_URL = Static_URL + new_position
        moves_data = requests.get(url=Dynamic_URL).json()['moves']
        starting_position = new_position
        A_turn = False
    else:
        new_position = pick_best_position_achi(moves_data)
        print(starting_position)
        print(new_position)
        move_coords = connect4_position_to_coord(starting_position, new_position)

        print("B : ", move_coords)
        flag = False
        while not flag:
            user = input("Enter y and Press ENTER: ")
            flag = user == 'y'

        for move in move_coords:
            # moveRobotPi.play(move[0], move[1])
            pass

        Dynamic_URL = Static_URL + new_position
        moves_data = requests.get(url=Dynamic_URL).json()['moves']
        starting_position = new_position
        A_turn = True