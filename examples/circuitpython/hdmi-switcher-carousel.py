# SPDX-FileCopyrightText: 2020 Diego Elio Pettenò
#
# SPDX-License-Identifier: MIT

"""Example CircuitPython code that rotates the input on an HDMI switcher.

The example expects the following files in the CIRCUITPY volume:

 - /sirc_transmitter.py
 - /pysirc/encoder.py

It also assumes the correct IR LED to be connected to the D5 line, with HIGH
corresponding to ON (common cathode or via transistor).

"""

import board
import time

import sirc_transmitter
from pysirc import encoder

transmitter = sirc_transmitter.SircTransmitter(board.D5)

inputs = [
    encoder.encode_nec(128, 5),
    encoder.encode_nec(128, 7),
    encoder.encode_nec(128, 8),
    encoder.encode_nec(128, 9),
    encoder.encode_nec(128, 27),
]

while True:
    for index, pulses in enumerate(inputs):
        print("Selecting input %d" % (index + 1))
        transmitter.transmit_pulses(pulses)
        time.sleep(30)
