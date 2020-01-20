from .digital_inout import DigitalInOut

_BUFFER = bytearray(3)

def _read_u8(dev, addr, register):
    with dev as spi:
        _BUFFER[0] = addr | 1
        _BUFFER[1] = register & 0xFF
        spi.write(_BUFFER, end=2)
        spi.readinto(_BUFFER, end=1)
        return _BUFFER[0]

def _write_u8(dev, addr, register, val):
    # Write an 8 bit value to the specified 8-bit register.
    with dev as spi:
        _BUFFER[0] = addr
        _BUFFER[1] = register & 0xFF
        _BUFFER[2] = val & 0xFF
        spi.write(_BUFFER)

class MCP23S17LO:
    def __init__(self, spid, addr):
         self._device = spid
         self._address = addr

    @property
    def gpio(self):
        return _read_u8(self._device, self._address, 0x12)

    @gpio.setter
    def gpio(self, val):
        _write_u8(self._device, self._address, 0x12, val)

    @property
    def iodir(self):
        return _read_u8(self._device, self._address, 0x0)

    @iodir.setter
    def iodir(self, val):
        _write_u8(self._device, self._address, 0x0, val)

class MCP23S17HI:
    def __init__(self, spid, addr):
         self._device = spid
         self._address = addr

    @property
    def gpio(self):
        return _read_u8(self._device, self._address, 0x13)

    @gpio.setter
    def gpio(self, val):
        _write_u8(self._device, self._address, 0x13, val)

    @property
    def iodir(self):
        return _read_u8(self._device, self._address, 0x1)

    @iodir.setter
    def iodir(self, val):
        _write_u8(self._device, self._address, 0x1, val)

class MCP23S17:
    def __init__(self, spid, address=0):
        self._device = spid
        self._address = 0x40 | (address << 1)

    def get_pin(self, pin):
        assert 0 <= pin <= 15
        if pin < 8:
          return DigitalInOut(pin, MCP23S17LO(self._device, self._address))
        else:
          return DigitalInOut(pin - 8, MCP23S17HI(self._device, self._address))


