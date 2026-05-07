from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student, StudentCard

@receiver(post_save, sender=Student)
def create_student(sender, instance, created, **kwargs):
    if created:
        StudentCard.objects.create(student=instance)
        print(f"Đã tự động tạo thẻ cho {instance.name}")