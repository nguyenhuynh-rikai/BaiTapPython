from rest_framework import viewsets, permissions
from .models import Interns
from .serializers import InternSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters # Import thêm filters

class InternsViewSet(viewsets.ModelViewSet):
    queryset = Interns.objects.all()
    serializer_class = InternSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['specialization', 'status']  # Cho phép lọc theo chuyên ngành và trạng thái
    filterset_fields = ['specialization', 'status']

    search_fields = ['name', 'email']

    ordering_fields = ['name', 'id']
    ordering = ['id']  # Sắp xếp mặc định theo ID

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]  # Chỉ Admin/Staff mới được POST/PUT/DELETE

        return [permission() for permission in permission_classes]