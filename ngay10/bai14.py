import click

@click.command()
@click.option('--token', envvar='APP_AUTH_TOKEN')
def sync(token):

    if token:
        click.echo(f"Auth Token detected.")
    else:
        click.echo("Error: No token provided.")

sync()