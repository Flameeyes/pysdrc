# SPDX-FileCopyrightText: Copyright (c) 2017 Scott Shawcroft for Adafruit Industries
# SPDX-FileCopyrightText: 2020 Diego Elio Pettenò
#
# SPDX-License-Identifier: MIT

import board
import pulseio

import adafruit_irremote

from pysirc import decoder

pulsein = pulseio.PulseIn(board.D9, maxlen=120, idle_state=True)
generic_decoder = adafruit_irremote.GenericDecode()

while True:
    pulses = generic_decoder.read_pulses(pulsein)
    print("Heard", len(pulses), "Pulses:", pulses)
    try:
        code = decoder.decode_sirc(pulses)
        print("Decoded (SIRC):", code)
    except decoder.SIRCDecodeException as e:  # failed to decode
        print("Failed to decode SIRC: ", e.args)

    try:
        code = decoder.decode_nec(pulses)
        print("Decoded (NEC):", code)
    except decoder.NECDecodeException as e:
        print("Failed to decode NEC: ", e.args)

    # We need to keep the generic_decoder last because it modifies the
    # pulses parameter. See
    # https://github.com/adafruit/Adafruit_CircuitPython_IRRemote/pull/38
    # for details.
    try:
        code = generic_decoder.decode_bits(pulses)
        print("Decoded (Other):", code)
    except adafruit_irremote.IRDecodeException as e:  # failed to decode
        print("Failed to decode generic: ", e.args)

    print(
        "------------------------------------------------------------------------------------------------------------"
    )
