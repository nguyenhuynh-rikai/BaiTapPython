# Kế Hoạch Triển Khai: Chuẩn Hóa Trạng Thái Kiểm Duyệt Phòng Trọ (Chờ Duyệt, Đã Duyệt, Từ Chối)

Tài liệu này vạch ra kế hoạch sửa lỗi logic kiểm duyệt phòng trọ. Hiện tại, khi tạo phòng trọ mới, phòng trọ tự động hiển thị và được duyệt luôn do `is_active` mặc định bằng `True`. Khi Admin từ chối tin, phòng trọ cũng không chuyển sang trạng thái "Từ chối" mà vẫn hiển thị là "Chờ kiểm duyệt" do thiếu trường `status` ở phía Backend.

Chúng ta sẽ bổ sung trường `status` (pending, approved, rejected) ở Backend và đồng bộ hóa toàn diện với Frontend.

## 1. Mục Tiêu Thực Hiện

1. **Backend Django (Cơ Sở Dữ Liệu)**:
   - Thay đổi giá trị mặc định của `is_active` trong model `Property` thành `False`.
   - Thêm trường `status` vào model `Property` với 3 trạng thái: `pending` (Chờ duyệt - mặc định), `approved` (Đã duyệt), `rejected` (Từ chối).
   - Đảm bảo các script import dữ liệu (`import_csv.py` và `services.py`) luôn đặt trực tiếp `is_active=True` và `status="approved"` để các tin đăng mẫu từ CSV hiển thị ngay lập tức.
   - Thêm trường `status` vào `PropertySerializer` để trả về cho Frontend và cho phép chỉnh sửa qua API PATCH.
   - Tạo và chạy tệp Migration trong Docker Postgres DB.

2. **Frontend React**:
   - Cập nhật hàm `mapBackendRoomToFrontend` trong [App.jsx](file:///c:/Nguyen/BaiTapPython/frontend/src/App.jsx) để map thuộc tính `status` trực tiếp từ API (`room.status`).
   - Cập nhật callback duyệt tin `handleApproveRoom` để gửi PATCH với cả `{ is_active: true, status: 'approved' }`.
   - Cập nhật callback từ chối tin `handleRejectRoom` để gửi PATCH với cả `{ is_active: false, status: 'rejected' }`.
   - Xác nhận rằng các bài đăng bị từ chối sẽ hiển thị badge màu đỏ "Từ chối (Cần sửa)" trên Dashboard chủ nhà, đồng thời biến mất khỏi danh sách chờ duyệt của Admin.

---

## 2. Chi Tiết Các Thay Đổi Dự Kiến

### 2.1 Backend Django

#### [MODIFY] [models.py](file:///c:/Nguyen/BaiTapPython/backend/properties/models.py)
- **Vị trí**: Dòng 62.
- **Hành động**: Thay đổi mặc định `is_active` thành `False` và thêm trường `status`:
  ```python
    is_active = models.BooleanField(default=False)
    STATUS_CHOICES = (
        ("pending", "Chờ duyệt"),
        ("approved", "Đã duyệt"),
        ("rejected", "Từ chối"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
  ```

#### [MODIFY] [serializers.py](file:///c:/Nguyen/BaiTapPython/backend/properties/serializers.py)
- **Vị trí**: `PropertySerializer` (khoảng dòng 53-78).
- **Hành động**: Thêm `"status"` vào danh sách `fields`.

#### [MODIFY] [import_csv.py](file:///c:/Nguyen/BaiTapPython/backend/properties/management/commands/import_csv.py)
- **Vị trí**: Dòng 102.
- **Hành động**: Thêm `'status': 'approved'` vào defaults của `update_or_create`.

#### [MODIFY] [services.py](file:///c:/Nguyen/BaiTapPython/backend/properties/services.py)
- **Vị trí**: Dòng 190.
- **Hành động**: Thêm `"status": "approved"` vào defaults của `update_or_create`.

---

### 2.2 Frontend React

#### [MODIFY] [App.jsx](file:///c:/Nguyen/BaiTapPython/frontend/src/App.jsx)
- **Vị trí**: Dòng 108.
- **Hành động**: Map trực tiếp status từ backend:
  - *Tìm*: `status: room.is_active ? 'approved' : 'pending'`
  - *Thay bằng*: `status: room.status || (room.is_active ? 'approved' : 'pending')`
- **Vị trí**: Dòng 233.
- **Hành động**: Cập nhật hàm `handleApproveRoom`:
  - *Tìm*: `await api.patch(\`/properties/\${roomId}/\`, { is_active: true });`
  - *Thay bằng*: `await api.patch(\`/properties/\${roomId}/\`, { is_active: true, status: 'approved' });`
- **Vị trí**: Dòng 244.
- **Hành động**: Cập nhật hàm `handleRejectRoom`:
  - *Tìm*: `await api.patch(\`/properties/\${roomId}/\`, { is_active: false });`
  - *Thay bằng*: `await api.patch(\`/properties/\${roomId}/\`, { is_active: false, status: 'rejected' });`

---

## 3. Kế Hoạch Chạy Migrations & Xác Minh

### Chạy lệnh Migrations trên Docker:
1. Tạo migration:
   `docker-compose exec web python manage.py makemigrations`
2. Chạy migration để cập nhật database PostgreSQL:
   `docker-compose exec web python manage.py migrate`

### Xác Minh Thủ Công (Manual Verification)
1. **Tạo Phòng Trọ Mới**: Đăng nhập tài khoản landlord, đăng phòng trọ mới. Xác nhận thông báo thành công và phòng trọ hiển thị trạng thái **"Chờ kiểm duyệt"** (màu vàng) trên Landlord Dashboard.
2. **Kiểm Tra Admin Queue**: Đăng nhập tài khoản admin. Xác nhận phòng trọ mới tạo xuất hiện trong danh sách **"📋 Kiểm Duyệt Tin Chờ"**.
3. **Từ Chối Kiểm Duyệt**: Admin bấm Từ chối phòng trọ đó. Xác nhận:
   - Phòng trọ biến mất khỏi danh sách chờ của Admin.
   - Khi quay lại Landlord Dashboard, phòng trọ đó hiển thị badge màu đỏ **"Từ chối (Cần sửa)"** chuẩn xác 100%!
4. **Duyệt Tin**: Nếu Admin bấm Duyệt, phòng trọ chuyển sang trạng thái **"Đang hiển thị"** (màu xanh) và xuất hiện ở trang chủ dành cho Tenant.
