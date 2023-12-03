from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from .models import *
from PIL import Image
import tempfile, os

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
        user = User.objects.create_user(
            email= 'test@domain.com',password= 'password'
        )
        self.marketplace = MarketPlace.objects.create(
            name='E-commerce', cover_image='path/to/image.extension'
        )
        vendor = StoreVendor.objects.create(
            user=user, email=user.email
        )
        store = Store.objects.create(
            marketplace= self.marketplace,  vendor=vendor, name='Apple',
            country='US', city='Chicago', province='Stonetown'
        )
        product_category = ProductCategory.objects.create(
            marketplace=self.marketplace, name='Electronics & Gadgets'
        )
        Product.objects.create(
            store=store, category=product_category,
            name='Apple Vision Pro', price=3499.99
        )

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
        ProductCategory.objects.create(marketplace=self.marketplace, name='Food & Health')
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
        marketplace = MarketPlace.objects.create(
            name='E-commerce', cover_image='path/to/image.extension'
        )
        vendor = StoreVendor.objects.create(
            user=self.user, email=self.user.email
        )
        store = Store.objects.create(
            marketplace= marketplace,  vendor=vendor, name='Apple',
            country='US', city='Chicago', province='Stonetown'
        )
        product_category = ProductCategory.objects.create(
            marketplace=marketplace, name='Electronics & Gadgets'
        )
        self.product = Product.objects.create(
            store=store, category=product_category,
            name='Apple Vision Pro', quantity=10, price=3499.99
        )
        self.cart = Cart.objects.create(owner=self.user)

    def test_get_user_cart_when_empty(self):
        Cart.objects.all().delete()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('MarketPlace:user-cart-detail'))

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

    def test_get_user_cart_when_not_empty(self):
        self.client.force_authenticate(user=self.user)

        CartItem.objects.create(cart=self.cart, product=self.product, quantity=5)
        response = self.client.get(reverse('MarketPlace:user-cart-detail'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(hasattr(response, 'json'))
        self.assertTrue('summary' in response.json())
        self.assertTupleEqual(
            (
                response.json()['owner'], response.json()['new_cart'], 
                response.json()['summary']['sub_total'], response.json()['summary']['total_discount']
            ), 
            (
                1, False, round(self.product.discounted_price*5, 2), 
                round((self.product.price-self.product.discounted_price)*5, 2)
            )
        )

    def test_get_user_cart_items(self):
        self.client.force_authenticate(self.user)
        
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=5)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=5)
        response = self.client.get(reverse('MarketPlace:user-cart-items-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(hasattr(response, 'json'))
        self.assertEqual(len(response.json()['results']), 2)

    def test_delete_user_cart_items(self):
        self.client.force_authenticate(self.user)

        CartItem.objects.create(cart=self.cart, product=self.product, quantity=5)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=5)
        response = self.client.delete(reverse('MarketPlace:user-cart-dump'))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        Cart.objects.all().delete()
        CartItem.objects.all().delete()
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()
        Store.objects.all().delete()
        MarketPlace.objects.all().delete()
        User.objects.all().delete()


class StoreVendorTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='test@example.com', password='testpassword'
        )
        self.image_tempfile1 = tempfile.NamedTemporaryFile(suffix='.jpg')
        self.image_tempfile2 = tempfile.NamedTemporaryFile(suffix='.jpg')

    def test_create_store_vendor_request(self):
        self.client.force_authenticate(user=self.user)

        Image.new('RGB', (100, 100)).save(self.image_tempfile1)
        Image.new('RGB', (100, 100)).save(self.image_tempfile2)
        self.image_tempfile1.seek(0)
        self.image_tempfile2.seek(0)

        response = self.client.post(
            reverse('MarketPlace:store-vendor-request-create'), 
            data={
                'email': 'official.storeventures@domain.com',
                'id_type': 'NIN',
                'id_front': self.image_tempfile1,
                'id_back': self.image_tempfile2
            }, 
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(hasattr(response, 'json'))
        self.assertEqual(response.json()['user'], 1)
        self.assertEqual(response.json()['is_approved'], False)
    
    def tearDown(self):
        """
        A little explanation: The image files' data are sent via the POST request from the 
        authenticated client. This means that the files are read from the tempfile, and transmitted 
        to the endpoint, automatically emptying the tempfile. This in turn means that the files are then 
        stored in the settings.MEDIA_ROOT directory. Until I'm able to find a way to dynamically get the file 
        locations (mainly the 'upload_to' directory of the ImageField), I just hardcoded in the url.
        """
        os.remove(
            os.path.join(
                settings.MEDIA_ROOT, 'store/vendors/id_files',
                os.path.split(self.image_tempfile1.name)[-1]
            )
        )
        os.remove(
            os.path.join(
                settings.MEDIA_ROOT, 'store/vendors/id_files',
                os.path.split(self.image_tempfile2.name)[-1]
            )
        )
        StoreVendor.objects.all().delete()
        User.objects.all().delete()


class StoreViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='name@domain.com', password='testpassword'
        )
        self.image_tempfile1 = tempfile.NamedTemporaryFile(suffix='.jpg')
        self.image_tempfile2 = tempfile.NamedTemporaryFile(suffix='.jpg')
        self.image_tempfile3 = tempfile.NamedTemporaryFile(suffix='.jpg')
        Image.new('RGB', (100, 100)).save(self.image_tempfile1)
        Image.new('RGB', (100, 100)).save(self.image_tempfile2)
        Image.new('RGB', (100, 100)).save(self.image_tempfile3)
        self.image_tempfile1.seek(0)
        self.image_tempfile2.seek(0)
        self.image_tempfile3.seek(0)
        self.marketplace = MarketPlace.objects.create(name='E-commerce', cover_image=self.image_tempfile1.name)
        vendor = StoreVendor.objects.create(
            user=self.user, email='vendor.email@domain.com', id_type='Voter\'s card',
            id_front=self.image_tempfile2.name, id_back=self.image_tempfile3.name,
            is_approved=True
        )
        Store.objects.create(
            marketplace=self.marketplace, vendor=vendor, name='Mike\'s Kicks & Co',
            country='Nigeria', city='Lagos', province='Province 23' 
        )
        Store.objects.create(
            marketplace=self.marketplace, vendor=vendor, name='Samsung Stores',
            country='Nigeria', city='Lagos', province='Province 16' 
        )

    def test_get_user_stores(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse('MarketPlace:store-list-create'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(hasattr(response, 'json'))
        self.assertEqual(len(response.json()), 2)
    
    def test_create_store(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('MarketPlace:store-list-create'),
            data={
                'marketplace': self.marketplace.id,
                'name':'Apple Stores',
                'country':'Nigeria', 
                'city':'Lagos', 
                'province':'Province 3' 
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(hasattr(response, 'json'))
        self.assertEqual(response.json()['name'], 'Apple Stores')
        self.assertEqual(len(self.user.store_vendor_profile.stores.all()), 3)

    def test_retrieve_store(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('MarketPlace:store-retrieve-update-delete', kwargs={'pk':1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(hasattr(response, 'json'))
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(response.json()['name'], 'Mike\'s Kicks & Co')

    def test_partial_update_store(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            reverse('MarketPlace:store-retrieve-update-delete', kwargs={'pk':1}),
            data={'name': 'Mike\'s Kicks & Co (updated)'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(hasattr(response, 'json'))
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(response.json()['name'], 'Mike\'s Kicks & Co (updated)')
    
    def test_delete_store(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse('MarketPlace:store-retrieve-update-delete', kwargs={'pk':1})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(hasattr(response, 'json'))
        self.assertEqual(len(self.user.store_vendor_profile.stores.all()), 1)

    def tearDown(self):
        """
        In this case, the images are not stored in the media directory, and rather paths to 
        the tempfiles are stored. This means that we only to delete the tempfiles.
        """
        os.remove(self.image_tempfile1.name)
        os.remove(self.image_tempfile2.name)
        os.remove(self.image_tempfile3.name)
        Store.objects.all().delete()
        StoreVendor.objects.all().delete()
        MarketPlace.objects.all().delete()
        User.objects.all().delete()


class FavouriteProductTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email= 'test@domain.com',password= 'password'
        )
        marketplace = MarketPlace.objects.create(
            name='E-commerce', cover_image='path/to/image.extension'
        )
        vendor = StoreVendor.objects.create(
            user=self.user, email=self.user.email
        )
        store = Store.objects.create(
            marketplace= marketplace,  vendor=vendor, name='Apple',
            country='US', city='Chicago', province='Stonetown'
        )
        product_category = ProductCategory.objects.create(
            marketplace=marketplace, name='Electronics & Gadgets'
        )
        self.product1 = Product.objects.create(
            store=store, category=product_category,
            name='Apple Vision Pro', price=3499.99
        )
        self.product2 = Product.objects.create(
            store=store, category=product_category,
            name='Ergonomic chair', price=2199.99
        )

    def test_retrieve_favourites_when_empty(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('MarketPlace:favourite-products-list-create')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_favourites_when_not_empty(self):
        self.client.force_authenticate(user=self.user)
        FavouriteProduct.objects.create(user=self.user, product=self.product1)
        FavouriteProduct.objects.create(user=self.user, product=self.product2)
        response = self.client.get(
            reverse('MarketPlace:favourite-products-list-create')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(hasattr(response, 'json'))
        self.assertEqual(response.json()['count'], 2)
        self.assertEqual(len(response.json()['results']), 2)

        FavouriteProduct.objects.first().delete()
        response = self.client.get(
            reverse('MarketPlace:favourite-products-list-create')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(hasattr(response, 'json'))
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(len(response.json()['results']), 1)

    def test_add_products_to_favourites(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('MarketPlace:favourite-products-list-create'),
            data = {'product': self.product1.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(hasattr(response, 'json'))
        self.assertEqual(response.json()['product'], self.product1.id)

    def tearDown(self):
        FavouriteProduct.objects.all().delete()
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()
        Store.objects.all().delete()
        MarketPlace.objects.all().delete()
        User.objects.all().delete()


class OrderModelTestCase(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')

        # Create a marketplace, vendor, store, category, and product
        self.marketplace = MarketPlace.objects.create(name='Test Marketplace')
        self.vendor = StoreVendor.objects.create(
            user=self.user,
            email='vendor@example.com',
            id_type='NIN',
        )
        self.store = Store.objects.create(
            marketplace=self.marketplace,
            vendor=self.vendor,
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
        self.vendor = StoreVendor.objects.create(
            user=self.user,
            email='vendor@example.com',
            id_type='NIN',
        )
        self.store = Store.objects.create(
            marketplace=self.marketplace,
            vendor=self.vendor,
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
        self.assertEqual(
            Product.objects.get(id=response.data[0]['product']).name, 'Test Product'
        )

    def test_user_can_create_order(self):
        url = reverse('MarketPlace:create_order')
        data = {
            'buyer': self.user.id, 
            'product': self.product.id, 
            'quantity': 1, 
            'status': 'shipped'
        }
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
        other_user = User.objects.create_user(
            email='otheruser@example.com', 
            password='testpassword'
        )

        # Log in the other user
        self.client.force_authenticate(user=other_user)

        # Attempt to access the order created by the first user
        url = reverse('MarketPlace:update_order', args=[self.order.id])
        response = self.client.patch(url, {'quantity': 3})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class StoreProductViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com", password="testpassword"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.marketplace = MarketPlace.objects.create(name="Test Marketplace")
        self.vendor = StoreVendor.objects.create(
            user=self.user,
            email="vendor@example.com",
            id_type="NIN",
        )
        self.store = Store.objects.create(
            marketplace=self.marketplace,
            vendor=self.vendor,
            name="Test Store",
            country="Test Country",
            city="Test City",
            province="Test Province",
        )
        self.category = ProductCategory.objects.create(
            marketplace=self.marketplace, name="Test Category"
        )
        self.product = Product.objects.create(
            store=self.store,
            category=self.category,
            name="Test Product",
            quantity=10,
            price=50.00,
            currency_symbol="₦",
            currency_abbrev="NGN",
            currency_verbose="Naira",
        )

    def test_store_product_list_create_view(self):
        url = reverse("MarketPlace:store-products", kwargs={"store_id": self.store.id})
        data = {
            "name": "New Product",
            "description": "New Product Description",
            "quantity": 20,
            "discount": "0.05",
            "price": "150.0",
            "currency_symbol": "-",
            "currency_abbrev": "BRR",
            "currency_verbose": "Birr",
            "store": self.store.id,
            "category": self.category.id
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_store_product_update_view(self):
        url = reverse(
            "MarketPlace:store-product",
            kwargs={"store_id": self.store.id, "pk": self.product.id},
        )
        data = {"quantity": 15}

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get(id=self.product.id).quantity, 15)

    def test_store_product_delete_view(self):
        url = reverse(
            "MarketPlace:store-product",
            kwargs={"store_id": self.store.id, "pk": self.product.id},
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)        


class MarketPlaceViewsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.marketplace = MarketPlace.objects.create(name='Test Market', cover_image='test_image.jpg')

        self.user = User.objects.create_user(email='testuser@example.com',  password ='testpassword')
       
        self.client.force_authenticate(user=self.user)

        self.vendor = StoreVendor.objects.create(
              user=self.user,
              email="vendor@example.com")

        self.store = Store.objects.create(
            marketplace=self.marketplace,
            vendor=self.vendor,
            name='Test Store',
            description='Test Store Description',
            country='Test Country',
            city='Test City',
            province='Test Province'
        )

        self.product_category = ProductCategory.objects.create(
            marketplace=self.marketplace,
            name='Test Category'
        )

        self.product = Product.objects.create(
            store=self.store,
            category=self.product_category,
            name='Test Product',
            description='Test Product Description',
            price=100.0,
            quantity=50,
            discount=60
        )

        # Create some ratings for the product
        ProductRating.objects.create(user=self.user, product=self.product, value=4)
        ProductRating.objects.create(user=self.user, product=self.product, value=5)
        ProductRating.objects.create(user=self.user, product=self.product, value=3)

    def test_get_popular_products_view(self):
        url = reverse('MarketPlace:marketplace-products-popular', kwargs={'pk': self.marketplace.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_hot_deals_view(self):
        url = reverse('MarketPlace:hot_deals', kwargs={'pk': self.marketplace.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_flash_sale_view(self):
        url = reverse('MarketPlace:create_flash_sale', kwargs={'pk': self.marketplace.pk, 'product_id': self.product.pk})
        data = {
            'product':self.product.pk,
            'discount_percentage': 10.0,
            'start_datetime': '2023-01-01T00:00:00Z',
            'end_datetime': '2024-02-01T00:00:00Z',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_flash_sale_products_view(self):
        # Assuming there is a flash sale for the product
        FlashSale.objects.create(
            product=self.product,
            discount_percentage=60,
            start_datetime='2023-01-01T00:00:00Z',
            end_datetime='2024-02-01T00:00:00Z'
        )

        url = reverse('MarketPlace:flash_sale_products', kwargs={'pk': self.marketplace.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
