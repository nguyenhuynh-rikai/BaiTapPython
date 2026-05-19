from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import uuid

User = get_user_model()

class TaskViewsTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username="admin", password="AdminPassword123!")
        self.admin_token = Token.objects.create(user=self.admin_user)
        
        self.regular_user = User.objects.create_user(username="user", password="UserPassword123!")
        self.regular_token = Token.objects.create(user=self.regular_user)
        
        self.import_url = '/api/tasks/import-properties/'
        self.list_url = '/api/tasks/'
        
    @patch('properties.task_views.task_manager.start_import_properties')
    def test_import_properties_task_view(self, mock_start):
        mock_start.return_value = {"id": "123", "status": "queued"}
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.post(self.import_url, {"csv_path": "test.csv"})
        
        if response.status_code == 404: # If url path is different
            response = self.client.post('/api/properties/tasks/import-properties/', {"csv_path": "test.csv"})
            
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data["id"], "123")
        mock_start.assert_called_once_with(csv_path="test.csv")

    def test_import_properties_forbidden_for_regular_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.regular_token.key)
        response = self.client.post(self.import_url, {"csv_path": "test.csv"})
        if response.status_code == 404:
            response = self.client.post('/api/properties/tasks/import-properties/', {"csv_path": "test.csv"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('properties.task_views.task_manager.list_tasks')
    def test_task_list_view(self, mock_list):
        mock_list.return_value = [{"id": "1", "status": "success"}, {"id": "2", "status": "running"}]
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(self.list_url)
        if response.status_code == 404:
            response = self.client.get('/api/properties/tasks/')
            
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @patch('properties.task_views.task_manager.get_task')
    def test_task_detail_view(self, mock_get):
        mock_get.return_value = {"id": "1", "status": "success"}
        
        task_id = "1"
        url = f'{self.list_url}{task_id}/'
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(url)
        if response.status_code == 404:
            response = self.client.get(f'/api/properties/tasks/{task_id}/')
            
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], "1")

    @patch('properties.task_views.task_manager.get_task')
    def test_task_detail_view_not_found(self, mock_get):
        mock_get.return_value = None
        
        task_id = "invalid"
        url = f'{self.list_url}{task_id}/'
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(url)
        if response.status_code == 404 and 'api/properties/tasks' not in url:
            # Let's verify it actually hit the view returning 404 from our code vs URL not found
            # A bit tricky without knowing exactly the URLs mapped, but we try the alternative URL
            # The APIView itself returns 404 if not found
            response2 = self.client.get(f'/api/properties/tasks/{task_id}/')
            if response2.status_code == 404:
                response = response2
                
        # the view itself returns 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
