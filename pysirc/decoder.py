# SPDX-FileCopyrightText: 2020 Diego Elio Pettenò
#
# SPDX-License-Identifier: MIT

"""Decoder interfaces for SIRC protocol."""

class DecodeException(Exception):
    """Raised when a set of pulse timings are not a valid SIRC command."""

def _bits_to_value_lsb(bits):
    result = 0

    for position, value in enumerate(bits):
        result += value << position

    return result


def decode_sirc(pulses):
    """Decode SIRC (Sony) protocol commands from raw pulses.

    The Sony command protocol uses a different format than the normal RC-5,
    which requires a different decoding scheme.

    Details of the protocol can be found at:

    https://www.sbprojects.net/knowledge/ir/sirc.php
    http://www.righto.com/2010/03/understanding-sony-ir-remote-codes-lirc.html
    """

    # SIRC supports 12-, 15- and 20-bit commands. There's always one header pulse,
    # and then two pulses per bit, so accept 25-, 31- and 41-pulses commands.
    if not len(pulses) in [25, 31, 41]:
        raise DecodeException("Invalid number of pulses %d" % len(pulses))

    if not 2200 <= pulses[0] <= 2600:
        raise DecodeException("Invalid header pulse length (%d usec)" % pulses[0])

    evens = pulses[1::2]
    odds = pulses[2::2]
    pairs = zip(evens, odds)
    bits = []
    for even, odd in pairs:
        if odd > even * 1.75:
            bits.append(1)
        else:
            bits.append(0)

    command_bits = bits[0:7]

    # 20-bit commands are the same as 12-bit but with an additional 8-bit
    # extension. 15-bit commands use 8-bit for the device address instead.
    if len(pulses) == 31:
        device_bits = bits[7:15]
        extended_bits = None
    else:
        device_bits = bits[7:12]
        extended_bits = bits[12:]

    command = _bits_to_value_lsb(command_bits)
    device = _bits_to_value_lsb(device_bits)
    if extended_bits:
        extended = _bits_to_value_lsb(extended_bits)
    else:
        extended = None

    if extended is None:
        return (command, device)

    return (command, device, extended)
