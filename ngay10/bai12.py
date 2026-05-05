import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)

args = parser.parse_args()

if not os.path.exists(args.input):
    print("File không tồn tại!")
    exit()

print("File hợp lệ, tiếp tục xử lý...")