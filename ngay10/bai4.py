import click

@click.command()
@click.option("--name", default="Guest")
def hello(name):
    print("Hello,", name)

if __name__ == "__main__":
    hello()