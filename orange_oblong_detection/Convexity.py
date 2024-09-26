import cv2 as cv
import numpy as np
import math
camera_index = 0

# If running in test environment then import helper
if __debug__:
    from classes.helper import *

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

    #Creates a kernel that is above a pixel 
    kernel2 = np.ones((5,5), np.float32)/25
    #averages the existing mask, making it blurry
    mask_smoothed = cv.filter2D(mask_smoothed, -1, kernel2)

    
    # Finds all the contours.
    #  Uses the smoothed out image
    # sets the mode to retrieve only extreme outer contours 
    # Sets the mode to condense the lines to the end points
    contours, _ = cv.findContours(mask_smoothed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    
    
    # If there are any detected contours
    if len(contours) > 0:
        # Get the largest contour found as this is likely the wanted shape
        largest_contour = max(contours, key=cv.contourArea)
        
        try:
            # Get the convex hull of a point set to detect angle point
            hull = cv.convexHull(largest_contour,returnPoints = False)
            # Get all the examples of convexity
            defects = cv.convexityDefects(largest_contour,hull)
            
            # We want to keep the furthest point so track params
            maxDefect = [0,0,0,0]
            
            # If there are defects
            if(defects is not None):
                # For all defects (convex points)
                for i in range(defects.shape[0]):
                    # Get relevant points [start, end, far, distance]
                    # start: index (of start of line of convexity),
                    # end: index (of end of line with convexity),
                    # far: convex point,
                    # distance: distance of far from line of convexity
                    test = defects[i,0]

                    # If distance is greater than current max
                    if(test[3] > maxDefect[3]):
                        ## far = tuple(largest_contour[test[2]][0])
                        # Update max to new largest
                        maxDefect = test 
                
                
                # Get the relevant points for the start, end, and far point
                start = tuple(largest_contour[maxDefect[0]][0])
                end = tuple(largest_contour[maxDefect[1]][0])
                far = tuple(largest_contour[maxDefect[2]][0])
                
                ## Code from https://gist.github.com/Dhruv454000/dce6491280e09ff8d920ed46fc625889
                # find length of all sides of triangle
                a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                s = (a+b+c)/2
                ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
                
                
                # apply cosine rule here
                angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            
                # Draw the two lines of the convexity to the convex point
                cv.line(frame,start,far,[0,255,0],2)
                cv.line(frame,far,end,[0,255,0],2)
                # Draw the point of the angle
                cv.circle(frame,far,5,[0,0,255],-1)
        # If error from opencv then skip this frame
        except cv.error:
            continue

    # If running in a test environment show the results visually
    if __debug__:            
        cv.imshow('img', frame)
        cv.imshow('mask', mask_smoothed)
        combined = blend_frame_with_mask(frame, mask_smoothed)
        cv.imshow('combined', combined)
    
    # Wait for q key to quit
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
cap.release()