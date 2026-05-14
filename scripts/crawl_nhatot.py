# Crawl dữ liệu phòng trọ Đà Nẵng từ Nhà Tốt.
# Cách chạy:
#   .\.venv\Scripts\python.exe scripts\crawl_nhatot.py

import csv
from datetime import datetime

import requests


# Nhà Tốt dùng chung API với Chợ Tốt.
# region_v2=3017 là Đà Nẵng, cg=1050 là danh mục Phòng trọ.
API_URL = "https://gateway.chotot.com/v1/public/ad-listing"
OUTPUT_FILE = "data/nhatot_realtime.csv"


def crawl_nhatot():
    # Bước 1: Chuẩn bị tham số gửi lên API.
    params = {
        "region_v2": 3017,
        "cg": 1050,
        "limit": 30,
        "o": 0,
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    # Bước 2: Gửi request lấy dữ liệu JSON.
    response = requests.get(API_URL, params=params, headers=headers, timeout=20)
    response.raise_for_status()
    data = response.json()

    rooms = []

    # Bước 3: Lặp qua từng tin đăng và lấy các trường cần dùng.
    for item in data.get("ads", []):
        room = {
            "source": "nhatot",
            "title": item.get("subject", ""),
            "price": item.get("price", ""),
            "price_text": item.get("price_string", ""),
            "area_m2": item.get("size", ""),
            "district": item.get("area_name", ""),
            "ward": item.get("ward_name", ""),
            "address": item.get("location", ""),
            "description": item.get("body", ""),
            "posted_at": item.get("date", ""),
            "url": f"https://gateway.chotot.com/v1/public/ad-listing/{item.get('list_id', '')}",
            "crawled_at": datetime.now().isoformat(timespec="seconds"),
        }
        rooms.append(room)

    return rooms


def save_csv(rooms):
    # Bước 4: Ghi dữ liệu ra file CSV.
    columns = [
        "source",
        "title",
        "price",
        "price_text",
        "area_m2",
        "district",
        "ward",
        "address",
        "description",
        "posted_at",
        "url",
        "crawled_at",
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rooms)


if __name__ == "__main__":
    rooms = crawl_nhatot()
    save_csv(rooms)
    print(f"Crawled {len(rooms)} rooms from NhaTot")
    print(f"Saved to {OUTPUT_FILE}")
