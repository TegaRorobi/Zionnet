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


class Job_BestMatch_MostRecent_and_Featured_Tests(TestCase):

    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.freelancer_profile = FreelancerProfile.objects.create(
            user=self.user,
            title='Software Engineer',
        )

        # Create some job-related objects for testing
        company = Company.objects.create(
            name='Test Company',
            description='Test Company Description',
            website='http://www.testcompany.com',
            country='Test Country',
            city='Test City',
            employee_number_range='11-50'
        )

        role = JobRole.objects.create(name='Test Role')
        category = JobCategory.objects.create(name='Test Category')
        skill1 = JobSkill.objects.create(name='Skill 1')
        skill2 = JobSkill.objects.create(name='Skill 2')
        skill3 = JobSkill.objects.create(name='Skill 3')

        self.job1 = JobOpening.objects.create(
            company=company,
            role=role,
            category=category,
            poster=self.user,
            poster_positon='Test Position 1',
            title='Job 1',
            description='Description 1',
            time_commitment='full-time',
            presence_type='remote',
            experience_range='2-5',
            resumption_date='2023-01-01',
            hourly_rate=50,
        )
        self.job1.required_skills.add(skill1, skill2)

        self.job2 = JobOpening.objects.create(
            company=company,
            role=role,
            category=category,
            poster=self.user,
            poster_positon='Test Position 2',
            title='Job 2',
            description='Description 2',
            time_commitment='part-time',
            presence_type='on-site',
            experience_range='5-10',
            resumption_date='2023-02-01',
            hourly_rate=75,
            featured=True,
        )
        self.job2.required_skills.add(skill2, skill3)

        self.job3 = JobOpening.objects.create(
            company=company,
            role=role,
            category=category,
            poster=self.user,
            poster_positon='Test Position 3',
            title='Job 3',
            description='Description 3',
            time_commitment='contract',
            presence_type='hybrid',
            experience_range='0-2',
            resumption_date='2023-03-01',
            hourly_rate=60,
        )
        self.job3.required_skills.add(skill1, skill3)

    def test_get_featured_jobs(self):
        response = self.client.get('/api/jobs/featured/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  

    def test_get_best_match_jobs(self):
        response = self.client.get('/api/jobs/best-match/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_most_recent_jobs(self):
        response = self.client.get('/api/jobs/most-recent/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3) 

    def tearDown(self):
        objects_to_delete = [self.job1, self.job2, self.job3]

        for obj in objects_to_delete:
            if hasattr(obj, 'id'):
                obj.delete()

