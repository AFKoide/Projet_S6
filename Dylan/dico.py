from PicoAutonomousRobotics import KitronikPicoRobotBuggy
from time import sleep_us, sleep, sleep_ms
from Fonction import *

buggy = KitronikPicoRobotBuggy()

buggy.setBrightness(50)
buggy.setMeasurementsTo("cm")
buggy.setLFDarkValue(40000)
buggy.setLFLightValue(15000)

etat = 0

commandes_rotation = {
    (1, 1, 0): (vitesse_moyenne, -vitesse_moyenne, 0.5),  # Tourner à gauche
    (1, 0, 0): (vitesse_lente, 0, 0.5),  # Tourner à droite
    (0, 1, 0): (0, vitesse_lente, 0.5),  # Tourner à gauche
}
