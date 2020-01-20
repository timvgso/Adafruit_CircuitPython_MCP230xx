""" mcp23s08 demo for CircuitPython
    Alternately flash two LEDs and read a button

    Circuit Playground Express connections:
    A1 / board.SCK to IC pin 1 / SCK
    A2 / board.MISO to IC pin 3 / SO
    A3 / board.MOSI to IC pin 2 / SI
    A4 / D3 to IC pin 7 / ^CS
    3.3V to pin 18 Vcc
    Gnd to pin 9 Vss

    mcp23s08 pinouts for this demo:
     1 SCK to cpe A1
     2 SI to cpe A3
     3 SO to cpe A2
     4 A1 to gnd
     5 A2 to gnd
     6 ^RESET to Vcc (pin 18)
     7 ^CS to cpe A4 (white)
     8 INT not connected
     9 Vss to gnd
    10 GP0 to LED0 anode
    11 GP1 to LED1 anode
    12 GP2 to tactile button
    13 GP3 not connected
    14 GP4 not connected
    15 GP5 not connected
    16 GP6 not connected
    17 GP7 not connected
    18 Vdd to 3.3v

    Alternate connections when using Hallowing M0 as test controller:
    (Uses the 4 "fang" pads. This will select a secondary SPI device
    since the primary one is tied to the display.)

    A2 to IC pin 7 / ^CS
    A3 to IC pin 2 / SI
    A4 to IC pin 1 / SCK
    A5 to IC pin 3 / SO
    3.3V from Feather headers pin 18 / Vdd
    Ground from Feather header to pin 9 / Vss

    Test board other connections:
    LED0, LED1 have 1k resistors from each cathode to ground
    tactile button has wire to ground on the other side 
"""

import board, time, digitalio, busio
from adafruit_mcp230xx.mcp23s08 import MCP23S08

# Uncomment for Circuit Playground Express:
cs = digitalio.DigitalInOut(board.D3)
with busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI) as spi:

# Uncomment for Hallowing M0:
# cs = digitalio.DigitalInOut(board.D3)
# with busio.SPI(clock=board.A4, MISO=board.A5, MOSI=board.A3) as spi:

    mcp = MCP23S08(spi, cs)
    pin0, pin1, pin2 = map(mcp.get_pin, range(3))

    # led 0
    pin0.direction = digitalio.Direction.OUTPUT
    pin0.value = True

    # led 1
    pin1.direction = digitalio.Direction.OUTPUT
    pin1.value = False

    # button
    pin2.direction = digitalio.Direction.INPUT
    pin2.pull = digitalio.Pull.UP

    while True:
        pin0.value = not pin0.value
        pin1.value = not pin1.value

        # read pin to check button, blink at double speed if it's pressed
        if pin2.value:
            # True is UP
            time.sleep(.42)
        else:
            # False is DOWN
            time.sleep(.21)

