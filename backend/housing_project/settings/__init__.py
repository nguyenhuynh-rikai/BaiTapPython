import os
from dotenv import load_dotenv
from pathlib import Path

# Xác định thư mục gốc của dự án
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / '.env')

# Đọc môi trường chạy (mặc định là development)
ENV = os.getenv('DJANGO_ENV', 'development')

if ENV == 'production':
    from .production import *
else:
    from .development import *
