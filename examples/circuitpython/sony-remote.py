# SPDX-FileCopyrightText: 2020 Facebook Inc.
#
# SPDX-License-Identifier: MIT
"""Scriptable Sony Remote in CircuitPython.

The example expects you copied the pysirc package to the CIRCUITPY volume.

It also assumes the correct IR LED to be connected to the D5 line, with HIGH
corresponding to ON (common cathode or via transistor).
"""

import time

import board

from pysirc.circuitpython import transmitter

_DEVICES = {
    "TV": (1, None),
    "VCR": (5, None),
}

_COMMANDS = {
    "POWER": 21,
    "POWER ON": 46,
    "POWER OFF": 47,
    "VOL+": 18,
    "VOL-": 19,
    "VIDEO1": 64,
    "VIDEO5": 72,
    "VIDEO6": 73,
}

selected_device = "TV"

print(
    """
Welcome to CircuitPython Sony Remote.

Type the command you want to send to your device from the available list.

You can send an arbitrary commands by prefixing their number with #
(e.g. #21).

Change the selected device by prefixing its name with ! (e.g. !TV).

Available commands: %s
Available devices: %s
"""
    % (", ".join(_COMMANDS), ", ".join(_DEVICES))
)

sony_transmitter = transmitter.SIRCTransmitter(board.D5)

time.sleep(1)

while True:
    request = input("%s> " % selected_device)
    try:
        if request.startswith("!"):
            if request[1:] in _DEVICES:
                selected_device = request[1:]
            else:
                raise ValueError("Unknown device %r" % request[1:])
        elif request.startswith("#"):
            device, extended_device = _DEVICES[selected_device]
            command = int(request[1:])
            sony_transmitter.transmit_command(
                command, device, extended_device=extended_device
            )
        elif request in _COMMANDS:
            device, extended_device = _DEVICES[selected_device]
            sony_transmitter.transmit_command(
                _COMMANDS[request], device, extended_device=extended_device
            )
        else:
            raise ValueError("Unknown command %r" % request)
    except Exception as error:
        print("ERROR", error, flush=True)
    except:
        print("ERROR", flush=True)
