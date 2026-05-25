from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from properties.models import Property, PropertyImage
from django.db.models import Count

User = get_user_model()

class Command(BaseCommand):

    def add_arguments(self, parser):
        # Tạo các "lệnh con" (subcommands)
        subparsers = parser.add_subparsers(dest='action', help='Hành động cần thực hiện')

        # Subcommand: stats
        subparsers.add_parser('stats', help='Xem thống kê hệ thống')

        # Subcommand: clean
        subparsers.add_parser('clean', help='Dọn dẹp dữ liệu rác')

        # Subcommand: promote
        promote_parser = subparsers.add_parser('promote', help='Nâng cấp user thành Admin')
        promote_parser.add_argument('email', type=str, help='Email của user cần nâng cấp')

    def handle(self, *args, **kwargs):
        action = kwargs['action']

        if action == 'stats':
            self.show_stats()
        elif action == 'clean':
            self.clean_data()
        elif action == 'promote':
            self.promote_user(kwargs['email'])
        else:
            self.print_help()

    def show_stats(self):
        self.stdout.write(self.style.SUCCESS("--- THỐNG KÊ HỆ THỐNG ---"))
        total_p = Property.objects.count()
        active_p = Property.objects.filter(is_active=True).count()
        total_u = User.objects.count()

        # Thống kê theo Quận
        districts = Property.objects.values('district__name').annotate(count=Count('id')).order_by('-count')[:5]

        self.stdout.write(f"Tổng số bài đăng: {total_p} ({active_p} đang hiển thị)")
        self.stdout.write(f"Tổng số người dùng: {total_u}")
        self.stdout.write("Top 5 khu vực nhiều phòng nhất:")
        for d in districts:
            self.stdout.write(f" - {d['district__name']}: {d['count']} bài")

    def clean_data(self):
        self.stdout.write(self.style.WARNING("Đang quét dữ liệu rác..."))
        # Xóa các bài không có tiêu đề hoặc giá = 0
        trash = Property.objects.filter(price=0) | Property.objects.filter(title="")
        count = trash.count()
        trash.delete()
        self.stdout.write(self.style.SUCCESS(f"Đã dọn dẹp {count} bài đăng lỗi."))

    def promote_user(self, email):
        try:
            user = User.objects.get(email=email)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Chúc mừng! {email} đã trở thành Admin."))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Không tìm thấy người dùng có email: {email}"))