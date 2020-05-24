import time
from st7789v.interface import RaspberryPi
from st7789v import Display

black, white = [(0, 0, 0)], [(255, 255, 255)]
red, green, blue = [(255, 0, 0)], [(0, 255, 0)], [(0, 0, 255)]
line = red * 64 + white * 24 + green * 64 + white * 24 + blue * 64

with RaspberryPi() as rpi:
    display = Display(rpi)
    for mirrored in (False, True):
        for rotation in (0, 90, 180, 270):
            display.initialize(rotation=rotation, mirror=mirrored)
            display.draw_rgb_bytes(black * 240 * 320)
            row = line + black * 80 if display.max_w == 320 else line
            display.draw_rgb_bytes(row * 64)
            time.sleep(1)
