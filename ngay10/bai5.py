import click

@click.group()
def cli():
    pass

@cli.command()
def add():
    click.echo("User added successfully.")

@cli.command()
def delete():
    click.echo("User deleted successfully.")

if __name__ == '__main__':
    cli()