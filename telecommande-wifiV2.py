#1 connexion wifi STATION
import network
import time

from machine import Pin
LED_builtin = Pin('LED', Pin.OUT) #create output pin 
LED_builtin.off()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm = 0xa11140)  #augmente la réactivité
wlan.connect('Robot', '123456789')

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)

print('Connexion wifi OK')
print('IP de la télécommande = ', wlan.ifconfig()[0])
LED_builtin.on()  #info serveur OK
time.sleep(3)
LED_builtin.off()

# Open socket
import socket
s = socket.socket() 

import random #simulation capteur 

while True:
    try :
        s.connect(('192.168.4.1',80))
        while True :
            LED_builtin.on()  #connexion serveur (robot)
                
            # Simulation lectures capteur
            capteurJoyX = random.randint(0,1024)
            capteurJoyY = random.randint(0,1024)
            # Assemblage des données avec séparateur csv 
            infos_telecommande  = str(capteurJoyX) + ';' + str(capteurJoyY) 
            request = infos_telecommande # données envoyée lors des échanges 
            s.send(request) # send request
            
            #reception infos_capteurs_robot 
            response = s.recv(1024)
            #analyse des infos_capteurs_robot (split)
            response_dec = response.decode() # transforme un  bytearray en str
            response_split= response_dec.split(';') #séparer les données CSV
            capteur_robot_mur = int(response_split[0])
            capteur_robot_ligne = int(response_split[1])
            print('robot_mur :',capteur_robot_mur, '\t robot_ligne :',capteur_robot_ligne)
            time.sleep(0.2)    # wait entre 2 liaisons wifi
                
    except :
        s.close()
        print('Problème de connexion')
        LED_builtin.off()  #problème de serveur
        time.sleep(1)
