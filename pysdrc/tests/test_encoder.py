# SPDX-FileCopyrightText: 2020 Diego Elio Pettenò
#
# SPDX-License-Identifier: MIT

import unittest

from pysdrc import encoder


class EncoderTest(unittest.TestCase):
    def test_simple(self):
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
            600,
        ]
        self.assertEqual(encoder.encode_sirc(18, 1), pulses)
