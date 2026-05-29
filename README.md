# Housing Project - API Quản Lý & Phân Tích Bất Động Sản

Dự án xây dựng hệ thống API quản lý, tìm kiếm và phân tích thông tin phòng trọ/bất động sản. Hệ thống hỗ trợ Docker hóa toàn bộ môi trường chạy thử, tích hợp Redis cache để tối ưu hóa hiệu năng, tìm kiếm Full-Text Search và quy trình CI/CD tự động kiểm thử trước khi deploy lên Render.

## Công nghệ sử dụng
* **Backend:** Django & Django REST Framework
* **Database:** PostgreSQL
* **Caching:** Redis
* **Môi trường:** Docker & Docker Compose
* **CI/CD:** GitHub Actions & Render Deploy Hook
* **Web Server (Production):** Gunicorn & WhiteNoise

---

## Hướng dẫn chạy dự án dưới Local (Docker)

Để chạy thử nghiệm hoặc demo dự án dưới máy cá nhân, bạn cần cài đặt sẵn Docker và Docker Desktop.

### 1. Khởi động các container
Mở terminal tại thư mục dự án và chạy:
```bash
docker-compose up --build
```
Lệnh này sẽ tự động khởi dựng 3 container: Web (Django), Database (PostgreSQL 16) và Cache (Redis 7).
* API chính sẽ truy cập được tại: `http://localhost:8000/api/`

### 2. Tạo tài khoản Admin (Superuser)
Chạy lệnh sau trong một terminal mới để tạo tài khoản đăng nhập trang quản trị:
```bash
docker-compose exec web python manage.py createsuperuser
```
Sau đó nhập username, email và password theo hướng dẫn trên màn hình.

### 3. Chạy Unit Test & Đo độ bao phủ (Coverage)
Chạy bộ test và kiểm tra độ bao phủ của code ngay trong môi trường Docker:
```bash
docker-compose exec web coverage run manage.py test properties
docker-compose exec web coverage report -m
```

---

## Các API Endpoints chính

| Endpoint | Chức năng | Tham số bộ lọc |
| :--- | :--- | :--- |
| `/api/properties/` | Lấy danh sách hoặc tạo bài đăng mới | `?min_price=`, `?max_price=`, `?search=` |
| `/api/properties/map_data/` | Lấy tọa độ phục vụ vẽ bản đồ (dữ liệu gọn nhẹ) | `?in_bbox=min_lon,min_lat,max_lon,max_lat` |
| `/api/properties/export_excel/` | Xuất toàn bộ danh sách phòng ra file Excel | Không |
| `/api/properties/stats/` | Xem thống kê giá cả, diện tích (có cache Redis) | Không |
| `/admin/` | Trang quản trị hệ thống của Django | Không |

* **Đường dẫn production chạy thực tế:** `https://baitappython-web.onrender.com/api/`

---

## Các điểm nhấn kỹ thuật trong dự án

* **Tối ưu hóa SQL (Chống lỗi N+1):** Áp dụng `select_related` cho các quan hệ khóa ngoại (Category, District, Ward) và `prefetch_related` cho quan hệ ManyToMany (Amenities) / ảnh ngược (Images). Đảm bảo API lấy danh sách bài đăng chỉ thực hiện đúng 3 truy vấn SQL bất kể số lượng bài đăng tăng lên bao nhiêu.
* **Full-Text Search:** Sử dụng `SearchVector` của PostgreSQL để hỗ trợ tìm kiếm không dấu/có dấu nâng cao trên các trường tiêu đề, địa chỉ và mô tả.
* **Redis Caching:** Lưu trữ kết quả thống kê nặng (`/api/properties/stats/`) vào bộ nhớ cache của Redis với thời gian timeout 5 phút, giúp giảm thời gian phản hồi từ 500ms xuống còn vài mili-giây.
* **Quy trình CI/CD khép kín:** 
  1. Khi push code lên nhánh `nguyen_day14`, GitHub Actions sẽ tự khởi động một container PostgreSQL để chạy toàn bộ 43 bài Unit Test.
  2. Nếu test PASS, GitHub Actions sẽ kích hoạt Render Deploy Hook để cập nhật code lên server thật. Nếu test FAIL, quá trình deploy sẽ bị hủy bỏ ngay lập tức để bảo vệ hệ thống.
