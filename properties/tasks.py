import logging
import threading
import uuid
from datetime import datetime

from django.conf import settings
from django.db import close_old_connections

from .services import PropertyImportService


logger = logging.getLogger(__name__)


class BackgroundTaskManager:
    # Class nay quan ly task chay nen bang threading.
    # Luu y: cach nay don gian de hoc/dev, khong phai giai phap production tot nhat.
    def __init__(self):
        self.tasks = {}
        self.lock = threading.Lock()

    def start_import_properties(self, csv_path=None):
        task_id = str(uuid.uuid4())
        csv_path = csv_path or settings.BASE_DIR / "data" / "rooms_cleaned.csv"

        with self.lock:
            self.tasks[task_id] = {
                "id": task_id,
                "name": "import_properties",
                "status": "queued",
                "csv_path": str(csv_path),
                "result": None,
                "error": "",
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "started_at": "",
                "finished_at": "",
            }

        thread = threading.Thread(
            target=self._run_import_properties,
            args=(task_id, str(csv_path)),
            daemon=True,
        )
        thread.start()

        return self.get_task(task_id)

    def _run_import_properties(self, task_id, csv_path):
        self._update_task(task_id, status="running", started_at=datetime.now().isoformat(timespec="seconds"))

        try:
            # Moi thread nen dong connection cu de Django mo connection DB phu hop voi thread moi.
            close_old_connections()

            service = PropertyImportService(csv_path)
            result = service.import_data()

            self._update_task(
                task_id,
                status="success",
                result=result,
                finished_at=datetime.now().isoformat(timespec="seconds"),
            )
            logger.info("Background task %s finished successfully", task_id)
        except Exception as exc:
            logger.exception("Background task %s failed", task_id)
            self._update_task(
                task_id,
                status="failed",
                error=str(exc),
                finished_at=datetime.now().isoformat(timespec="seconds"),
            )
        finally:
            close_old_connections()

    def _update_task(self, task_id, **values):
        with self.lock:
            task = self.tasks.get(task_id)

            if task is None:
                return

            task.update(values)

    def get_task(self, task_id):
        with self.lock:
            task = self.tasks.get(task_id)

            if task is None:
                return None

            return task.copy()

    def list_tasks(self):
        with self.lock:
            return [task.copy() for task in self.tasks.values()]


task_manager = BackgroundTaskManager()
