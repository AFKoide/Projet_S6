# BIBLIOTHEQUE
import rp2
from PicoAutonomousRobotics import KitronikPicoRobotBuggy
buggy = KitronikPicoRobotBuggy()
from time import sleep_us, sleep, sleep_ms


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


### FONCTION
def moyenne(table):
    echantillon = 5
    if len(table)<echantillon:
        echantillon = len(table)
    moyenne = sum(table[-echantillon:])/echantillon
    
    if len(table)>echantillon+1:
        table.pop(0)
    return moyenne


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
    (int(0),int(0),int(1)): "angle_droite",
    (int(0),int(1),int(0)): "tout_droit",
    (int(0),int(1),int(1)): "gauche",
    (int(1),int(0),int(0)): "angle_gauche",
    (int(1),int(0),int(1)): "angle_gauche",
    (int(1),int(1),int(0)): "droite",
    (int(1),int(1),int(1)): "defaut"
}

vgauche = 0
vdroite = 0

gauche = []
droite = []
centre = []
devant = []
### BOUCLE PRINCIPALE
while True:
## Ecrit dans la mémoire les valeurs stockées
    gauche.append(buggy.getRawLFValue("l"))
    droite.append(buggy.getRawLFValue("r"))
    centre.append(buggy.getRawLFValue("c"))
    
    print("taille gauche=",len(gauche))
    print("taille droite=",len(droite))
    print("taille centre=",len(centre))
    
    print("moyenne gauche=",moyenne(gauche))
    print("moyenne droite=",moyenne(droite))
    print("moyenne centre=",moyenne(centre))
    
    capteurs = (int(moyenne(gauche) > seuils_capteurs["capteur_gauche_noir"]),
                int(moyenne(centre) > seuils_capteurs["capteur_centre_noir"]),
                int(moyenne(droite) > seuils_capteurs["capteur_droite_noir"])
            )
    
    ordre = directions.get(capteurs)
    
    print(ordre)
    
    if ordre == "perdu":
        vgauche = 50
        vdroite = 0
    elif ordre == "droite":
        vgauche = 50
        vdroite = 30
    elif ordre == "angle_droite":
        vgauche = 70
        vdroite = 0
    elif ordre == "gauche":
        vgauche = 30
        vdroite = 50
    elif ordre == "angle_gauche":
        vgauche = 0
        vdroite = 70
    elif ordre == "tout_droit":
        vgauche = 80
        vdroite = 80
    elif ordre == "defaut":
        vgauche = 0
        vdroite = 0
    else:
        print("ERREUR")
    
    
    ## BLOC DIRECTION (degueux, mais j'ai pas mieux)
# Marche/arret du moteur
    if etat == 0:
        buggy.setLED(1,buggy.RED)
    elif etat == 1:
        buggy.motorOn("l","f",vgauche)
        buggy.motorOn("r","f",vdroite)
        buggy.setLED(1,buggy.GREEN)
    buggy.show()
    
    sleep_ms(20)
    buggy.motorOn("l","f",0)
    buggy.motorOn("r","f",0)
    sleep(0.1)
