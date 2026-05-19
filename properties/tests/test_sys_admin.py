from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model
from properties.models import Property, District, Category

User = get_user_model()

class SysAdminCommandTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@test.com", password="pwd")
        
        self.district = District.objects.create(name="Test District")
        self.category = Category.objects.create(name="Test Cat", slug="test-cat")
        
        # Valid property
        Property.objects.create(
            title="Valid Property", source_url="http://valid.com", price=1000, area=50, 
            district=self.district, category=self.category,
            is_active=True
        )
        # Invalid properties (trash)
        Property.objects.create(
            title="", source_url="http://trash1.com", price=1000, area=50, 
            district=self.district, category=self.category,
            is_active=True
        )
        Property.objects.create(
            title="Invalid Price", source_url="http://trash2.com", price=0, area=50, 
            district=self.district, category=self.category,
            is_active=True
        )

    def test_sys_admin_stats(self):
        out = StringIO()
        call_command('sys_admin', 'stats', stdout=out)
        output = out.getvalue()
        
        self.assertIn("--- THỐNG KÊ HỆ THỐNG ---", output)
        self.assertIn("Tổng số bài đăng: 3", output)
        self.assertIn("Tổng số người dùng: 1", output)

    def test_sys_admin_clean(self):
        out = StringIO()
        call_command('sys_admin', 'clean', stdout=out)
        output = out.getvalue()
        
        self.assertIn("Đã dọn dẹp 2 bài đăng lỗi.", output)
        self.assertEqual(Property.objects.count(), 1)
        self.assertEqual(Property.objects.first().title, "Valid Property")

    def test_sys_admin_promote_success(self):
        out = StringIO()
        call_command('sys_admin', 'promote', 'test@test.com', stdout=out)
        output = out.getvalue()
        
        self.assertIn("đã trở thành Admin.", output)
        
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_superuser)

    def test_sys_admin_promote_not_found(self):
        out = StringIO()
        call_command('sys_admin', 'promote', 'notfound@test.com', stdout=out)
        output = out.getvalue()
        
        self.assertIn("Không tìm thấy người dùng", output)
