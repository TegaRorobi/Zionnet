from rest_framework import serializers
from .models import BusinessListingRequest, BusinessListing

class BusinessListingRequestSerializer(serializers.ModelSerializer):
    vendor_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BusinessListingRequest
        fields = '__all__'

class BusinessListingSerializer(serializers.ModelSerializer):
    vendor_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BusinessListing
        fields = '__all__'
