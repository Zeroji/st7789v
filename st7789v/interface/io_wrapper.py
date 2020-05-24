"""Abstract IO and SPI wrapper."""


class IOWrapper:
    """Abstract IO and SPI wrapper."""

    def __init__(self, pin_cs=8, pin_dc=25, pin_rst=27, pin_bl=18):
        """You should not instantiate this directly.

        Args:
            pin_cs:     Chip Select pin
            pin_dc:     Data Carry pin
            pin_rst:    Reset pin
            pin_bl:     Backlight pin
        """
        self.cs = pin_cs
        self.dc = pin_dc
        self.rst = pin_rst
        self.bl = pin_bl
        self._open = False

    def __enter__(self):
        """Wrapper for open() for use as a context."""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_trace):
        """Wrapper for close() for use as a context."""
        self.close()
        self._open = False

    def open(self):
        """Setup the interface and mark it as ready."""
        if self._open:
            raise IOError("Interface is already opened")
        self._open = True

    def close(self):
        """Close the interface."""
        if not self._open:
            raise IOError("Interface is not opened")
        self.set_low(self.bl)
        self.set_low(self.dc)
        self.set_high(self.rst)
        self._open = False

    def is_open(self):
        """Whether the interface is ready to use."""
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
        """Write data to the SPI bus."""
        raise NotImplementedError

    def spi_read(self, size: int):
        """Read data from the SPI bus."""
        raise NotImplementedError
