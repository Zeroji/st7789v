import time
from . import colors
from . import commands
from .interface import IOWrapper

ROT_TO_MADCTL = {
    0: [0x00, 0x40],
    90: [0x60, 0xE0],
    180: [0xC0, 0x80],
    270: [0xA0, 0x20],
}

class Display:
    def __init__(self, io_wrapper: IOWrapper, width: int = 240, height: int = 320):
        self._io = io_wrapper
        self._initialized = False
        self.base_width = width
        self.base_height = height
        self.width = self.base_width
        self.height = self.base_height
        self.image_to_rgb = None

    @property
    def initialized(self):
        return self._initialized

    def initialize(self, color_mode=565, inverted=True, rotation=0, mirror=False, bounds=None, reset=True):
        if not self._io.is_open():
            raise ValueError("IO wrapper is not opened")
        if reset:
            self.reset()
        self._initialized = True

        # Set colors
        self.set_color_mode(color_mode)
        self.command('INVON' if inverted else 'INVOFF')

        # Set MADCTL
        if rotation not in ROT_TO_MADCTL:
            raise ValueError("Rotation must be 0, 90, 180 or 270")
        self.set_madctl(madctl=ROT_TO_MADCTL[rotation][mirror])

        # Set col/row addresses
        self.max_w = (self.base_height if self.mv else self.base_width)
        self.max_h = (self.base_width if self.mv else self.base_height)
        if not bounds:
            bounds = (0, 0, self.max_w, self.max_h)
        self.set_bounds(*bounds)

        # Wake up
        self.command('SLPOUT')
        self.command('DISPON')

    def set_color_mode(self, colmod):
        if colmod not in colors.MODES:
            raise ValueError("Unexpected color mode, expected RGB 4-4-4, 5-6-5 or 6-6-6")
        self.color_mode = colors.MODES[colmod]
        self.image_to_rgb = self.color_mode['func']
        self.command('COLMOD', self.color_mode['id'])

    def set_madctl(self, mirror_y=False, mirror_x=False, exchange=False, madctl=None):
      if madctl is None:
        madctl = mirror_y << 7 | mirror_x << 6 | exchange << 5
      self.mv = bool(madctl & 0x20)
      self.max_w = (self.base_height if self.mv else self.base_width) - 1
      self.max_h = (self.base_width if self.mv else self.base_height) - 1
      self.command('MADCTL', madctl)

    def set_bounds(self, left, top, right, bottom):
        if not 0 <= left < right <= self.max_w:
            raise ValueError("Invalid bounds: expected 0 <= LEFT < RIGHT <= %d, got LEFT=%d and RIGHT=%d" % (self.max_w, left, right))
        if not 0 <= top < bottom <= self.max_h:
            raise ValueError("Invalid bounds: expected 0 <= TOP < BOTTOM <= %d, got TOP=%d and BOTTOM=%d" % (self.max_h, top, bottom))
        self.width = right - left
        self.height = bottom - top
        self.bounds = (left, top, right, bottom)
        self.command('CASET', left.to_bytes(2, 'big') + (right-1).to_bytes(2, 'big'))
        self.command('RASET', top.to_bytes(2, 'big') + (bottom-1).to_bytes(2, 'big'))

    def turn_on(self):
        self.command('SLPOUT')
        self.command('DISPON')

    def turn_off(self):
        self.command('DISPOFF')
        self.command('SLPIN')

    def command(self, name, data=None, read=True):
        if not self._initialized:
            raise ValueError("Uninitialized display, call initialize() first")
        # cast data to bytes
        if isinstance(data, int):
            data = [data]
        if isinstance(data, (list, tuple)):
            data = bytes(data)
        # get command info
        cmd = commands.by_name[name.upper()]
        wrx, rdx = cmd['wrx'], cmd['rdx']
        # check data length
        if wrx > 0 and (data is None or len(data) != wrx):
            raise ValueError('Expected %d bytes of data for command %s' % (wrx, name))
        if wrx == 0 and data:
            raise ValueError('No data expected for command %s but got %d bytes' % (name, len(data)))
        # send command and read result
        self.raw_command(cmd['id'], data)
        if rdx > 0 and read:
            return self._io.spi_read(rdx)

    def raw_command(self, cmd, data=None):
        self._io.set_low(self._io.cs)
        self._io.set_low(self._io.dc)
        self._io.spi_write(bytes([cmd]))
        if data:
            # cast data to bytes
            if isinstance(data, int):
                data = [data]
            if isinstance(data, (list, tuple)):
                data = bytes(data)
            self._io.set_high(self._io.dc)
            self._io.spi_write(data)
        self._io.set_high(self._io.cs)

    def draw_rgb_bytes(self, image_data: list):
        """Expects a list of [R,G,B] elements."""
        data = self.image_to_rgb(image_data[:self.width*self.height])
        self.command('RAMWR', data)

    def reset(self):
        self._io.set_high(self._io.rst)
        time.sleep(0.01)
        self._io.set_low(self._io.rst)
        time.sleep(0.01)
        self._io.set_high(self._io.rst)
        time.sleep(0.01)

    def set_backlight(self, level):
        if isinstance(level, bool):
            level = int(level)
        self._io.set_pin_pwm(self._io.bl, level)
