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


class BusinessListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListing
        fields = '__all__'


class BusinessListingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingRequest
        fields = '__all__'


class BusinessListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingImage
        fields = '__all__'


class BusinessListingFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingFile
        fields = '__all__'


class BusinessListingSocialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingSocials
        fields = '__all__'


class BusinessListingReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingReview
        fields = '__all__'
        