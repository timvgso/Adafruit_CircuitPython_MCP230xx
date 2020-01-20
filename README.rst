Work in Progress for MCP23Sxx SPI Devices
============
MCP23S08 is complete as far as matching the library features of the MCP23008. It uses
the same digital_inout.py module for pin objects as the MCP23008, but otherwise is
an independent implementation, meaning that users only need to have the file for
the device they're using in their /lib folder.

One difference between the MCP23S08 and the MCP23008 device objects is an extra
optional command parameter that was added to the `__init__` member function: `NO_MISO`,
which defaults to `False`. When this option is set to `True`, pins can be set as
outputs but cannot be read as inputs. This is meant for a device such as the Gemma M0
which doesn't expose enough pins for a full SPI interface, or for cases where a user
doesn't need to read from device inputs and wants to save a pin. 

The demo in examples/mcp23s08_blinkandbutton.py shows how to allocate pins, create
a device object, then control two outputs and read an input. It gives details for
pin connections for the two CircuitPython devices I used most of the time in testing,
a Circuit Playground Express and a Hallowing M0.
 
The files mcp23s17.py and mcp23s17_test.py represent my work so far on the MCP23S17
devie. I have been able to read and write pins with it but got stuck trying to add
interrupt support to match what's provided for the MCP23017. To be honest, I'm not
sure exactly how far along the code in those files is, but it's most definitely a work
in progress.

Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-mcp230xx/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/mcp230xx/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx/actions/
    :alt: Build Status

CircuitPython module for the MCP23017 and MCP23008 I2C I/O extenders.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-mcp230xx/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-mcp230xx

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-mcp230xx

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-mcp230xx

Usage Example
=============

See examples/mcp230xx_simpletest.py for a demo of the usage.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
