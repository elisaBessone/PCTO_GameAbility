from fcntl import LOCK_WRITE
import io
import socket
import struct
from PIL import Image
import matplotlib.pyplot as pl
import numpy as np
import argparse
import cv2
import time
FONT_HERSHEY_SIMPLEX = 0

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
		if radius > 20:
			# draw the circle on the frame
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)

def red(mask):
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 20:
        print('ROSSO')
        time.sleep(0.1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, "APERTURA PORTA", (230, 50), font , 0.8, (0, 0, 255), 2, cv2.LINE_AA)
        

def blue(mask):
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 20:
        print('BLU')
        time.sleep(0.1)
        
        
        
        
def green(mask):
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 20:
        print('VERDE')
        time.sleep(0.1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, "ACCENDO LA LUCE", (230, 50), font , 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        #cv2.putText(np.array(img), "ACCENDO LA LUCE", (230, 50), font , 0.8, (0, 255, 0), 2, cv2.LINE_AA)

print('1')
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))  # ADD IP HERE
server_socket.listen(0)
print('2')

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
kernel = np.ones((8,8), np.uint8)

try:
    img = None
    
    while True:
       
        
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        print('3')
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        print('4')
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        #image = Image.open(image_stream)
        image = np.array(Image.open(image_stream))
        
        if img is None:
            img = pl.imshow(image)
            print(1)
        else:
            img.set_data(image)
            print(2)

        pl.pause(0.01)
        pl.draw()

        #print('Image is %dx%d' % image.size)
        #image.verify()
        #print('Image is verified')

        print(9)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        print('prima')

        lower_red = np.array([105, 175, 109])
        upper_red = np.array([140, 305, 200])

        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        
        traceCircle(image, mask_red)
        red(mask_red)
        #***********************************************
        
        lower_blue = np.array([115, 42, 100 ])
        upper_blue = np.array([125, 50, 106])
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        
        traceCircle(image, mask_blue)
        blue(mask_blue)
        
        lower_green = np.array([25, 40, 165])
        upper_green = np.array([50, 65, 188])
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        
        traceCircle(image, mask_green)
        green(mask_green)
                
        

        #opening = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)
        opening = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
        opening = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)
        x, y, w, h = cv2.boundingRect(opening)
        print(x, ",",y)

        cv2.imshow('frame',image) 
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    connection.close()
    server_socket.close()

    # Destroys all of the HighGUI windows. 
    cv2.destroyAllWindows() 
   