
from rest_framework import serializers 
from .models import *


class MarketPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPlace
        fields = '__all__'

class ProductCategorySerializer(serializers.ModelSerializer):
    marketplace_id = serializers.PrimaryKeyRelatedField(queryset=MarketPlace.objects.all())
    marketplace_display = serializers.CharField(source='marketplace.__str__', read_only=True)
    marketplace = serializers.HiddenField(default=None)
    class Meta:
        model = ProductCategory
        fields = '__all__'