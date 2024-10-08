import cv2 as cv
import numpy as np
import os

# Which camera on the device to use
camera_index = 0
# Initialize Video Capture
cap = cv.VideoCapture(camera_index)

# Make sure that the camera is available
if not cap.isOpened():
    print(f"Error: Camera with index {camera_index} not accessible or not found")
    exit()


#Creates a frame for the image and flips it
def createFrame():
    # Get the frame to read. with ret being a flag to indicate success
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame")
        raise ValueError("Error: Failed to capture frame")
        

    # Flips the frame to make it more user viewable
    frame = cv.flip(frame, 1)
    return frame

#creates a mask for the frame that had previously been created by createFrame
def createMask(frame, lower_color, upper_color):
    # Converts the frame to HSV color range
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Creates a "mask" for the frame that is in the color range for orange
    mask = cv.inRange(hsv, lower_color, upper_color)
    return mask

## Draw a line around the orange thing

while True:
   
   #makes a frame and flips it
    try: 
        frame = createFrame()
        # frame = cv.imread('redblue.png')
    except ValueError as e:
        break

    #create a mask for the frame
    # blue_mask = createMask(frame, (200, 128, 128), (260, 255, 255))
    blue_mask = createMask(frame, (75, 128, 128), (130, 255, 255))
    
    red_mask_1 = createMask(frame, (150, 128, 128), (180, 255, 255))
    red_mask_2 = createMask(frame, (0, 128, 128), (15, 255, 255))
    red_mask = cv.add(red_mask_1, red_mask_2)

    mask = cv.add(blue_mask, red_mask)

    kernel = np.ones((3,3),np.uint8)
    dilated = cv.dilate(mask, kernel)

    # Creates an array of 15x15 of np.uint8 of all ones 
    kernel = np.ones((15, 15), np.uint8)

    # This next step uses morphological transformation (https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)
    # Uses a "closing" morphological transformation which means that dilation followed by erosion occurs
    # dilation means that the boundaries of the foreground object increases
    # Erosion means that the boundaries of the foreground object will be made smaller. It removes white noise
    # in other words the "closing" morphological change removes the small holes and connects everything up
    # this is just basically cleaning up the image
    mask_smoothed = cv.morphologyEx(dilated, cv.MORPH_CLOSE, kernel)

    # Finds all the contours.
    #  Uses the smoothed out image
    # sets the mode to retrieve only extreme outer contours 
    # Sets the mode to condense the lines to the end points
    blue_contours, blue__ = cv.findContours(red_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    red_contours, red__ = cv.findContours(blue_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    both_contours, both__ = cv.findContours(blue_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Makes sure that there was at least 1 contour else skip
    if len(blue_contours) > 0 and len(red_contours) > 0:
        # Get the largest contour found as this is likely the wanted shape
        blue_largest_contour = max(blue_contours, key=cv.contourArea)
        red_largest_contour = max(red_contours, key=cv.contourArea)
        both_largest_contour = max(both_contours, key=cv.contourArea)

        # Get the bounding points of this rectangle
        bx, by, bw, bh = cv.boundingRect(blue_largest_contour)
        rx, ry, rw, rh = cv.boundingRect(red_largest_contour)
        both_x, both_y, both_w, both_h = cv.boundingRect(both_largest_contour)
        # Draw this rectangle on frame in green (BGR)
        cv.rectangle(frame, (bx, by), (bx + bw, by + bh), (0, 255, 0), 2)
        cv.rectangle(frame, (rx, ry), (rx + rw, ry + rh), (255, 0, 0), 2)
        cv.rectangle(frame, (both_x, both_y), (both_x + both_w, both_y + both_h), (0, 0, 255), 2)

        os.system("cls")
        print(f"Area of red {rw * rh}, Area of blue {bw * bh}")
        print(f"\t Similarity of {(rw * rh) / (bw * bh)}")

    # Show the displays
    cv.imshow('Contours', frame)
    # cv.imshow('BMask', blue_mask)
    # cv.imshow('RMask', red_mask)
    cv.imshow('Mask', mask)
    # cv.imshow('Dilated', dilated)
    # cv.imshow('Smoothed', mask_smoothed)

    # Wait for a q to quit the program
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Close the windows and release the camera
cv.destroyAllWindows()
cap.release()