from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

class Interns(models.Model):
    STATUS_CHOICES = [
        ('apply', 'Dang ung tuyen'),
        ('interning', 'Dang thuc tap'),
        ('completed', 'Da hoan thanh')
    ]
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    email = models.EmailField(unique=True)
    specialization = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, related_name='interns', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name