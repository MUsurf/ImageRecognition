def get_oblong_position ():
    pass
def soft_left_turn():
    pass
def soft_right_turn():
    pass
def full_forward():
    pass
def move_left():
    pass
def move_right():
    pass
def move_up():
    pass
def move_down():
    pass
def turn_left():
    pass
def turn_right():
    pass

## Constant for screen length & height
SCREEN_LENGTH = 100
SCREEN_HEIGHT = 100

## Front Camera
# Center Horizontal & Go Forward

## Percent of deviance from middle
HORIZONTAL_THRESH = 0.1
## Percent goal away from bottom
VERTICAL_THRESH = 0.1
## Midpoint value of found orange blob
midpoint_x, midpoint_y = get_oblong_position()

while midpoint_y > (SCREEN_HEIGHT * VERTICAL_THRESH):
    if midpoint_x > (SCREEN_LENGTH * (0.5 - 0.1)):
        soft_left_turn()
    elif midpoint_x < (SCREEN_LENGTH * (0.5 - 0.1)):
        soft_right_turn()
    else:
        full_forward()

# Stop When Bottom, See

## Bottom Camera
# Center Orange X, Y
## Percent of deviance from middle
HORIZONTAL_THRESH = 0.1
VERTICAL_THRESH = 0.1

## Midpoint value of found orange blob
midpoint_x, midpoint_y = get_oblong_position()

centered = [False, False]
while centered[0] and centered[1]:
    horizontal_middle = (SCREEN_LENGTH * (0.5 - HORIZONTAL_THRESH))

    if midpoint_x > horizontal_middle:
        move_left()
        centered[0] = False
    elif midpoint_x < horizontal_middle:
        move_right()
        centered[0] = False
    else:
        centered[0] = True

    vertical_middle = (SCREEN_HEIGHT * (0.5 - VERTICAL_THRESH))
    if midpoint_y > vertical_middle:
        move_up()
        centered[1] = False
    elif midpoint_x < vertical_middle:
        move_down()
        centered[1] = False
    else:
        centered[1] = True

# Z Height Comment
# Center Rotation
while abs(angle - 90):
    horizontal_middle = (SCREEN_LENGTH * (0.5 - HORIZONTAL_THRESH))

    if midpoint_x > horizontal_middle:
        move_left()
        centered[0] = False
    elif midpoint_x < horizontal_middle:
        move_right()
        centered[0] = False
    else:
        centered[0] = True
# Stop

## Back
# Go Forward & Center Horizontally