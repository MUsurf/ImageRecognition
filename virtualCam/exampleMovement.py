from vCam import move_sub

_step = 0

def tick():
    global _step
    print(_step)
    if(_step < 10):
        move_sub(1, -1, -1, -1)
    elif(_step < 20):
        move_sub(-1, 1, -1, 1)
    else:
        _step = 0
    _step += 1