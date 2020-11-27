# SPDX-FileCopyrightText: 2020 Diego Elio Pettenò
#
# SPDX-License-Identifier: MIT

"""Example CircuitPython code that raises/lowers volume continuously.

The example expects you copied the pysirc package to the CIRCUITPY volume.

It also assumes the correct IR LED to be connected to the D5 line, with HIGH
corresponding to ON (common cathode or via transistor).

"""

import time

import board

from pysirc.circuitpython import transmitter

transmitter = transmitter.SIRCTransmitter(board.D5)

while True:
    print("Volume++")
    transmitter.transmit_command(18, 1)
    time.sleep(2)

    print("Volume--")
    transmitter.transmit_command(19, 1)
    time.sleep(2)
