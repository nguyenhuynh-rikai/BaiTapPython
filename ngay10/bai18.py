import click

@click.command()
@click.version_option("1.0.0")
def main():
    print("Running tool...")

main()