from rest_framework import serializers
from .models import BusinessListingRequest, BusinessListing

class BusinessListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListing
        fields = '__all__'

class BusinessListingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingRequest
        fields = '__all__'
