# MediFlow - Clinic Management System

MediFlow là một hệ thống quản lý phòng khám (Clinic Management System) được phát triển bằng **Django** và **Django REST Framework (DRF)**. Hệ thống cung cấp các API quản lý thông tin phòng khám, bác sĩ, lịch hẹn (appointments), danh mục thuốc (drugs), thanh toán (payments) và nhiều tính năng tối ưu cho production.

Hệ thống đã được container hóa hoàn toàn bằng Docker và cấu hình CI/CD tự động deploy lên Render.com.

---

## 🛠️ Công nghệ sử dụng (Tech Stack)

- **Backend**: Django 6.0.5 + Django REST Framework (DRF)
- **Database**: PostgreSQL (Quản lý dữ liệu chính)
- **Caching**: Redis (Cache cho các truy vấn hiệu năng cao)
- **Static Files**: WhiteNoise (Phục vụ file tĩnh tối ưu trên production)
- **API Documentation**: `drf-spectacular` (Swagger UI & ReDoc)
- **DevOps**: Docker & Docker Compose
- **CI/CD**: GitHub Actions (Tự động test và trigger deploy lên Render.com)

---

## ✨ Tính năng chính

- **Xác thực & Người dùng**: Đăng ký, đăng nhập JWT, đổi mật khẩu, xem thông tin cá nhân.
- **Quản lý phòng khám (Clinics)**: Thêm, sửa, xóa, tìm kiếm phòng khám.
- **Quản lý bác sĩ (Doctors)**: Quản lý thông tin bác sĩ, lịch làm việc.
- **Đặt lịch hẹn (Appointments)**: Tìm kiếm các khung giờ trống (slots), đặt lịch hẹn cho bệnh nhân.
- **Quản lý thuốc (Drugs)**: Danh mục thuốc, xuất dữ liệu thuốc ra định dạng Excel (XLSX) và PDF.
- **Thanh toán (Payments)**: Quản lý hóa đơn và trạng thái thanh toán.
- **Tài liệu API tự động**: Tích hợp Swagger UI giúp test API trực quan.

---

## 🚀 Hướng dẫn chạy dự án trên máy cá nhân (Local)

### Cách 1: Sử dụng Docker & Docker Compose (Khuyên dùng)

Đảm bảo bạn đã cài đặt Docker và Docker Compose trên máy tính.

1. **Khởi động các dịch vụ (Django Web, PostgreSQL, Redis)**:
   ```bash
   docker-compose up -d --build
   ```
2. **Kiểm tra trạng thái container**:
   ```bash
   docker-compose ps
   ```
3. **Truy cập ứng dụng**:
   - API chính: `http://localhost:8000/api/`
   - Tài liệu API (Swagger UI): `http://localhost:8000/api/docs/`
   - Giao diện Admin: `http://localhost:8000/admin/`

---

### Cách 2: Chạy trực tiếp (Không dùng Docker)

Yêu cầu máy có cài sẵn **Python 3.13+**, **PostgreSQL** và **Redis**.

1. **Tạo và kích hoạt môi trường ảo**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```
2. **Cài đặt thư viện**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Cấu hình môi trường**:
   Tạo file `.env` tại thư mục gốc và cấu hình các biến sau:
   ```env
   DB_NAME=clinicdb
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=127.0.0.1
   DB_PORT=5432
   REDIS_URL=redis://127.0.0.1:6379/1
   ```
4. **Chạy Migrations & Gom file tĩnh**:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
5. **Chạy server**:
   ```bash
   python manage.py runserver
   ```

---

## 🧪 Chạy Unit Tests

Dự án đi kèm với bộ test case đầy đủ (>36 tests) để kiểm tra các luồng API:

* Chạy test bằng công cụ `pytest` có sẵn:
  ```bash
  pytest
  # Hoặc dùng manage.py:
  python manage.py test
  ```

---

## 🌐 Triển khai lên Production (Render.com)

Dự án được cấu hình sẵn cơ sở hạ tầng dạng Code (Infrastructure as Code) qua file `render.yaml`. Khi liên kết Repo với Render, hệ thống sẽ tự động tạo:
- **Web Service**: Chạy ứng dụng Django sử dụng Gunicorn và WhiteNoise.
- **PostgreSQL Database**: Lưu trữ dữ liệu.
- **Redis Instance**: Dành cho tính năng Caching.

### Cấu hình biến môi trường (Environment Variables) trên Render:
- `DJANGO_SETTINGS_MODULE`: `clinic_management.settings.production`
- `ALLOWED_HOSTS`: Tên miền Render của bạn (hoặc `*`)
- `SECRET_KEY`: Khóa bảo mật ngẫu nhiên của Django.
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`: Được Render tự động liên kết qua Blueprint.
