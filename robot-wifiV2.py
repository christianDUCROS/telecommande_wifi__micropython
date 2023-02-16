#1 connexion wifi ACCESS POINT
import network
import time

from machine import Pin
LED_builtin = Pin('LED', Pin.OUT) #create output pin 
LED_builtin.off()

wlan = network.WLAN(network.AP_IF)
wlan.config(essid= 'Robot', password = '123456789') 
wlan.active(True)
wlan.config(pm = 0xa11140)  #augmente la réactivité

while wlan.active == False :
    pass

print("Access point actif")
print(wlan.ifconfig())
print('Réseau wifi : Robot et mot de passe : 123456789')
LED_builtin.on()  #info serveur OK
time.sleep(3)
LED_builtin.off()


# Open socket
import socket
s = socket.socket()
s.bind(('0.0.0.0', 80))
s.listen(1)

import random #simulation capteur 

# Listen for connections
while True:
        cl,port = s.accept()
        while True :
            LED_builtin.on()  #connexion client (télécommande)
            
            request = cl.recv(1024) #reception données client
            #Analyse des infos télécommande  (request)
            request_dec = request.decode() # transforme un  bytearray en str
            request_split= request_dec.split(';') #séparer les données CSV
            joy_X_reçu = int(request_split[0]) #int car c’est des nombres
            joy_Y_reçu = int(request_split[1])
            print('joy_X_reçu :', joy_X_reçu,'\t joy_y_reçu :', joy_Y_reçu)
            
            # Préparation donnéees capteurs du robot (réponse au request)
            # simulation valeur capteurs robot
            capteur_robot_mur = random.randint(0,125)
            capteur_robot_ligne = random.randint(1,5)
            # Assemblage des données avec séparateur csv 
            infos_capteurs_robot = str(capteur_robot_mur) + ';' + str(capteur_robot_ligne)
            response = infos_capteurs_robot # Préparation de la réponse
            cl.send(response) # envoie au client
        cl.close()
        print('connection close')
        LED_builtin.off()
