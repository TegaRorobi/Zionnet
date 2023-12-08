from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import *

User = get_user_model()

class FreelancerProfileViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="test@example.com", password="testpassword"
        )
        JobSkill.objects.create(name='Python')
        JobSkill.objects.create(name='Git')
        JobSkill.objects.create(name='Django')

    def test_create_freelancer_profile(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            reverse('JobPosting:freelancer-profile-create'),
            data = {
                'title': 'Software Engineer',
                'skills': [1, 2, 3],
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(hasattr(response, 'json'))
        self.assertEqual(FreelancerProfile.objects.count(), 1)
        self.assertTrue(hasattr(self.user, 'freelancer_profile'))

    def test_create_freelancer_profile_unauthenticated(self):
        response = self.client.post(
            reverse('JobPosting:freelancer-profile-create'),
            data = {
                'title': 'Software Engineer',
                'skills': [1, 2, 3],
            }
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        JobSkill.objects.all().delete()
        FreelancerProfile.objects.all().delete()
        User.objects.all().delete()


class JobApplicationViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="test@example.com", password="testpassword"
        )
        self.freelancer_profile = FreelancerProfile.objects.create(
            user=self.user,
            title='Senior Software Engineer',
        )
        role = JobRole.objects.create(name='Software Engineer')
        category = JobCategory.objects.create(name='Technology')
        company = Company.objects.create(
            name='XYZ Corp.',
            employee_number_range='11-50'
        )
        self.job_opening = JobOpening.objects.create(
            title='Senor Software Engineer @ XYZ Corp.',
            company=company, role=role, category=category,
            experience_range='2-5',
            time_commitment = 'part-time',
            presence_type = 'hybrid'
        )

    def test_create_job_application(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('JobPosting:job-application-create'),
            data = {
                'job_opening': self.job_opening.id,
                'first_name':'John',
                'last_name':'Doe',
                'email':'testemail@domain.com',
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobApplication.objects.count(), 1)
        self.assertTrue(hasattr(response, 'json'))
        self.assertEqual(response.json()['applicant'], self.user.freelancer_profile.id)

    def test_create_job_application_without_freelancer_profile(self):
        FreelancerProfile.objects.all().delete()
        self.user.refresh_from_db()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('JobPosting:job-application-create'),
            data = {
                'job_opening': self.job_opening.id,
                'first_name':'John',
                'last_name':'Doe',
                'email':'testemail@domain.com',
            }
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_job_applications(self):
        self.client.force_authenticate(user=self.user)
        
        job_application = JobApplication.objects.create(
            applicant=self.user.freelancer_profile,
            job_opening=self.job_opening,
            first_name='John', last_name='Doe',
            email='johndoe@lorem.ipsum'
        )

        response = self.client.get(reverse('JobPosting:job-applications-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(hasattr(response, 'json'))
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json()['results'][0]['id'], job_application.id)

    def tearDown(self):
        JobApplication.objects.all().delete()
        JobOpening.objects.all().delete()
        Company.objects.all().delete()
        JobCategory.objects.all().delete()
        JobRole.objects.all().delete()
        FreelancerProfile.objects.all().delete()
        User.objects.all().delete()


class JobPosting_Search_Sort_and_GetByCategoryTestCase(TestCase):
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
        response = self.client.post('/api/jobs/sort/', {'sort_by':
        'id','reverse':'true'})
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
