import signal
import time
from PicoAutonomousRobotics import KitronikPicoRobotBuggy
buggy = KitronikPicoRobotBuggy()
buggy.setBrightness(50)
buggy.setMeasurementsTo("cm")

from Direction import *

etat = 0
def ButtonIRQHandler(pin):
    etat+=1
    if etat==2:
        buggy.motorOn("l","f",0)
        buggy.motorOn("r","f",0)
        etat=0

buggy.button.irq(trigger=machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)

def interrupt_handler(signum, frame):
    Obstacle(sensor_front,sensor_left,sensor_right,sensor_center)
    exit(0)
signal.signal(signal.SIGINT, interrupt_handler)

# Boucle principale
while True:
    # Lire les valeurs des capteurs de ligne
    sensor_left = buggy.getRawLFValue("l")
    sensor_right = buggy.getRawLFValue("r")
    sensor_center = buggy.getRawLFValue("c")
    sensor_front = buggy.getDistance("f")


    if buggy.isLFSensorLight("l") and buggy.isLFSensorLight("f") is True:
        motor_left_speed,motor_right_speed = Intersection("left")
    elif buggy.isLFSensorLight("r") and buggy.isLFSensorLight("f") is True:
        motor_left_speed,motor_right_speed = Intersection("front")
    elif buggy.isLFSensorLight("l") and buggy.isLFSensorLight("r") is True and buggy.isLFSensorLight("f") is False:
        motor_left_speed,motor_right_speed = Intersection("left")
    elif buggy.isLFSensorLight("l") and buggy.isLFSensorLight("r") and buggy.isLFSensorLight("f") is True:
        motor_left_speed,motor_right_speed = Intersection("left")
    elif buggy.isLFSensorLight("l") and buggy.isLFSensorLight("r") and buggy.isLFSensorLight("f") is False:
        motor_left_speed,motor_right_speed = Perdu()
    else: 
        motor_left_speed,motor_right_speed = PID(sensor_left,sensor_right,sensor_center)
    
    # On envoie l'ordre d'avancer si le bouton a été pressé
    if etat==1:
        buggy.motorOn("l","f",motor_left_speed)
        buggy.motorOn("r","f",motor_right_speed)
    
    # Pause pour éviter une boucle trop rapide
    time.sleep(0.1)