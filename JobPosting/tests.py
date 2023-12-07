from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class JobPostingTests(TestCase):
    def setUp(self):
        # Create a user, category, and jobs for testing
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.category = JobCategory.objects.create(name='Test Category')
        self.company = Company.objects.create(name='Test Company')
        self.role = JobRole.objects.create(name='Test Role')
        self.job1 = JobOpening.objects.create(
            company=self.company,
            role=self.role,
            category=self.category,
            poster=self.user,
            title='Test Job 1',
            description='Description 1',
            time_commitment='full-time',
            presence_type='remote', 
            experience_range='0-2', 
            resumption_date='2023-01-01'
        )
        self.job2 = JobOpening.objects.create(
            company=self.company, 
            role=self.role, 
            category=self.category,
            poster=self.user,
            title='Test Job 2', 
            description='Description 2',
            time_commitment='part-time', 
            presence_type='on-site', 
            experience_range='2-5', 
            resumption_date='2023-01-15'
        )

    def test_job_search_view(self):
        response = self.client.post('/api/jobs/search/', {'title': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)  # Assuming both jobs match the search

    def test_job_sort_view(self):
        response = self.client.post('/api/jobs/sort/', {'sort_by': 'role',})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'][0]['title'], 'Test Job 2')

    def test_job_category_view(self):
        response = self.client.get('/api/jobs/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)  # Assuming only one category is created

    def test_get_jobs_by_category_view(self):
        response = self.client.get('/api/jobs/categories/1/jobs/')  # Assuming the first category has id=1
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)  # Assuming both jobs are in the specified Category

    def tearDown(self):
        objects_to_delete = [self.job1]

        for obj in objects_to_delete:
            if hasattr(obj, 'id'):
                obj.delete()