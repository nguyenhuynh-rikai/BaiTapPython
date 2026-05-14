import argparse
import csv
import re
import time
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


NHATOT_URL = "https://www.nhatot.com/thue-phong-tro-da-nang"
PHONGTRO123_URL = "https://phongtro123.com/tinh-thanh/da-nang"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}

CSV_COLUMNS = [
    "source",
    "title",
    "price_text",
    "price_vnd",
    "area_m2",
    "district",
    "address",
    "posted_at_text",
    "description",
    "url",
    "crawled_at",
]


def clean_text(text):
    """Xoa khoang trang thua de text de doc hon."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def fetch_html(url):
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return response.text


def parse_price_to_vnd(price_text):
    text = clean_text(price_text).lower().replace(",", ".")
    match = re.search(r"(\d+(?:\.\d+)?)", text)
    if not match:
        return None

    number = float(match.group(1))
    if "tỷ" in text or "ty" in text:
        return int(number * 1_000_000_000)
    if "triệu" in text or "trieu" in text:
        return int(number * 1_000_000)
    if "nghìn" in text or "ngan" in text or "k/" in text:
        return int(number * 1_000)
    return int(number)


def parse_area_m2(text):
    text = clean_text(text).lower()
    match = re.search(r"(\d+(?:[,.]\d+)?)\s*m", text)
    if not match:
        return None
    return float(match.group(1).replace(",", "."))


def first_match(pattern, text):
    match = re.search(pattern, text, flags=re.IGNORECASE)
    return clean_text(match.group(1)) if match else ""


def make_row(source, title, price_text, area_m2, district, address, posted_at_text, description, url):
    return {
        "source": source,
        "title": clean_text(title),
        "price_text": clean_text(price_text),
        "price_vnd": parse_price_to_vnd(price_text),
        "area_m2": area_m2,
        "district": clean_text(district),
        "address": clean_text(address),
        "posted_at_text": clean_text(posted_at_text),
        "description": clean_text(description),
        "url": url,
        "crawled_at": datetime.now().isoformat(timespec="seconds"),
    }


def crawl_phongtro123(max_pages=1, delay=1):
    rows = []

    for page in range(1, max_pages + 1):
        url = PHONGTRO123_URL if page == 1 else f"{PHONGTRO123_URL}?page={page}"
        soup = BeautifulSoup(fetch_html(url), "html.parser")

        # Moi tin dang tren trang nay thuong co h3 chua link chi tiet.
        for title_tag in soup.select("h3 a"):
            card = title_tag.find_parent(["article", "li", "div"])
            text = clean_text(card.get_text(" ", strip=True)) if card else ""

            title = title_tag.get_text(" ", strip=True)
            detail_url = urljoin(PHONGTRO123_URL, title_tag.get("href", ""))

            price_text = first_match(r"(\d+(?:[,.]\d+)?\s*(?:triệu|nghìn|tỷ).*?/tháng)", text)
            area_m2 = parse_area_m2(text)
            district = first_match(r"((?:Hải Châu|Cẩm Lệ|Liên Chiểu|Ngũ Hành Sơn|Sơn Trà|Thanh Khê|Hoà Vang|Hòa Vang),\s*Đà Nẵng)", text)
            posted_at_text = first_match(r"((?:\d+\s+(?:phút|giờ|ngày|tuần|tháng)\s+trước)|hôm qua)", text)

            description = text
            rows.append(
                make_row(
                    "phongtro123",
                    title,
                    price_text,
                    area_m2,
                    district,
                    "",
                    posted_at_text,
                    description,
                    detail_url,
                )
            )

        time.sleep(delay)

    return rows


def crawl_nhatot(max_pages=1, delay=1):
    rows = []

    for page in range(1, max_pages + 1):
        url = NHATOT_URL if page == 1 else f"{NHATOT_URL}?page={page}"
        soup = BeautifulSoup(fetch_html(url), "html.parser")

        # NhaTot render danh sach thanh cac link. Loc link co noi dung gia + dien tich.
        for link in soup.select("a[href]"):
            text = clean_text(link.get_text(" ", strip=True))
            if "triệu/tháng" not in text and "đ/tháng" not in text:
                continue
            if "m²" not in text and "m2" not in text:
                continue

            detail_url = urljoin(NHATOT_URL, link.get("href", ""))
            price_text = first_match(r"(\d+(?:[,.]\d+)?\s*(?:triệu|tỷ|đ).*?/tháng)", text)
            area_m2 = parse_area_m2(text)
            district = first_match(r"((?:Quận|Huyện)\s+[^()]+)", text)
            posted_at_text = first_match(r"((?:\d+\s+(?:phút|giờ)\s+trước)|\d+\s+ngày\s+trước|hôm qua)", text)

            title = text
            if price_text:
                title = text.split(price_text)[0]
            title = re.sub(r"^\+?\s*\d*\s*", "", title).strip()

            rows.append(
                make_row(
                    "nhatot",
                    title,
                    price_text,
                    area_m2,
                    district,
                    "",
                    posted_at_text,
                    text,
                    detail_url,
                )
            )

        time.sleep(delay)

    return rows


def remove_duplicates(rows):
    seen = set()
    unique_rows = []

    for row in rows:
        key = row["url"] or (row["source"], row["title"], row["price_text"])
        if key in seen:
            continue
        seen.add(key)
        unique_rows.append(row)

    return unique_rows


def save_csv(rows, output_path):
    with open(output_path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Crawl phong tro Da Nang tu NhaTot va Phongtro123.")
    parser.add_argument("--pages", type=int, default=1, help="So trang moi website can crawl.")
    parser.add_argument("--delay", type=float, default=1, help="So giay nghi giua cac request.")
    parser.add_argument("--output", default="data/realtime_rooms_da_nang.csv", help="File CSV dau ra.")
    args = parser.parse_args()

    rows = []
    rows.extend(crawl_nhatot(max_pages=args.pages, delay=args.delay))
    rows.extend(crawl_phongtro123(max_pages=args.pages, delay=args.delay))

    rows = remove_duplicates(rows)
    save_csv(rows, args.output)

    print(f"Da crawl {len(rows)} tin dang.")
    print(f"Da luu vao: {args.output}")


if __name__ == "__main__":
    main()
