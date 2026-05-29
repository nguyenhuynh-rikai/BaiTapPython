import os
import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from properties.models import Property, District, Ward, Category

def is_demand_side_post(title):
    if not title:
        return False
    title_lower = str(title).lower()
    keywords = [
        "cần thuê", "can thue",
        "cần tìm", "can tim",
        "tìm trọ", "tim tro",
        "tìm phòng", "tim phong",
        "muốn thuê", "muon thue",
        "muốn tìm", "muon tim",
        "kiếm trọ", "kiem tro",
        "kiếm phòng", "kiem phong",
        "tìm nhà", "tim nha",
        "cần kiếm", "can kiem"
    ]
    return any(kw in title_lower for kw in keywords)

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='data/rooms_cleaned.csv',
        )

    def handle(self, *args, **kwargs):
        relative_path = kwargs['file']
        full_path = os.path.join(settings.BASE_DIR, relative_path)

        if not os.path.exists(full_path):
            self.stdout.write(self.style.ERROR(f"Không tìm thấy file tại: {full_path}"))
            return

        try:
            # 1. Dọn dẹp dữ liệu cũ bị lỗi trong DB
            keywords = [
                "cần thuê", "can thue",
                "cần tìm", "can tim",
                "tìm trọ", "tim tro",
                "tìm phòng", "tim phong",
                "muốn thuê", "muon thue",
                "muốn tìm", "muon tim",
                "kiếm trọ", "kiem tro",
                "kiếm phòng", "kiem phong",
                "tìm nhà", "tim nha",
                "cần kiếm", "can kiem"
            ]
            from django.db.models import Q
            query = Q()
            for kw in keywords:
                query |= Q(title__icontains=kw)
            deleted_count, _ = Property.objects.filter(query).delete()
            if deleted_count > 0:
                self.stdout.write(self.style.SUCCESS(f"Đã dọn dẹp {deleted_count} bài đăng cũ loại 'cần thuê/tìm trọ' khỏi cơ sở dữ liệu."))

            # Đọc file CSV
            df = pd.read_csv(full_path)
            self.stdout.write(self.style.SUCCESS(f"Đã đọc file. Đang xử lý {len(df)} dòng..."))

            # Đảm bảo có Category mặc định
            category, _ = Category.objects.get_or_create(name="Phòng trọ", slug="phong-tro")

            count = 0
            skipped_demand = 0
            for _, row in df.iterrows():
                try:
                    title = row.get('title', 'Không có tiêu đề')
                    if is_demand_side_post(title):
                        skipped_demand += 1
                        continue

                    # Khớp nối Quận/Phường
                    district_name = str(row.get('district', 'Chưa rõ')).strip()
                    district, _ = District.objects.get_or_create(name=district_name)

                    ward_name = str(row.get('ward', 'Chưa rõ')).strip()
                    ward, _ = Ward.objects.get_or_create(name=ward_name, district=district)

                    # Khớp nối dữ liệu từ CSV vào Model Property
                    Property.objects.update_or_create(
                        source_url=row['url'],
                        defaults={
                            'title': title,
                            'description': row.get('description', ''),
                            'price': row.get('price_vnd', 0),
                            'area': row.get('area_m2', 0),
                            'price_per_m2': row.get('price_per_m2'),
                            'address': row.get('address', ''),
                            'district': district,
                            'ward': ward,
                            'category': category,
                            'source_name': row.get('source', 'NhaTot'),
                            'posted_at_text': str(row.get('posted_at', '')),
                            'is_active': True,
                            'status': 'approved'
                        }
                    )
                    count += 1
                except Exception as row_e:
                    self.stdout.write(self.style.WARNING(f"Bỏ qua 1 dòng do lỗi: {row_e}"))

            self.stdout.write(self.style.SUCCESS(f"Thành công! Đã nạp {count} bài đăng vào PostgreSQL (Bỏ qua {skipped_demand} bài tìm trọ)."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Lỗi hệ thống: {e}"))