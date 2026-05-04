import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--num", type=int, required=True)

args = parser.parse_args()

try:
    print(10 / args.num)
except ZeroDivisionError:
    print("❌ Không được chia cho 0!")