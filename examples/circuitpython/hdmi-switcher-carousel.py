# SPDX-FileCopyrightText: 2020 Diego Elio Pettenò
#
# SPDX-License-Identifier: MIT

"""Example CircuitPython code that rotates the input on an HDMI switcher.

The example expects you copied the pysdrc package to the CIRCUITPY volume.

It also assumes the correct IR LED to be connected to the D5 line, with HIGH
corresponding to ON (common cathode or via transistor).

"""

import time

import board

from pysdrc.circuitpython import transmitter

transmitter = transmitter.NECTransmitter(board.D5)

inputs = [5, 7, 8, 9, 27]

while True:
    for index, input_id in enumerate(inputs):
        print("Selecting input %d" % (index + 1))
        transmitter.transmit_command(128, input_id)
        time.sleep(30)
