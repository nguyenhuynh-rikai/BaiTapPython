from django.urls import path
from .views import post_list

urlpatterns = [
    path('posts/', post_list),
]