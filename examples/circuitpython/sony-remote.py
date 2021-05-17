# SPDX-FileCopyrightText: 2020 Facebook Inc.
#
# SPDX-License-Identifier: MIT
# type: ignore
"""Scriptable Sony Remote in CircuitPython.

The example expects you copied the pysdrc package to the CIRCUITPY volume.

It also assumes the correct IR LED to be connected to the D5 line, with HIGH
corresponding to ON (common cathode or via transistor).
"""

import time

import board

from pysdrc.circuitpython import transmitter

_DEVICES = {
    "TV": (1, None, False),
    "VCR": (5, None, False),
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

Change the selected device by prefixing its name with ! (e.g. !TV), or by
providing a specific device target (e.g. !151).

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
                if "*" in request:
                    force_8bit_device = True
                    request, _ = request.split("*", 1)
                else:
                    force_8bit_device = False
                if "," in request:
                    device, extended_device = request[1:].split(",")
                else:
                    device = request[1:]
                    extended_device = None

                selected_device = request[1:]
                _DEVICES[selected_device] = (
                    int(device),
                    int(extended_device) if extended_device is not None else None,
                    force_8bit_device,
                )
        elif request.startswith("#"):
            device, extended_device, force_8bit_device = _DEVICES[selected_device]
            command = int(request[1:])
            sony_transmitter.transmit_command(
                command,
                device,
                extended_device=extended_device,
                force_8bit_device=force_8bit_device,
            )
        elif request in _COMMANDS:
            device, extended_device, force_8bit_device = _DEVICES[selected_device]
            sony_transmitter.transmit_command(
                _COMMANDS[request],
                device,
                extended_device=extended_device,
                force_8bit_device=force_8bit_device,
            )
        else:
            raise ValueError("Unknown command %r" % request)
    except Exception as error:
        print("ERROR", error, flush=True)
