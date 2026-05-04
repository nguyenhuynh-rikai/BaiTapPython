import click

@click.command()
@click.version_option(version='1.2.0', prog_name="SuperTool")
def main():
    click.echo("Application is running...")

main()