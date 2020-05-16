# SPDX-FileCopyrightText: 2020 Diego Elio Pettenò
#
# SPDX-License-Identifier: MIT

import unittest

from pysirc import decoder


class DecoderTest(unittest.TestCase):
    def test_simple(self):
        pulses = [
            2442,
            560,
            623,
            575,
            1221,
            577,
            617,
            582,
            622,
            577,
            1219,
            579,
            625,
            574,
            620,
            578,
            1218,
            580,
            624,
            575,
            619,
            581,
            623,
            575,
            618,
        ]
        self.assertEqual(decoder.decode_sirc(pulses), (18, 1))

    def test_ideal(self):
        pulses = [
            2400,
            600,
            600,
            600,
            1200,
            600,
            600,
            600,
            600,
            600,
            1200,
            600,
            600,
            600,
            600,
            600,
            1200,
            600,
            600,
            600,
            600,
            600,
            600,
            600,
            600,
        ]
        self.assertEqual(decoder.decode_sirc(pulses), (18, 1))

    def test_bad_header(self):
        pulses = [
            200000,
            600,
            600,
            600,
            1200,
            600,
            600,
            600,
            600,
            600,
            1200,
            600,
            600,
            600,
            600,
            600,
            1200,
            600,
            600,
            600,
            600,
            600,
            600,
            600,
            600,
        ]
        with self.assertRaises(decoder.DecodeException):
            decoder.decode_sirc(pulses)

    def test_short(self):
        pulses = [
            2400,
            600,
            600,
        ]
        with self.assertRaises(decoder.DecodeException):
            decoder.decode_sirc(pulses)

    def test_bad_length(self):
        pulses = [
            2400,
            600,
            600,
            600,
            1200,
            600,
            600,
            600,
            600,
            600,
            1200,
            600,
            600,
            600,
            600,
            600,
            1200,
            600,
            600,
            600,
            600,
            600,
        ]
        with self.assertRaises(decoder.DecodeException):
            decoder.decode_sirc(pulses)
