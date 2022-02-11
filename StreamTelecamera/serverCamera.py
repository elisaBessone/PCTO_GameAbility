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
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]

	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)


		if radius > 20:
			# disegno del cerchio sull'oggetto colorato
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
     
        
def green(mask):
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 20:
        print('VERDE')
        time.sleep(0.1)
	#scrittura su telecamera
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, "ACCENDO LA LUCE", (230, 50), font , 0.8, (0, 255, 0), 2, cv2.LINE_AA)


server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))  # ADD IP HERE
server_socket.listen(0)

#Accettazione della connessione e creazione file simile a un oggetto
connection = server_socket.accept()[0].makefile('rb')
kernel = np.ones((8,8), np.uint8)

try:
    img = None
    
    while True:
        # RLettura lunghezza dell'immagine, se = 0 chiusura
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
	
        if not image_len:
            break
        # Costruzione del flusso di dati
        image_stream = io.BytesIO()
    
        image_stream.write(connection.read(image_len))
        # Riavvolgimento del flusso e elaborazione di esso
        image_stream.seek(0)
        #image = Image.open(image_stream)
        image = np.array(Image.open(image_stream))
        
        if img is None:
            img = pl.imshow(image)
       
        else:
            img.set_data(image)
     

        pl.pause(0.01)
        pl.draw()
	
	#riconoscimento colore tramite BGR  e HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
        lower_red = np.array([105, 175, 109])
        upper_red = np.array([140, 305, 200])
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        traceCircle(image, mask_red)
        red(mask_red)
	
        #***********************************************
             
        lower_green = np.array([25, 40, 165])
        upper_green = np.array([50, 65, 188])
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        traceCircle(image, mask_green)
        green(mask_green)
                
       
        opening = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
        opening = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)
        x, y, w, h = cv2.boundingRect(opening)
        print(x, ",",y)

        cv2.imshow('frame',image) 
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    #Chiusura connessione
    connection.close()
    server_socket.close()
    # Distruzione finestra  
    cv2.destroyAllWindows() 
   
