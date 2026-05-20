import logging
import threading
import uuid
from datetime import datetime

from django.conf import settings
from celery import shared_task
from celery.result import AsyncResult

from .services import PropertyImportService

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def import_properties_task(self, csv_path):
    """Celery task để import dữ liệu phòng trọ từ CSV chạy nền"""
    logger.info("Celery task %s started with path %s", self.request.id, csv_path)
    service = PropertyImportService(csv_path)
    result = service.import_data()
    logger.info("Celery task %s finished successfully", self.request.id)
    return result


class BackgroundTaskManager:
    # Class này làm nhiệm vụ bọc (Wrapper) ngoài Celery
    # Giúp giữ nguyên giao diện gọi API /api/tasks/ và không phải sửa đổi Views/Tests
    def __init__(self):
        self.tasks = {}
        self.lock = threading.Lock()

    def start_import_properties(self, csv_path=None):
        csv_path = csv_path or settings.BASE_DIR / "data" / "rooms_cleaned.csv"

        # Gọi Celery task chạy ngầm dưới nền
        celery_task = import_properties_task.delay(str(csv_path))  # type: ignore
        task_id = celery_task.id

        with self.lock:
            self.tasks[task_id] = {
                "id": task_id,
                "name": "import_properties",
                "csv_path": str(csv_path),
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "result_obj": celery_task,
            }

        return self.get_task(task_id)

    def get_task(self, task_id):
        with self.lock:
            task_meta = self.tasks.get(task_id)
            if task_meta is None:
                return None

            # Sử dụng trực tiếp đối tượng kết quả (có thể là EagerResult trong dev/test hoặc AsyncResult)
            res = task_meta["result_obj"]

            try:
                status_raw = res.status
                result_raw = res.result
            except Exception as exc:
                # Fallback nếu mất kết nối tới Redis backend ở môi trường không có Redis
                logger.warning("Could not connect to Redis to get task status, fallback to queued. Error: %s", exc)
                status_raw = "PENDING"
                result_raw = None

            status_map = {
                "PENDING": "queued",
                "STARTED": "running",
                "RETRY": "running",
                "SUCCESS": "success",
                "FAILURE": "failed",
            }
            status = status_map.get(status_raw, "queued")

            error_msg = ""
            if status == "failed":
                error_msg = str(result_raw) if result_raw else "Unknown error"

            task = task_meta.copy()
            # Loại bỏ result_obj trước khi trả về dữ liệu thuần túy cho API/views
            task.pop("result_obj", None)
            task.update({
                "status": status,
                "result": result_raw if status == "success" else None,
                "error": error_msg,
                "started_at": task_meta["created_at"] if status in ["running", "success", "failed"] else "",
                "finished_at": datetime.now().isoformat(timespec="seconds") if status in ["success", "failed"] else "",
            })
            return task

    def list_tasks(self):
        with self.lock:
            # Cập nhật thông tin mới nhất cho toàn bộ danh sách task từ Celery
            return [self.get_task(tid) for tid in self.tasks.keys()]


task_manager = BackgroundTaskManager()
