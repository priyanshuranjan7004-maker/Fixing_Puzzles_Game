
import sys
from machine import Pin, SPI
import vga1_8x8 as font
import st7789


BAUDRATE = 30000000
COLUMNS = 240
ROWS = 240
SCK_PIN = 2
MOSI_PIN = 3
RESET_PIN = 0
DC_PIN = 1

MADCTL_MY = 0x80
MADCTL_MX = 0x40
MADCTL_MV = 0x20
MADCTL_ML = 0x10
MADCTL_MH = 0x04
MADCTL_RGB = 0x08

COLSTART = 0
ROWSTART = 1
NAME = 0
VAL = 1
KEYS = 0
FUNC = 1
ARGS = 2

COLORS = [['Red', st7789.RED],['Green', st7789.GREEN], ['Blue', st7789.BLUE]]
ORDERS = [['st7789.RGB', st7789.RGB], ['st7789.BGR', st7789.BGR]]
INVERSIONS = [['False', False], ['True', True]]

def show_help():
    print('\n\nKeys:')
    print('+ Next rotation')
    print('- Previous rotation')
    print('W -10 rowstart, w -1 rowstart')
    print('A -10 colstart, a -1 colstart')
    print('S +10 rowstart, s +1 rowstart')
    print('D +10 colstart, d +1 colstart')
    print('O, o toggle MADCTL_RGB Change color_order')
    print('Y, y Toggle MADCTL_MY Page Address Order')
    print('X, x Toggle MADCTL_MX Column Address Order')
    print('V, v Toggle MADCTL_MV Page/Column Order ')
    print('L, l Toggle MADCTL_ML Line Address Order')
    print('H, h Toggle MADCTL_MH Display Data Latch Order')
    print('C, c Set Columns')
    print('R, r Set Rows')
    print('I, i Toggle inversion')
    print('B, b Change background')
    print('P, p Print current settings')
    print('?    Show Help\n')

