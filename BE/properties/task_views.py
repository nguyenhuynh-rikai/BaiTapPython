from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .tasks import task_manager
from .serializers import ImportPropertiesSerializer


@extend_schema(tags=["System Administration"])
class ImportPropertiesTaskAPIView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = ImportPropertiesSerializer

    def post(self, request):
        csv_path = request.data.get("csv_path")
        task = task_manager.start_import_properties(csv_path=csv_path)

        return Response(task, status=202)


@extend_schema(tags=["System Administration"])
class TaskListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response(task_manager.list_tasks())


@extend_schema(tags=["System Administration"])
class TaskDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, task_id):
        task = task_manager.get_task(task_id)

        if task is None:
            return Response({"detail": "Task not found."}, status=404)

        return Response(task)

