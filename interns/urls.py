from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InternsViewSet

# Tạo bộ định tuyến
router = DefaultRouter()

# Đăng ký ViewSet (để trống rỗng '' để có URL ngắn gọn như bạn muốn)
router.register(r'', InternsViewSet, basename='interns')

urlpatterns = [
    path('', include(router.urls)),
]