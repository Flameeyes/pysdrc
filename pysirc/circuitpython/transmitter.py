# SPDX-FileCopyrightText: 2020 Diego Elio Pettenò
# SPDX-FileCopyrightText: 2020 Facebook Inc.
#
# SPDX-License-Identifier: MIT

"""CircuitPython-compatible infrared remote transmitters."""

import array
import time

import pulseio

from pysirc import encoder


class Transmitter:
    """Generic transmitter for infrared remotes."""

    def __init__(self, pin, frequency=38_000, duty_cycle=2 ** 15):
        self._pwm = pulseio.PWMOut(pin, frequency=frequency, duty_cycle=duty_cycle)
        self._pulseout = pulseio.PulseOut(self._pwm)

    def transmit_pulses(self, pulses):
        """Transmit a set of pre-calculated pulses."""

        if not isinstance(pulses, array.array):
            pulses = array.array("H", pulses)

        for _ in range(4):
            self._pulseout.send(pulses)
            time.sleep(0.025)


class SIRCTransmitter(Transmitter):
    """Transmitter for Sony SIRC remote protocol."""

    def __init__(self, pin, frequency=40_000, duty_cycle=2 ** 15):
        super().__init__(pin, frequency=frequency, duty_cycle=duty_cycle)

    def transmit_command(self, command, device, extended_device=None):
        pulses = encoder.encode_sirc(command, device, extended_device)
        self.transmit_pulses(pulses)


class NECTransmitter(Transmitter):
    """Transmitter for NEC remote protocol."""

    def transmit_command(self, address, command):
        pulses = encoder.encode_nec(address, command)
        self.transmit_pulses(pulses)

    def transmit_repeat(self):
        self.transmit_pulses(encoder.NEC_REPEAT)
