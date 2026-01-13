import struct
from typing import Final


ST7789_NOP: Final[int] = ...
ST7789_SWRESET: Final[int] = ...
ST7789_RDDID: Final[int] = ...
ST7789_RDDST: Final[int] = ...

ST7789_SLPIN: Final[int] = ...
ST7789_SLPOUT: Final[int] = ...
ST7789_PTLON: Final[int] = ...
ST7789_NORON: Final[int] = ...

ST7789_INVOFF: Final[int] = ...
ST7789_INVON: Final[int] = ...
ST7789_DISPOFF: Final[int] = ...
ST7789_DISPON: Final[int] = ...
ST7789_CASET: Final[int] = ...
ST7789_RASET: Final[int] = ...
ST7789_RAMWR: Final[int] = ...
ST7789_RAMRD: Final[int] = ...

ST7789_PTLAR: Final[int] = ...
ST7789_VSCRDEF: Final[int] = ...
ST7789_COLMOD: Final[int] = ...
ST7789_MADCTL: Final[int] = ...
ST7789_VSCSAD: Final[int] = ...

ST7789_MADCTL_MY: Final[int] = ...
ST7789_MADCTL_MX: Final[int] = ...
ST7789_MADCTL_MV: Final[int] = ...
ST7789_MADCTL_ML: Final[int] = ...
ST7789_MADCTL_BGR: Final[int] = ...
ST7789_MADCTL_MH: Final[int] = ...
ST7789_MADCTL_RGB: Final[int] = ...

ST7789_RDID1: Final[int] = ...
ST7789_RDID2: Final[int] = ...
ST7789_RDID3: Final[int] = ...
ST7789_RDID4: Final[int] = ...

COLOR_MODE_65K: Final[int] = ...
COLOR_MODE_262K: Final[int] = ...
COLOR_MODE_12BIT: Final[int] = ...
COLOR_MODE_16BIT: Final[int] = ...
COLOR_MODE_18BIT: Final[int] = ...
COLOR_MODE_16M: Final[int] = ...

BLACK: Final[int] = ...
BLUE: Final[int] = ...
RED: Final[int] = ...
GREEN: Final[int] = ...
CYAN: Final[int] = ...
MAGENTA: Final[int] = ...
YELLOW: Final[int] = ...
WHITE: Final[int] = ...

_ENCODE_PIXEL: Final[str] = ...
_ENCODE_POS: Final[str] = ...
_DECODE_PIXEL: Final[str] = ...

_BUFFER_SIZE: Final[int] = ...

_BIT7: Final[int] = ...
_BIT6: Final[int] = ...
_BIT5: Final[int] = ...
_BIT4: Final[int] = ...
_BIT3: Final[int] = ...
_BIT2: Final[int] = ...
_BIT1: Final[int] = ...
_BIT0: Final[int] = ...

WIDTH_320: list[tuple[int, int, int, int]]

WIDTH_240: list[tuple[int, int, int, int]]

WIDTH_135: list[tuple[int, int, int, int]]

ROTATIONS: list[int]


def color565(red: int, green: int = 0, blue: int = 0) -> int:
    """
    Convert red, green and blue values (0-255) into a 16-bit 565 encoding.
    """


def _encode_pos(x: int, y: int) -> bytes:
    """Encode a position into bytes."""


def _encode_pixel(color: int):
    """Encode a pixel color into bytes."""


