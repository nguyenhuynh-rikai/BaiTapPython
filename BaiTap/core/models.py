from django.db import models
from django.utils.text import slugify

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    # Thêm trường slug, unique=True để không bao giờ có 2 người trùng link
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Nếu chưa có slug, tự động tạo từ tên
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class StudentCard(models.Model):
    # Dùng OneToOneField vì 1 Sinh viên chỉ có 1 Thẻ, và 1 Thẻ chỉ thuộc về 1 Sinh viên
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=20, default="CHUA_CAP_SO")
    issue_date = models.DateField(auto_now_add=True)  # Tự động lấy ngày hôm nay

    def __str__(self):
        return f"Thẻ của {self.student.name}"
