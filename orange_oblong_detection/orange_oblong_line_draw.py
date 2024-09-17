import cv2 as cv
import numpy as np

# If running while testing, import the compass
if __debug__:
    from classes.compass import *

# Which camera on the device to use
camera_index = 0
# Initialize Video Capture
cap = cv.VideoCapture(camera_index)

# Make sure that the camera is available
if not cap.isOpened():
    print(f"Error: Camera with index {camera_index} not accessible or not found")
    exit()

## Draw a line around the orange thing

while True:
    # Get the frame to read. with ret being a flag to indicate success
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame")
        break

    # Flips the frame to make it more user viewable
    frame = cv.flip(frame, 1)

    # Converts the frame to HSV color range
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Creates an array of colors to "bound" orange color
    lower_color = np.array([0, 150, 150])
    upper_color = np.array([30, 255, 255])

    # Creates a "mask" for the frame that is in the color range for orange
    mask = cv.inRange(hsv, lower_color, upper_color)

    # Creates an array of 15x15 of np.uint8 of all ones 
    kernel = np.ones((15, 15), np.uint8)

    # This next step uses morphological transformation (https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)
    # Uses a "closing" morphological transformation which means that dilation followed by erosion occurs
    # dilation means that the boundaries of the foreground object increases
    # Erosion means that the boundaries of the foreground object will be made smaller. It removes white noise
    # in other words the "closing" morphological change removes the small holes and connects everything up
    # this is just basically cleaning up the image
    mask_smoothed = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

    # Finds all the contours.
    #  Uses the smoothed out image
    # sets the mode to retrieve only extreme outer contours 
    # Sets the mode to condense the lines to the end points
    contours, _ = cv.findContours(mask_smoothed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Makes sure that there was at least 1 contour else skip
    if len(contours) > 0:
        # Get the largest contour found as this is likely the wanted shape
        largest_contour = max(contours, key=cv.contourArea)
        # Get the bounding points of this rectangle
        x, y, w, h = cv.boundingRect(largest_contour)
        # Draw this rectangle on frame in green (BGR)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        #! Test functions for future contour approx
        #! https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html
        epsilon = 0.02 * cv.arcLength(largest_contour, True)
        approx = cv.approxPolyDP(largest_contour, epsilon, True)
        # Draw these onto frame
        cv.drawContours(frame, [approx], -1, (255, 0, 0), 2)

        # Get camera width and height for math
        camera_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH)) * 20 #! Why * 20? Test without
        camera_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

        # Get the first two items in the frame's shape
        rows, cols = frame.shape[:2] #* What does this actually mean?

        # Get best fit line for the largest countour
        #* Research function parameters
        #* Are there better values
        [vx, vy, x, y] = cv.fitLine(largest_contour, cv.DIST_L2, 0, 0.01, 0.01)
        print(f"y is {y}, x is {x}, vy is {vy}, vx is {vx}")

        # Derive slope from classic rise over run
        m = vy / vx
        # Clamp the slope to avoid extreme values causing seeming overflow issues
        m = min(max(m, -25), 25)

        # If running while testing, display the compass with the found angle
        if __debug__:
            angle = calculate_angle(vx, vy)
            draw_compass(angle)

        # Find the left and right points of the line
        lefty = int((-x * m) + y)
        righty = int(((cols - x) * m) + y)

        # Clamp these values to the edges of the camera
        lefty = max(min(lefty, camera_width), -camera_width)
        righty = max(min(righty, camera_width), -camera_width)

        # Find where the line lines up on the y axis, top or bottom
        colMin1 = cols - 1 if cols - 1 else 0 #* How does this actually work?

        # Draw the best fit line on the frame in green (BGR)
        cv.line(frame, (colMin1, righty), (0, lefty), (0, 255, 0), 2)

    # Show the displays
    cv.imshow('Contours', frame)
    cv.imshow('Mask', mask)
    cv.imshow('Smoothed', mask_smoothed)

    # Wait for a q to quit the program
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Close the windows and release the camera
cv.destroyAllWindows()
cap.release()