from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from helpers import *
User = get_user_model()


class MarketPlace(TimestampsModel):
    name = models.CharField(_('market name'), max_length=255)
    cover_image = ExtensionAwareImageField(upload_to='marketplace/cover_images')

    def __str__(self) -> str:
        return self.name


class Store(TimestampsModel):
    marketplace = models.ForeignKey(MarketPlace, related_name='stores', on_delete=models.PROTECT)
    vendor = models.ForeignKey(User, verbose_name=_('store vendor'), related_name='stores', on_delete=models.CASCADE)
    name = models.CharField(_('store name'), max_length=255)
    description = models.TextField(_('store description'), null=True, blank=True)
    logo = ExtensionAwareImageField(upload_to='store/logos', null=True, blank=True)
    cover_image = ExtensionAwareImageField(upload_to='store/cover_images', null=True, blank=True)
    country = models.CharField(_('country of location'), max_length=255)
    city = models.CharField(_('store city'), max_length=255)
    province = models.CharField(_('store province'), max_length=255)
    additional_information = models.JSONField(_('store additional information'), null=True, blank=True)

    def __str__(self) -> str:
        return self.name.__str__()


class ProductCategory(TimestampsModel):
    name = models.CharField(_('store name'), max_length=255)
    image = ExtensionAwareImageField(upload_to='products/category_images', null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Product(TimestampsModel):
    store = models.ForeignKey(Store, related_name='products', on_delete=models.CASCADE)
    merchant = models.ForeignKey(User, related_name='store_products', on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(_('product name'), max_length=255)
    description = models.TextField(_('product description'), null=True, blank=True)
    cover_image = ExtensionAwareImageField(upload_to='products/cover_images', null=True, blank=True)
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
    image = ExtensionAwareImageField(_('image file'), upload_to='products/product_images')

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
