from django.test import TestCase
from django.conf import settings 
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import BusinessListingRequest, BusinessListingVendor, BusinessListingCategory
from PIL import Image
import tempfile, os

User = get_user_model()

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