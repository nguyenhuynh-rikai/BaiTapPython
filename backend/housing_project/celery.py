import os
from celery import Celery

# Thiết lập settings mặc định của Django cho Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'housing_project.settings')

app = Celery('housing_project')

# Đọc cấu hình Celery từ settings của Django có tiền tố "CELERY_"
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tự động quét các tasks trong tất cả các app Django được đăng ký
app.autodiscover_tasks()
