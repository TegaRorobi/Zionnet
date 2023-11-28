from django.contrib import admin
from .models import *

class MarketplaceAdmin(admin.ModelAdmin):
    model = MarketPlace
    list_display = 'name', 'cover_image'


class StoreAdmin(admin.ModelAdmin):
    model = Store 
    list_display = 'name', 'marketplace', 'vendor', 'country', 'city'


class ProductCategoryAdmin(admin.ModelAdmin):
    model = ProductCategory
    list_display = 'name', 'image'

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = 'name', 'merchant', 'category', 'store', 'price'
