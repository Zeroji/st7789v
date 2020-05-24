from st7789v.interface import RaspberryPi
from st7789v import Display

with RaspberryPi() as rpi:
    display = Display(rpi)
    display.initialize()
    display.draw_rgb_bytes([[0, 0, 255]] * 240 * 320)
