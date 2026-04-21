from contextlib import suppress

with suppress(Exception):
    x = int("abc")
    y = 10 / 0
