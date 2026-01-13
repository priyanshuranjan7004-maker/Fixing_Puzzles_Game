from machine import Pin
from machine import SPI

import gc



_expanded_bits = [0x88, 0x8C, 0xC8, 0xCC]


def _expand_byte(b, mv):
    mv[0] = _expanded_bits[(b >> 6) & 0x3]
    mv[1] = _expanded_bits[(b >> 4) & 0x3]
    mv[2] = _expanded_bits[(b >> 2) & 0x3]
    mv[3] = _expanded_bits[(b) & 0x3]


def _compress_byte(mv):
    b1, b2, b3, b4 = mv
    T, B = 0x40, 0x04
    v = (((b1 & T) << 1) | ((b1 & B) << 4) |
         ((b2 & T) >> 1) | ((b2 & B) << 2) |
         ((b3 & T) >> 3) | ((b3 & B)) |
         ((b4 & T) >> 5) | ((b4 & B) >> 2))
    return v


class NeoPixel:
    """The NeoPixel object can be treated as a 2D array, pixel_count long and 3
    wide."""

    def __init__(self, spi_device, pixel_count):
        self._n = pixel_count
        self._data = memoryview(bytearray(pixel_count * 12))
        self._spi = spi_device
        self[:] = (0, 0, 0)

    def _unpack_slice(self, s):
        start, stop, step = s.start, s.stop, s.step
        if step is not None and step != 1:
            raise NotImplementedError("Slices must have step of 1")
        step = 1
        if start == None:
            start = 0
        elif start < 0:
            start += self._n
        if stop == None:
            stop = self._n
        elif stop < 0:
            stop += self._n
        return (start, stop, step)

    def __getitem__(self, index):
        data = self._data
        n = self._n
        if isinstance(index, int):
            if index < -n or index >= n:
                raise IndexError("Pixel index out of range")
            index *= 12
            return (_compress_byte(data[index:index + 4]),
                    _compress_byte(data[index + 4:index + 8]),
                    _compress_byte(data[index + 8:index + 12]))
        elif isinstance(index, tuple):
            if len(index) != 2:
                raise IndexError(
                    "Pixel array has only two dimensions (index and colour)")
            ind1, ind2 = index
            if isinstance(ind1, slice):
                raise NotImplementedError("2D slicing not supported")
            if (not isinstance(ind1, int)) or (not isinstance(ind2, int)):
                raise IndexError("Indecies must be integers")
            if ind1 < -n or ind1 >= n or ind2 < 0 or ind2 >= 3:
                raise IndexError("Pixel index out of range")
            ind1 *= 12
            ind1 += ind2 * 4
            return _compress_byte(data[ind1:ind1 + 4])
        elif isinstance(index, slice):
            start, stop, step = self._unpack_slice(index)
            dd = data[start * 12:stop * 12]
            return [(_compress_byte(dd[i:i + 4]),
                     _compress_byte(dd[i + 4:i + 8]),
                     _compress_byte(dd[i + 8:i + 12])) for i in
                    range(0, len(dd), 12)]
        else:
            raise IndexError("Can not index on type {}".format(type(index)))

    def __setitem__(self, index, value):
        data = self._data
        n = self._n
        if isinstance(index, int):
            if index < -n or index >= n:
                raise IndexError("Pixel index out of range")
            if not isinstance(value, tuple) or len(value) != 3:
                raise ValueError("Pixel value must be a 3-tuple")
            index *= 12
            _expand_byte(value[0], data[index:index + 4])
            _expand_byte(value[1], data[index + 4:index + 8])
            _expand_byte(value[2], data[index + 8:index + 12])
        elif isinstance(index, tuple):
            if len(index) != 2:
                raise IndexError(
                    "Pixel array has only two dimensions (index and colour)")
            ind1, ind2 = index
            if isinstance(ind1, slice):
                raise NotImplementedError("2D slice assignment not supported")
            if (not isinstance(ind1, int)) or (not isinstance(ind2, int)):
                raise IndexError("Indecies must be integers")
            if ind1 < -n or ind1 >= n or ind2 < 0 or ind2 >= 3:
                raise IndexError("Pixel index out of range")
            if not isinstance(value, int) or value < 0 or value > 255:
                raise ValueError(
                    "Pixel value must be an integer in range 0 to 255")
            ind1 *= 12
            ind1 += ind2 * 4
            _expand_byte(value, data[ind1:ind1 + 4])
        elif isinstance(index, slice):
            start, stop, step = self._unpack_slice(index)
            dd = memoryview(data)[start * 12:stop * 12]
            if len(dd) == 0:
                return
            if isinstance(value, tuple) and len(value) == 3:
                _expand_byte(value[0], dd[0: 4])
                _expand_byte(value[1], dd[4: 8])
                _expand_byte(value[2], dd[8:12])
                for i in range(12, len(dd), 12):
                    dd[i:i + 12] = dd[0:12]
            elif isinstance(value, list) and all(
                    (isinstance(i, tuple) and len(i) == 3) for i in value):
                for i in range(0, len(dd), 12):
                    v0, v1, v2 = value[i // 3]
                    _expand_byte(v0, dd[i + 0:i + 4])
                    _expand_byte(v1, dd[i + 4:i + 8])
                    _expand_byte(v2, dd[i + 8:i + 12])
            else:
                raise ValueError(
                    "Assigned value must be a list of 3-tuples or a single 3-tuple")

    def write(self):
        """Write the buffer value out to the pixels"""
        self._spi.write(self._data)

    def rotate(self, count):
        """Rotate the whole buffer content by 'count' pixels"""
        count = count % self._n
        count *= 12
        tail = bytearray(self._data[-count:])
        head = bytearray(self._data[:-count])
        self._data[count:] = head
        self._data[:count] = tail
        del head, tail
        gc.collect()

    @property
    def n(self):
        return self._n


brightness = 0
neo: NeoPixel = None

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)


def init_led(sck, mosi, miso, led_num, brightness_):
    global neo, brightness
    sp = SPI(1, baudrate=3200000, phase=1, polarity=1,
             sck=Pin(sck), mosi=Pin(mosi), miso=Pin(miso))
    brightness = brightness_
    neo = NeoPixel(sp, led_num)


def decode_x_y(x, y):
    y = 31 - y
    if y % 2 != 0:
        x = 7 - x
    return y * 8 + x


def neo_set_pixel(x, y, color):
    global neo
    neo[decode_x_y(x, y)] = (
    int(color[0] * brightness), int(color[1] * brightness),
    int(color[2] * brightness))

