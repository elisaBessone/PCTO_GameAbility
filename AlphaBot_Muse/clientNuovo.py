# final client version to command the alphabot through the muse 2
# go ahead if you are focused
#If you are focused and you turn your head, the robot turns in the direction the subject turned their head
#if you are not focused the alphabot stands still

import logging
import socket
import threading as thr
import time
import ModuloClient

registered = False
nickname = ""
SERVER=('192.168.0.123', 3450) #192.168.0.123 IP address alphabot
class Receiver(thr.Thread):
    def __init__(self, s): #Thread constructor, self is like this, s is the socket
        thr.Thread.__init__(self)  #constructor 
        self.running = True   #as long as it exists
        self.s = s 

    def stop_run(self): #if it stops
        self.running = False

    def run(self): #Inside it all actions are performed
        global registered

        while self.running:
            data = self.s.recv(4096).decode()   #reception
            
            if data == "OK":    #If it receives OK, the connection is successful
                registered = True
                logging.info(f"\nConnessione avvenuta, registrato. Entrando nella chat mode...")
            
            else:
                logging.info(f"\n{data}")

def main():
    global registered
    global nickname
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #I create a TCP / IPv4 socket, first it sends, I create the base that does everything
    s.connect(SERVER)       #connection to the server

    ricev = Receiver(s) #receives messages, so that when the server sends the message back to clients, it reaches everyone
    ricev.start()

    comando = 'ESCI'
    while True:
        time.sleep(0.2) 

        concentrazione = ModuloClient.museConcentrazione() #function that calculates the concentration level
        
        #print("comando concentrazione: ", concentrazione)
        
        time.sleep(0.5)
        
        #lettura_file = open("file.txt", "r").read()
        if(concentrazione == 'W'): #concentrated subject
            comando = ModuloClient.museDxSx() #control of where and if the subject turns his head
            print("comando concentrazione: ", comando)
            s.sendall(comando.encode()) #send the message to the server
            #time.sleep(5)       
        else:
            comando = concentrazione #alphabot stopped (ESCI) cause unconcentrated subject
            print("comando concentrazione: ", concentrazione)
            s.sendall(comando.encode()) #send the message to the server
            #time.sleep(5)

        if 'exit' in comando:   #In case the connection should be interrupted
            ricev.stop_run()    #breaks the connection
            logging.info("Disconnessione...")
            break

    ricev.join()
    s.close()

if __name__ == "__main__":
    main()
