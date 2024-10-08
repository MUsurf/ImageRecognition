from vCam import move_sub

# forward, right, up, cw rotate
_directions = [0, 0, 0, 0]

def tick(fit_line, width, height, camera_rotation):
    """Runs every frame of the virtualCam and should analyze info and return movement directions
    
    Parameters
    ----------
    fit_line : int arr
        [vx, vy, x, y] best fit line information
        vx: change in x
        vy: change in y
        x: pixel x value of center point
        y: pixel y value of center point
    width : int
        width in pixels of camera
    height : int
        height in pixels of camera
    camera_rotation : int
        rotation of camera in degrees

    Returns
    -------
    forward : int
        -1, 0, or 1
        Whether to move backwards, not at all or forwards
    right : int
        -1, 0, or 1
        Whether to move right, not at all or left
    up : int
        -1, 0, or 1
        Whether to move up, not at all or down
    cw_rotate : int
        -1, 0, or 1
        Whether to rotate counter clockwise, not at all or clockwise
    """
    global _directions

    mid_point = width // 2
    if(fit_line[2] > mid_point):
        _directions[1] = -1
    elif(fit_line[2] < mid_point):
        _directions[1] = 1
    
    move_sub(*_directions)