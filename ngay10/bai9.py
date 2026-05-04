from rich.console import Console
from rich.table import Table

table = Table(title="System Status Report")
table.add_column("Service", style="cyan", no_wrap=True)
table.add_column("Status", style="magenta")
table.add_column("Uptime", justify="right", style="green")

table.add_row("Database", "Online", "14d 2h")
table.add_row("Auth-API", "Online", "3d 12h")
table.add_row("Cache", "Degraded", "1h 5m")

Console().print(table)