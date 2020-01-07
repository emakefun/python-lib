from microbit import *
import neopixel
from random import randint
np = neopixel.NeoPixel(pin16, 4)
while True:
    for pixel_id in range(0, len(np)):
        red = randint(0, 60)
        green = randint(0, 60)
        blue = randint(0, 60)
        np[pixel_id] = (red, green, blue)
        np.show()
        sleep(100)
