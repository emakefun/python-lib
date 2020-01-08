from microbit import *   #Reference microbit library
from Magicbit import *   #Reference Magicbit library
import neopixel
np = neopixel.NeoPixel(pin16, 10)  #RGB ultrasonic contains 6 RGB lamps inside, so the number is 10 (the expansion plate contains 4)
while True:
    for pixel_id in range(4, len(np)):  #The serial number of RGB lamps in ultrasonic wave is 4~9
        red = randint(0, 60)
        green = randint(0, 60)
        blue = randint(0, 60)
        np[pixel_id] = (red, green, blue)
        np.show()
        sleep(20)
    distance = get_UTdistance('P2', 'P2')   #Obtain the forward distance (cm) measured by ultrasound
    print(distance,'cm')

