import os
import tempfile
import pandas as pd
from io import StringIO
from unittest.mock import patch
from django.core.management import call_command
from django.test import TestCase
from properties.models import Property, District, Ward, Category

class ImportCSVCommandTests(TestCase):
    def setUp(self):
        # Create a temp CSV
        self.fd, self.csv_path = tempfile.mkstemp(suffix='.csv')
        os.close(self.fd)  # Close the file descriptor so pandas can read it safely without lock
        df = pd.DataFrame({
            "title": ["Test Property"],
            "url": ["http://test.com"],
            "description": ["Test desc"],
            "price_vnd": [1000],
            "area_m2": [50.0],
            "price_per_m2": [20.0],
            "address": ["123 Test St"],
            "district": ["Test District"],
            "ward": ["Test Ward"],
            "source": ["Test Source"],
            "posted_at": ["2023-01-01"]
        })
        df.to_csv(self.csv_path, index=False)

    def tearDown(self):
        try:
            os.remove(self.csv_path)
        except OSError:
            pass

    @patch('properties.management.commands.import_csv.os.path.join')
    def test_import_csv_success(self, mock_join):
        # Mock os.path.join to return our temp file path instead of the relative one
        mock_join.return_value = self.csv_path
        
        out = StringIO()
        call_command('import_csv', '--file', 'dummy.csv', stdout=out)
        
        self.assertEqual(Property.objects.count(), 1)
        prop = Property.objects.first()
        self.assertEqual(prop.title, "Test Property")
        self.assertEqual(prop.district.name, "Test District")
        self.assertEqual(prop.ward.name, "Test Ward")

    @patch('properties.management.commands.import_csv.os.path.exists')
    def test_import_csv_file_not_found(self, mock_exists):
        mock_exists.return_value = False
        
        out = StringIO()
        call_command('import_csv', '--file', 'nonexistent.csv', stdout=out)
        
        self.assertEqual(Property.objects.count(), 0)

    @patch('properties.management.commands.import_csv.pd.read_csv')
    @patch('properties.management.commands.import_csv.os.path.exists')
    @patch('properties.management.commands.import_csv.os.path.join')
    def test_import_csv_exception_during_row(self, mock_join, mock_exists, mock_read_csv):
        mock_join.return_value = 'dummy.csv'
        mock_exists.return_value = True
        
        df = pd.DataFrame([{"url": "test"}])
        mock_read_csv.return_value = df
        
        with patch('properties.models.Property.objects.update_or_create') as mock_update:
            mock_update.side_effect = Exception("Test error")
            out = StringIO()
            call_command('import_csv', '--file', 'dummy.csv', stdout=out)
            
            # Count should still be 0 as it failed and caught the exception
            self.assertEqual(Property.objects.count(), 0)
