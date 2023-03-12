# Faire Avancer le Robot

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
    etat = etat+1;etat = etat%2

buggy.button.irq(trigger=machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)

vdroite = 5
vgauche = 5

while True:
    gauche = buggy.isLFSensorLight("l")
    droite = buggy.isLFSensorLight("r")
    centre = buggy.isLFSensorLight("c")
    devant = buggy.getDistance("f")

    if etat is 0:
        pass
    elif etat is 1:
        buggy.motorOn("l","f",vdroite);buggy.motorOn("r","f",vgauche)

    if centre is False:
        if gauche is False:
            if vdroite <= 8: vdroite +=1
            if vgauche >= 3: vgauche -=1
        elif droite is False:
            if vdroite <= 3: vdroite +=1
            if vgauche >= 8: vgauche -=1
        elif gauche is False and droite is False:
            if vdroite <= 5: vdroite +=1
            if vdroite >= 5: vdroite -=1
            if vgauche <= 5: vgauche +=1
            if vgauche >= 5: vgauche -=1
        elif gauche is True and droite is True:
            vdroite =0
            vgauche =0

    elif centre is True:
        if gauche is True:
            vdroite =0
            vgauche =3
        elif droite is True:
            vdroite =3
            vgauche =0
        elif gauche is True and droite is True:
            vdroite =5
            vgauche =1

    sleep(5)

