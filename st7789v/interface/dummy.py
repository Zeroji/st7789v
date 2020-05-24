from . import IOWrapper
import logging

class Dummy(IOWrapper):
    def __init__(self, logger='dummy_io', handler=None, **kwargs):
        super().__init__(**kwargs)
        self._pin_map = {self.bl: 'BL', self.dc: 'DC', self.cs: 'CD', self.rst: 'RST'}
        self.log = logging.getLogger(logger)
        self.log.setLevel(logging.DEBUG)
        if handler:
            self.log.addHandler(handler)
        else:
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            console.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(levelname)s\t%(message)s'))
            self.log.addHandler(console)
        self.log.info('Initialized')

    def set_pin(self, pin: int, state: bool):
        self.log.debug('Set pin %s %s', self._pin_map.get(pin, str(pin)), 'high' if state else 'low')
    
    def set_pin_pwm(self, pin: int, value: float):
        self.log.debug('Set pin %s to %f', self._pin_map.get(pin, str(pin)), value)
    
    def spi_write(self, data: bytes):
        self.log.debug('Send data: %s', data.hex())

    def spi_read(self, size: int):
        self.log.debug('Read data: %d bytes', size)
        return bytes(size)
