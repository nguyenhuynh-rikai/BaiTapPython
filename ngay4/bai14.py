from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove("file_không_tồn_tại.txt")