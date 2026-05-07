from rest_framework import viewsets
from .models import Interns
from .serializers import InternSerializer

class InternsViewSet(viewsets.ModelViewSet):
    """
    Một mình Class này sẽ cân hết:
    - GET /interns/ -> Lấy danh sách
    - POST /interns/ -> Thêm mới
    - GET /interns/{id}/ -> Xem chi tiết 1 người
    - PUT /interns/{id}/ -> Sửa toàn bộ
    - PATCH /interns/{id}/ -> Sửa một phần
    - DELETE /interns/{id}/ -> Xóa
    """
    queryset = Interns.objects.all()
    serializer_class = InternSerializer