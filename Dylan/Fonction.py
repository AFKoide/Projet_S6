from PicoAutonomousRobotics import KitronikPicoRobotBuggy


def moyenne(i,table):
    echantillon = i
    moyenne = table[-echantillon:]/echantillon
    return round(moyenne,0)