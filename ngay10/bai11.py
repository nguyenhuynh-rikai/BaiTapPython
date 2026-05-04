import click

@click.command()
@click.option('--port', default=8000, help='Port to listen on (default: 8000)')
def start_server(port):
    click.echo(f"Server starting on port: {port}")

start_server()