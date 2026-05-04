import click

@click.command()
@click.password_option()
def login(password):

    click.echo(f"Password received (Length: {len(password)})")

if __name__ == '__main__':
    login()