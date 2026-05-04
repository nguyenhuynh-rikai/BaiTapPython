import click
import os

@click.command()
@click.argument('path', type=click.Path(exists=True))
def validate_path(path):

    click.echo(f"Path '{path}' is valid.")

validate_path()