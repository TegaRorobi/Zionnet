from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from helpers import *
from helpers.validators import validate_positive_decimal
User = get_user_model()



class MarketPlace(TimestampsModel):
    name = models.CharField(_('market name'), max_length=255)
    cover_image = ValidatedImageField(upload_to='marketplace/cover_images')

    def __str__(self) -> str:
        return self.name


class StoreVendor(TimestampsModel):
    ID_TYPE_CHOICES = [
        ('NIN', 'NIN'),
        ("Driver's License", "Driver's License"),
        ("Voter's Card", "Voter's Card")
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='store_vendor_profile')
    email = models.EmailField(_('vendor email address'))
    id_type = models.CharField(_('id type'), max_length=30, choices=ID_TYPE_CHOICES)
    id_front = models.FileField(_('id front'), upload_to='store/vendors/id_files', null=True, blank=True)
    id_back = models.FileField(_('id back'), upload_to='store/vendors/id_files', null=True, blank=True)
    request_info = models.CharField(_('additional request information'), max_length=400, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return 'Store Vendor: ' + self.email.__str__()


class Store(TimestampsModel):
    marketplace = models.ForeignKey(MarketPlace, related_name='stores', on_delete=models.PROTECT)
    vendor = models.ForeignKey(StoreVendor, verbose_name=_('store vendor'), related_name='stores', on_delete=models.CASCADE)
    name = models.CharField(_('store name'), max_length=255)
    description = models.TextField(_('store description'), null=True, blank=True)
    logo = ValidatedImageField(upload_to='store/logos', null=True, blank=True)
    cover_image = ValidatedImageField(upload_to='store/cover_images', null=True, blank=True)
    country = models.CharField(_('country of location'), max_length=255)
    city = models.CharField(_('store city'), max_length=255)
    province = models.CharField(_('store province'), max_length=255)
    additional_information = models.JSONField(_('store additional information'), null=True, blank=True)

    def __str__(self) -> str:
        return self.name.__str__()


class ProductCategory(TimestampsModel):
    marketplace = models.ForeignKey(MarketPlace, related_name='product_categories', on_delete=models.CASCADE)
    name = models.CharField(_('category name'), max_length=255)
    image = ValidatedImageField(upload_to='products/category_images', null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Product(TimestampsModel):
    store = models.ForeignKey(Store, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(_('product name'), max_length=255)
    description = models.TextField(_('product description'), null=True, blank=True)
    cover_image = ValidatedImageField(upload_to='products/cover_images', null=True, blank=True)
    quantity = models.IntegerField(_('available quantity'), default=0)
    discount = models.DecimalField(_('discount percentage'), decimal_places=2, max_digits=5, default=0.00)

    # in the future, these fields will be replaced with a better-suited currency or amount field from a third-party library
    price = models.DecimalField(_('product selling price'), decimal_places=2, max_digits=11)
    currency_symbol = models.CharField(_('product currency symbol'), max_length=1, default='₦')
    currency_abbrev = models.CharField(_('abbreviated product currency'), max_length=3, default='NGN')
    currency_verbose = models.CharField(_('verbose product currency'), max_length=20, default='Naira')

    @property
    def discounted_price(self):
        return self.price - (self.price * self.discount / 100)

    def __str__(self) -> str:
        return self.name


class ProductImage(TimestampsModel):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = ValidatedImageField(_('image file'), upload_to='products/product_images')

    def __str__(self) -> str:
        return 'Image representation of ' + self.product.__str__()


class ProductRating(TimestampsModel):
    user = models.ForeignKey(User, related_name='product_ratings', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    value = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self) -> str:
        return f"{self.user.__str__()} rates {self.product.__str__()} a {self.value}/5"


class ProductReaction(TimestampsModel):
    REACTION_CHOICES = [
        ('like', 'like'),
        ('dislike', 'dislike')
    ]
    user = models.ForeignKey(User, related_name='product_reactions', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, related_name='reactions', on_delete=models.CASCADE)
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)

    def __str__(self) -> str:
        return f"{self.product.__str__()} {self.reaction}d by {self.reactor.__str__() or 'AnonymousUser'}"


class Cart(TimestampsModel):
    owner = models.OneToOneField(User, related_name='cart', on_delete=models.CASCADE)
    delivery_address = models.CharField(_('delivery address'), max_length=255, blank=True)

    @property
    def _summary(self):
        cartitems = self.items.prefetch_related('product').all()
        if not cartitems:
            return {'sub_total':0, 'total_discount':0, 'currency':'₦'}
        sub_total = total_discount = 0
        for cartitem in cartitems:
            actual_price = cartitem.product.price
            discounted_price = cartitem.product.discounted_price
            sub_total += (discounted_price * cartitem.quantity)
            total_discount += (actual_price - discounted_price)
        return {
            # getting the currency from the first cartitem's product (#noqa)
            'currency':self.items.first().product.currency_symbol,
            'delivery_address':self.delivery_address,
            'sub_total':sub_total,
            'total_discount':total_discount
        }

    def __str__(self) -> str:
        return 'Cart owned by ' + self.owner.__str__()


class CartItem(TimestampsModel):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cartitems', on_delete=models.CASCADE)
    quantity = models.IntegerField(_('number of products'), default=1)

    @property
    def _product_details(self):
        product = self.product
        try:
            hasattr(product.cover_image, 'url')
            return {
                'name': product.name,
                'cover_image': product.cover_image.url
            }
        except ValueError:
            return {
                'name': product.name,
                'cover_image': None
            }

    @property
    def _actual_price(self):
        return self.product.price * self.quantity
    
    @property
    def _discounted_price(self):
        return self.product.discounted_price * self.quantity

    def delete(self, *args, **kwargs): # noqa
        # return the product(s) to the shelves
        self.product.quantity += self.quantity
        self.product.save()
        return super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return f"Cart item: {self.quantity} nos of '{self.product.__str__()}'"


class Order(TimestampsModel):
    ORDER_STATUS_CHOICES = [
        ('shipped', 'En route'),
        ('cancelled', 'Cancelled'),
        ('delivered', 'Delivered')
    ]
    buyer = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    quantity = models.IntegerField(_('number of products'), default=1)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES)

    def __str__(self) -> str:
        return f"{self.status}: {self.quantity} nos of {self.product.__str__()}"


class FlashSale(TimestampsModel):
    product = models.ForeignKey(Product, related_name='flashsaleproducts', on_delete=models.CASCADE)
  
    discount_percentage = models.DecimalField(
        _('discount percentage'), 
        decimal_places=2, 
        max_digits=5, 
        validators=[validate_positive_decimal])
    start_datetime = models.DateTimeField(_('start datetime'))
    end_datetime = models.DateTimeField(_('end datetime'))

    def __str__(self) -> str:
        return f"Flash Sale for {self.product.name} - {self.discount_percentage}% off"
    
    @property
    def is_available(self):
        now = timezone.now()
        return self.start_datetime <= now <= self.end_datetime
 