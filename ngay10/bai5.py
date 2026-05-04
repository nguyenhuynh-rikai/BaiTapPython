import click

@click.group()
def cli():
    pass

@cli.group()
def user():
    pass

@user.command()
@click.argument("name")
def add(name):
    print("add {}".format(name))

@user.command()
@click.argument("name")
def delete(name):
    print("delete {}".format(name))

if __name__ == "__main__":
    cli()