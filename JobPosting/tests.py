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

    def tearDown(self):
        JobApplication.objects.all().delete()
        JobOpening.objects.all().delete()
        Company.objects.all().delete()
        JobCategory.objects.all().delete()
        JobRole.objects.all().delete()
        FreelancerProfile.objects.all().delete()
        User.objects.all().delete()
