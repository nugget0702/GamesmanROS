import requests


BASE_URL = "https://nyc.cs.berkeley.edu/universal/v1/"

achi_col_coord_map = {10: 1.5, 50: 2.5, 90: 3.5}
achi_row_coord_map = {10: 3.5, 50: 2.5, 90: 1.5}

connect4_col_coord_map = {0.5: 1, 1.5: 2, 2.5: 3, 3.5: 4, 4.5: 5, 5.5: 6, 6.5: 7}
connect4_row_coord_map = {1.5: 6, 2.5: 5, 3.5: 4, 4.5: 3, 5.5: 2, 6.5: 1}

def get_game_name(game_index: int):
    if game_index == 4:
        return "Achi"
    elif game_index == 16:
        return "Connect 4"
    else:
        return "Unknown"

def initialize_game(game_index: int, variant_index: int):
    ######################### Get All Games #####################################
    games_data = requests.get(url=BASE_URL).json()
    url = BASE_URL + games_data[game_index]['id'] + '/'
    #############################################################################


    ########################## Get Variant #######################################
    variants_data = requests.get(url=url).json()['variants']
    variant = variants_data[variant_index]["id"]
    ##############################################################################


    ################# Get Starting Positon and Meta Data  #######################
    static_URL = url + variant
    static_data = requests.get(url=static_URL).json()
    theme = list(static_data["imageAutoGUIData"]["themes"].keys())[0]
    centers = static_data["imageAutoGUIData"]["themes"][theme]["centers"]
    starting_position = static_data["startPosition"]
    ###############################################################################

    static_URL = static_URL + "/positions/?p="
    dynamic_URL = static_URL + starting_position

    # List of available moves from starting position
    moves_data = requests.get(url=dynamic_URL).json()['moves']

    return static_URL, centers, starting_position, moves_data


def pick_best_position(moves):
    position_values = {}
    for i in range(len(moves)):
        if moves[i]['moveValue'] not in position_values:
            position_values[moves[i]['moveValue']] = [moves[i]['position']]
        else:
            position_values[moves[i]['moveValue']].append(moves[i]['position'])

    if 'win' in position_values and len(position_values['win']) > 0:
        # print("best position: " + position_values['win'][0])
        return "", position_values['win'][0]
    elif 'draw' in position_values and len(position_values['draw']) > 0:
        return "", position_values['draw'][0]
    elif 'lose' in position_values and len(position_values['lose']) > 0:
        return "", position_values['lose'][0]
    else:
        return 'error: in pick_best_postion', position_values


def achi_position_to_coord(start, end, centers, _):
    moves = []
    # For achi, start_cord is always outside the board when the value is None so that the robot can pickup new pieces.
    # Once the start_cord is not grab_new_piece, then we can move pieces within the board.
    start_cord = "grab_new_piece"
    end_cord = None

    start = start[2:]
    end = end[2:]

    if len(start) != len(end) or start == end:
        return "error: invalid position_to_coord_achi inputs", moves
    else:
        for i in range(len(start)):
            if start[i] != end[i]:
                if start[i] != "-" and end[i] != "-":
                    moves.append([centers[i], [-1, -1]])
                    end_cord = [achi_col_coord_map[centers[i][0]], achi_row_coord_map[centers[i][1]]] 
                elif start[i] == "-":
                    end_cord = [achi_col_coord_map[centers[i][0]], achi_row_coord_map[centers[i][1]]] 
                else:
                    start_cord = [achi_col_coord_map[centers[i][0]], achi_row_coord_map[centers[i][1]]]
        moves.append([start_cord, end_cord])
        return "", moves


def connect4_position_to_coord(start, end, centers, variant):
    moves = []
    # For connect 4, you are always grabbing a new piece, similar to the grabbing new piece part of achi.
    start_cord = "grab_new_piece"
    end_cord = None

    start = start[2:]
    end = end[2:]

    if len(start) != len(end) or start == end:
        return "error: invalid connect4_position_to_coord inputs", moves
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
        return "", moves
