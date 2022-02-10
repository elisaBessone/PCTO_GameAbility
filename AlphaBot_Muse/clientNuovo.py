#versione client finale per comandare l'alphabot attraverso il muse 2
#va avanti se si è concentrati
#se si è concentrati e si gira la testa il robot gira nella direzione in cui il soggetto ha girato la testa
#se non si è concentrati l'alphabot sta fermo

import logging
import socket
import threading as thr
import time
import ModuloClient

registered = False
nickname = ""
SERVER=('192.168.0.123', 3450) #192.168.0.123 indirizzo IP alphabot
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

    comando = 'ESCI'
    while True:
        time.sleep(0.2) 

        concentrazione = ModuloClient.museConcentrazione() #funzione che calcola il livello di concentrazione
        
        print("comando concentrazione: ", concentrazione)
        
        time.sleep(0.5)
        
        if(concentrazione == 'W'): #soggetto concentrato
            comando = ModuloClient.museDxSx() #controllo di dove e se il soggetto gira la testa
            s.sendall(comando.encode()) #manda il messaggio al server
            #time.sleep(5)       
        else:
            comando = concentrazione #alphabot fermo (ESCI) causa soggetto non concentrato
            s.sendall(comando.encode()) #manda il messaggio al server
            #time.sleep(5)

        if 'exit' in comando:   #In caso si dovesse interrompere la connessione
            ricev.stop_run()    #interrompe la connessione
            logging.info("Disconnessione...")
            break

    ricev.join()
    s.close()

if __name__ == "__main__":
    main()