# SPDX-FileCopyrightText: 2020 Diego Elio Pettenò
#
# SPDX-License-Identifier: MIT

"""Example CircuitPython code that raises/lowers volume continuously.

The example expects you copied the pysdrc package to the CIRCUITPY volume.

It also assumes the correct IR LED to be connected to the D5 line, with HIGH
corresponding to ON (common cathode or via transistor).

"""

import time

import board

from pysdrc.circuitpython import transmitter

sirc_transmitter = transmitter.SIRCTransmitter(board.D5)

while True:
    print("Volume++")
    sirc_transmitter.transmit_command(18, 1)
    time.sleep(2)

    print("Volume--")
    sirc_transmitter.transmit_command(19, 1)
    time.sleep(2)
