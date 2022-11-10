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


def show_message():
    message = "move/"
    move_y = microbit.accelerometer.get_y()
    move_x = microbit.accelerometer.get_x()

    if move_y > 100:
        message += "up"
    elif move_y > -100:
        message += "down"
    elif move_x > 100:
        message += "right"
    elif move_x > -100:
        message += "left"
    return message


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
    microbit.display.show(Image(view))
    
    # wait for button A or B to be pressed
    while not (microbit.button_a.is_pressed() or microbit.button_b.is_pressed()):
        microbit.sleep(50)

    if microbit.button_a.is_pressed():
        # send current direction
        radio.send(radio.send(show_message()))
    elif microbit.button_b.is_pressed():
        # notify that the piece should be dropped
        radio.send("dropped")
