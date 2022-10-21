# first client to move the alphabot with commands received from the keyboard with first test using muse 2

import logging
import socket
import threading as thr
import time
import read_muse_data
import utils

registered = False
nickname = ""
SERVER=('192.168.0.112', 3450)
class Receiver(thr.Thread):
    def __init__(self, s):
        thr.Thread.__init__(self) 
        self.running = True   
        self.s = s 

    def stop_run(self): 
        self.running = False

    def run(self): 
        global registered

        while self.running:
            data = self.s.recv(4096).decode()   #ricezione
            
            if data == "OK":    # If it gets OK, the connection is made
                registered = True
                logging.info(f"\nConnessione avvenuta, registrato. Entrando nella chat mode...")
            
            else:
                logging.info(f"\n{data}")

def main():
    global registered
    global nickname
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #I create a TCP socket / IPv4, first that sends, I create the base that does everything
    s.connect(SERVER)       #connessione to server

    ricev = Receiver(s) # receives messages, to ensure that the server when it sends the message to the clients arrives at all
    ricev.start()

    while True:
        time.sleep(0.2) 

        comando = input("Inserisci il comando >>>") #input from users
        
        #prova muse 2
        #fs = int(info.nominal_srate())
        #data_epoch = utils.get_last_data(eeg_buffer, EPOCH_LENGTH * fs)
        #comando = read_muse_data.muse()
        
        if(comando == 'W'): 
            print("comando ricevuto", comando)
            time.sleep(5)
        else:
            comando = 'ESCI' 
            print("comando ricevuto", comando)
            time.sleep(5)
            
        s.sendall(comando.encode()) # send the message to the server

        if 'exit' in comando:   # In case you break the connection
            ricev.stop_run()    #stop
            logging.info("Disconnessione...")
            break

    ricev.join()
    s.close()

if __name__ == "__main__":
    main()
