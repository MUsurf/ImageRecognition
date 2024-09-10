import cv2 as cv
import numpy as np

if __debug__:
    from classes.compass import *

camera_index = 0
cap = cv.VideoCapture(camera_index)

if not cap.isOpened():
    print(f"Error: Camera with index {camera_index} not accessible or not found")
    exit()

## Get the direction of the orange thing and translate that into directions for sub, maybe?

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame")
        break

    frame = cv.flip(frame, 1)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    lower_color = np.array([0, 150, 150])
    upper_color = np.array([30, 255, 255])
    mask = cv.inRange(hsv, lower_color, upper_color)

    kernel = np.ones((15, 15), np.uint8)
    mask_smoothed = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

    contours, _ = cv.findContours(mask_smoothed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        largest_contour = max(contours, key=cv.contourArea)
        x, y, w, h = cv.boundingRect(largest_contour)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        [vx, vy, cx, cy] = cv.fitLine(largest_contour, cv.DIST_L2, 0, 0.01, 0.01)

        m = vy / vx
        angle = np.degrees(np.arctan(m))

        frame_center = frame.shape[1] // 2

        # Lateral Movement
        if cx < frame_center - 20:
            direction = "Move Left"
        elif cx > frame_center + 20:
            direction = "Move Right"
        else:
            direction = "Center"

        # Forward/Backward Movement
        if h < frame.shape[0] // 3:
            forward_backward = "Move Forward"
        elif h > 2 * frame.shape[0] // 3:
            forward_backward = "Move Backward"
        else:
            forward_backward = "Hold Position"

        # Rotational Movement
        if angle < -10:
            rotation = "Rotate Left"
        elif angle > 10:
            rotation = "Rotate Right"
        else:
            rotation = "Hold Orientation"

        print(f"Direction: {direction}, Forward/Backward: {forward_backward}, Rotation: {rotation}")

    cv.imshow('Contours', frame)
    cv.imshow('Mask', mask)
    cv.imshow('Smoothed', mask_smoothed)


    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
cap.release()