# SPDX-FileCopyrightText: 2020 Diego Elio Pettenò
#
# SPDX-License-Identifier: MIT

"""CircuitPython-compatible transmitter for Sony SIRC protocol."""

import array
import time

import pulseio

from pysirc import encoder


class SircTransmitter:
    def __init__(self, pin):
        self._pwm = pulseio.PWMOut(pin, frequency=40_000, duty_cycle=2 ** 15)
        self._pulseout = pulseio.PulseOut(self._pwm)

    def transmit_pulses(self, pulses):
        """Transmit a set of pre-calculated pulses."""

        if not isinstance(pulses, array.array):
            pulses = array.array("H", pulses)

        for _ in range(4):
            self._pulseout.send(pulses)
            time.sleep(0.025)

    def transmit_command(self, command, device, extended_device=None):
        pulses = encoder.encode_sirc(command, device, extended_device)
        self.transmit_pulses(pulses)
