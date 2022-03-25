#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module template
"""


channels = ["1H", "13C", "15N"]


def calculate_frequency(pulse_length):
    """Calculate the frequency of a pulse in kHz from its length in μs

    Args:
        pulse_length (float): Pulse length in μs

    Returns:
        pulse_frequency: Pulse frequency in kHz
    """
    pulse_frequency = 1e3 / (pulse_length * 4)
    return pulse_frequency
