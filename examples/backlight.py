"""Demonstrate PWM backlight control."""
import time
from st7789v.interface import RaspberryPi

with RaspberryPi() as rpi:
    for i in range(10):
        rpi.set_pin_pwm(rpi.bl, i/10)
        time.sleep(0.5)
    rpi.set_pin_pwm(rpi.bl, 1)
