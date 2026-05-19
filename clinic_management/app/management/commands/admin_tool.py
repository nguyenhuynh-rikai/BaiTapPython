import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from app.models import Clinic, Doctor, Patient, Appointment, TimeSlot, Drug
from django.utils import timezone
from datetime import timedelta
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'CLI Admin Tool để quản trị hệ thống nhanh'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action', 
            type=str, 
            choices=['stats', 'clear_data', 'create_admin', 'cancel_stale_appointments', 'interactive'],
            default='interactive',
            help='Hành động cần thực hiện'
        )

    def handle(self, *args, **options):
        action = options['action']

        if action == 'interactive':
            self.run_interactive()
        elif action == 'stats':
            self.show_stats()
        elif action == 'clear_data':
            self.clear_data()
        elif action == 'create_admin':
            self.create_admin()
        elif action == 'cancel_stale_appointments':
            self.cancel_stale_appointments()

    def run_interactive(self):
        self.stdout.write(self.style.SUCCESS('=== CLI ADMIN TOOL - CLINIC MANAGEMENT ===\n'))
        while True:
            self.stdout.write("Chọn một hành động:")
            self.stdout.write("1. Xem thống kê hệ thống (stats)")
            self.stdout.write("2. Tạo tài khoản Admin (create_admin)")
            self.stdout.write("3. Hủy các lịch hẹn chờ lâu (cancel_stale_appointments)")
            self.stdout.write("4. Xóa dữ liệu rác/test (clear_data)")
            self.stdout.write("0. Thoát")
            
            choice = input("\nNhập lựa chọn (0-4): ").strip()
            
            if choice == '1':
                self.show_stats()
            elif choice == '2':
                self.create_admin()
            elif choice == '3':
                self.cancel_stale_appointments()
            elif choice == '4':
                self.clear_data()
            elif choice == '0':
                self.stdout.write(self.style.SUCCESS("Đã thoát CLI Admin Tool."))
                sys.exit(0)
            else:
                self.stdout.write(self.style.ERROR("Lựa chọn không hợp lệ. Vui lòng thử lại.\n"))
            
            self.stdout.write("-" * 40)

    def show_stats(self):
        self.stdout.write(self.style.WARNING('\n--- THỐNG KÊ HỆ THỐNG ---'))
        users = User.objects.count()
        admins = User.objects.filter(role=User.Role.ADMIN).count()
        doctors = Doctor.objects.count()
        patients = Patient.objects.count()
        clinics = Clinic.objects.count()
        appointments = Appointment.objects.count()
        drugs = Drug.objects.count()

        self.stdout.write(f"- Users tổng cộng: {users} (Admin: {admins})")
        self.stdout.write(f"- Bác sĩ: {doctors}")
        self.stdout.write(f"- Bệnh nhân: {patients}")
        self.stdout.write(f"- Phòng khám: {clinics}")
        self.stdout.write(f"- Lịch hẹn: {appointments}")
        self.stdout.write(f"- Loại thuốc: {drugs}\n")

    def create_admin(self):
        self.stdout.write(self.style.WARNING('\n--- TẠO ADMIN TÀI KHOẢN ---'))
        email = input("Nhập email admin: ").strip()
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f"Email {email} đã tồn tại!"))
            return

        password = input("Nhập password (mặc định 'Admin@123'): ").strip()
        if not password:
            password = 'Admin@123'
            
        full_name = input("Nhập tên admin (mặc định 'System Admin'): ").strip()
        if not full_name:
            full_name = 'System Admin'

        try:
            User.objects.create_superuser(email=email, password=password, full_name=full_name)
            self.stdout.write(self.style.SUCCESS(f"Đã tạo thành công admin với email: {email}\n"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Lỗi khi tạo admin: {e}\n"))

    def cancel_stale_appointments(self):
        self.stdout.write(self.style.WARNING('\n--- HỦY LỊCH HẸN TREO ---'))
        try:
            hours_str = input("Nhập số giờ tối đa cho phép ở trạng thái 'pending' (mặc định 24): ").strip()
            hours = int(hours_str) if hours_str else 24
        except ValueError:
            self.stdout.write(self.style.ERROR("Vui lòng nhập một số hợp lệ.\n"))
            return

        cutoff_time = timezone.now() - timedelta(hours=hours)
        stale_appointments = Appointment.objects.filter(
            status=Appointment.Status.PENDING,
            booked_at__lt=cutoff_time
        )
        count = stale_appointments.count()
        
        if count == 0:
            self.stdout.write(f"Không có lịch hẹn nào treo quá {hours} giờ.\n")
            return

        confirm = input(f"Tìm thấy {count} lịch hẹn. Bạn có chắc muốn hủy? (y/n): ").strip().lower()
        if confirm == 'y':
            with transaction.atomic():
                for apt in stale_appointments:
                    apt.cancel(reason="Hủy tự động qua Admin Tool")
            self.stdout.write(self.style.SUCCESS(f"Đã hủy {count} lịch hẹn.\n"))
        else:
            self.stdout.write("Đã bỏ qua thao tác hủy.\n")

    def clear_data(self):
        self.stdout.write(self.style.WARNING('\n--- XÓA DỮ LIỆU ---'))
        self.stdout.write(self.style.ERROR('CẢNH BÁO: Hành động này không thể hoàn tác!'))
        confirm = input("Gõ 'DELETE_ALL' để xác nhận xóa toàn bộ Lịch hẹn & Slot: ").strip()
        
        if confirm == 'DELETE_ALL':
            with transaction.atomic():
                ap_count, _ = Appointment.objects.all().delete()
                ts_count, _ = TimeSlot.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"Đã xóa {ap_count} lịch hẹn và {ts_count} time slot.\n"))
        else:
            self.stdout.write("Hủy thao tác xóa.\n")
