"""Turn the display and backlight off and back on."""
import time
from st7789v.interface import RaspberryPi
from st7789v import Display

with RaspberryPi() as rpi:
    display = Display(rpi)
    display.initialize()
    display.draw_rgb_bytes([[255, 255, 255]] * 240 * 320)
    time.sleep(1)
    display.turn_off()
    time.sleep(1)
    display.set_backlight(0)
    time.sleep(1)
    display.turn_on()
    time.sleep(1)
    display.set_backlight(1)
