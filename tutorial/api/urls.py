from django.urls import path
from .views import post_list
from .views import create_post
from .views import profile

urlpatterns = [
    # path('posts/', post_list),
    # path('posts/create/', create_post),
    path('profile/', profile),
]
