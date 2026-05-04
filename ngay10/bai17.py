import yaml

def load_settings():
    yaml_content = """
    app_name: MyCLI
    version: 1.0.4
    debug: true
    """
    return yaml.safe_load(yaml_content)

config = load_settings()
print(f"Loaded Config: {config['app_name']} v{config['version']}")