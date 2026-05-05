import click

@click.group()
def cli():
    pass

@cli.command()
@click.option("--name")
def hello(name):
    print("Hello", name)

if __name__ == "__main__":
    cli()