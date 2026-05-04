import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--verbose", "-v", action="store_true", help="Hiển thị chi tiết")
args = parser.parse_args()

if args.verbose:
    print("Chế độ chi tiết đang BẬT...")
print("Đang thực hiện công việc...")