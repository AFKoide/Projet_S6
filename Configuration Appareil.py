# Suit la ligne noire
# Si se pert, tourne sur lui-même jusqu'à la trouver
# Si rencontre un obstacle, fait demi-tour
# Si les trois capteurs activés, s'arrete
# Une LED clignote pour indiquer que ca fonctionne
# Appuie sur un bouton pour lancer programme
# Avant lancement programme, LED indique si capteur fonctionne

from PicoAutonomousRobotics import KitronikPicoRobotBuggy
from time import sleep_us, sleep, sleep_ms
buggy = KitronikPicoRobotBuggy()

buggy.setBrightness(50)
buggy.setMeasurementsTo("cm")
buggy.setLFDarkValue(40000)
buggy.setLFLightValue(15000)

etat = 0

def ButtonIRQHandler(pin):
    global etat
    etat=etat+1
    etat=etat%3
    buggy.beepHorn()
    sleep(1)

buggy.button.irq(trigger=machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)

while True:
    if (etat == 0):
        buggy.setLED(2,buggy.GREEN)
        buggy.show()
        pass
    elif (etat == 1):
        buggy.setLED(2,buggy.YELLOW)
        print ("L" , buggy.getRawLFValue("l"), " R", buggy.getRawLFValue("r"), " C",buggy.getRawLFValue("c"))
        buggy.show()
        sleep(3)
        pass
    elif (etat == 2):
        buggy.setLED(2,buggy.BLUE)
        print(buggy.getDistance("f"))
        print(buggy.getDistance("r"))
        buggy.show()
        sleep(3)
        pass






















