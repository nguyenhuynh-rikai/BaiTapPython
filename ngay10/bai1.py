import argparse

parser = argparse.ArgumentParser(description="Chào hỏi người dùng.")
parser.add_argument("--name", help="Tên của bạn")
args = parser.parse_args()

if args.name:
    print(f"Xin chào, {args.name}!")
else:
    print("Xin chào người lạ!")