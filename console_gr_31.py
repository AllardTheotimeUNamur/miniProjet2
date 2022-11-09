import math
import random

import radio
import microbit

# definition of functions
def get_message():
    """Wait and return a message from another micro:bit.
    
    Returns
    -------
    message: message sent by another micro:bit (str)
        
    """

    message = None    
    while message == None:
        microbit.sleep(250)
        message = radio.receive()
    
    return message


def create_new_piece(pieces_models, x, y):
    """Create a new piece in the top left corner

    Parameters
    ----------
    pieces_models : a dictionary with all piece shapes (dic)
    x : x position of the top left of the piece (int)
    y : y position of the top left of the piece (int)

    Returns
    -------
    A dictionary with the shape, the x position and the y position of a piece chosen randomly (dict)

    """

    new_piece = pieces_models[random.randint(0, len(pieces_models) - 1)]
    new_piece["pos_x"] = x
    new_piece["pos_y"] = y

    return new_piece


def collides_checker(board, piece, x_board, y_board):
    """Check if the new piece collides with a dropped piece or the outside of the board

    Parameters
    ----------
    board : a dictionary with the shape of the board (dict)
    piece : a dictionary with the shape, the x position and the y position of the new piece (dict)
    x_board : x position on the board where we want to test if there is a collision (int)
    y_board : y position on the board where we want to test if there is a collision (int)

    Return
    ------
    True, if the new piece collides with a dropped piece or the outside of the board (bool)

    """

    # Check if the new piece collides with a dropped piece
    #   for each element of the piece,
    #   I multiply it with the elements of the board relative to the position of the piece
    #       if the element of the piece is 0 and the element of the board is 0 the result will be 0
    #       if the element of the piece is 1 and the element of the board is 0 or
    #           the element of the piece is 0 and the element of the board is 1 the result will be 0
    #       if the element of the piece is 1 and the element of the board is 1 the result will be 1
    #   if the result is 1 there's a collision
    for y in range(piece["height"]):
        for x in range(piece["width"]):
            if (piece["shape"][y][x] * board["shape"][y_board + y][x_board + x]) == 1:
                return True

    # Check if the new piece collides with the outside of the board
    if (piece["pos_x"] < 0) or (piece["pos_x"] >= board["width"]):
        return True
    if (piece["pos_y"] < 0) or (piece["pos_y"] >= board["height"]):
        return True

    return False


def board_and_piece_to_string(board, piece):
    """Transform the board shape and the piece shape on a string

    Parameters
    ----------
    board : a dictionary with the shape of the board (dict)
    piece : a dictionary with the shape, the x position and the y position of the new piece (dict)

    Returns
    -------
    A string with the board shape and the piece shape on string (str)

    """

    string = ""

    # for each element of the board
    for y in range(board["height"]):
        for x in range(board["width"]):
            # if you are in the board elements related to the piece
            if ((x >= piece["pos_x"]) and (x < (piece["pos_x"] + piece["width"]))) and (
                    (y >= piece["pos_y"]) and (y < (piece["pos_y"] + piece["height"]))):
                # if the element of the piece is 1 we add 9 in the string
                if piece['shape'][y - piece["pos_y"]][x - piece["pos_x"]] == 1:
                    string += "9"
                # if the element of the board is 1 we add 3 in the string
                elif board['shape'][y][x] == 1:
                    string += "3"
                # else there is nothing and we add 0
                else:
                    string += "0"
            else:
                # for all other elements we add 3 if the element is 1 and we add 0 if the element is 0
                string += str(3 * board['shape'][y][x])
        # Add the delimiter ":" to each line
        string += ":"
    # return the string without the last ":"
    return string[:-1]


