# SPDX-FileCopyrightText: 2020 Diego Elio Pettenò
#
# SPDX-License-Identifier: MIT

"""Example CircuitPython code that raises/lowers volume continuously.

The example expects the following files in the CIRCUITPY volume:

 - /sirc_transmitter.py
 - /pysirc/encoder.py

It also assumes the correct IR LED to be connected to the D5 line, with HIGH
corresponding to ON (common cathode or via transistor).

"""

import board
import time

import sirc_transmitter

transmitter = sirc_transmitter.SircTransmitter(board.D5)

while True:
    print("Volume++")
    transmitter.transmit_command(18, 1)
    time.sleep(2)

    print("Volume--")
    transmitter.transmit_command(19, 1)
    time.sleep(2)
