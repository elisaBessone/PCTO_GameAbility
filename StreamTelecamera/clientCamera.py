import io
import socket
import struct
import time
import picamera


client_socket = socket.socket()

client_socket.connect(('192.168.0.119', 8000))  # add IP

# creation of an object similar to a connection file
connection = client_socket.makefile('wb')
try:
    camera = picamera.PiCamera()
    camera.vflip = True
    camera.resolution = (500, 480)

    camera.start_preview()
    time.sleep(2)

    
    start = time.time()
    stream = io.BytesIO()
    for foo in camera.capture_continuous(stream, 'jpeg'):
        
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        
        # data sent to the server
        stream.seek(0)
        connection.write(stream.read())
        
        if time.time() - start > 60:
            break
        # reset stream
        stream.seek(0)
        stream.truncate()
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
