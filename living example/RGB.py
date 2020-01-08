from microbit import *   
import neopixel    #Reference library of RGB
from random import randint   #Reference random number function library
np = neopixel.NeoPixel(pin16, 4)    #Set the number of RGB lights connected to pin P16 to 4
while True:
    for pixel_id in range(0, len(np)):   #Update 4 RGB lamps in a loop
        red = randint(0, 60)    #Gets a random number between 0 and 60
        green = randint(0, 60)
        blue = randint(0, 60)
        np[pixel_id] = (red, green, blue)   #Trichromatic values are updated
        np.show()   #Status update of RGB lamp
        sleep(100)
