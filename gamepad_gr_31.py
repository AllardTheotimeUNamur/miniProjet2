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
    

def show_view_on_the_board(view):
    """Show the board on the controller

    Parameters
    ----------
    view: the message received from the console (string)
        the format ("xxxxx:xxxxx:xxxxx:xxxxx:xxxxx") where the "x"s can be 0, 3, 6, 9

    """
    display.show(Image(view))


def send_direction():
    """Create a string with the order to move and the direction

    Returns
    -------
    A message with the order to move and the direction

    """

    # get the accelerometer values
    rotation_x = accelerometer.get_x()
    rotation_y = accelerometer.get_y()

    # take their absolute value
    abs_rotation_x = abs(rotation_x)
    abs_rotation_y = abs(rotation_y)

    # choose a sensitivity for having a minimum speed before sending the message
    sensitivity = 500

    message = "move/"

    # if the controller rotates more on the x-axis
    if abs_rotation_x >= abs_rotation_y:
        # move right
        if rotation_x > sensitivity:
            message += "1"
        # move left
        elif rotation_x < -sensitivity:
            message += "3"

    # if the controller rotates more on the y-axis
    else:
        # move top
        if rotation_y > sensitivity:
            message += "0"
        # move down
        elif rotation_y < -sensitivity:
            message += "2"

    return message


def send_drop():
    """Create a string with the order to drop

    Returns
    -------
    A message with the order to drop

    """

    return "drop"


# settings
group_id = 31

# setup radio to receive/send messages
radio.on()
radio.config(group=group_id)
    
# loop forever (until micro:bit is switched off)
while True:
    # get view of the board
    view = get_message()
    
    # clear screen
    microbit.display.clear()
    
    # show view of the board
    show_view_on_the_board(view)
    
    # wait for button A or B to be pressed
    while not (microbit.button_a.is_pressed() or microbit.button_b.is_pressed()):
        microbit.sleep(50)

    if microbit.button_a.is_pressed():
        # send current direction
        radio.send(send_direction())

    elif microbit.button_b.is_pressed():
        # notify that the piece should be dropped
        radio.send(send_drop())
