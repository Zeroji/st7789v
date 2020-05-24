import atexit
from st7789v.interface import RaspberryPi
from st7789v import BufferedDisplay

rpi = RaspberryPi()
rpi.open()
display = BufferedDisplay(rpi, rotation=270, reset=False)
draw = display.draw
atexit.register(rpi.close)

print('# Use `display` to control the display, and `draw` to draw on the buffer.')
