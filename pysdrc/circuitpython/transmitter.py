# SPDX-FileCopyrightText: 2020 Diego Elio Pettenò
# SPDX-FileCopyrightText: 2020 Facebook Inc.
#
# SPDX-License-Identifier: MIT

"""CircuitPython-compatible infrared remote transmitters.

Hardware compatibility is finnicky. This code has been tested with the following boards:

 - Feather M4 Express
 - Feather M0
 - Feather nrf52840
 - Feather S2
 - Trinket M0

Most of these boards only support a single transmitter for the lifetime of the board,
the exception being the Feather S2, that appears to support multiple transmitters
correctly.

Note that while it is possible to use this transmitter to simulate the output of an
Infrared _decoder_ (which does not include a carrier wave), this is only been tested
to work on the following:

 - Feather nrf52840

And has been confirmed not working on Feather S2.
"""

import array
import sys
import time

import pulseio

from pysdrc import encoder

# This is very annoying: different CircuitPython ports have different interfaces
# for the PulseOut class, so we need to abstract the PulseOut creation ourselves.
_PULSEOUT_NO_CARRIER_PLATFORMS = {"Espressif ESP32-S2"}


class Transmitter:
    """Generic transmitter for infrared remotes."""

    def __init__(
        self,
        pin,
        carrier_frequency: int = 38_000,
        duty_cycle: int = 2 ** 15,
        default_repeat: int = 1,
    ) -> None:
        if sys.platform in _PULSEOUT_NO_CARRIER_PLATFORMS:
            self._pulseout = pulseio.PulseOut(
                pin=pin, frequency=carrier_frequency, duty_cycle=duty_cycle
            )
        else:
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
            pulse_array = array.array("H", pulses)

        for _ in range(repeat):
            self._pulseout.send(pulse_array)
            time.sleep(0.025)


class SIRCTransmitter(Transmitter):
    """Transmitter for Sony SIRC remote protocol."""

    def __init__(
        self,
        pin,
        carrier_frequency: int = 40_000,
        duty_cycle: int = 2 ** 15,
        default_repeat: int = 4,
    ) -> None:
        super().__init__(
            pin,
            carrier_frequency=carrier_frequency,
            duty_cycle=duty_cycle,
            default_repeat=default_repeat,
        )

    def transmit_command(
        self,
        command: int,
        device: int,
        extended_device=None,
        repeat=None,
        force_8bit_device: bool = False,
    ) -> None:
        pulses = encoder.encode_sirc(
            command, device, extended_device, force_8bit_device=force_8bit_device
        )
        self.transmit_pulses(pulses, repeat=repeat)


class NECTransmitter(Transmitter):
    """Transmitter for NEC remote protocol."""

    def transmit_command(self, address: int, command: int, repeat=None) -> None:
        pulses = encoder.encode_nec(address, command)
        self.transmit_pulses(pulses, repeat=repeat)

    def transmit_repeat(self, repeat=None) -> None:
        self.transmit_pulses(encoder.NEC_REPEAT, repeat=repeat)
