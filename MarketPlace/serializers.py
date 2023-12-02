from rest_framework import serializers
from .models import *


class MarketPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPlace
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    marketplace_id = serializers.PrimaryKeyRelatedField(
        queryset=MarketPlace.objects.all()
    )
    marketplace_display = serializers.CharField(
        source='marketplace.__str__', read_only=True
    )
    marketplace = serializers.HiddenField(default=None)

    class Meta:
        model = ProductCategory
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    summary = serializers.JSONField(source='_summary')

    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product_details = serializers.JSONField(source='_product_details')
    discounted_price = serializers.DecimalField(source='_discounted_price', max_digits=20, decimal_places=2)
    actual_price = serializers.DecimalField(source='_actual_price', max_digits=20, decimal_places=2)

    class Meta:
        model = CartItem
        fields = '__all__'

class ProductSearchSerializer(serializers.Serializer):
    search_query = serializers.CharField(max_length = 255, write_only = True)  

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class StoreVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreVendor
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'is_approved': {'read_only': True},
        }


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        extra_kwargs = {
            'vendor': {'read_only':True},
        }


class OrderSerializer(serializers.ModelSerializer):
    buyer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Order
        fields = '__all__'
