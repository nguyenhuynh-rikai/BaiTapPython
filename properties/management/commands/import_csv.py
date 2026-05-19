import os
import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from properties.models import Property, District, Ward, Category

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
            # Đọc file CSV
            df = pd.read_csv(full_path)
            self.stdout.write(self.style.SUCCESS(f"Đã đọc file. Đang xử lý {len(df)} dòng..."))

            # Đảm bảo có Category mặc định
            category, _ = Category.objects.get_or_create(name="Phòng trọ", slug="phong-tro")

            count = 0
            for _, row in df.iterrows():
                try:
                    # 1. Khớp nối Quận/Phường
                    district_name = str(row.get('district', 'Chưa rõ')).strip()
                    district, _ = District.objects.get_or_create(name=district_name)

                    ward_name = str(row.get('ward', 'Chưa rõ')).strip()
                    ward, _ = Ward.objects.get_or_create(name=ward_name, district=district)

                    # 2. Khớp nối dữ liệu từ CSV vào Model Property
                    # Lưu ý: Tên cột bên trái (ví dụ: source_url) là của Django Model
                    # Tên trong ngoặc row['...'] là tên cột bạn vừa gửi
                    Property.objects.update_or_create(
                        source_url=row['url'], # Map 'url' trong CSV vào 'source_url' trong DB
                        defaults={
                            'title': row.get('title', 'Không có tiêu đề'),
                            'description': row.get('description', ''),
                            'price': row.get('price_vnd', 0), # Map 'price_vnd'
                            'area': row.get('area_m2', 0),    # Map 'area_m2'
                            'price_per_m2': row.get('price_per_m2'),
                            'address': row.get('address', ''),
                            'district': district,
                            'ward': ward,
                            'category': category,
                            'source_name': row.get('source', 'NhaTot'),
                            'posted_at_text': str(row.get('posted_at', '')),
                            'is_active': True
                        }
                    )
                    count += 1
                except Exception as row_e:
                    self.stdout.write(self.style.WARNING(f"Bỏ qua 1 dòng do lỗi: {row_e}"))

            self.stdout.write(self.style.SUCCESS(f"Thành công! Đã nạp {count} bài đăng vào PostgreSQL."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Lỗi hệ thống: {e}"))