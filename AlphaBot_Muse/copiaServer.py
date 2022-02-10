#!/usr/bin/python
# _*_ coding: utf-8 -*-
#server tpc

#copia del server sull'alphabot

import socket as sck
import threading as thr
import time
import RPi.GPIO as GPIO
import sqlite3 #libreria data base

TEMPO_PER_CURVARE_DI_90_GRADI = 0.5



lista_client = []

#classe thread

#funzione che si avvia alla creazione della classe
def __init__(self, connessione, indirizzo ,alphabot):
    thr.Thread.__init__(self)   #costruttore super (java)
    self.connessione = connessione
    self.indirizzo=indirizzo
    self.alphabot=alphabot          #per usare la classe del robot all'interno del thread
    self.running = True

#funzione che si avvia con il comando start()
"""def run(self):
    while self.running:     #ciclo infinito del programma
        messaggio = (self.connessione.recv(4096)).decode()          #ricevo il comando

        if messaggio == 'exit':             #per chiudere il programma e scollegare i client
            self.running = False

            lista_client.remove(self)
            
        else:
            print(messaggio)
        
            
            if messaggio.upper().startswith("W"):
                self.alphabot.forward()
                time.sleep(1)        #durata del movimento
                self.alphabot.stop()
            if messaggio.upper().startswith("D"):
                self.alphabot.right()
                time.sleep(1)   
                self.alphabot.stop()
            if messaggio.upper().startswith("S"):
                self.alphabot.backward()
                time.sleep(1)   
                self.alphabot.stop()
            if messaggio.upper().startswith("A"):
                self.alphabot.left()
                time.sleep(1)   
                self.alphabot.stop()
            if messaggio.upper().startswith("STOP"):
                self.alphabot.stop()
"""
            


class AlphaBot(object):  #classe dell'Alfabot
    
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 20  #velocità in girare
        self.PB  = 20   #velocità per girare

        #motori
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    def backward(self, speed=80):  #avanti a velocità 60
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)


        
    def stop(self):     #fermare i motori
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def forward(self , speed = 60):   #indietro velocità 60
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        
        

    def left(self, speed = 25):     #girare a sinistra velocità settata in precedenza
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
    
    
    def right(self, speed = 25):    #destra con la velocità settata in precedenza
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        
    def set_pwm_a(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)    
        
    def set_motor(self, left, right):
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM) 
    s.bind(('0.0.0.0', 3450))       #bind del server tcp
    s.listen()
    Ab = AlphaBot()      #inizzializzo alphabot

    running = True
   
    connessione, indirizzo = s.accept()   #connessioni dei client
    

    #client = Classe_Thread(connessione, indirizzo, Ab)
    #mettere codice run
    while running:     #ciclo infinito del programma
        messaggio = (connessione.recv(4096)).decode()          #ricevo il comando

        if messaggio == 'exit':             #per chiudere il programma e scollegare i client
            running = False

            lista_client.remove()
            
        else:
            print(messaggio)
                    
            if messaggio.upper().startswith("W"): #avanti
                Ab.forward()
                time.sleep(1)        #durata del movimento
                Ab.stop()
            if messaggio.upper().startswith("D"): #destra
                Ab.right()
                time.sleep(1)   
                Ab.stop()
            if messaggio.upper().startswith("S"): #indietro
                Ab.backward()
                time.sleep(1)   
                Ab.stop()
            if messaggio.upper().startswith("A"): #sinistra
                Ab.left()
                time.sleep(1)   
                Ab.stop()
            if messaggio.upper().startswith("ESCI"): #fermo
                Ab.stop()

    s.close()
   
main()