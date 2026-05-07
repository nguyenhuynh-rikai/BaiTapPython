from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudentListView.as_view(), name='student_list'),

    path('student/<slug:slug>/', views.StudentDetailView.as_view(), name='student_detail'),
]