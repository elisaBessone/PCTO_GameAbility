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
#FONT_HERSHEY_SIMPLEX = 0


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
        #https://www.reddit.com/r/opencv/comments/9scy4j/question_can_i_create_a_videocapture_object_from/e8o19hv/
        cap = np.frombuffer(image.getValue(), dtype='int8')

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        cv2.imshow('frame',image) 
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    #Chiusura connessione
    connection.close()
    server_socket.close()
    # Distruzione finestra  
    cv2.destroyAllWindows() 