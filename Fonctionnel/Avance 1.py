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

noir = 40000
blanc = 20000

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
        if vdroite<=100: vdroite += 1
        if vgauche>=70: vgauche -= 1
    elif droite >= noir:
        if vdroite>=70: vdroite -= 1
        if vgauche<=100: vgauche += 1
    elif gauche <=blanc and noir <= blanc:
        vgauche = 75
        vdroite = 75

    if etat == 1:
        buggy.motorOn("l","f",vgauche)
        buggy.motorOn("r","f",vdroite)
        
        
    sleep_ms(20)
    buggy.motorOn("l","f",0)
    buggy.motorOn("r","f",0)
    sleep(0.2)

