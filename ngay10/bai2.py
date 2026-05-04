import argparse

parser = argparse.ArgumentParser()
parser.add_argument("x", type=int, help="Number one")
parser.add_argument("y", type=int, help="Number two")
args = parser.parse_args()

print(f"Sum: {args.x + args.y}")