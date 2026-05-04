import click

@click.command()
def delete():
    if click.confirm("Are you sure?"):
        print("Deleted!")
    else:
        print("Cancelled!")

if __name__ == "__main__":
    delete()