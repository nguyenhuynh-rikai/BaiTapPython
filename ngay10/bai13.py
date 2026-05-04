import click

@click.command()
@click.option('--env', type=click.Choice(['dev', 'staging', 'prod'], case_sensitive=False))
def deploy(env):

    click.echo(f"Deploying to: {env}")

deploy()