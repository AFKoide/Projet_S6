from PicoAutonomousRobotics import KitronikPicoRobotBuggy
from time import sleep_us, sleep, sleep_ms
from Fonction import *

buggy = KitronikPicoRobotBuggy()

buggy.setBrightness(50)
buggy.setMeasurementsTo("cm")
buggy.setLFDarkValue(40000)
buggy.setLFLightValue(15000)

etat = 0

def ButtonIRQHandler(pin):
    global etat
    etat ^= 1

    if etat is False:
        buggy.motorOn("l","f",0);buggy.motorOn("r","f",0)
buggy.button.irq(trigger=machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)

i = 0

while True:
    if etat is True:
        buggy.motorOn("l","f",v_gauche);buggy.motorOn("r","f",v_droit)

    gauche[i] = buggy.isLFSensorLight("l")
    droite[i] = buggy.isLFSensorLight("r")
    centre[i] = buggy.isLFSensorLight("c")
    devant[i] = buggy.getDistance("f")

    if 