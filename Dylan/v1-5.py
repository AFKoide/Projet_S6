# Faire Avancer le Robot

from PicoAutonomousRobotics import KitronikPicoRobotBuggy
buggy = KitronikPicoRobotBuggy()
from time import sleep_us, sleep, sleep_ms

etat = 0

def ButtonIRQHandler(pin):
    global etat
    etat +=1
    etat = etat%2
buggy.button.irq(trigger=machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)

buggy.setLED(0,buggy.PURPLE)
buggy.setLED(1,buggy.PURPLE)
buggy.setLED(2,buggy.PURPLE)
buggy.setLED(3,buggy.PURPLE)
buggy.show()

Cnoir = 35000
Cblanc = 25000
Dnoir = 35000
Dblanc = 25000
Gnoir = 35000
Gblanc = 25000
noir = 35000
blanc = 25000

vgauche = 75
vdroite = 75

while True:    
    gauche = buggy.getRawLFValue("l")
    droite = buggy.getRawLFValue("r")
    centre = buggy.getRawLFValue("c")
    devant = buggy.getDistance("f")
    
    print("\netat=",etat)
    print("gauche=",gauche)
    print("droite=",droite)
    print("centre=",centre)
    
    print("vitesse gauche=",vgauche)
    print("vitesse droite=",vdroite)
    
    if gauche >= noir:
        vdroite = 80
        vgauche = 70
    elif droite >= noir:
        vdroite = 70
        vgauche = 80
    elif gauche <=blanc and noir <= blanc:
        vgauche = 75
        vdroite = 75

    if etat == 1:
        buggy.motorOn("l","f",vgauche)
        buggy.motorOn("r","f",vdroite)
        

        
    sleep_ms(20)
    buggy.motorOn("l","f",0)
    buggy.motorOn("r","f",0)
    sleep(0.1)
