from contextlib import suppress
import os

with suppress(FileNotFoundError):
    os.remove("file_không_tồn_tại.txt")