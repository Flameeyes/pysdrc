<!--
SPDX-FileCopyrightText: 2020 Diego Elio Pettenò

SPDX-License-Identifier: MIT
-->

# Python Software Defined Remote Control

This started as a rough implementation of the SIRC infrared transmission protocol as used
by Sony TV and equipment, aimed at being used with
[CircuitPython](https://circuitpython.readthedocs.io/).

Following from that, proper decoding of NEC commands was also added, making the project
name a misnomer.

## Protocol Information

Please see [SB-Projects](https://www.sbprojects.net/knowledge/ir) for a lot of information
about Infrared protocols, including
[SIRC](https://www.sbprojects.net/knowledge/ir/sirc.php) and
[NEC](https://www.sbprojects.net/knowledge/ir/nec.php).
