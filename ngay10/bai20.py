import questionary

action = questionary.select(
    "What would you like to do?",
    choices=[
        "Start Service",
        "View Logs",
        "Configure Settings",
        "Exit"
    ]
).ask()

print(f"Selected action: {action}")