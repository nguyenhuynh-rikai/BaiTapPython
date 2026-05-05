import sys, os

def get_path(path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.path.abspath("."), path)

with open(get_path("bai20.json")) as f:
    print(f.read())