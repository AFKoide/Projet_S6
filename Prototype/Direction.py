import time
from PicoAutonomousRobotics import KitronikPicoRobotBuggy
buggy = KitronikPicoRobotBuggy()
buggy.setMeasurementsTo("cm")

def Obstacle(sensor_front,sensor_left,sensor_right,sensor_center):
    while sensor_left<=40000: 
        buggy.motorOn("l","f",5)
        buggy.motorOn("r","r",5)


def Intersection(type):
    match type:
        case "left":
            buggy.motorOn("l","f",8)
            buggy.motorOn("r","f",4)
            time.sleep_ms(10)
            return 0

        case "front":
            buggy.motorOn("l","f",5)
            buggy.motorOn("r","r",5)
            time.sleep_ms(10)
            return 0


def Perdu():
    i=0;j=0
    while buggy.isLFSensorLight("l") and buggy.isLFSensorLight("r") and buggy.isLFSensorLight("f") is False:
        buggy.motorOn("l","f",j-2)
        buggy.motorOn("r","r",j)
        i+=1
        if i>=10:
            j+=1
            i=0
        time.sleep(0.5)

# Initialiser les paramètres du PID
Kp = 0.5  # Constante proportionnelle
Ki = 0.1  # Constante intégrale
Kd = 0.2  # Constante dérivée

# Initialiser les variables PID 
last_error = 0
integral = 0

def PID(sensor_left,sensor_right,sensor_center):
    # Calculer l'erreur de suivi de ligne
    error = sensor_left - sensor_right
    
    # Calculer la correction PID
    proportional = Kp * error
    integral = integral + Ki * error
    derivative = Kd * (error - last_error)
    correction = proportional + integral + derivative
    
    # Appliquer la correction à la commande de mouvement du robot
    # à remplacer par la fonction de contrôle moteur du robot
    motor_left_speed = 5 + correction
    motor_right_speed = 5 - correction
    
    # Enregistrer l'erreur pour la prochaine itération
    last_error = error

    return motor_left_speed, motor_right_speed