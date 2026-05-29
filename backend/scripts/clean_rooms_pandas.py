from pathlib import Path
import re

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

NHATOT_FILE = BASE_DIR / "data" / "nhatot_all.csv"
PHONGTRO123_FILE = BASE_DIR / "data" / "phongtro123_all.csv"
OUTPUT_FILE = BASE_DIR / "data" / "rooms_cleaned.csv"


def clean_text(value):
    # Xoa xuong dong, tab va khoang trang thua.
    if pd.isna(value):
        return ""

    value = str(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def price_text_to_vnd(value):
    # Chuyen "3.5 trieu/thang" thanh 3500000.
    if pd.isna(value) or value == "":
        return None

    text = str(value).lower().replace(",", ".")
    number_match = re.search(r"\d+(?:\.\d+)?", text)

    if not number_match:
        return None

    number = float(number_match.group())

    if "ty" in text or "tỷ" in text:
        return int(number * 1_000_000_000)

    if "trieu" in text or "triệu" in text:
        return int(number * 1_000_000)

    if "nghin" in text or "nghìn" in text:
        return int(number * 1_000)

    return int(number)


def clean_area(value):
    # Chuyen dien tich ve so float.
    if pd.isna(value) or value == "":
        return None

    text = str(value).replace(",", ".")
    number_match = re.search(r"\d+(?:\.\d+)?", text)

    if not number_match:
        return None

    return float(number_match.group())


def normalize_district(value):
    # Chuan hoa ten quan/huyen de de loc va tim kiem.
    text = clean_text(value).lower()

    if "hải châu" in text or "hai chau" in text:
        return "Hải Châu"
    if "cẩm lệ" in text or "cam le" in text:
        return "Cẩm Lệ"
    if "liên chiểu" in text or "lien chieu" in text:
        return "Liên Chiểu"
    if "ngũ hành sơn" in text or "ngu hanh son" in text:
        return "Ngũ Hành Sơn"
    if "sơn trà" in text or "son tra" in text:
        return "Sơn Trà"
    if "thanh khê" in text or "thanh khe" in text:
        return "Thanh Khê"
    if "hòa vang" in text or "hoà vang" in text or "hoa vang" in text:
        return "Hòa Vang"

    return clean_text(value)


def standardize_nhatot(df):
    # File NhaTot lay tu API co ten cot goc:
    # subject, price_string, size, area_name...
    df = df.rename(
        columns={
            "subject": "title",
            "price_string": "price_text",
            "size": "area_m2",
            "area_name": "district",
            "ward_name": "ward",
            "location": "address",
            "body": "description",
            "date": "posted_at",
        }
    )

    df["source"] = "nhatot"
    df["url"] = df["list_id"].apply(
        lambda value: f"https://gateway.chotot.com/v1/public/ad-listing/{value}"
        if not pd.isna(value)
        else ""
    )

    if "crawled_at" not in df.columns:
        df["crawled_at"] = ""

    return df


def standardize_phongtro123(df):
    # File Phongtro123 da gan dung cot chung, chi can them cot con thieu.
    if "price" not in df.columns:
        df["price"] = None

    if "ward" not in df.columns:
        df["ward"] = ""

    if "address" not in df.columns:
        df["address"] = ""

    if "posted_at" not in df.columns:
        df["posted_at"] = ""

    return df


def select_common_columns(df):
    # Dam bao DataFrame nao cung co du cac cot chung.
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

    for column in columns:
        if column not in df.columns:
            df[column] = ""

    return df[columns]


def main():
    # Buoc 1: Doc 2 file CSV.
    nhatot_df = pd.read_csv(NHATOT_FILE)
    phongtro_df = pd.read_csv(PHONGTRO123_FILE)

    input_rows = len(nhatot_df) + len(phongtro_df)

    # Buoc 2: Doi ten cot cua tung nguon ve chung mot format.
    nhatot_df = standardize_nhatot(nhatot_df)
    phongtro_df = standardize_phongtro123(phongtro_df)

    # Buoc 3: Chi giu cac cot can dung.
    nhatot_df = select_common_columns(nhatot_df)
    phongtro_df = select_common_columns(phongtro_df)

    # Buoc 4: Gop 2 nguon du lieu.
    df = pd.concat([nhatot_df, phongtro_df], ignore_index=True)

    # Buoc 5: Lam sach text.
    text_columns = ["title", "price_text", "district", "ward", "address", "description", "url"]

    for column in text_columns:
        df[column] = df[column].apply(clean_text)

    # Buoc 6: Lam sach gia.
    df["price_vnd"] = pd.to_numeric(df["price"], errors="coerce")
    df["price_from_text"] = df["price_text"].apply(price_text_to_vnd)
    df["price_vnd"] = df["price_vnd"].fillna(df["price_from_text"])

    # Buoc 7: Lam sach dien tich va quan/huyen.
    df["area_m2"] = df["area_m2"].apply(clean_area)
    df["district"] = df["district"].apply(normalize_district)

    # Buoc 8: Tao cot gia tren moi m2.
    df["price_per_m2"] = df["price_vnd"] / df["area_m2"]

    # Buoc 9: Xoa dong thieu thong tin quan trong.
    df = df.dropna(subset=["price_vnd", "area_m2"])
    df = df[df["title"] != ""]
    df = df[df["url"] != ""]

    # Buoc 10: Loc du lieu bat thuong don gian.
    df = df[df["price_vnd"] >= 500_000]
    df = df[df["price_vnd"] <= 50_000_000]
    df = df[df["area_m2"] >= 5]
    df = df[df["area_m2"] <= 200]

    # Buoc 11: Xoa trung theo URL.
    df = df.drop_duplicates(subset=["url"])

    # Buoc 12: Sap xep cot va luu file.
    final_columns = [
        "source",
        "title",
        "price_vnd",
        "price_text",
        "area_m2",
        "price_per_m2",
        "district",
        "ward",
        "address",
        "description",
        "posted_at",
        "url",
        "crawled_at",
    ]

    df = df[final_columns]
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"Input rows: {input_rows}")
    print(f"Clean rows: {len(df)}")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
