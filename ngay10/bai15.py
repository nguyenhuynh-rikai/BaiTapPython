import argparse

parser = argparse.ArgumentParser(
    description="Tool xử lý dữ liệu CSV",
    epilog="Ví dụ: python ngay10/bai15.py --file data.csv --mode summary"
)

parser.add_argument(
    "--file",
    help="Đường dẫn tới file CSV",
    required=True
)

parser.add_argument(
    "--mode",
    help="Chế độ chạy (summary/filter)",
    choices=["summary", "filter"],
    required=True
)

args = parser.parse_args()