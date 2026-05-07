from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f'Profile của {self.user.username}'