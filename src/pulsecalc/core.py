#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module template
"""
from pathlib import Path

import click

channels = ["1H", "13C", "15N"]


def get_reference_table():
    """Get the reference pulse table

    Returns:
        reference_table (list): List of reference pulse definitions
    """
    reference_table = Path.cwd() / "reference_pulses.csv"
    if not reference_table.is_file():
        click.echo("The reference pulse table does not exist")
        return
    return reference_table


def calculate_frequency(pulse_length):
    """Calculate the frequency of a pulse in kHz from its length in μs

    Args:
        pulse_length (float): Pulse length in μs

    Returns:
        pulse_frequency: Pulse frequency in kHz
    """
    pulse_frequency = 1e3 / (pulse_length * 4)
    return pulse_frequency


def create_reference_table():
    """Create the reference pulse table.
    By default, the table is created in the current directory.
    """
    reference_table = Path.cwd() / "reference_pulses.csv"
    if reference_table.is_file():
        click.confirm(
            "The reference pulse table already exists. Do you want to overwrite it?",
            abort=True,
        )
        reference_table.unlink()
    reference_table.write_text("Channel\tLength (μs)\tPower (W)\tFrequency (kHz)\n")
    return


def reset_reference_table():
    """Reset the reference pulse table"""
    reference_table = Path.cwd() / "reference_pulses.csv"
    if not reference_table.is_file():
        click.echo("The reference pulse table does not exist")
        return

    click.confirm(
        "Are you sure you want to reset the reference pulse table?", abort=True
    )
    reference_table.unlink()
    click.echo("Reference pulse table has been reset")

    return


def set_reference_pulse(channel, pulse_length, pulse_power, pulse_frequency):
    """Set a reference pulse definition

    Args:
        channel (str): Channel name. Must be one of the following: 1H, 13C, 15N.
        pulse_length (float): Pulse length in μs
        pulse_power (float): Pulse power in W
        pulse_frequency (float): Pulse frequency in kHz
    """
    # read the table
    reference_table = Path.cwd() / "reference_pulses.csv"
    # update the line for the given channel
    new_line = (
        f"{channel}\t{pulse_length:.2f}\t{pulse_power:.2f}\t{pulse_frequency:.2f}\n"
    )
    with reference_table.open("r+") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith(channel):
                lines[i] = new_line
                break
        else:
            lines.append(new_line)
        f.seek(0)
        f.writelines(lines)
    return
