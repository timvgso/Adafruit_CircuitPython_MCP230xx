# The MIT License (MIT)
#
# Copyright (c) 2017 Tony DiCola for Adafruit Industries
#                    refactor by Carter Nelson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`mcp23s08`
====================================================

CircuitPython module for the MCP23S08 I2C I/O extenders.

* Author(s): Tony DiCola, Tim Victor
"""

from micropython import const
from .digital_inout import DigitalInOut

from adafruit_bus_device import spi_device

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx.git"

# pylint: disable=bad-whitespace
_MCP23S08_ADDRESS       = const(0x40)
_MCP23S08_IODIR         = const(0x00)
_MCP23S08_GPPU          = const(0x06)
_MCP23S08_GPIO          = const(0x09)

""" Reset values for MCP23S08 registers
    Begin writing at register 0 (IODIR), set it to 0xFF (all INPUT),
    enable hardware addressing in IOCON (register 5 = 0x8),
    set the other registers to 0.
"""
_MCP23S08_RESET_STR = b'\x00\xFF\x00\x00\x00\x00\x08\x00\x00\x00\x00'

_BUFFER = bytearray(3)

class MCP23S08:
    """Supports MCP23S08 instance on specified SPI bus and optionally
    at the specified SPI address.
    """
    def __init__(self, spi, cs, address=0, NO_MISO=False):
        if address < 0 or address >= 4:
            raise ValueError('MCP23S08 hardware address range is from 0 to 3')
        self._no_miso = NO_MISO
        self._iodir = self._gppu = self._gpio = 0
        self._address = _MCP23S08_ADDRESS | (address << 1)
        self._device = spi_device.SPIDevice(spi, cs)
        with self._device as device:
            device.write(bytearray([self._address]))
            device.write(_MCP23S08_RESET_STR)

    @property
    def gpio(self):
        """The raw GPIO output register.  Each bit represents the
        output value of the associated pin (0 = low, 1 = high), assuming that
        pin has been configured as an output previously.
        """
        if self._no_miso:
          return self._gpio
        return self._read_u8(_MCP23S08_GPIO)

    @gpio.setter
    def gpio(self, val):
        self._gpio = val
        self._write_u8(_MCP23S08_GPIO, val)

    @property
    def iodir(self):
        """The raw IODIR direction register.  Each bit represents
        direction of a pin, either 1 for an input or 0 for an output mode.
        """
        if self._no_miso:
          return self._iodir
        return self._read_u8(_MCP23S08_IODIR)

    @iodir.setter
    def iodir(self, val):
        self._iodir = val
        self._write_u8(_MCP23S08_IODIR, val)

    @property
    def gppu(self):
        """The raw GPPU pull-up register.  Each bit represents
        if a pull-up is enabled on the specified pin (1 = pull-up enabled,
        0 = pull-up disabled).  Note pull-down resistors are NOT supported!
        """
        if self._no_miso:
          return self._gppu
        return self._read_u8(_MCP23S08_GPPU)

    @gppu.setter
    def gppu(self, val):
        self._gppu = val
        self._write_u8(_MCP23S08_GPPU, val)

    def get_pin(self, pin):
        """Convenience function to create an instance of the DigitalInOut class
        pointing at the specified pin of this MCP23S08 device.
        """
        assert 0 <= pin <= 7
        return DigitalInOut(pin, self)

    """ The following methods duplicate ones in mcp230xx.py but use spi
    instead of i2c to communicate with the device
    """
    def _read_u8(self, register):
        # Read an unsigned 8 bit value from the specified 8-bit register.
        with self._device as spi:
            _BUFFER[0] = self._address | 1
            _BUFFER[1] = register & 0xFF
            spi.write(_BUFFER, end=2)
            spi.readinto(_BUFFER, end=1)
            return _BUFFER[0]

    def _write_u8(self, register, val):
        # Write an 8 bit value to the specified 8-bit register.
        with self._device as spi:
            _BUFFER[0] = self._address
            _BUFFER[1] = register & 0xFF
            _BUFFER[2] = val & 0xFF
            spi.write(_BUFFER)
