"""Demonstrate the quality difference between RGB modes."""
from st7789v.interface import RaspberryPi
from st7789v import Display

data = [(0, 0, 0)] * 320 * 240

for y in range(72):
    for x in range(320):
        val4 = (x * 256 // 320) & 0xf0
        val5 = (x * 256 // 320) & 0xf8
        val6 = (x * 256 // 320) & 0xfc
        if y < 24:
            data[y * 320 + x] = (val4, 0, 0)
            data[(y + 84) * 320 + x] = (val5, 0, 0)
            data[(y + 168) * 320 + x] = (val6, 0, 0)
        elif y < 48:
            data[y * 320 + x] = (0, val4, 0)
            data[(y + 84) * 320 + x] = (0, val6, 0)
            data[(y + 168) * 320 + x] = (0, val6, 0)
        else:
            data[y * 320 + x] = (0, 0, val4)
            data[(y + 84) * 320 + x] = (0, 0, val5)
            data[(y + 168) * 320 + x] = (0, 0, val6)


with RaspberryPi() as rpi:
    display = Display(rpi)
    display.initialize(rotation=270, color_mode=666)
    display.draw_rgb_bytes(data)
