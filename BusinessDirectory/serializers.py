from rest_framework import serializers
from .models import BusinessListing

class BusinessListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListing
        fields = '__all__' 