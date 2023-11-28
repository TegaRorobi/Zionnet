from rest_framework import serializers
from .models import (
    BusinessListingCategory,
    BusinessListing,
    BusinessListingRequest,
    BusinessListingImage,
    BusinessListingFile,
    BusinessListingSocials,
    BusinessListingReview,
)


class BusinessListingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingCategory
        fields = '__all__'

class BusinessListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingImage
        fields = ['id', 'image']
       
class BusinessListingFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingFile
        fields = '__all__'
        
    def validate_file(self, value):
        max_size = 5 * 1024 * 1024  # 5MB in bytes

        if value.size > max_size:
            raise serializers.ValidationError("File size should not exceed 5MB.")
        
        return value

class BusinessListingSocialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingSocials
        fields = '__all__'


class BusinessListingSerializer(serializers.ModelSerializer):
    listing_images = BusinessListingImageSerializer(many=True, read_only=True)
   # listing_socials = BusinessListingSocialsSerializer(many=True, read_only=True)
    class Meta:
        model = BusinessListing
        fields = '__all__'


class BusinessListingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingRequest
        fields = '__all__'

class BusinessListingReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingReview
        fields = '__all__'
        