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

    def __init__(
        self, pin, carrier_frequency=38_000, duty_cycle=2 ** 15, default_repeat=1
    ):
        self._pwm = pulseio.PWMOut(
            pin, frequency=carrier_frequency, duty_cycle=duty_cycle
        )
        self._pulseout = pulseio.PulseOut(self._pwm)
        self._default_repeat = default_repeat
        if default_repeat < 1:
            raise ValueError(
                "default_repeat should be at least 1, got %d" % default_repeat
            )

    def transmit_pulses(self, pulses, repeat=None):
        """Transmit a set of pre-calculated pulses."""

        if not repeat:
            repeat = self._default_repeat

        if not isinstance(pulses, array.array):
            pulses = array.array("H", pulses)

        for _ in range(repeat):
            self._pulseout.send(pulses)
            time.sleep(0.025)


class SIRCTransmitter(Transmitter):
    """Transmitter for Sony SIRC remote protocol."""

    def __init__(
        self, pin, carrier_frequency=40_000, duty_cycle=2 ** 15, default_repeat=4
    ):
        super().__init__(
            pin,
            carrier_frequency=carrier_frequency,
            duty_cycle=duty_cycle,
            default_repeat=default_repeat,
        )

    def transmit_command(self, command, device, extended_device=None, repeat=None):
        pulses = encoder.encode_sirc(command, device, extended_device)
        self.transmit_pulses(pulses, repeat=repeat)


class NECTransmitter(Transmitter):
    """Transmitter for NEC remote protocol."""

    def transmit_command(self, address, command, repeat=None):
        pulses = encoder.encode_nec(address, command)
        self.transmit_pulses(pulses, repeat=repeat)

    def transmit_repeat(self, repeat=None):
        self.transmit_pulses(encoder.NEC_REPEAT, repeat=repeat)
