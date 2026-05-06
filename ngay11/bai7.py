import os
import sys

def get_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Command: pyinstaller --add-data "config.json;." 07_data_files.py
print(f"Loading config from: {get_path('config.json')}")