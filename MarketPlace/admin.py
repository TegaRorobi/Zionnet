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
    list_display = 'name', '_vendor', 'category', 'store', 'price'

    @admin.display()
    def _vendor(self, obj):
        return self.vendor.__str__()

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

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = 'owner', 'created_at'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    model = CartItem
    list_display = 'cart_owner_', 'product', 'quantity'

    @admin.display()
    def cart_owner_(self, obj):
        return obj.cart.owner.__str__()

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = 'buyer', 'product', 'quantity', 'status'
