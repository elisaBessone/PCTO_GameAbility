import logging
import socket
import threading as thr
import time

registered = False
nickname = ""
SERVER=('192.168.0.123', 3450)
class Receiver(thr.Thread):
    def __init__(self, s): #Costruttore Thread, self è come il this, s è il socket
        thr.Thread.__init__(self)  #costruttore 
        self.running = True   #fino a quando esiste
        self.s = s 

    def stop_run(self): #in caso di stop
        self.running = False

    def run(self): #Al suo interno vengono eseguite tutte le zioni 
        global registered

        while self.running:
            data = self.s.recv(4096).decode()   #ricezione
            
            if data == "OK":    #Se riceve OK, la connessione è avvenuta
                registered = True
                logging.info(f"\nConnessione avvenuta, registrato. Entrando nella chat mode...")
            
            else:
                logging.info(f"\n{data}")

def main():
    global registered
    global nickname
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creo un socket TCP / IPv4, primo che manda, creo la base che fa tutto
    s.connect(SERVER)       #connessione al server

    ricev = Receiver(s) #riceve i messaggi, per far modo che il server quando rimanda il messaggio ai client arriva a tutti
    ricev.start()

    while True:
        time.sleep(0.2) 

        comando = input("Inserisci il comando >>>") #prende in input dall'utente il comando

        s.sendall(comando.encode()) #manda il messaggio al server

        if 'exit' in comando:   #In caso si dovesse interrompere la connessione
            ricev.stop_run()    #interrompe la connessione
            logging.info("Disconnessione...")
            break

    ricev.join()
    s.close()

if __name__ == "__main__":
    main()