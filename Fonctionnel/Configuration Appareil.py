# Utilisé pour configurer la machine

from PicoAutonomousRobotics import KitronikPicoRobotBuggy
from time import sleep_us, sleep, sleep_ms
buggy = KitronikPicoRobotBuggy()

etat = 0

def ButtonIRQHandler(pin):
    global etat
    etat=etat+1
    etat=etat%3
    buggy.beepHorn()
    sleep(1)

buggy.button.irq(trigger=machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)

while True:
    if (etat == 0): # ATTENTE POUR CONFIGURATION
        buggy.setLED(2,buggy.GREEN)
        buggy.show()
        pass
    elif (etat == 1):  # DETERMINER LES SEUILS
        buggy.setLED(2,buggy.YELLOW)
        print ("L" , buggy.getRawLFValue("l"), " R", buggy.getRawLFValue("r"), " C",buggy.getRawLFValue("c"))
        buggy.show()
        sleep(3)
        pass
    elif (etat == 2): # VERIFIER LA DISTANCE
        buggy.setLED(2,buggy.BLUE)
        print(buggy.getDistance("f"))
        print(buggy.getDistance("r"))
        buggy.show()
        sleep(3)
        pass






















