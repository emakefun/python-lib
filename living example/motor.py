from microbit import *  #Reference microbit library
from Magicbit import *  #Reference Magicbit library
while True:
    motor_run(1, 250)   #Connect to the dc motor on the M1 pin, turn forward at speed 250
    motor_run(2, 250)   #Connect to the dc motor on the M2 pin, turn forward at speed 250
    motor_run(3, 250)   #Connect to the dc motor on the M3 pin, turn forward at speed 250
    motor_run(4, 250)   #Connect to the dc motor on the M4 pin, turn forward at speed 250
