class IOWrapper:
    def __init__(self, pin_cs=8, pin_dc=25, pin_rst=27, pin_bl=18):
        self.cs = pin_cs
        self.dc = pin_dc
        self.rst = pin_rst
        self.bl = pin_bl
        self._open = False

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_trace):
        self.close()
        self._open = False

    def open(self):
        if self._open:
            raise IOError("Interface is already opened")
        self._open = True

    def close(self):
        if not self._open:
            raise IOError("Interface is not opened")
        self.set_low(self.bl)
        self.set_low(self.dc)
        self.set_high(self.rst)
        self._open = False

    def is_open(self):
        return self._open

    def set_low(self, pin: int):
        """Set pin low."""
        self.set_pin(pin, False)

    def set_high(self, pin: int):
        """Set pin high."""
        self.set_pin(pin, True)

    def set_pin(self, pin: int, state: bool):
        """Write digital pin state."""
        raise NotImplementedError

    def set_pin_pwm(self, pin: int, value: float):
        """Write analog pin value (0-1)."""
        raise NotImplementedError

    def spi_write(self, data: bytes):
        raise NotImplementedError

    def spi_read(self, size: int):
        raise NotImplementedError
