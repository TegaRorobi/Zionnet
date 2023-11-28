from django.contrib import admin
from .models import *

@admin.register(MarketPlace)
class MarketplaceAdmin(admin.ModelAdmin):
    model = MarketPlace
    list_display = 'name', 'cover_image'

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    model = Store 
    list_display = 'name', 'marketplace', 'vendor', 'country', 'city'

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    model = ProductCategory
    list_display = 'name', 'image'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = 'name', 'merchant', 'category', 'store', 'price'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    model = ProductImage
    list_display = 'product', 'image'

@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    model = ProductRating
    list_display = 'user', 'product', 'value'

@admin.register(ProductReaction)
class ProductReactionAdmin(admin.ModelAdmin):
    model = ProductReaction
    list_display = 'user', 'product', 'reaction'
