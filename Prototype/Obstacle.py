# BIBLIOTHEQUE
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

def Moteur(roue,vitesse):
    sens = "f" if vitesse >= 0 else "r"
    vitesse = 100 if vitesse > 100 else vitesse
    vitesse = abs(vitesse)

    buggy.motorOn(roue, sens, vitesse)

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

### BOUCLE PRINCIPALE
while True:
## Ecrit dans la mémoire les valeurs stockées
    gauche.append(buggy.getRawLFValue("l"))
    droite.append(buggy.getRawLFValue("r"))
    centre.append(buggy.getRawLFValue("c"))
    distance = buggy.getDistance("f")
    
    capteurs = (
        int(moyenne(gauche) > seuils_capteurs["capteur_gauche_noir"]),
        int(moyenne(centre) > seuils_capteurs["capteur_centre_noir"]),
        int(moyenne(droite) > seuils_capteurs["capteur_droite_noir"])
    )
    
    ordre = directions.get(capteurs)   
#    print(ordre)
    
  if distance > 5:
    buggy.setLED(2,buggy.YELLOW)
  if distance < 20: 
    buggy.setLED(2,buggy.BLUE)
  elif distance < 5:
    buggy.setLED(2,buggy.RED)
  else:
    buggy.setLED(2,buggy.WHITE)
    
    
    if ordre == "perdu" or distance <= 5:
        vgauche = -80
        vdroite = -80
        while moyenne(centre) > seuils_capteurs["capteur_centre_noir"]:
            centre.append(buggy.getRawLFValue("c"))
            Moteur("r", vdroite)
            Moteur("l", vgauche)

    elif ordre == "droite":
        vgauche = 70
        vdroite = 30

    elif ordre == "angle_droite":
        vgauche = 80
        vdroite = -80

        while moyenne(centre) > seuils_capteurs["capteur_centre_noir"] and :
            centre.append(buggy.getRawLFValue("c"))
            Moteur("r", vdroite)
            Moteur("l", vgauche)
            

    elif ordre == "gauche":
        vgauche = 30
        vdroite = 70

    elif ordre == "angle_gauche":
        vgauche = -80
        vdroite = 80
        while moyenne(centre) > seuils_capteurs["capteur_centre_noir"]:
            centre.append(buggy.getRawLFValue("c"))
            Moteur("r", vdroite)
            Moteur("l", vgauche)

    elif ordre == "tout_droit":
        vgauche = 80
        vdroite = 80

    else:
        print("ERREUR")
        
    print("Vitesse Gauche:",vgauche)
    print("Vitesse Droite:",vdroite)
    print("Distance:",distance)


    ## BLOC DIRECTION (degueux, mais j'ai pas mieux)
# Marche/arret du moteur
    if etat == 0:
        buggy.setLED(1,buggy.RED)
        Moteur("r", 0)
        Moteur("l", 0)
    elif etat == 1:
        Moteur("r", vdroite)
        Moteur("l", vgauche)
        buggy.setLED(1,buggy.GREEN)
    buggy.show()
