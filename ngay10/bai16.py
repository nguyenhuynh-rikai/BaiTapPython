import click
import sys

@click.command()
def execute():
    try:
        result = 10 / 0
    except ZeroDivisionError:
        click.secho("CRITICAL ERROR: Division by zero is not allowed.", fg="red", bold=True)
        sys.exit(1)

execute()