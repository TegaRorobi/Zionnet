from rest_framework import serializers
from .models import *


class MarketPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPlace
        fields = "__all__"


class ProductCategorySerializer(serializers.ModelSerializer):
    marketplace_id = serializers.PrimaryKeyRelatedField(
        queryset=MarketPlace.objects.all()
    )
    marketplace_display = serializers.CharField(
        source="marketplace.__str__", read_only=True
    )
    marketplace = serializers.HiddenField(default=None)

    class Meta:
        model = ProductCategory
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    summary = serializers.JSONField(source="_summary")

    class Meta:
        model = Cart
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    product_details = serializers.JSONField(source="_product_details")
    discounted_price = serializers.CharField(source="_discounted_price")
    actual_price = serializers.CharField(source="_actual_price")

    class Meta:
        model = CartItem
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
