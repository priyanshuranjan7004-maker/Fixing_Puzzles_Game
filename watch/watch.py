
import utime
import time
import math
import st7789
import gc
import uos
import machine
from libs import lcd

gc.collect()
spi_sck = machine.Pin(2, machine.Pin.OUT)
spi_tx = machine.Pin(3, machine.Pin.OUT)
lcd_reset = machine.Pin(0, machine.Pin.OUT)
lcd_dc = machine.Pin(1, machine.Pin.OUT)
spi_lcd = machine.SPI(0, baudrate=40000000, phase=1, polarity=1, sck=spi_sck, mosi=spi_tx)
tft = lcd.lcd_config(spi_lcd, width=240, height=240, reset=lcd_reset, dc=lcd_dc, rotation=0)


def hand_polygon(length, radius):
    return [
        (0, 0),
        (-radius, radius),
        (-radius, int(length * 0.3)),
        (-1, length),
        (1, length),
        (radius, int(length * 0.3)),
        (radius, radius),
        (0,0)
    ]


def main():
    tft.init()
    width = tft.width()
    height = tft.height()
    radius = min(width, height)         # face is the smaller of the two
    ofs = (width - radius) // 2         # offset from the left to center the face
    center_x = radius // 2 + ofs - 1    # center of the face horizontally
    center_y = radius // 2 - 1          # center of the face vertically

    face = "face_{}x{}.jpg".format(width, height)
    tft.jpg(face, 0, 0, st7789.SLOW)


    second_len = int(radius * 0.65 / 2)
    second_poly = hand_polygon(second_len, 2)

    minute_len = int(radius * 0.6 / 2)
    minute_poly = hand_polygon(minute_len, 2)

    hour_len = int(radius * 0.5 / 2)
    hour_poly = hand_polygon(hour_len, 3)

    pi_div_6 = math.pi/6
    pi_div_30 = math.pi/30
    pi_div_360 = math.pi/360
    pi_div_1800 = math.pi/1800
    pi_div_2160 = math.pi/2160


    tft.bounding(True)
    hour_bound = tft.bounding(True)
    minute_bound = tft.bounding(True)
    second_bound = tft.bounding(True)

    while True:
        last = utime.time()

        _, _, _, hour, minute, second, _, _ = utime.localtime()

        hour %= 12

        hour_ang = (
            (hour * pi_div_6) +
            (minute * pi_div_360) +
            (second * pi_div_2160))

        minute_ang = ((minute*pi_div_30)+(second*pi_div_1800))

        second_ang = (second*pi_div_30)

        x1, y1, x2, y2 = hour_bound
        tft.fill_rect(x1, y1, x2, y2, st7789.WHITE)

        x1, y1, x2, y2 = minute_bound
        tft.fill_rect(x1, y1, x2, y2, st7789.WHITE)

        x1, y1, x2, y2 = second_bound
        tft.fill_rect(x1, y1, x2, y2, st7789.WHITE)

        tft.fill_circle(center_x, center_y, 5, st7789.BLACK)

        tft.bounding(True)

        tft.fill_polygon(hour_poly, center_x, center_y, st7789.BLACK, hour_ang)

        hour_bound = tft.bounding(True, True)

        tft.fill_polygon(minute_poly, center_x, center_y, st7789.BLACK, minute_ang)

        minute_bound = tft.bounding(True, True)


        tft.fill_polygon(second_poly, center_x, center_y, st7789.RED, second_ang)

        second_bound = tft.bounding(True, True)

        tft.fill_circle(center_x, center_y, 5, st7789.BLACK)

        while last == utime.time():
           utime.sleep_ms(50)


main()
