from time import sleep
import numpy as np
from numpy.random import default_rng
rng = default_rng()

i= 0

gauche = np.zeros(10)

while True:
    gauche[i] = rng.random(1)*10
    
    i+= 1

    if i>= 10:
        avr_gauche = np.average(gauche)
        i= 0
        print("gauche: ",gauche,"  average: ",avr_gauche)

    sleep(1)