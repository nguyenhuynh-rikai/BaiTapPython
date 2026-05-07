# core/context_processors.py
from datetime import datetime

def global_info(request):
    # Trả về một dictionary chứa các thông tin dùng chung
    return {
        'site_name': 'Hệ Thống Quản Lý Sinh Viên',
        'current_year': datetime.now().year,
        'author': 'Nhật Nguyên'
    }