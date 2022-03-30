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
    """Show the reference pulse definitions"""
    reference_table = core.get_reference_table()

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
    core.reset_reference_table()


@main.command()
def update():
    """Update a given reference pulse definition"""
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


if __name__ == "__main__":
    main()
