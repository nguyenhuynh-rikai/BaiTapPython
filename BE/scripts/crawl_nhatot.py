import requests
import math
import time
import csv
import os


def crawl_all_nhatot():
    limit = 30
    api_url = "https://gateway.chotot.com/v1/public/ad-listing"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    params = {"region_v2": 3017, "cg": 1050, "limit": limit, "o": 0}
    response = requests.get(api_url, params=params, headers=headers, timeout=20)
    print(response.url)

    if response.status_code != 200:
        print("Lỗi khi gọi API")
        return

    data = response.json()

    total_ads = data.get("total", 0)
    total_pages = math.ceil(total_ads / limit)
    #math.ceil làm tròn

    print(f"Hệ thống báo cáo: Có tổng cộng {total_ads} tin đăng.")
    print(f"Bot sẽ tiến hành cào {total_pages} trang...\n")
    print("-" * 30)

    all_ads = []

    for page in range(1, total_pages + 1):
        offset = (page - 1) * limit
        print(f"Đang cào Trang {page}/{total_pages} (offset = {offset})...")

        params["o"] = offset

        page_res = requests.get(api_url, params=params, headers=headers, timeout=20)

        if page_res.status_code == 200:
            page_data = page_res.json()
            ads = page_data.get("ads", [])

            all_ads.extend(ads)

            print(f" -> Lấy thành công {len(ads)} tin.")
        else:
            print(f" -> Lỗi trang {page}")

        time.sleep(3)

    columns = [
        "ad_id",
        "list_id",
        "subject",
        "price",
        "price_string",
        "size",
        "area_name",
        "ward_name",
        "location",
        "body",
        "date",
    ]

    os.makedirs("data",exist_ok=True)
    with open("data/nhatot_all.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=columns)

        writer.writeheader()

        for ad in all_ads:
            row = {
                "ad_id": ad.get("ad_id", ""),
                "list_id": ad.get("list_id", ""),
                "subject": ad.get("subject", ""),
                "price": ad.get("price", ""),
                "price_string": ad.get("price_string", ""),
                "size": ad.get("size", ""),
                "area_name": ad.get("area_name", ""),
                "ward_name": ad.get("ward_name", ""),
                "location": ad.get("location", ""),
                "body": ad.get("body", ""),
                "date": ad.get("date", ""),
            }

            writer.writerow(row)

    print(f"\nĐã lưu tổng cộng {len(all_ads)} tin vào data/nhatot_all.csv")


if __name__ == "__main__":
    crawl_all_nhatot()