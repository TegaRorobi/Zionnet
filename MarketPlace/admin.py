from django.contrib import admin
from .models import *

@admin.register(MarketPlace)
class MarketplaceAdmin(admin.ModelAdmin):
    list_display = 'name', 'cover_image'

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = 'name', 'marketplace', 'vendor', 'country', 'city'

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = 'name', 'image'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'name', '_vendor', 'category', 'store', 'price'

    @admin.display()
    def _vendor(self, obj):
        return self.vendor.__str__()

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = 'product', 'image'

@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = 'user', 'product', 'value'

@admin.register(ProductReaction)
class ProductReactionAdmin(admin.ModelAdmin):
    list_display = 'user', 'product', 'reaction'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = 'owner', 'created_at'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = 'cart_owner_', 'product', 'quantity'

    @admin.display()
    def cart_owner_(self, obj):
        return obj.cart.owner.__str__()

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'buyer', 'product', 'quantity', 'status'

@admin.register(StoreVendor)
class StoreVendorAdmin(admin.ModelAdmin):
    list_display = 'user', 'email', 'is_approved'

@admin.register(FlashSale)
class FlashSaleAdmin(admin.ModelAdmin):
    model = FlashSale
    list_display = ('product', 'discount_percentage', 'start_datetime', 'end_datetime', 'is_available')
    search_fields = ('product__name',) 
    list_filter = ( 'start_datetime', 'end_datetime')
