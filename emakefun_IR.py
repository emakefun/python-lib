from microbit import *
import neopixel
np = neopixel.NeoPixel(pin16, 20)
import time
pins = {'P0': pin0, 'P1': pin1, 'P2': pin2, 'P8': pin8, 'P12': pin12, 'P13': pin13, 'P14': pin14, 'P15': pin15, 'P16': pin16}
def IR(Pin):   #红外基础库
    time_start = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    time_end = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if not pin2.read_digital():
        while pins[Pin].read_digital():  #高电平等待
            pass
        for i in range(32):
            while not pins[Pin].read_digital():  #低电平等待
                pass
            time_start[i] = time.ticks_us()   #开始记录
            while pins[Pin].read_digital():
                pass
            time_end[i] = time.ticks_us()   #结束记录
        for i in range(32):   #时间转换为二进制数据
            if (time_end[i] - time_start[i]) > 500 and (time_end[i] - time_start[i]) < 1000:
                data[i] = 0
            elif (time_end[i] - time_start[i]) > 1300 and (time_end[i] - time_start[i]) < 2000:
                data[i] = 1
            else:
                pass
        sign = 1  #数据检验变量
        data_hex = 0   #十六进制数据变量
        for i in range(8):   #检验数据是否正确
            if data[i + 16] - data[i + 24] == 0:
                sign = 0
                break
        if sign:   #数据转换
            data_hex = hex(data[16] * 128 + data[17] * 64 + data[18] * 32 + data[19] * 16 + data[20] * 8 + data[21] * 4 + data[22] * 2 + data[23] * 1)
        pins[Pin].write_digital(1)
        if data_hex == 0:  #连续按下按键，会返回一个‘FF’
            return 'FF'
        elif data_hex == '0xd1':
            return 'A'
        elif data_hex == '0xb1':
            return 'B'
        elif data_hex == '0xf1':
            return 'C'
        elif data_hex == '0x91':
            return 'D'
        elif data_hex == '0x81':
            return 'UP'
        elif data_hex == '0xe1':
            return 'ADD'
        elif data_hex == '0xf0' or data_hex == '0xfc':
            return 'LEFT'
        elif data_hex == '0xd4' or data_hex == '0xf5':
            return 'OK'
        elif data_hex == '0xc8' or data_hex == '0xf2':
            return 'RIGHT'
        elif data_hex == '0xb4' or data_hex == '0xed':
            return '0'
        elif data_hex == '0xcc' or data_hex == '0xf3':
            return 'DOWN'
        elif data_hex == '0xd8' or data_hex == '0xf6':
            return 'MINUS'
        elif data_hex == '0x98' or data_hex == '0xe6':
            return '1'
        elif data_hex == '0x8c' or data_hex == '0xe3':
            return '2'
        elif data_hex == '0xbd':
            return '3'
        elif data_hex == '0x88' or data_hex == '0xe2':
            return '4'
        elif data_hex == '0x9c' or data_hex == '0xe7':
            return '5'
        elif data_hex == '0xad':
            return '6'
        elif data_hex == '0xa1':
            return '7'
        elif data_hex == '0xa5':
            return '8'
        elif data_hex == '0xa9':
            return '9'
        else:
            return 'none'  #数据错误返回'none'
    else:
        return 'none'   #没有接收到信号返回'none'
def get_UTdistance(trig): #trig:P0、P1、P2、P8、P12、P13、P14、P15    #读取RGB超声波距离， 引脚 trig cm
    pins[trig].write_digital(0)
    time.sleep_us(2)
    pins[trig].write_digital(1)
    time.sleep_us(15)
    pins[trig].write_digital(0)
    while(pins[trig].read_digital() == 0):
        pass
    time_start = time.ticks_us()
    while pins[trig].read_digital():
        pass
    distance = ((time.ticks_us() - time_start) / 10000) * 340 / 2
    distance = [distance, 300][distance > 300]
    return distance

def RGB(start, end, red, green, blue):    #RGB基础库
    for RGB_id in range(0, start):
        np[RGB_id] = (0, 0, 0)
        np.show()
    for RGB_id in range(start, end):
        np[RGB_id] = (green, red, blue)
        np.show()
    for RGB_id in range(end, 20):
        np[RGB_id] = (0, 0, 0)
        np.show()

colours = {'Red': (255, 1, 1), 'Orange': (255, 165, 1), 'Yellow': (255, 255, 1), 'Green': (1, 255, 1), 'Blue': (1, 1, 255), 'Indigo': (75, 1, 130), 'Violet': (138, 43, 226), 'purple': (255, 1, 255), 'white': (255, 255, 255), 'black': (0, 0, 0)}
#derection:'left', 'right', 'all'
#colour:'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Indigo', 'Violet', 'Purple', 'White', 'Black'
#magic:'none', 'breathing', 'rotate', 'flicker'
def RGB_UT(direction, colour, magic):
    if direction == 'left':
        start = 4
        end = 7
    elif direction == 'right':
        start = 7
        end = 10
    elif direction == 'all':
        start = 4
        end = 10

    if magic == 'none':
        RGB(start, end, colours[colour][0], colours[colour][1], colours[colour][2])
    elif magic == 'breathing':   #呼吸灯
        if colour == 'black':
            RGB(start, end, colours[colour][0], colours[colour][1], colours[colour][2])
        else:
            for r, g, b in zip(range(0, colours[colour][0] * 50, colours[colour][0] * 100//40), range(0, colours[colour][1] * 50, colours[colour][1] * 100//40), range(0, colours[colour][2] * 50, colours[colour][2] * 100//40)):
                RGB(start, end, r//100, g//100, b//100)
                sleep(40)
            for r, g, b in zip(range(colours[colour][0] * 50, 0, -colours[colour][0] * 100//40), range(colours[colour][1] * 50, 0, -colours[colour][1] * 100//40), range(colours[colour][2] * 50, 0, -colours[colour][2] * 100//40)):
                RGB(start, end, r//100, g//100, b//100)
                sleep(40)
    elif magic == 'rotate':     #旋转流星
        if start == 4 and end == 10:
            for i in range(start, 7):
                RGB(i, i + 1, colours[colour][0], colours[colour][1], colours[colour][2])
                sleep(75)
                RGB(i + 3, i + 4, colours[colour][0], colours[colour][1], colours[colour][2])
                sleep(75)
        else:
            for i in range(start, end):
                RGB(i, i + 1, colours[colour][0], colours[colour][1], colours[colour][2])
                sleep(100)
    elif magic == 'flicker':     #闪烁灯
        RGB(start, end, colours[colour][0], colours[colour][1], colours[colour][2])
        sleep(150)
        RGB(start, end, 0, 0, 0)
        sleep(150)
    else:
        pass

if __name__ == '__main__':
    while True:
        print(get_UTdistance('P13'))
        sleep(500)
