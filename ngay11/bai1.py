import os
import sys


def check_env():
    if hasattr(sys, 'real_prefix') or (sys.base_prefix != sys.prefix):
        print("Success: You are inside a Virtual Environment!")
    else:
        print("Warning: You are still using the Global Python.")

if __name__ == "__main__":
    check_env()