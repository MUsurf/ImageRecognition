import cv2 as cv
import numpy as np
import math
camera_index = 0

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

    # Finds all the contours.
    #  Uses the smoothed out image
    # sets the mode to retrieve only extreme outer contours 
    # Sets the mode to condense the lines to the end points
    contours, _ = cv.findContours(mask_smoothed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    
    

    if len(contours) > 0:
        # Get the largest contour found as this is likely the wanted shape
        largest_contour = max(contours, key=cv.contourArea)
        
        
        
        try:
            hull = cv.convexHull(largest_contour,returnPoints = False)
            defects = cv.convexityDefects(largest_contour,hull)
            
            maxF = 0
            maxE = 0
            maxD = 0
            maxS = 0
            
            if(defects is not None):
                for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0]
                    
                    if(d > maxD):
                        far = tuple(largest_contour[f][0])
                        maxS = s
                        maxE = e
                        maxD = d
                        maxF = f
                
                
                    
                start = tuple(largest_contour[maxS][0])
                end = tuple(largest_contour[maxE][0])
                far = tuple(largest_contour[maxF][0])
                
                
                # find length of all sides of triangle
                a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                s = (a+b+c)/2
                ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
                
                
                # apply cosine rule here
                angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            
                cv.line(frame,start,far,[0,255,0],2)
                cv.line(frame,far,end,[0,255,0],2)
                
                

                cv.circle(frame,far,5,[0,0,255],-1)
                
                    
                    
                
        except cv.error:
            continue
            
    cv.imshow('img', frame)
    cv.imshow('mask', mask_smoothed)
    
    if __debug__:
        combined = blend_frame_with_mask(frame, mask_smoothed)
        cv.imshow('combined', combined)
    

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
cap.release()


# img_gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
# ret,thresh = cv.threshold(img_gray, 127, 255,0)
# contours,hierarchy = cv.findContours(thresh,2,1)
# cnt = contours[0]
# print(cnt)




#print(defects)

