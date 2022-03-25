"""Entrypoint module, in case you use `python -m pulsecalc`.
"""

import click
from pulsecalc import core


@click.group(help="NMR pulse calculator")
def main():
    """Just a placeholder for the main entrypoint."""
    pass


@main.command()
def init():
    """Create a table containint the reference pulse definitions"""
    click.echo("Initializing reference pulse table")
    # core.create_table()
    for channel in core.channels:
        pulse_length = click.prompt(
            f"Enter {channel} reference pulse length in μs", type=float
        )
        pulse_power = click.prompt(
            f"Enter {channel} reference pulse power in W", type=float
        )
        pulse_frequency = core.calculate_frequency(pulse_length)
        # core.set_reference_pulse(channel, pulse_length, pulse_power, pulse_frequency)


@main.command()
def show_reference():
    """Show the reference pulse definitions"""
    # core.show_reference_table()
    return


@main.command()
def reset():
    """Reset the reference pulse definitions"""
    # core.reset_reference_table()
    click.confirm(
        "Are you sure you want to reset the reference pulse table?", abort=True
    )
    # core.reset_reference_table()
    click.echo("Reference pulse table has been reset")
    click.confirm("Are you sure you want to reset the calculations table?", abort=True)
    # core.reset_calculations_table()
    print("Calculations table has been reset")


@main.command()
def update_reference():
    """Update a given reference pulse definition"""
    channel = click.prompt(
        "Which channel do you want to update?",
        show_choices=True,
        type=click.Choice(["1H", "13C", "15N"], case_sensitive=False),
    )
    pulse_length = click.prompt("What is the reference pulse length in μs?", type=float)
    pulse_power = click.prompt("What is the reference pulse power in W?", type=float)
    pulse_frequency = core.calculate_frequency(pulse_length)
    # core.update_reference_table(channel, pulse_length, pulse_power)
    click.echo(
        f"{channel} reference pulse updated: {pulse_length:.2f} μs @ {pulse_power:.2f} W == {pulse_frequency:.2f} kHz"
    )


if __name__ == "__main__":
    main()
