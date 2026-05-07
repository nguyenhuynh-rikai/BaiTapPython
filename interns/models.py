from django.db import models

class Interns(models.Model):
    STATUS_CHOICES = [
        ('apply', 'Dang ung tuyen'),
        ('interning', 'Dang thuc tap'),
        ('completed', 'Da hoan thanh')
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    specialization = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.specialization}"