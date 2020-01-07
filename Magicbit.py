import math, ustruct, utime, microbit, neopixel
from microbit import sleep, pin0, pin1, pin2, pin8, pin12, pin13, pin14, pin15, pin16
from microbit import i2c
from random import randint

pins = {'P0': pin0, 'P1': pin1, 'P2': pin2, 'P8': pin8, 'P12': pin12, 'P13': pin13, 'P14': pin14, 'P15': pin15}
class PCA9685(object):
    def __init__(self, i2c, address = 0x40):
        self.address = address
        i2c.write(self.address, bytearray([0x00, 0x00]))  # reset not sure if needed but other libraries do it
        i2c.write(self.address, bytearray([0x01, 0x04]))
        i2c.write(self.address, bytearray([0x00, 0x01]))
        sleep(5)  # wait for oscillator
        i2c.write(self.address, bytearray([0x00]))  # write register we want to read from first
        mode1 = i2c.read(self.address, 1)
        mode1 = ustruct.unpack('<H', mode1)[0]
        mode1 = mode1 & ~0x10  # wake up (reset sleep)
        i2c.write(self.address, bytearray([0x00, mode1]))
        sleep(5)  # wait for oscillator
    def set_pwm_freq(self, freq_hz):
        prescaleval = 25000000.0  # 25MHz
        prescaleval /= 4096.0  # 12-bit
        prescaleval /= float(freq_hz)
        prescaleval -= 1
        prescale = int(math.floor(prescaleval + 0.5))
        i2c.write(self.address, bytearray([0x00]))  # write register we want to read from first
        oldmode = i2c.read(self.address, 1)
        oldmode = ustruct.unpack('<H', oldmode)[0]
        newmode = (oldmode & 0x7F) | 0x10  # sleep
        i2c.write(self.address, bytearray([0x00, newmode]))  # go to sleep
        i2c.write(self.address, bytearray([0xFE, prescale]))
        i2c.write(self.address, bytearray([0x00, oldmode]))
        sleep(5)
        i2c.write(self.address, bytearray([0x00, oldmode | 0x80]))
    def set_pwm(self, channel, on, off):
        if on is None or off is None:
            i2c.write(self.address, bytearray([0x06 + 4 * channel]))  # write register we want to read from first
            distance = i2c.read(self.address, 4)
            return ustruct.unpack('<HH', distance)
        i2c.write(self.address, bytearray([0x06 + 4 * channel, on & 0xFF]))
        i2c.write(self.address, bytearray([0x07 + 4 * channel, on >> 8]))
        i2c.write(self.address, bytearray([0x08 + 4 * channel, off & 0xFF]))
        i2c.write(self.address, bytearray([0x09 + 4 * channel, off >> 8]))
    def set_all_pwm(self, on, off):
        i2c.write(self.address, bytearray([0xFA, on & 0xFF]))
        i2c.write(self.address, bytearray([0xFB, on >> 8]))
        i2c.write(self.address, bytearray([0xFC, off & 0xFF]))
        i2c.write(self.address, bytearray([0xFD, off >> 8]))

pwm = PCA9685(i2c)
pwm.set_pwm_freq(50)

def servo(index, degree): #index:1~8,degree:0~180
    degree = (degree * 10 + 600) * 4096 // 20000
    pwm.set_pwm(index, 0, degree)

def stepper(index, sense_of_rotation):  #index:1~2,sense_of_rotation:0~1
    if index == 2:
        if sense_of_rotation == 0:
            pwm.set_pwm(0, 2047, 4095)
            pwm.set_pwm(2, 1, 2047)
            pwm.set_pwm(1, 1023, 3071)
            pwm.set_pwm(3, 3071, 1023)
        elif sense_of_rotation == 1:
            pwm.set_pwm(3, 2047, 4095)
            pwm.set_pwm(1, 1, 2047)
            pwm.set_pwm(2, 1023, 3071)
            pwm.set_pwm(0, 3071, 1023)
    elif index == 1:
        if sense_of_rotation == 0:
            pwm.set_pwm(4, 2047, 4095)
            pwm.set_pwm(6, 1, 2047)
            pwm.set_pwm(5, 1023, 3071)
            pwm.set_pwm(7, 3071, 1023)
        elif sense_of_rotation == 1:
            pwm.set_pwm(7, 2047, 4095)
            pwm.set_pwm(5, 1, 2047)
            pwm.set_pwm(6, 1023, 3071)
            pwm.set_pwm(4, 3071, 1023)

def stepper_degree(index, degree): #index:1 ~ 2,degree:-360 ~ 360
    stepper(index, degree > 0)
    degree = abs(degree)
    sleep(10240 * degree / 360)
    for i in range(0, 16):
        pwm.set_pwm(i, 0, 0)

def motor_run(index, speed):  #index:1~4,speed:-250~250
    speed = speed * 16
    if speed >= 4096:
        speed = 4095
    if speed <= -4096:
        speed = -4095
    if index > 4 or index <= 0:
        return
    if index == 1:index = 3
    elif index == 2:index = 4
    elif index == 3:index = 1
    elif index == 4:index = 2
    pp = (index - 1) * 2
    pn = (index - 1) * 2 + 1
    if speed >= 0:
        pwm.set_pwm(pp, 0, speed)
        pwm.set_pwm(pn, 0, 0)
    else:
        pwm.set_pwm(pp, 0, 0)
        pwm.set_pwm(pn, 0, -speed)

def stop_pwm_more(start, end): #start:1~16,end>=start
    for i in range(start-1, end-1):
        pwm.set_pwm(i, 0, 0)

def stop_car():
    stop_pwm_more(1, 9)

def get_UTdistance(trig, echo): #trig/echo:P0、P1、P2、P8、P12、P13、P14、P15
    pins[echo].write_digital(0)
    utime.sleep_us(2)
    pins[trig].write_digital(1)
    utime.sleep_us(15)
    pins[trig].write_digital(0)
    while(pins[echo].read_digital() == 0):
        pass
    time_start = utime.ticks_us()
    while pins[echo].read_digital():
        pass
    distance = ((utime.ticks_us() - time_start) / 10000) * 340 / 2
    distance = [distance, 300][distance > 300]
    return distance