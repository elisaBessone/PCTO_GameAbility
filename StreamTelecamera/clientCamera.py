import io
import socket
import struct
import time
import picamera


client_socket = socket.socket()

client_socket.connect(('192.168.0.119', 8000))  # aggiungere IP

# creazione di un oggetto simile a un file di connessione
connection = client_socket.makefile('wb')
try:
    camera = picamera.PiCamera()
    camera.vflip = True
    camera.resolution = (500, 480)

    #avvio anteprima per scaldare la telecamera
    camera.start_preview()
    time.sleep(2)

    # creazione del flusso per contenere temporaneamente i dati dell'immagine
    start = time.time()
    stream = io.BytesIO()
    for foo in camera.capture_continuous(stream, 'jpeg'):
        # scrittura della lunghezza della cattura del flusso per assicurarsi che venga attivato
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        # riavvolgo i dati e li invio al server
        stream.seek(0)
        connection.write(stream.read())
        # condizione di uscita
        if time.time() - start > 60:
            break
        # reset dello stream per la prossima cattura video
        stream.seek(0)
        stream.truncate()
    # scrittura della fine della connessione
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