def execute_order(order, nb_dropped_pieces):
    """Split and execute the order and the parameter

    Parameters
    ----------
    order : the order received by the controller (string)
    nb_dropped_pieces : number of pieces dropped (int)

    Returns
    -------
    A list with [0] => True, if the piece is dropped (bool)
                [1] => number of pieces dropped (int)

    """

    split_order = order.split("/")

    is_dropped = False

    # move order
    if split_order[0] == "move":
        move_piece(board, piece, split_order[1])

    # drop order
    elif split_order[0] == "drop":
        drop_piece(board, piece)
        nb_dropped_pieces += 1
        is_dropped = True

    return [is_dropped, nb_dropped_pieces]


def move_piece(board, piece, direction):
    """Move de piece on the board

    Parameters
    ----------
    board : a dictionary with the shape of the board (dict)
    piece : a dictionary with the shape, the x position and the y position of the new piece (dict)
    direction : the direction in which we want to move the piece (string)

    """

    # move top
    if direction == "0":
        new_y = piece["pos_y"] - 1
        if not collides_checker(board, piece, piece["pos_x"], new_y):
            piece["pos_y"] = new_y

    # move right
    elif direction == "1":
        new_x = piece["pos_x"] + 1
        if not collides_checker(board, piece, new_x, piece["pos_y"]):
            piece["pos_x"] = new_x

    # move down
    elif direction == "2":
        new_y = piece["pos_y"] + 1
        if not collides_checker(board, piece, piece["pos_x"], new_y):
            piece["pos_y"] = new_y

    # move left
    elif direction == "3":
        new_x = piece["pos_x"] - 1
        if not collides_checker(board, piece, new_x, piece["pos_y"]):
            piece["pos_x"] = new_x


def drop_piece(board, piece):
    """Drop the piece on the board

    Parameters
    ----------
    board : a dictionary with the shape of the board (dict)
    piece : a dictionary with the shape, the x position and the y position of the new piece (dict)

    """

    for y in range(piece["height"]):
        # piece_y is the relative position y of the piece on the board
        piece_y = y + piece["pos_y"]
        for x in range(piece["width"]):
            # piece_x is the relative position x of the piece on the board
            piece_x = x + piece["pos_x"]
            # changes only if the element is a 1
            if piece["shape"][y][x] == 1:
                board["shape"][piece_y][piece_x] = 1


# settings
group_id = 31

# setup radio to receive orders
radio.on()
radio.config(group=group_id)

# create empty board + available pieces
board = {
    "shape": [[0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0]],
    "width": 5,
    "height": 5
}

pieces_models = [{
    "shape": [
        [1, 1],
        [1, 1]
    ],
    "width": 2,
    "height": 2,
}, {
    "shape": [
        [1, 1]
    ],
    "width": 2,
    "height": 1,
}, {
    "shape": [
        [1],
        [1]
    ],
    "width": 1,
    "height": 2,
}, {
    "shape": [
        [1, 1],
        [1, 0]
    ],
    "width": 2,
    "height": 2,
}, {
    "shape": [
        [0, 1],
        [1, 1]
    ],
    "width": 2,
    "height": 2,
}]

piece = None

# loop until game is over
nb_dropped_pieces = 0
game_is_over = False

while not game_is_over:
    # show score (number of pieces dropped)
    microbit.display.show(nb_dropped_pieces)

    # create a new piece in the top left corner
    piece = create_new_piece(pieces_models, 0, 0)
    
    # check if the new piece collides with dropped pieces
    game_is_over = collides_checker(board, piece, 0, 0)
    
    if not game_is_over:
        # ask orders until the current piece is dropped
        piece_dropped = False
        while not piece_dropped:
            # send state of the board to gamepad (as a string)
            radio.send(board_and_piece_to_string(board, piece))
            
            # wait until gamepad sends an order
            order = get_message()
            
            # execute order (drop or move piece)
            piece_dropped, nb_dropped_pieces = execute_order(order, nb_dropped_pieces)
        
        # wait a few milliseconds and clear screen
        microbit.sleep(500)
        microbit.display.clear()
    
# tell that the game is over
microbit.display.scroll('Game is over', delay=100)
