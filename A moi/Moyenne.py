# On va calculer la moyenne de chaque capteur pour Xms.

import _thread
from time import sleep_us, sleep, sleep_ms
import numpy as np
from PicoAutonomousRobotics import KitronikPicoRobotBuggy
buggy = KitronikPicoRobotBuggy()


etat= 1

def ButtonIRQHandler(pin):
    etat=-etat
    buggy.beepHorn()
buggy.button.irq(trigger=machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)


i= 0
# Taille moyenne
gauche= np.zeros(10)
droite= np.zeros(10)
centre= np.zeros(10)
devant= np.zeros(10)
# Vitesse Initiale
vitesse_gauche= 1
vitesse_droit= 1

while True:
    if etat< 0:
        buggy.motorOn("l","f",vitesse_gauche)
        buggy.motorOn("r","f",vitesse_droit)


    gauche[i]= buggy.getRawLFValue("l")
    droite[i]= buggy.getRawLFValue("r")
    centre[i]= buggy.getRawLFValue("c")
    devant[i]= buggy.getRawLFValue("c")
    i+= 1

    if i>= 10: # Calcul de la moyenne des 10 valeurs
        avr_gauche= np.average(gauche)/10
        avr_droite= np.average(droite)/10
        avr_centre= np.average(centre)/10
        i= 0