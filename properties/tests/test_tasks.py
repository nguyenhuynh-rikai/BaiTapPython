from unittest.mock import patch
from django.test import TestCase
from properties.tasks import BackgroundTaskManager
import time

class TasksTests(TestCase):
    def setUp(self):
        self.manager = BackgroundTaskManager()

    @patch('properties.tasks.PropertyImportService')
    def test_start_import_properties(self, MockService):
        mock_instance = MockService.return_value
        mock_instance.import_data.return_value = {"created": 10, "updated": 5, "skipped": 2}
        
        task = self.manager.start_import_properties("dummy.csv")
        self.assertIn("id", task)
        self.assertIn(task["status"], ["queued", "running", "success"])
        self.assertEqual(task["csv_path"], "dummy.csv")
        
        # Allow thread to execute
        time.sleep(0.1)
        
        updated_task = self.manager.get_task(task["id"])
        self.assertEqual(updated_task["status"], "success")
        self.assertEqual(updated_task["result"], {"created": 10, "updated": 5, "skipped": 2})

    @patch('properties.tasks.PropertyImportService')
    def test_start_import_properties_failure(self, MockService):
        mock_instance = MockService.return_value
        mock_instance.import_data.side_effect = Exception("Test error")
        
        task = self.manager.start_import_properties("dummy.csv")
        
        time.sleep(0.1)
        
        updated_task = self.manager.get_task(task["id"])
        self.assertEqual(updated_task["status"], "failed")
        self.assertEqual(updated_task["error"], "Test error")

    def test_list_tasks(self):
        task1 = self.manager.start_import_properties("dummy1.csv")
        task2 = self.manager.start_import_properties("dummy2.csv")
        
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 2)
        task_ids = [t["id"] for t in tasks]
        self.assertIn(task1["id"], task_ids)
        self.assertIn(task2["id"], task_ids)

    def test_get_nonexistent_task(self):
        self.assertIsNone(self.manager.get_task("invalid_id"))
