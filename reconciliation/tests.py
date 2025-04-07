from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

class ReconciliationTests(APITestCase):
    def create_csv_file(self, content):
        return SimpleUploadedFile("file.csv", content.encode('utf-8'), content_type="text/csv")

    def test_successful_reconciliation(self):
        source = self.create_csv_file("id,name\n1,Alice\n2,Bob\n3,Carol")
        target = self.create_csv_file("id,name\n1,Alice\n3,Carol\n4,David")
        response = self.client.post(reverse('reconcile'), {'source': source, 'target': target})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(len(data['missing_in_target']), 1)  # Bob
        self.assertEqual(len(data['missing_in_source']), 1)  # David

    def test_missing_file_error(self):
        source = self.create_csv_file("id,name\n1,Alice")
        response = self.client.post(reverse('reconcile'), {'source': source})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

