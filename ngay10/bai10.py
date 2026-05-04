import click

if click.confirm('Are you sure you want to drop the production database?', abort=True):
    click.echo('Dropping tables...')