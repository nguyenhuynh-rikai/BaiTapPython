import csv
import logging
import time
from functools import wraps

from .models import Category, District, Property, Ward


logger = logging.getLogger(__name__)


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()
        print(f"{func.__name__} finished in {end - start:.2f} seconds")

        return result

    return wrapper


def log_errors(func):
    # Decorator nay dung de ghi log khi ham bi loi.
    # Ly do dung:
    # - Khi import CSV nhieu dong, neu loi thi minh can biet loi o dau.
    # - logger.exception se luu ca traceback, huu ich hon print binh thuong.
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.exception("Error while running %s", func.__name__)
            raise

    return wrapper


def safe_text(value):
    # Chuyen du lieu ve text an toan.
    if value is None:
        return ""

    return str(value).strip()


def safe_int(value):
    # Chuyen du lieu ve so nguyen an toan.
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def safe_float(value):
    # Chuyen du lieu ve so thuc an toan.
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def is_valid_property_data(title, source_url, price, area):
    # Ham core logic de kiem tra 1 dong CSV co du du lieu toi thieu khong.
    # Tach rieng de import_row gon hon va sau nay de test unit test.
    if not title:
        return False
    if not source_url:
        return False
    if price is None:
        return False
    if area is None:
        return False

    return True


def calculate_price_per_m2(price, area):
    # Ham core logic tinh gia/m2 neu CSV khong co san cot price_per_m2.
    # Can check area > 0 de tranh loi chia cho 0.
    if price is None or area is None or area <= 0:
        return None

    return int(price / area)


class PropertyImportService:
    # Class nay gom toan bo logic import Property tu file CSV.
    # Ly do dung class:
    # - Can luu csv_path.
    # - Can luu cac bien dem created/updated/skipped.
    # - Cac method get_or_create_* dung chung trong qua trinh import.
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.created_count = 0
        self.updated_count = 0
        self.skipped_count = 0

    @measure_time
    @log_errors
    def import_data(self):
        # Method chinh: doc toan bo CSV va import tung dong.
        # DictReader bien moi dong CSV thanh dict:
        # row["title"], row["price_vnd"], row["url"], ...
        with open(self.csv_path, newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                self.import_row(row)

        return {
            "created": self.created_count,
            "updated": self.updated_count,
            "skipped": self.skipped_count,
        }

    def import_row(self, row):
        # Method nay xu ly 1 dong CSV.
        # Ly do tach rieng:
        # - import_data chi lo doc file.
        # - import_row chi lo chuyen 1 row thanh du lieu database.
        title = safe_text(row.get("title"))
        source_url = safe_text(row.get("url"))
        source_name = safe_text(row.get("source"))

        price = safe_int(row.get("price_vnd"))
        area = safe_float(row.get("area_m2"))
        price_per_m2 = safe_int(row.get("price_per_m2"))

        if price_per_m2 is None:
            price_per_m2 = calculate_price_per_m2(price, area)

        if not is_valid_property_data(title, source_url, price, area):
            self.skipped_count += 1
            return None

        category = self.get_or_create_category()
        district = self.get_or_create_district(row.get("district"))
        ward = self.get_or_create_ward(row.get("ward"), district)

        # update_or_create phu hop voi du lieu crawl.
        # source_url la unique:
        # - Neu URL chua co: tao Property moi.
        # - Neu URL da co: update Property cu bang defaults.
        property_obj, created = Property.objects.update_or_create(
            source_url=source_url,
            defaults={
                "title": title,
                "description": safe_text(row.get("description")),
                "price": price,
                "area": area,
                "price_per_m2": price_per_m2,
                "address": safe_text(row.get("address")),
                "district": district,
                "ward": ward,
                "category": category,
                "source_name": source_name,
                "posted_at_text": safe_text(row.get("posted_at")),
                "is_active": True,
            },
        )

        if created:
            self.created_count += 1
        else:
            self.updated_count += 1

        return property_obj

    def get_or_create_category(self):
        # Project hien tai chi crawl phong tro, nen category mac dinh la Phong tro.
        # get_or_create giup tranh tao trung category khi import nhieu lan.
        category, created = Category.objects.get_or_create(
            slug="phong-tro",
            defaults={"name": "Phong tro"},
        )

        return category

    def get_or_create_district(self, district_name):
        # Tao District neu CSV co ten quan/huyen.
        district_name = safe_text(district_name)

        if not district_name:
            return None

        district, created = District.objects.get_or_create(name=district_name)

        return district

    def get_or_create_ward(self, ward_name, district):
        # Ward can di kem District.
        # Neu khong co district thi khong nen tao ward, vi ward trung ten o nhieu noi.
        ward_name = safe_text(ward_name)

        if not ward_name or district is None:
            return None

        ward, created = Ward.objects.get_or_create(
            name=ward_name,
            district=district,
        )

        return ward
