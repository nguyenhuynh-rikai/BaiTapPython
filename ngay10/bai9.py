from rich.table import Table
from rich.console import Console

console = Console()

table = Table(title="User List")

table.add_column("Name")
table.add_column("Age")

table.add_row("Nguyen", "22")
table.add_row("An", "21")

console.print(table)