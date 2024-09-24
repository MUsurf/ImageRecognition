from vCam import move_sub

# forward, right, up, cw rotate
_directions = [0, 0, 0, 0]

def tick(fit_line, width, height, camera_rotation):
    global _directions

    mid_point = width // 2
    if(fit_line[2] > mid_point):
        _directions[1] = -1
    elif(fit_line[2] < mid_point):
        _directions[1] = 1
    
    move_sub(*_directions)