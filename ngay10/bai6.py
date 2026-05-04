import click

@click.command()
@click.password_option()
def login(password):
    print("Password da nhan")

if __name__ == "__main__":
    login()