import csv
import os
import re
import time
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://phongtro123.com/tinh-thanh/da-nang"
OUTPUT_FILE = "data/phongtro123_all.csv"


def clean_text(text):
    return re.sub(r"\s+", " ", text or "").strip()


def find_price(text):
    # Lấy giá dạng: 3 triệu/tháng, 3.5 triệu/tháng, 3,5 triệu/tháng.
    match = re.search(r"\d+(?:[,.]\d+)?\s*triệu/tháng", text, re.IGNORECASE)
    return match.group(0) if match else ""


def find_area(text):
    # Lấy diện tích dạng: 25 m2, 25 m², 25m2.
    match = re.search(r"(\d+(?:[,.]\d+)?)\s*m", text, re.IGNORECASE)
    return match.group(1).replace(",", ".") if match else ""


def find_district(text):
    # Danh sách quận/huyện Đà Nẵng thường gặp trong tin đăng.
    match = re.search(
        r"(Hải Châu|Cẩm Lệ|Liên Chiểu|Ngũ Hành Sơn|Sơn Trà|Thanh Khê|Hoà Vang|Hòa Vang),\s*Đà Nẵng",
        text,
        re.IGNORECASE,
    )
    return match.group(0) if match else ""


def get_total_pages(headers):
    # Bước 1: Tải trang đầu để xem web có bao nhiêu trang phân trang.
    response = requests.get(BASE_URL, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    total_pages = 1

    for link in soup.select("a[href*='page=']"):
        href = link.get("href", "")
        match = re.search(r"page=(\d+)", href)

        if match:
            page_number = int(match.group(1))
            total_pages = max(total_pages, page_number)

    return total_pages


def crawl_one_page(page, headers):
    if page == 1:
        page_url = BASE_URL
    else:
        page_url = f"{BASE_URL}?page={page}"

    response = requests.get(page_url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    rooms = []


    for title_tag in soup.select("h3 a"):
        title = clean_text(title_tag.get_text())
        detail_url = urljoin(BASE_URL, title_tag.get("href", ""))

        card = title_tag.find_parent(["article", "li", "div"])
        card_text = clean_text(card.get_text(" ", strip=True)) if card else title

        room = {
            "source": "phongtro123",
            "title": title,
            "price_text": find_price(card_text),
            "area_m2": find_area(card_text),
            "district": find_district(card_text),
            "description": card_text,
            "url": detail_url,
            "crawled_at": datetime.now().isoformat(timespec="seconds"),
        }
        rooms.append(room)

    return rooms


def save_csv(rooms):
    # Tạo thư mục data nếu chưa có.
    os.makedirs("data", exist_ok=True)

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


def crawl_all_phongtro123():
    headers = {"User-Agent": "Mozilla/5.0"}

    total_pages = get_total_pages(headers)

    print(f"Found {total_pages} pages")
    print("-" * 30)

    all_rooms = []

    for page in range(1, total_pages + 1):
        print(f"Crawling page {page}/{total_pages}")

        rooms = crawl_one_page(page, headers)
        all_rooms.extend(rooms)

        print(f" -> Got {len(rooms)} rooms")
        time.sleep(3)

    save_csv(all_rooms)

    print(f"Saved {len(all_rooms)} rooms to {OUTPUT_FILE}")


if __name__ == "__main__":
    crawl_all_phongtro123()
