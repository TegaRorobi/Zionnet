from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import *


User = get_user_model()
class GetAllMarketPlacesTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        test_data = [
            {'name':'E-commerce', 'cover_image':'path/to/image.extension'},
            {'name':'Rentals & Leasing', 'cover_image':'path/to/image2.extension'},
        ]
        for item in test_data:
            MarketPlace.objects.create(**item)
    
    def test_get_all_marketplaces(self):
        url = reverse('MarketPlace:marketplaces-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(hasattr(response, 'json'))
        self.assertEqual(len(response.json()), MarketPlace.objects.count())
    
    def tearDown(self):
        MarketPlace.objects.all().delete()


class GetProductCategoriesTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_user(**{
            'email': 'test@domain.com','password': 'password'
        })
        self.marketplace = MarketPlace.objects.create(**{
            'name':'E-commerce', 'cover_image':'path/to/image.extension'
        })
        store = Store.objects.create(**{
            'marketplace': self.marketplace,  'vendor': user, 'name':'Apple', 
            'country':'US', 'city':'Chicago', 'province':'Stonetown' 
        })
        product_category = ProductCategory.objects.create(**{
            'marketplace':self.marketplace, 'name':'Electronics & Gadgets'
        })
        Product.objects.create(**{
            'store':store, 'merchant':user, 'category':product_category, 
            'name':'Apple Vision Pro', 'price':3499.99
        })

    def test_get_all_categories(self):
        ProductCategory.objects.create(**{'marketplace':self.marketplace, 'name':'Food & Health'})
        url = reverse('MarketPlace:marketplace-product-categories-list', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(hasattr(response, 'json'))
        self.assertEqual(len(response.json()), ProductCategory.objects.count())
    
    def test_get_all_categories_with_invalid_pk(self):
        url = reverse('MarketPlace:marketplace-product-categories-list', kwargs={'pk':0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(hasattr(response, 'json'))
        self.assertIn('0', response.json()['error'])

    def test_get_popular_categories(self):
        ProductCategory.objects.create(**{'marketplace':self.marketplace, 'name':'Food & Health'})
        url = reverse('MarketPlace:marketplace-popular-product-categories-list', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(hasattr(response, 'json'))
        self.assertEqual(response.json()[0]['name'], 'Electronics & Gadgets')
    
    def test_get_popular_categories_with_invalid_pk(self):
        url = reverse('MarketPlace:marketplace-popular-product-categories-list', kwargs={'pk':0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(hasattr(response, 'json'))
        self.assertIn('0', response.json()['error'])

    def tearDown(self):
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()
        Store.objects.all().delete()
        MarketPlace.objects.all().delete()
        User.objects.all().delete()


class GetCartViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@domain.com', password='password'
        )

    def test_get_user_cart(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/me/cart/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(hasattr(response, 'json'))
        self.assertTrue('summary' in response.json())
        self.assertTupleEqual(
            (
                response.json()['owner'],
                response.json()['new_cart'],
                response.json()['summary']['sub_total'],
                response.json()['summary']['total_discount']
            ), (1, True, 0, 0)
        )

    def tearDown(self):
        Cart.objects.all().delete()
        User.objects.all().delete()


class OrderModelTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')

        # Create a marketplace, store, category, and product
        self.marketplace = MarketPlace.objects.create(name='Test Marketplace')
        self.store = Store.objects.create(
            marketplace=self.marketplace,
            vendor=self.user,
            name='Test Store',
            country='Test Country',
            city='Test City',
            province='Test Province'
        )
        self.category = ProductCategory.objects.create(
            marketplace=self.marketplace,
            name='Test Category'
        )
        self.product = Product.objects.create(
            store=self.store,
            merchant=self.user,
            category=self.category,
            name='Test Product',
            quantity=10,
            price=50.00,
            currency_symbol='₦',
            currency_abbrev='NGN',
            currency_verbose='Naira'
        )

    def test_order_creation(self):
        order = Order.objects.create(
            buyer=self.user,
            product=self.product,
            quantity=2,
            status='shipped'
        )
        self.assertEqual(order.buyer, self.user)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.status, 'shipped')

class OrderAPITestCase(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')

        # Log in the user
        self.client.force_authenticate(user=self.user)

        # Create a marketplace, store, category, and product
        self.marketplace = MarketPlace.objects.create(name='Test Marketplace')
        self.store = Store.objects.create(
            marketplace=self.marketplace,
            vendor=self.user,
            name='Test Store',
            country='Test Country',
            city='Test City',
            province='Test Province'
        )
        self.category = ProductCategory.objects.create(
            marketplace=self.marketplace,
            name='Test Category'
        )
        self.product = Product.objects.create(
            store=self.store,
            merchant=self.user,
            category=self.category,
            name='Test Product',
            quantity=10,
            price=50.00,
            currency_symbol='₦',
            currency_abbrev='NGN',
            currency_verbose='Naira'
        )

        # Create an order for the user using the product instance
        self.order = Order.objects.create(
            buyer=self.user,
            product=self.product,  # Use the product instance
            quantity=2,
            status='shipped'
        )

    def test_user_can_retrieve_orders(self):
        url = reverse('MarketPlace:user_order_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['product']['name'], 'Test Product')

    def test_user_can_create_order(self):
        url = reverse('MarketPlace:create_order')
        data = {'buyer': self.user.id, 'product': self.product.id, 'quantity': 1, 'status': 'shipped'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_update_order(self):
        url = reverse('MarketPlace:update_order', args=[self.order.id])
        data = {'quantity': 3}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.quantity, 3)

    def test_user_can_cancel_order(self):
        url = reverse('MarketPlace:cancel_order', args=[self.order.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Order.DoesNotExist):
            self.order.refresh_from_db()

    def test_other_users_cannot_access_order(self):
        # Create a second user
        other_user = User.objects.create_user(email='otheruser@example.com', password='testpassword')

        # Log in the other user
        self.client.force_authenticate(user=other_user)

        # Attempt to access the order created by the first user
        url = reverse('MarketPlace:update_order', args=[self.order.id])
        response = self.client.patch(url, {'quantity': 3})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
