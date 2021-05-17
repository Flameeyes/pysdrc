# SPDX-FileCopyrightText: 2020 Diego Elio Pettenò
#
# SPDX-License-Identifier: MIT

"""Decoder interfaces for SIRC protocol."""


class DecodeException(Exception):
    """Raised when a set of pulse timings are not a valid SIRC command."""


class SIRCDecodeException(DecodeException):
    pass


class NECDecodeException(DecodeException):
    pass


def _bits_to_value_lsb(bits: list):
    result = 0

    for position, value in enumerate(bits):
        result += value << position

    return result


def _pulses_to_bits(pulses: list):
    bits = []
    evens = pulses[0::2]
    odds = pulses[1::2]
    pairs = zip(evens, odds)

    for even, odd in pairs:
        if odd > even * 1.75:
            bits.append(1)
        else:
            bits.append(0)

    return bits


def decode_sirc(pulses: list) -> tuple:
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
        raise SIRCDecodeException("Invalid number of pulses %d" % len(pulses))

    if not 2200 <= pulses[0] <= 2600:
        raise SIRCDecodeException("Invalid header pulse length (%d usec)" % pulses[0])

    bits = _pulses_to_bits(pulses[1:])

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


# Constant object to signify a NEC repeat code.
NEC_REPEAT = "NEC Repeat"


def decode_nec(pulses: list):
    """Decode (extended) NEC protocol commands from raw pulses.

    The NEC command protocol is a structured 16-bit protocol that can be validated.

    Details of the protocol can be found at:

    https://www.sbprojects.net/knowledge/ir/nec.php
    """

    if not len(pulses) in [67, 3]:
        raise NECDecodeException("Invalid number of pulses %d" % len(pulses))

    if not 8800 <= pulses[0] <= 9300:
        raise NECDecodeException("Invalid AGC pulse length (%d usec)" % pulses[0])

    if 2100 <= pulses[1] <= 2300 and 450 <= pulses[2] <= 700:
        return NEC_REPEAT

    if not 4400 <= pulses[1] <= 4600:
        raise NECDecodeException("Invalid AGC space length (%d usec)" % pulses[1])

    bits = _pulses_to_bits(pulses[2:])

    # Decode the command first, because that is alwasy sent twice, once straight and
    # once inverted. The address _might_ be inverted.
    command = _bits_to_value_lsb(bits[16:24])
    command_inverted = _bits_to_value_lsb(bits[24:32])

    if command_inverted != (~command & 0xFF):
        raise NECDecodeException(
            "Not a valid NEC command: command != ~command_inverted"
        )

    address = _bits_to_value_lsb(bits[0:8])
    address_inverted = _bits_to_value_lsb(bits[8:16])

    if address_inverted == (~address & 0xFF):
        return address, command
    else:
        return (address + address_inverted << 8), command
