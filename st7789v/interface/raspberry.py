"""Raspberry Pi implementation of generic IOWrapper."""
import RPi.GPIO as GPIO
import spidev
from .io_wrapper import IOWrapper


class RaspberryPi(IOWrapper):
    """RaspberryPi GPIO/SPI wrapper."""
    PWM_FREQ = 100

    def __init__(self, spi_bus=0, gpio_mode=GPIO.BCM, **kwargs):
        super().__init__(**kwargs)
        self._spi_bus = spi_bus
        self._gpio_mode = gpio_mode
        self._backlight = None
        self._spi = None
        self._spi_limit = 4096

    def open(self):
        super().open()
        GPIO.setmode(self._gpio_mode)
        GPIO.setup(self.cs, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.dc, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.rst, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.bl, GPIO.OUT)
        self._backlight = GPIO.PWM(self.bl, RaspberryPi.PWM_FREQ)
        self._backlight.start(100)
        self._spi = spidev.SpiDev(self._spi_bus, 0)
        self._spi.mode = 0b00
        self._spi.max_speed_hz = 90000000
        return self

    def close(self):
        super().close()
        self._spi.close()
        self._backlight.stop()
        GPIO.output(self.bl, 0)
        GPIO.cleanup()

    def set_pin(self, pin: int, state: bool):
        GPIO.output(pin, state)

    def set_pin_pwm(self, pin: int, value: float):
        if pin != self.bl:
            raise NotImplementedError('Only backlight pin is set up as PWM')
        self._backlight.ChangeDutyCycle(min(100, max(0, int(100*value))))

    def spi_write(self, data: bytes):
        for i in range(0, len(data), self._spi_limit):
            self._spi.writebytes(data[i:i+self._spi_limit])

    def spi_read(self, size: int):
        return self._spi.readbytes(size)
