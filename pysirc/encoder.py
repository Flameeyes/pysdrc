# SPDX-FileCopyrightText: 2020 Diego Elio Pettenò
#
# SPDX-License-Identifier: MIT

"""Encoder for SIRC protocol."""


class EncodeError(ValueError):
    """Raised when the provided value is not valid for the protocol."""


class SIRCEncodeError(EncodeError):
    pass


class NECEncodeError(EncodeError):
    pass


def _sirc_value_to_pulses(value, bits):
    pulses = []
    for _ in range(bits):
        if value & 1:
            pulses.extend((600, 1200))
        else:
            pulses.extend((600, 600))

        value = value >> 1

    return pulses


def encode_sirc(command, device, extended_device=None):
    if command >= 2 ** 12:
        raise EncodeError("Invalid command %x" % command)
    if extended_device:
        if extended_device >= 2 ** 8:
            raise EncodeError("Invalid extended device %x" % extended_device)
        if device >= 2 ** 5:
            raise EncodeError("Invalid device %x" % device)
    else:
        if device >= 2 ** 8:
            raise EncodeError("Invalid device ID %x" % device)

    pulses = [2400]
    pulses.extend(_sirc_value_to_pulses(command, 7))
    if device >= 2 ** 5:
        pulses.extend(_sirc_value_to_pulses(device, 8))
    else:
        pulses.extend(_sirc_value_to_pulses(device, 5))
    if extended_device:
        pulses.extend(_sirc_value_to_pulses(extended_device, 8))

    return pulses


def _nec_value_to_pulses(value, bits):
    pulses = []
    for _ in range(bits):
        if value & 1:
            pulses.extend((560, 2250 - 560))
        else:
            pulses.extend((560, 560))

        value = value >> 1

    return pulses


def encode_nec(address, command):
    if command >= 2 ** 8:
        raise EncodeError("Invalid command %x" % command)

    if address >= 2 ** 16:
        raise EncodeError("Invalid address %x" % address)
    elif address >= 2 ** 8:
        address_low = address & 0xFF
        address_high = (address >> 8) & 0xFF

        if address_low == ~address_high & 0xFF:
            raise EncodeError("Invalid address %x (low == ~high)" % address)
    else:
        address_low = address
        address_high = ~address & 0xFF

    pulses = [9000, 4500]
    pulses.extend(_nec_value_to_pulses(address_low, 8))
    pulses.extend(_nec_value_to_pulses(address_high, 8))
    pulses.extend(_nec_value_to_pulses(command, 8))
    pulses.extend(_nec_value_to_pulses(~command & 0xFF, 8))
    pulses.append(560)

    return pulses
