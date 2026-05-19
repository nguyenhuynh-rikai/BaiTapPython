#!/bin/bash

# Dừng script nếu có bất kỳ lệnh nào bị lỗi
set -e

echo "🚀 Bắt đầu quá trình Deploy..."

# 1. Kéo code mới nhất từ nhánh chính
echo "📥 Đang lấy code mới nhất từ Github..."
git fetch origin
git pull origin main

# Di chuyển vào thư mục dự án
cd clinic_management

# 2. Xây dựng lại Image Docker và khởi động bằng Docker Compose
echo "📦 Đang build và khởi động lại hệ thống Docker..."
docker-compose down
docker-compose up -d --build

# 3. Dọn dẹp rác hệ thống Docker để giải phóng ổ cứng (tùy chọn)
echo "🧹 Đang dọn dẹp các images không còn sử dụng..."
docker image prune -f

echo "✅ Quá trình Deploy đã hoàn tất thành công!"
