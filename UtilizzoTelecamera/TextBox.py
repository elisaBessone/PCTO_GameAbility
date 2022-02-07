# Python program for Detection of a  
# specific color(blue here) using OpenCV with Python 
import cv2
import argparse
import numpy as np


def traceCircle(frame, mask):
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)


		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle on the frame
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)



kernel = np.ones((8 ,8), np.uint8)

# Webcamera no 0 is used to capture the frames 
cap = cv2.VideoCapture(0)  
  
# This drives the program into an infinite loop. 
while(1):        
    # Captures the live stream frame-by-frame 
    _, frame = cap.read()  
    # Converts images from BGR to HSV 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    

    # define range of color in HSV
    
    ##lower_blue = np.array([90, 100, 100])
    ##upper_blue = np.array([150, 255, 255])

    #lower_green = np.array([30, 100, 100])
    #lower_green = np.array([90, 255, 255])

##    lower_red = np.array([150,200,50])
##    upper_red = np.array([250,255,255])

    lower_c=np.array([150, 100, 100])
    upper_c=np.array([250, 255, 255])
  
# Here we are defining range of color in HSV 
# This creates a mask of selected colour  
# objects found in the frame. 

    mask = cv2.inRange(hsv, lower_c, upper_c) 
    mask = cv2.erode(mask, None, iterations=5)
    mask = cv2.dilate(mask, None, iterations=5)
    traceCircle(frame,mask)
  
# The bitwise and of the frame and mask is done so  
# that only the blue coloured objects are highlighted  
# and stored in res

    res = cv2.bitwise_and(frame,frame, mask= mask) 

    cv2.imshow('mask',mask) 
    cv2.imshow('res',res)

    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    x, y, w, h = cv2.boundingRect(opening)
    print(x, ",",y)

    cv2.imshow('frame',frame) 
  
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# Destroys all of the HighGUI windows. 
cv2.destroyAllWindows() 
  
# release the captured frame 
cap.release() 