import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-v", "--verbose", action="store_true")

args = parser.parse_args()

if args.verbose:
    print("dang bat..")
else:
    print("dang tat...")