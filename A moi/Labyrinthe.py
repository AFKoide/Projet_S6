# Suit la ligne noire
# Si se pert, tourne sur lui-même jusqu'à la trouver
# Si rencontre un obstacle, fait demi-tour
# Si les trois capteurs activés, s'arrete
# Une LED clignote pour indiquer que ca fonctionne
# Appuie sur un bouton pour lancer programme
# Avant lancement programme, LED indique si capteur fonctionne

from PicoAutonomousRobotics import KitronikPicoRobotBuggy
buggy = KitronikPicoRobotBuggy()
from time import sleep_us, sleep, sleep_ms
 


def thread0_Lumiere(status):
    global status
    while True:
        if status == 0:
            buggy.setLED(2,buggy.WHITE)
        elif status == "avant":
            buggy.setLED(0,buggy.GREEN)
            buggy.setLED(1,buggy.GREEN)
            buggy.clear(2)
            buggy.clear(3)
        elif status == "arriere":
            buggy.clear(0)
            buggy.clear(1)
            buggy.setLED(2,buggy.GREEN)
            buggy.setLED(3,buggy.GREEN)
        else: # Erreur etc.
            buggy.setLED(0,buggy.RED)
            buggy.setLED(1,buggy.RED)
            buggy.setLED(2,buggy.RED)
            buggy.setLED(3,buggy.RED)
        
        buggy.show()
        sleep(1)


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

vitesse_gauche = 50
vitesse_droit = 50
status = 0

def thread1_Commande():
    global vitesse_gauche, vitesse_droit, status, etat
    while True:
        gauche = buggy.getRawLFValue("l")
        droite = buggy.getRawLFValue("r")
        centre = buggy.getRawLFValue("c")
        devant = buggy.getDistance("f")
        if etat == 0:
            pass
        elif etat == 1:
            status = "avant"
            buggy.motorOn("l","f",vitesse_gauche);buggy.motorOn("r","f",vitesse_droit)

            if buggy.isLFSensorLight("l") is True:
                
        else:
            status = "erreur"




second_thread = _thread.start_new_thread(thread0_Lumiere, ())

thread1_Commande()