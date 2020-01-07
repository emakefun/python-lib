from microbit import *
from Magicbit import *
import neopixel
np = neopixel.NeoPixel(pin16, 10)
while True:
    for pixel_id in range(4, len(np)):
        red = randint(0, 60)
        green = randint(0, 60)
        blue = randint(0, 60)
        np[pixel_id] = (red, green, blue)
        np.show()
        sleep(20)
    distance = get_UTdistance('P2', 'P2')
    print(distance,'cm')

