from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_world, name='hello'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('create_post/', views.create_post, name='create_post'),
    # path('post_detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]