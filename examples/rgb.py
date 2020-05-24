from st7789v.interface import RaspberryPi
from st7789v import Display

data = [(0, 0, 0)] * 320 * 240
full = [(255,0,0), (255,255,0), (0,255,0), (0,255,255), (0,0,255), (255,0,255)]

for y in range(240):
    for x in range(320):
        g = (y // 32) * 10 + (x // 32)
        if g < 64:
            data[y * 320 + x] = ((x % 32) * 8, g * 4, (y % 32) * 8)
        elif y < 224:
            data[y * 320 + x] = full[g-64]
        else:
            gray = 255 * (x // 32) // 9
            data[y * 320 + x] = (gray, gray, gray)

with RaspberryPi() as rpi:
    display = Display(rpi)
    display.initialize(rotation=270)
    display.draw_rgb_bytes(data)
