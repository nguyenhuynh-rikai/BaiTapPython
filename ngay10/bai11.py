import click

@click.command()
@click.option("--name", default="Guest")
def hello(name):
    print("Hello,", name)

hello()