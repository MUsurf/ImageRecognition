import cv2 as cv
import numpy as np

if __debug__:
    from classes.compass import *

camera_index = 0
cap = cv.VideoCapture(camera_index)

if not cap.isOpened():
    print(f"Error: Camera with index {camera_index} not accessible or not found")
    exit()

## Draw a line around the orange thing

while True:
    #returns the frame to read. with ret being a flag to indicate success
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame")
        break
    #flips the frame to make it readable
    frame = cv.flip(frame, 1)

    #converts the frame to HSV color range
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    #creates an array of colors to "bound" orange color
    lower_color = np.array([0, 150, 150])
    upper_color = np.array([30, 255, 255])

    #creates a "mask" for the frame that is in the color range for orange
    mask = cv.inRange(hsv, lower_color, upper_color)

    #creates an array of 15x15 of np.uint8 of all ones 
    kernel = np.ones((15, 15), np.uint8)

    #This next step uses morphological transformation (https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)
    #Uses a "closing" morphological transformation which means that dilation followed by erosion occurs
    #dilation means that the boundaries of the foreground object increases
    #Erosion means that the boundaries of the foreground object will be made smaller. It removes white noise
    #in other words the "closing" morphological change removes the small holes and connects everything up
    #this is just basically cleaning up the image
    mask_smoothed = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

    #finds all the contours.
    #  Uses the smoothed out image
    # sets the mode to retrieve only extreme outer contours 
    # Sets the mode to condense the lines to the end points
    contours, _ = cv.findContours(mask_smoothed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    #makes sure that there was atleast 1 contour
    if len(contours) > 0:
        largest_contour = max(contours, key=cv.contourArea)
        x, y, w, h = cv.boundingRect(largest_contour)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        epsilon = 0.02 * cv.arcLength(largest_contour, True)
        approx = cv.approxPolyDP(largest_contour, epsilon, True)
        cv.drawContours(frame, [approx], -1, (255, 0, 0), 2)

        camera_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH)) * 20
        camera_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

        rows, cols = frame.shape[:2]
        [vx, vy, x, y] = cv.fitLine(largest_contour, cv.DIST_L2, 0, 0.01, 0.01)
        print(f"y is {y}, x is {x}, vy is {vy}, vx is {vx}")

        m = vy / vx
        m = min(max(m, -25), 25)

        if __debug__:
            angle = calculate_angle(vx, vy)
            draw_compass(angle)

        lefty = int((-x * m) + y)
        righty = int(((cols - x) * m) + y)

        lefty = max(min(lefty, camera_width), -camera_width)
        righty = max(min(righty, camera_width), -camera_width)

        colMin1 = cols - 1 if cols - 1 else 0
        cv.line(frame, (colMin1, righty), (0, lefty), (0, 255, 0), 2)

    cv.imshow('Contours', frame)
    cv.imshow('Mask', mask)
    cv.imshow('Smoothed', mask_smoothed)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
cap.release()