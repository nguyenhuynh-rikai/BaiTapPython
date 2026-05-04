from rich.console import Console

console = Console()
console.print("ERROR: Operation failed!", style="bold red")
console.print("SUCCESS: Deployment complete!", style="bold green")
console.print("WARNING: Low disk space.", style="yellow")