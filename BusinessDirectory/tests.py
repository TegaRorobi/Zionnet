from django.test import TestCase
from django.conf import settings 
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import BusinessListingRequest, BusinessListingVendor, BusinessListingCategory, BusinessListing, BusinessListingRating
from PIL import Image
import tempfile, os
from django.urls import reverse
from .serializers import BusinessListingSerializer




User = get_user_model()

class BusinessListingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor_user = User.objects.create_user(email='testvendor@example.com', password='testpass')
        self.business_listing_vendor = BusinessListingVendor.objects.create(
            user=self.vendor_user,
            email='testvendor@example.com',
            id_type='NIN',
        )
        category = BusinessListingCategory.objects.create(id=1, name='Your Category Name')
        self.listing1 = BusinessListing.objects.create(
            vendor=self.business_listing_vendor,
            category_id=1,
            name='Test Business 1',
            description='Description for Test Business 1',
            country='Test Country',
            province='Test Province',
            city='Test City',
            phone_number='123456789',
            physical_address='Test Address 1',
        )

        self.listing2 = BusinessListing.objects.create(
            vendor=self.business_listing_vendor,
            category_id=1,
            name='Test Business 2',
            description='Description for Test Business 2',
            country='Test Country',
            province='Test Province',
            city='Test City',
            phone_number='987654321',
            physical_address='Test Address 2',

        )

        self.listing3 = BusinessListing.objects.create(
            vendor=self.business_listing_vendor,
            category_id=1,
            name='Test Business 3',
            description='Description for Test Business 3',
            country='Test Country',
            province='Test Province',
            city='Test City',
            phone_number='987654321',
            physical_address='Test Address 3',

        )

        self.listing4 = BusinessListing.objects.create(
            vendor=self.business_listing_vendor,
            category_id=1,
            name='Test Business 4',
            description='Description for Test Business 4',
            country='Test Country',
            province='Test Province',
            city='Test City',
            phone_number='987654321',
            physical_address='Test Address 4',

        )
        self.rating1 = BusinessListingRating.objects.create(
            listing=self.listing1,
            user=self.vendor_user,
            value=4
        )

        self.rating2 = BusinessListingRating.objects.create(
            listing=self.listing2,
            user=self.vendor_user,
            value=5
        )

        self.rating3 = BusinessListingRating.objects.create(
            listing=self.listing3,
            user=self.vendor_user,
            value=1
        )

        self.rating4 = BusinessListingRating.objects.create(
            listing=self.listing4,
            user=self.vendor_user,
            value=2
        )

    def test_top_rated_listings(self):
        url = reverse('top-rated-listings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        print(response.data)
        
        # ratings = [listing['avg_rating'] for listing in response.data]
        # self.assertEqual(ratings, sorted(ratings, reverse=True))
        
    def test_top_rated_listings_no_data(self):
        BusinessListingRating.objects.all().delete()
        url = reverse('top-rated-listings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_listings(self):
        self.client.force_authenticate(user=self.vendor_user)
        url = reverse('user-listings')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  

    def test_listing_detail(self):
        url = reverse('business-listing', kwargs={'pk': self.listing1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Business 1')

    def test_listing_detail_not_found(self):
        url = reverse('business-listing', kwargs={'pk': 999})  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class BusinessListingRequestCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        self.listing_category = BusinessListingCategory.objects.create(name='Categoryname')
        self.image_tempfile1 = tempfile.NamedTemporaryFile(suffix='.jpg')
        self.image_tempfile2 = tempfile.NamedTemporaryFile(suffix='.jpg')
        Image.new('RGB', (100, 100)).save(self.image_tempfile1)
        Image.new('RGB', (100, 100)).save(self.image_tempfile2)
        self.image_tempfile1.seek(0)
        self.image_tempfile2.seek(0)

    def test_create_business_listing_request(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'listing_category': self.listing_category.id,
            'id_type': 'type_1',
            'id_front': self.image_tempfile1,
            'id_back': self.image_tempfile2
        }

        response = self.client.post('/api/listings/request/', data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BusinessListingRequest.objects.count(), 1)
        self.assertEqual(BusinessListingRequest.objects.first().vendor, self.user)

    def test_create_business_listing_request_unauthenticated(self):
        data = {
            'listing_category': self.listing_category.id,
            'id_type': 'type_1',
            'id_front': self.image_tempfile1,
            'id_back': self.image_tempfile2
        }

        response = self.client.post('/api/listings/request/', data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def tearDown(self):
        try:
            os.remove(
                os.path.join(
                    settings.MEDIA_ROOT, 'business_listing_request_id_front', 
                    os.path.split(self.image_tempfile1.name)[-1]
                )
            )
            os.remove(
                os.path.join(
                    settings.MEDIA_ROOT, 'business_listing_request_id_back', 
                    os.path.split(self.image_tempfile2.name)[-1]
                )
            )
        except FileNotFoundError:
            pass
        BusinessListingRequest.objects.all().delete()
        User.objects.all().delete()


class BusinessListingVendorRequestCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        self.image_tempfile1 = tempfile.NamedTemporaryFile(suffix='.jpg')
        self.image_tempfile2 = tempfile.NamedTemporaryFile(suffix='.jpg')
        Image.new('RGB', (100, 100)).save(self.image_tempfile1)
        Image.new('RGB', (100, 100)).save(self.image_tempfile2)
        self.image_tempfile1.seek(0)
        self.image_tempfile2.seek(0)

    def test_create_business_listing_vendor_request(self):
        self.client.force_authenticate(user=self.user)
    
        data = {
            'email': 'listing@domain.com',
            'id_type': 'NIN',
            'id_front': self.image_tempfile1,
            'id_back': self.image_tempfile2
        }

        response = self.client.post('/api/listings/vendor/request/', data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BusinessListingVendor.objects.count(), 1)
        self.assertEqual(BusinessListingVendor.objects.first().user, self.user)

    def test_create_business_listing_vendor_request_unauthenticated(self):
        data = {
            'email': 'listing@domain.com',
            'id_type': 'NIN',
            'id_front': self.image_tempfile1,
            'id_back': self.image_tempfile2
        }

        response = self.client.post('/api/listings/vendor/request/', data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        try:
            os.remove(
                os.path.join(
                    settings.MEDIA_ROOT, 'listings/vendors/id_files', 
                    os.path.split(self.image_tempfile1.name)[-1]
                )
            )
            os.remove(
                os.path.join(
                    settings.MEDIA_ROOT, 'listings/vendors/id_files', 
                    os.path.split(self.image_tempfile2.name)[-1]
                )
            )
        except FileNotFoundError:
            pass
        BusinessListingVendor.objects.all().delete()
        User.objects.all().delete()