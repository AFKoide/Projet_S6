# BIBLIOTHEQUE
import threading
from PicoAutonomousRobotics import KitronikPicoRobotBuggy
buggy = KitronikPicoRobotBuggy()
from time import sleep_us, sleep, sleep_ms


### FONCTION
## Affiche les valeurs en temps réels des différents capteurs
def Affichage():
    print("\netat=",etat)
    print("gauche=",gauche[-1])
    print("droite=",droite[-1])
    print("centre=",centre[-1])
    
    print("vitesse gauche=",vgauche)
    print("vitesse droite=",vdroite)

## Fait la moyenne de ce qu'on lui donne
def moyenne(table):
    echantillon = 10
    if len(table)<echantillon:
        echantillon = len(table)
    moyenne = sum(table[-echantillon:])/echantillon
    return moyenne


### DEBUG - Robot allumé
buggy.setLED(0,buggy.PURPLE)
buggy.show()


### COMMANDE - Allume/éteint les moteurs
etat = 0

def ButtonIRQHandler(pin):
    global etat
    etat +=1
    etat = etat%2
buggy.button.irq(trigger=machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)


### VARIABLE - stockage global
seuils_capteurs = {
    "capteur_gauche_blanc": 25000,
    "capteur_gauche_noir": 35000,
    "capteur_droite_blanc": 25000,
    "capteur_droite_noir": 35000,
    "capteur_centre_blanc": 25000,
    "capteur_centre_noir": 35000,
}
directions = {
    (int(0),int(0),int(0)): "perdu",
    (int(0),int(0),int(1)): "angle droite",
    (int(0),int(1),int(0)): "tout droit",
    (int(0),int(1),int(1)): "tout droit",
    (int(1),int(0),int(0)): "angle gauche",
    (int(1),int(0),int(1)): "gauche",
    (int(1),int(1),int(0)): "gauche",
    (int(1),int(1),int(1)): "gauche"
}

n = 0
gauche = []
droite = []
centre = []
devant = []

vgauche = 75
vdroite = 75

### BOUCLE PRINCIPALE
while True:


## DEBUG
    

    
    # blanc = (int(moyenne(gauche) < seuils_capteurs["capteur_gauche_blanc"]),
    #          int(moyenne(centre) > seuils_capteurs["capteur_centre_blanc"]),
    #          int(moyenne(droite) > seuils_capteurs["capteur_droite_blanc"]))
    #         )

    direction = directions[capteurs]
    print("Direction :", direction)







def moteurs():
    global vgauche
    global vdroite
    
    while True: 
        if etat == 0:
            buggy.setLED(1,buggy.RED)
        elif etat == 1:
            buggy.motorOn("l","f",vgauche)
            buggy.motorOn("r","f",vdroite)
            buggy.setLED(1,buggy.GREEN)
        buggy.show()

## "Horloge" pour ralentir le robot.
    sleep_ms(20)
    buggy.motorOn("l","f",0)
    buggy.motorOn("r","f",0)
    sleep(0.1)



def capteurs():
    while True: 
        ## Ecrit dans la mémoire les valeurs stockées
        gauche[n] = buggy.getRawLFValue("l")
        droite[n] = buggy.getRawLFValue("r")
        centre[n] = buggy.getRawLFValue("c")
        devant[n] = buggy.getDistance("f")
        n+=1

        capteurs = (int(moyenne(gauche) > seuils_capteurs["capteur_gauche_noir"]),
                int(moyenne(centre) > seuils_capteurs["capteur_centre_noir"]),
                int(moyenne(droite) > seuils_capteurs["capteur_droite_noir"])
            )

        Affichage()






# création des threads
thread1 = threading.Thread(target=moteurs)
thread2 = threading.Thread(target=capteurs)

# démarrage des threads
thread1.start()
thread2.start()