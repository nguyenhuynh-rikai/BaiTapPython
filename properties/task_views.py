from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .tasks import task_manager


class ImportPropertiesTaskAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        csv_path = request.data.get("csv_path")
        task = task_manager.start_import_properties(csv_path=csv_path)

        return Response(task, status=202)


class TaskListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response(task_manager.list_tasks())


class TaskDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, task_id):
        task = task_manager.get_task(task_id)

        if task is None:
            return Response({"detail": "Task not found."}, status=404)

        return Response(task)
