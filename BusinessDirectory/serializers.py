from rest_framework import serializers
from .models import BusinessListing, BusinessListingRating
from django.db.models import Avg

class BusinessListingRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingRating
        fields = '__all__'

class BusinessListingSerializer(serializers.ModelSerializer):
    # You can include the rating information in the BusinessListingSerializer
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = BusinessListing
        fields = '__all__'

    def get_avg_rating(self, obj):
        # Calculate the average rating for the business listing
        avg_rating = BusinessListingRating.objects.filter(listing=obj).aggregate(Avg('value'))['value__avg']
        return avg_rating if avg_rating is not None else 0