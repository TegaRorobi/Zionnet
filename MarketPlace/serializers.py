
from rest_framework import serializers 
from .models import *


class MarketPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPlace
        fields = '__all__'
