# BIBLIOTHEQUE
from PicoAutonomousRobotics import KitronikPicoRobotBuggy
buggy = KitronikPicoRobotBuggy()
from time import sleep_us, sleep, sleep_ms


### DEBUG - Est ce que le code est executé
buggy.setLED(0,buggy.PURPLE)
buggy.show()


### COMMANDE - Switch des moteurs
etat = 0

def ButtonIRQHandler(pin):
    global etat
    etat +=1
    etat = etat%2
buggy.button.irq(trigger=machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)


### FONCTION
## Moyenne : calcul la moyenne d'une liste.
def moyenne(table):
    echantillon = 8
    # Nombre de valeur
    if len(table)<echantillon:
        echantillon = len(table)
    # Réduit le nombre de valeur à calculer si la liste est inférieure à l'échantillon
    moyenne = sum(table[-echantillon:])/echantillon
    # Calcul de la moyenne
    if len(table)>echantillon+1:
        table.pop(0)
    # Supprime la plus vieille valeur de la liste.
    return moyenne
    # Retourne la moyenne

## Moteur : simplifie l'utilisation de la fonction motorOn
def Moteur(roue,vitesse):
    sens = "f" if vitesse >= 0 else "r" # Si la vitesse est négative, alors la roue tourne dans le sens des aiguille d'une montre, sinon, elle tourne dans le sens anti-horaire
    vitesse = 100 if vitesse > 100 else vitesse # Empèche la vitesse d'être supérieure à 100.
    vitesse = abs(vitesse) # Retire le signe à la vitesse (une valeur négative dans motorOn équivaut à une vitesse nulle)

    buggy.motorOn(roue, sens, vitesse) # Fait tourner la roue


## Dictionnaire des seuils des capteurs : défini pour chaque capteur la valeur de seuil pour le blanc et le noir
seuils_capteurs = {
    "capteur_gauche_blanc": 25000,
    "capteur_gauche_noir": 35000,
    "capteur_droite_blanc": 25000,
    "capteur_droite_noir": 35000,
    "capteur_centre_blanc": 25000,
    "capteur_centre_noir": 35000,
}
## Dictionnaire des directions : dicte le comportement des roues selon une série de valeur binaire obtenue en comparant les capteurs et les seuils.
directions = {
    (int(0),int(0),int(0)): "perdu",
    (int(0),int(0),int(1)): "angle_droite",
    (int(0),int(1),int(0)): "tout_droit",
    (int(0),int(1),int(1)): "gauche",
    (int(1),int(0),int(0)): "angle_gauche",
    (int(1),int(0),int(1)): "angle_gauche",
    (int(1),int(1),int(0)): "droite",
    (int(1),int(1),int(1)): "croisement"
}

# Vitesse des moteurs (variables globale)
vgauche = 0
vdroite = 0

# Liste où seront stockées les valeurs des capteurs (variables globales)
gauche = []
droite = []
centre = []

### BOUCLE PRINCIPALE
while True:
## Ecrit dans la mémoire les valeurs stockées
    gauche.append(buggy.getRawLFValue("l"))
    droite.append(buggy.getRawLFValue("r"))
    centre.append(buggy.getRawLFValue("c"))

## Compare les capteurs avec les seuils, puis stock une valeur binaire
    capteurs = (
        int(moyenne(gauche) > seuils_capteurs["capteur_gauche_noir"]),
        int(moyenne(centre) > seuils_capteurs["capteur_centre_noir"]),
        int(moyenne(droite) > seuils_capteurs["capteur_droite_noir"])
    )

## Récupère le comportement à adopter après avoir comparé avec les capteurs
    ordre = directions.get(capteurs)
    

## DEBUG
    print(ordre)
    
## IF/ELSE pour piloter les moteurs
    if ordre == "perdu": # On tourne sur soi-même jusqu'à ce que le capteur du centre détecte la ligne centrale
        vgauche = -80
        vdroite = -80
        while moyenne(centre) > seuils_capteurs["capteur_centre_noir"]:
            centre.append(buggy.getRawLFValue("c"))
            Moteur("r", vdroite)
            Moteur("l", vgauche)

    elif ordre == "droite":
        vgauche = 80
        vdroite = 30

    elif ordre == "angle_droite":
        vgauche = 80
        vdroite = -80
        while moyenne(centre) > seuils_capteurs["capteur_centre_noir"]: # On tourne sur soi-même vers la droite jusqu'à ce que le capteur du centre détecte la ligne centrale
            centre.append(buggy.getRawLFValue("c"))
            Moteur("r", vdroite)
            Moteur("l", vgauche)

    elif ordre == "gauche":
        vgauche = 30
        vdroite = 80

    elif ordre == "angle_gauche":
        vgauche = -80
        vdroite = 80
        while moyenne(centre) > seuils_capteurs["capteur_centre_noir"]: # On tourne sur soi-même vers la gauche jusqu'à ce que le capteur du centre détecte la ligne centrale
            centre.append(buggy.getRawLFValue("c"))
            Moteur("r", vdroite)
            Moteur("l", vgauche)

    elif ordre == "tout_droit":
        vgauche = 80
        vdroite = 80

    else:
        print("ERREUR") # DEBUG
        
## DEBUG
    print("Vitesse Gauche: ",vgauche)
    print("Vitesse Droite: ",vdroite)
    


## BLOC DE COMMANDE
# Marche/arret du moteur
    if etat == 0:
        buggy.setLED(1,buggy.RED)
        Moteur("r", 0)
        Moteur("l", 0)
    elif etat == 1:
        buggy.setLED(1,buggy.GREEN)
        Moteur("r", vdroite)
        Moteur("l", vgauche)
    buggy.show() #Allume les DELs
