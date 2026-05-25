# Sử dụng Python image chính thức làm nền tảng
FROM python:3.13-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Thiết lập các biến môi trường cho Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cài đặt các công cụ biên dịch cơ bản (cần thiết cho một số thư viện C của pandas/numpy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Sao chép và cài đặt các thư viện Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn dự án vào container
COPY . /app/

# Port mà Django sẽ chạy bên trong container
EXPOSE 8000

# Lệnh khởi chạy ứng dụng mặc định
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
