def get_oblong_position ():
    pass
def soft_left_turn():
    pass
def soft_right_turn():
    pass
def full_forward():
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
        soft_left_turn()
        centered[0] = False
    elif midpoint_x < horizontal_middle:
        soft_right_turn()
        centered[0] = False
    else:
        centered[0] = True

# Z Height Comment
# Center Rotation
# Stop

## Back
# Go Forward & Center Horizontally