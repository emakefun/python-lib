from microbit import *
from Magicbit import *
while True:
    servo(1, 180)   #The PWM steering gear connected to pin S1 rotates to 180° position
    sleep(2000)
    servo(1, 0)     #The PWM steering gear connected to pin S1 rotates to the 0° position
    sleep(2000)
