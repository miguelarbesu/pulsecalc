"""CLI interface
"""

import click
from pulsecalc import core
from rich import print as rprint
from rich.table import Table


@click.group(help="NMR pulse calculator")
def main():
    """Just a placeholder for the main entrypoint."""
    pass


@main.command()
def init():
    """Create a table containing the reference pulse definitions"""
    click.echo("Initializing reference pulse table")
    core.create_reference_table()
    for channel in core.channels:
        pulse_length = click.prompt(
            f"Enter {channel} reference pulse length in μs", type=float
        )
        pulse_power = click.prompt(
            f"Enter {channel} reference pulse power in W", type=float
        )
        pulse_frequency = core.calculate_frequency(pulse_length)
        core.set_reference_pulse(channel, pulse_length, pulse_power, pulse_frequency)


@main.command()
def show():
    try:
        reference_table = core.get_reference_table()
    except FileNotFoundError:
        return
    """Show the reference pulse definitions"""

    rich_table = Table(title="Reference pulses", row_styles=["yellow", "blue", "red"])
    rich_table.add_column("Channel", style="bold")
    rich_table.add_column(
        "Length (μs)",
    )
    rich_table.add_column("Power (W)")
    rich_table.add_column("Frequency (kHz)")

    with open(reference_table, "r") as f:
        # skip header
        lines = f.readlines()[1:]
        for line in lines:
            channel, pulse_length, pulse_power, pulse_frequency = line.split("\t")
            rich_table.add_row(
                channel,
                pulse_length,
                pulse_power,
                pulse_frequency,
            )

    rprint(rich_table)
    return


@main.command()
def reset():
    """Reset the reference pulse definitions and/or calculations"""
    try:
        core.get_reference_table()
    except FileNotFoundError:
        return
    core.reset_reference_table()


@main.command()
def update():
    """Update a given reference pulse definition"""
    try:
        core.get_reference_table()
    except FileNotFoundError:
        return
    channel = click.prompt(
        "Which channel do you want to update?",
        show_choices=True,
        type=click.Choice(["1H", "13C", "15N"], case_sensitive=False),
    )
    pulse_length = click.prompt("What is the reference pulse length in μs?", type=float)
    pulse_power = click.prompt("What is the reference pulse power in W?", type=float)
    pulse_frequency = core.calculate_frequency(pulse_length)
    core.set_reference_pulse(channel, pulse_length, pulse_power, pulse_frequency)
    click.echo(
        f"{channel} reference pulse updated: {pulse_length:.2f} μs @ {pulse_power:.2f} W == {pulse_frequency:.2f} kHz"
    )


@main.command()
# request mas frequency
def hh():
    """Calculate typical Hartmann-Hahn conditions for Cross Polarization
    at a given MAS frequency based on the reference pulses.
    Conditions are given in kHz and as a fraction of the MAS frequency.
    Powers are given in W.
    """
    try:
        core.get_reference_table()
    except FileNotFoundError:
        return

    mas = click.prompt("What is the MAS frequency in kHz?", type=float)

    rich_table = Table(
        title=f"Hartmann-Hanh frequencies @ {mas} kHz (as n*MAS)",
        row_styles=["yellow", "blue", "red"],
    )
    rich_table.add_column("Channel", style="bold")
    hh_frequency_list = []

    for condition, ratio in core.hh_conditions.items():
        rich_table.add_column(condition, justify="center")
        hh_frequency_list.append(ratio * mas)

    for channel in core.channels:
        try:
            _, reference_power, reference_frequency = core.get_reference_pulse(channel)
        except TypeError:
            click.echo(f"No reference pulse defined for {channel}")
            continue
        hh_power_list = []
        for hh_frequency in hh_frequency_list:
            hh_power_list.append(
                core.calculate_power(reference_frequency, reference_power, hh_frequency)
            )
        hh_power_list = ["{:.2f}".format(power) for power in hh_power_list]
        rich_table.add_row(channel, *hh_power_list)
    rprint(rich_table)
    return


if __name__ == "__main__":
    main()