class ST7789:

    def __init__(self, spi, width, height, dc=None, reset=None,
                 cs=None, backlight=None, rotations=None, rotation=0, color_order=None,
                 inversion=None, options=None, buffer_size=None):
        """
        Initialize display.

        """

    def hard_reset(self):
        """
        Hard reset display.
        """


    def soft_reset(self):
        """
        Soft reset display.
        """

    def sleep_mode(self, value: bool):
        """
        Enable or disable display sleep mode.

        """

    def inversion_mode(self, value: bool):
        """
        Enable or disable display inversion mode.

        """

    def rotation(self, rotation: int):
        """
        Set display rotation.

        """

    def vline(self, x: int, y: int, length: int, color: int):
        """
        Draw vertical line at the given location and color.

        """

    def hline(self, x: int, y: int, length: int, color: int):
        """
        Draw horizontal line at the given location and color.

        """

    def pixel(self, x: int, y: int, color: int):
        """

        """

    def blit_buffer(self, buffer: bytes, x: int, y: int, width: int, height: int):
        """
        Copy buffer to display at the given location.

        """

    def rect(self, x: int, y: int, w: int, h: int, color: int):
        """
        Draw a rectangle at the given location, size and color.
        """

    def fill_rect(self, x: int, y: int, width: int, height: int, color: int):
        """
        Draw a rectangle at the given location, size and filled with color.

        """

    def fill(self, color: int):
        """
        Fill the entire FrameBuffer with the specified color.
        """

    def line(self, x0: int, y0: int, x1: int, y1: int, color: int):
        """
        Draw a single pixel wide line starting at x0, y0 and ending at x1, y1.

        """

    def vscrdef(self, tfa: int, vsa: int, bfa: int):
        """
        Set Vertical Scrolling Definition.

        """

    def vscsad(self, vssa: int):
        """
        Set Vertical Scroll Start Address of RAM.

        """

    def text(self, font, text: str, x0: int, y0: int, color: int=WHITE, background: int=BLACK):
        """
        Draw text on display in specified font and colors. 8 and 16 bit wide
        """

    def bitmap(self, bitmap, x: int, y: int, index: int=0):
        """
        Draw a bitmap on display at the specified column and row
        """

    def write(self, font, string: str, x: int, y: int, fg: int=WHITE, bg: int=BLACK,
              background_tuple=None, fill_flag=None):
        """
        Write a string using a converted true-type font on the display starting
        at the specified column and row
        """

    def write_len(self, font, string: str):
        """
        Returns the width in pixels of the string if it was written with the
        specified font.

        """

    def madctl(self, value):
        """
        Returns the current value of the MADCTL register. Optionally sets the
        """

    def init(self):
        """
        Must be called to initalize the display.
        """

    def on(self):
        """
        Turn on the backlight pin if one was defined during init.
        """

    def off(self):
        """
        Turn off the backlight pin if one was defined during init.
        """

    def circle(self, x: int, y: int, r: int, color: int):
        """
        Draws a circle with radius r centered at the (x, y) coordinates in the given color.
        """

    def fill_circle(self, x: int, y: int, r: int, color: int):
        """
        Draws a filled circle with radius r centered at the (x, y) coordinates in the given color.
        """

    def draw(self, vector_font, s: str, x: int, y: int, fg: int=WHITE, scale: int=1.0):
        """
        Draw text to the display using the specified hershey vector font with
        the coordinates as the lower-left corner of the text.
        """

    def draw_len(self, vector_font, s: str, scale: int=1.0):
        """
        Returns the width of the string in pixels if drawn with the specified font.
        """

    def jpg(self, jpg_filename: str, x: int, y: int, method=None):
        """
        Draw JPG file on the display at the given x and y coordinates as the
        upper left corner of the image.
        """

    def jpg_decode(self, jpg_filename: str, x: int, y: int, width: int, height: int):
        """
        Decode a jpg file and return it or a portion of it as a tuple composed
        of (buffer, width, height).
        """

    def polygon_center(self, polygon: list[tuple[int, int]]):
        """
        Return the center of the polygon as an (x, y) tuple.
        """

    def fill_polygon(self, polygon: list[tuple[int, int]], x: int, y: int, color: int,
                     angle: int=0, center_x: int=0, center_y: int=0):
        """
        Draw a filled polygon at the x, y coordinates in the color given.
        """

    def polygon(self, polygon: list[tuple[int, int]], x: int, y: int, color: int,
                angle: int, center_x: int, center_y: int):
        """
        Draw a polygon at the x, y coordinates in the color given.

        See the T-Display roids.py for an example.
        """

    def bounding(self, status: bool, as_rect=False):
        """
        Bounding turns on and off tracking the area of the display that has been written to.
        """

    def width(self):
        """
        Returns the current logical width of the display.
        """

    def height(self):
        """
        Returns the current logical height of the display.
        """

    def offset(self, x_start: int, y_start: int):
        """
        The memory in the ST7789 controller is configured for a 240x320 display.
        """
