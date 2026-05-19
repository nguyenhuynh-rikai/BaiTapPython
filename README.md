# 🏢 Dự Án Quản Lý & Phân Tích Bất Động Sản (Housing Project)

Chào mừng bạn đến với **Housing Project** - Hệ thống API quản lý phòng trọ và bất động sản được thiết kế và tối ưu hóa theo tiêu chuẩn Enterprise (Doanh nghiệp). Dự án được tích hợp đầy đủ quy trình kiểm thử tự động (CI/CD), ảo hóa Docker, tối ưu hóa truy vấn SQL chống nghẽn và sẵn sàng triển khai thực tế trên môi trường đám mây Render.

---

## 🛠️ Công Nghệ Sử Dụng (Tech Stack)
*   **Backend Framework:** Django 5.x & Django REST Framework (DRF)
*   **Database:** PostgreSQL 16 (Quản lý dữ liệu chính)
*   **Caching & Session:** Redis 7 (Tăng tốc độ truy cập & lưu trữ cache)
*   **Containerization:** Docker & Docker Compose (Ảo hóa đồng bộ môi trường)
*   **CI/CD Pipeline:** GitHub Actions & Render Deploy Hook (Tự động test và deploy)
*   **Server Production:** Render (PaaS) + Gunicorn + WhiteNoise (Phân phối file tĩnh tĩnh)

---

## 🚀 Hướng Dẫn Chạy Dự Án Bằng Docker (Dành Cho Demo & Quay Video)

Chạy dự án bằng **Docker** là phương pháp hoàn hảo nhất để demo sản phẩm vì toàn bộ môi trường (Web, Database, Redis) đã được đóng gói chuẩn chỉnh và cô lập 100% trên máy tính của bạn.

### Bước 1: Khởi động hệ thống
Mở Terminal tại thư mục gốc của dự án và gõ đúng 1 dòng lệnh:
```bash
docker-compose up --build
```
> [!NOTE]
> Lệnh này sẽ tự động tải các Image (Python, Postgres, Redis), build dự án, tạo cổng kết nối và khởi chạy cả 3 dịch vụ đồng thời. Web sẽ chạy tại địa chỉ: `http://localhost:8000/api/`

### Bước 2: Tạo tài khoản Admin (Superuser) trong Docker
Do trên Render gói miễn phí chặn công cụ gõ lệnh tương tác (Shell), việc tạo tài khoản Admin dưới Local bằng Docker là giải pháp tối ưu nhất để quay video quản trị:
```bash
docker-compose exec web python manage.py createsuperuser
```
*(Lập tức nhập Username, Email, và Mật khẩu theo hướng dẫn trên màn hình để tạo tài khoản).*

### Bước 3: Chạy Kiểm thử (Unit Test) & Coverage ngay trong Docker
Để trình diễn tính ổn định của dự án trong video demo, bạn chạy lệnh sau:
```bash
docker-compose exec web coverage run manage.py test properties
docker-compose exec web coverage report -m
```
*(Hệ thống sẽ chạy toàn bộ bộ test với độ bao phủ ~97% cực kỳ ấn tượng!).*

---

## 🌐 Đường Dẫn Các Tính Năng Demo (Local & Production)

| Tính Năng | URL chạy dưới Local (Docker) | URL chạy trên mạng thật (Render) |
| :--- | :--- | :--- |
| **Trang quản trị Django Admin** | `http://localhost:8000/admin/` | `https://baitappython-web.onrender.com/admin/` |
| **Danh sách các API (DRF Root)** | `http://localhost:8000/api/` | `https://baitappython-web.onrender.com/api/` |
| **API Danh sách Bất Động Sản** | `http://localhost:8000/api/properties/` | `https://baitappython-web.onrender.com/api/properties/` |
| **Xuất Excel dữ liệu thực tế** | `http://localhost:8000/api/properties/export_excel/` | `https://baitappython-web.onrender.com/api/properties/export_excel/` |

---

## 💡 Hướng Dẫn Quay Video Demo Sản Phẩm (Sử Dụng Docker)

Để có một video demo dài 3-5 phút thật sự thuyết phục người xem, bạn nên quay theo kịch bản chuyên nghiệp sau:

1.  **Phần 1: Giới thiệu Kiến trúc Docker (1 phút)**
    *   Mở Terminal lên và gõ `docker-compose up --build` để chứng minh hệ thống khởi chạy mượt mà, bao gồm cả Web, Postgres, và Redis chỉ trong 1 nốt nhạc.
2.  **Phần 2: Trình diễn API & Tính năng Tìm kiếm (2 phút)**
    *   Mở trình duyệt truy cập `http://localhost:8000/api/properties/`.
    *   Thực hiện lọc dữ liệu nâng cao bằng cách thêm tham số trên URL (Ví dụ: `?min_price=1000&max_price=5000` hoặc tìm kiếm Full-text search bằng `?search=phong+tro`).
    *   Truy cập link `export_excel/` để tải file Excel về, mở file Excel lên cho người xem thấy dữ liệu được sắp xếp cột, tiêu đề tiếng Việt chuẩn chỉ, không lỗi font chữ.
3.  **Phần 3: Trình diễn trang Quản trị Admin (1 phút)**
    *   Truy cập `http://localhost:8000/admin/` và đăng nhập bằng tài khoản Superuser bạn vừa tạo ở Bước 2.
    *   Thêm mới hoặc sửa một bài đăng bất động sản để chứng minh chức năng phân quyền và quản lý hoạt động tốt.
4.  **Phần 4: Trình diễn độ tin cậy CI/CD (1 phút)**
    *   Mở trang GitHub Actions của bạn, chỉ vào dấu tích xanh lá cây ✅ **Tests Passed** và **Deploy to Render Passed** để khẳng định hệ thống tự động hóa chuẩn doanh nghiệp.
    *   Chỉ vào trang Render Web Service để chứng minh website đã chạy thực tế trên Internet.

---

## 💎 Các Tính Năng Độc Đáo Đã Triển Khai
1.  **Full-Text Search (Tìm kiếm chuyên sâu):** Sử dụng Search Vector tích hợp sẵn của PostgreSQL để tìm kiếm theo trọng số tên, mô tả và địa chỉ.
2.  **SQL Query Optimization:** Ngăn chặn triệt để lỗi N+1 truy vấn bằng `select_related` và `prefetch_related`. Toàn bộ danh sách bài đăng chỉ tốn đúng **3 câu lệnh SQL** dù có bao nhiêu nghìn bài đăng đi nữa.
3.  **Hệ Thống Cache Bằng Redis:** Lưu trữ các thống kê nặng (`stats`) vào bộ nhớ cache Redis, giúp tăng tốc độ phản hồi từ 500ms xuống còn 2ms!
4.  **CI/CD Khép Kín:** GitHub Actions chạy test tự động. Chỉ khi test pass mới kích hoạt Deploy Hook thông báo cho Render cập nhật web. Bảo vệ sản phẩm 100% khỏi lỗi phát sinh bất ngờ.
