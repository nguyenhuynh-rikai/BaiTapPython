#   .\.venv\Scripts\python.exe scripts\crawl_phongtro123.py
import csv
import re
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


URL = "https://phongtro123.com/tinh-thanh/da-nang"
OUTPUT_FILE = "data/phongtro123_realtime.csv"


def clean_text(text):
    # Xóa xuống dòng và khoảng trắng thừa.
    return re.sub(r"\s+", " ", text or "").strip()


def find_price(text):
    # Tìm chuỗi giá kiểu: 3.3 triệu/tháng, 2 triệu/tháng...
    match = re.search(r"\d+(?:[,.]\d+)?\s*triệu/tháng", text, re.IGNORECASE)
    return match.group(0) if match else ""


def find_area(text):
    # Tìm diện tích kiểu: 25 m2, 25 m²...
    match = re.search(r"(\d+(?:[,.]\d+)?)\s*m", text, re.IGNORECASE)
    return match.group(1).replace(",", ".") if match else ""


def crawl_phongtro123():
    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    # Bước 1: Tải HTML của trang danh sách.
    response = requests.get(URL, headers=headers, timeout=20)
    response.raise_for_status()

    # Bước 2: Dùng BeautifulSoup để đọc HTML.
    soup = BeautifulSoup(response.text, "html.parser")
    rooms = []

    # Bước 3: Mỗi tin đăng trên trang có tiêu đề nằm trong thẻ h3 a.
    for title_tag in soup.select("h3 a"):
        title = clean_text(title_tag.get_text())
        detail_url = urljoin(URL, title_tag.get("href", ""))

        # Lấy phần cha gần nhất để gom giá, diện tích, khu vực, mô tả.
        card = title_tag.find_parent(["article", "li", "div"])
        card_text = clean_text(card.get_text(" ", strip=True)) if card else title

        price_text = find_price(card_text)
        area_m2 = find_area(card_text)

        # Khu vực thường có dạng: Hải Châu, Đà Nẵng
        district_match = re.search(
            r"(Hải Châu|Cẩm Lệ|Liên Chiểu|Ngũ Hành Sơn|Sơn Trà|Thanh Khê|Hoà Vang|Hòa Vang),\s*Đà Nẵng",
            card_text,
            re.IGNORECASE,
        )
        district = district_match.group(0) if district_match else ""

        room = {
            "source": "phongtro123",
            "title": title,
            "price_text": price_text,
            "area_m2": area_m2,
            "district": district,
            "description": card_text,
            "url": detail_url,
            "crawled_at": datetime.now().isoformat(timespec="seconds"),
        }
        rooms.append(room)

    return rooms


def save_csv(rooms):
    # Bước 4: Ghi dữ liệu ra file CSV.
    columns = [
        "source",
        "title",
        "price_text",
        "area_m2",
        "district",
        "description",
        "url",
        "crawled_at",
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rooms)


if __name__ == "__main__":
    rooms = crawl_phongtro123()
    save_csv(rooms)
    print(f"Crawled {len(rooms)} rooms from Phongtro123")
    print(f"Saved to {OUTPUT_FILE}")