class CfgHelper():
    def __init__(self, spi, columns, rows):
        self.spi = spi
        self.rows = rows
        self.columns = columns
        self.rotation = 0
        self.order = 0
        self.color = 0
        self.inversion = 0
        self.madctl = 0
        self.change = True
        self.init_required = False
        self.starts = [[0, 0], [0, 0], [0, 0], [0, 0]]
        self.tft = self.init_display()

    def init_display(self):
        tft = st7789.ST7789(
            self.spi,
            self.columns,
            self.rows,
            reset=Pin(RESET_PIN, Pin.OUT),
            dc=Pin(DC_PIN, Pin.OUT),
            color_order=ORDERS[self.order][VAL],
            rotation=self.rotation)

        tft.init()
        self.madctl = tft.madctl()
        self.init_required = False
        return tft

    def center(self, line, text):
        col = (self.columns >> 1) - (len(text) * font.WIDTH >> 1)
        self.tft.text(
            font,
            text,
            col,
            line,
            st7789.WHITE,
            COLORS[self.color][VAL])

    def decode_madctl(self):
        bits = [bit[NAME] for bit in [
            ("MY", MADCTL_MY),
            ("MX", MADCTL_MX),
            ("MV", MADCTL_MV),
            ("ML", MADCTL_ML),
            ("RGB", MADCTL_RGB),
            ("MH", MADCTL_MH)] if bit[VAL] & self.madctl]

        return " ".join(bits)

    def change_rowstart(self, value):
        self.starts[self.rotation][ROWSTART] += value
        self.starts[self.rotation][ROWSTART] %= self.rows

    def change_colstart(self, value):
        self.starts[self.rotation][COLSTART] += value
        self.starts[self.rotation][COLSTART] %= self.columns

    def change_rotation(self, value):
        self.rotation += value
        self.rotation %= 4
        self.tft.rotation(self.rotation)
        self.columns = self.tft.width()
        self.rows = self.tft.height()

    def print_settings(self):
        print("\n\nCurrent settings:")
        print(f'rotation = {self.rotation}')
        print(f'madctl = 0x{self.madctl:02x} ({self.decode_madctl()})')
        print(f'inversion_mode({INVERSIONS[self.inversion][NAME]})')
        print(f'color_order = {ORDERS[self.order][NAME]}')
        for index, offset in enumerate(self.starts):
            print(f'for rotation {index} use offset({offset[COLSTART]}, {offset[ROWSTART]})')
        print()

    def toggle_inversion(self):
        self.inversion += 1
        self.inversion %= len(INVERSIONS)
        print(f'inversion({INVERSIONS[self.inversion][NAME]})')

    def change_background(self, value):
        self.color += value
        self.color %= len(COLORS)
        print(f'background = {COLORS[self.color][NAME]}')

    def toggle_madctl_bit(self, name, bit):
        self.madctl ^= bit
        self.tft.madctl(self.madctl)
        if self.madctl & bit:
            print(f'{name} Set')
        else:
            print(f'{name} Cleared')

        self.order = 1 if self.madctl & MADCTL_RGB else 0

    def set_rows(self):
        rows_entered = int(input("Enter Rows (0-Cancel) ?"))
        if  rows_entered != 0:
            self.rows = rows_entered
            self.init_required = True

    def set_columns(self):
        cols_entered = int(input("Enter Columns (0-Cancel) ?"))
        if  cols_entered != 0:
            self.columns = cols_entered
            self.init_required = True

    def reset_rotations(self):
        self.starts = [[0, 0], [0, 0], [0, 0], [0, 0]]
        self.rotation = 0
        self.init_required = True

    def update_display(self):
        self.tft.fill(COLORS[self.color][VAL])

        self.center(font.HEIGHT, f'Rot {self.rotation}')
        self.center(font.HEIGHT*3, COLORS[self.color][NAME])
        self.center(font.HEIGHT*5, f'MADCTL 0x{self.madctl:02x}')
        self.center(font.HEIGHT*6, self.decode_madctl())
        self.center(font.HEIGHT*8, f'colstart {self.starts[self.rotation][COLSTART]}')
        self.center(font.HEIGHT*9, f'rowstart {self.starts[self.rotation][ROWSTART]}')
        self.center(font.HEIGHT*11,"inversion")
        self.center(font.HEIGHT*12, f'{INVERSIONS[self.inversion][NAME]}')

        self.tft.rect(0, 0, self.columns, self.rows, st7789.WHITE)
        print('? for help: ', end='')

    def menu(self):
        menu_items = [
            ({'W'},      self.change_rowstart,    (-10,)),
            ({'w'},      self.change_rowstart,    (-1,)),
            ({'S'},      self.change_rowstart,    (10,)),
            ({'s'},      self.change_rowstart,    (1,)),
            ({'A'},      self.change_colstart,    (-10,)),
            ({'a'},      self.change_colstart,    (-1,)),
            ({'D'},      self.change_colstart,    (10,)),
            ({'d'},      self.change_colstart,    (1,)),
            ({'+'},      self.change_rotation,    (1,)),
            ({'-'},      self.change_rotation,    (-1,)),
            ({'P', 'p'}, self.print_settings,     ()),
            ({'I', 'i'}, self.toggle_inversion,   ()),
            ({'B'},      self.change_background,  (1,)),
            ({'b'},      self.change_background,  (-1,)),
            ({'O', 'o'}, self.toggle_madctl_bit,  ("MADCTL_RGB", MADCTL_RGB)),
            ({'Y', 'y'}, self.toggle_madctl_bit,  ("MADCTL_MY",  MADCTL_MY)),
            ({'X', 'x'}, self.toggle_madctl_bit,  ("MADCTL_MX",  MADCTL_MX)),
            ({'V', 'v'}, self.toggle_madctl_bit,  ("MADCTL_MV",  MADCTL_MV)),
            ({'L', 'l'}, self.toggle_madctl_bit,  ("MADCTL_ML",  MADCTL_ML)),
            ({'H', 'h'}, self.toggle_madctl_bit,  ("MADCTL_MH",  MADCTL_MH)),
            ({'R', 'r'}, self.set_rows,           ()),
            ({'C', 'c'}, self.set_columns,        ()),
            ({'0'},      self.reset_rotations,    ()),
            ({'?'},      show_help,               ())]

        while True:
            if self.change:
                if self.init_required:
                    self.tft = self.init_display()

                self.tft.offset(
                    self.starts[self.rotation][COLSTART],
                    self.starts[self.rotation][ROWSTART])

                self.tft.inversion_mode(INVERSIONS[self.inversion][VAL])

                self.update_display()

            key_pressed = sys.stdin.read(1)
            self.change = False

            for menu_item in menu_items:
                if key_pressed in menu_item[KEYS]:
                    print(key_pressed)
                    _, action, args = menu_item
                    action(*args)
                    self.change = True

def main():

    display_spi = SPI(0, baudrate=BAUDRATE, sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN))
    cfg = CfgHelper(display_spi, COLUMNS, ROWS)
    show_help()
    while True:
        cfg.menu()

main()
