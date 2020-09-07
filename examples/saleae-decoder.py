# SPDX-FileCopyrightText: 2020 Diego Elio Pettenò
# SPDX-FileCopyrightText: 2020 Facebook Inc.
#
# SPDX-License-Identifier: MIT
"""Hacky Saleae capture decoder.

This tool allows decoding traces coming from an IR Decoder chip (such as the TSOP4830)
signal line.

For the decode to work, a single channel export of the timing in digital format should
be exported as CSV.
"""

import csv
import logging

import click

import pysirc.decoder


def times_to_pulses(times):
    previous_pulse_time = 0
    signal = []
    for pulse_time in times:
        pulse_duration = int((pulse_time - previous_pulse_time) * 1_000_000)
        previous_pulse_time = pulse_time
        if pulse_duration > 10000:
            if signal:
                yield signal
            signal = []
            continue
        signal.append(pulse_duration)


def extract_times_from_reader(reader):
    next(reader)  # Ignore the headers
    next(reader)  # Ignore the starting state

    return [float(pulse_time) for pulse_time, _ in reader]


def try_all_decoders(pulses):
    try:
        code = pysirc.decoder.decode_sirc(pulses)
        return "SIRC", code
    except pysirc.decoder.SIRCDecodeException as e:  # failed to decode
        logging.debug(f"Failed to decode as SIRC: {e.args}")

    try:
        code = pysirc.decoder.decode_nec(pulses)
        return "NEC", code
    except pysirc.decoder.NECDecodeException as e:
        logging.debug(f"Failed to decode as NEC: {e.args}")

    return "RAW", pulses


@click.command()
@click.argument("input", type=click.File())
def convert(input):
    reader = csv.reader(input)

    for pulses in times_to_pulses(extract_times_from_reader(reader)):
        code_type, code = try_all_decoders(pulses)
        print(f"Decoded as {code_type}: {code}")


if __name__ == "__main__":
    convert()
