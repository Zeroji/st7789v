import time
from PIL import Image
from st7789v.interface import RaspberryPi
from st7789v import Display

lena = Image.open('examples/lena.png')
data = list(lena.convert('RGB').getdata())

with RaspberryPi() as rpi:
    display = Display(rpi)
    display.initialize(color_mode=444)
    display.draw_rgb_bytes(data)
    time.sleep(1)
    display.set_color_mode(565)
    display.draw_rgb_bytes(data)
    time.sleep(1)
    display.set_color_mode(666)
    display.draw_rgb_bytes(data)
