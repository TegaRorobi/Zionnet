from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import BusinessListingRequest, BusinessListing, BusinessListingCategory

User = get_user_model()

class BusinessListingRequestCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')

    def test_create_business_listing_request(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'listing_category': 'type_1',
            'id_type': 'Type 1',
            'id_front': 'path/to/id_front.jpg',
            'id_back': 'path/to/id_back.jpg'
        }

        response = self.client.post('/api/listings/request/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BusinessListingRequest.objects.count(), 1)
        self.assertEqual(BusinessListingRequest.objects.get().vendor_id, self.user)

    def test_create_business_listing_request_unauthenticated(self):
        data = {
            'listing_category': 'type_1',
            'id_type': 'Type 1',
            'id_front': 'path/to/id_front.jpg',
            'id_back': 'path/to/id_back.jpg'
        }

        response = self.client.post('/api/listings/request/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class BusinessListingVendorRequestCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')

    def test_create_business_listing_vendor_request(self):
        self.client.force_authenticate(user=self.user)

        category = BusinessListingCategory.objects.create(name='Category 1', image='path/to/image.jpg')

        data = {
            'category': category.id,
            'name': 'Business Name',
            'description': 'Business Description',
            'country': 'Country',
            'province': 'Province',
            'city': 'City',
            'phone_number': '123456789',
            'physical_address': 'Address'
        }

        response = self.client.post('/api/listings/vendor/request/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BusinessListing.objects.count(), 1)
        self.assertEqual(BusinessListing.objects.get().vendor_id, self.user)

    def test_create_business_listing_vendor_request_unauthenticated(self):
        data = {
            'category': 1,
            'name': 'Business Name',
            'description': 'Business Description',
            'country': 'Country',
            'province': 'Province',
            'city': 'City',
            'phone_number': '123456789',
            'physical_address': 'Address'
        }

        response = self.client.post('/api/listings/vendor/request/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
