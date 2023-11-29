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
from .models import (
    BusinessListingCategory,
    BusinessListing,
    BusinessListingRequest,
    BusinessListingImage,
    BusinessListingFile,
    BusinessListingSocials,
    BusinessListingReview,
    BusinessLoan,
)


class BusinessListingRequestSerializer(serializers.ModelSerializer):
    vendor_id = serializers.HiddenField(default=serializers.CurrentUserDefault())


class BusinessListingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingCategory
        fields = "__all__"


class BusinessListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingImage
        fields = ["id", "image"]


class BusinessListingFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingFile
        fields = "__all__"

    def validate_file(self, value):
        max_size = 5 * 1024 * 1024  # 5MB in bytes

        if value.size > max_size:
            raise serializers.ValidationError("File size should not exceed 5MB.")

        return value


class BusinessListingSocialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingSocials
        fields = "__all__"


class BusinessListingSerializer(serializers.ModelSerializer):
    listing_images = BusinessListingImageSerializer(many=True, read_only=True)

    # listing_socials = BusinessListingSocialsSerializer(many=True, read_only=True)
    class Meta:
        model = BusinessListing
        fields = "__all__"


class BusinessListingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingRequest
        fields = "__all__"


class BusinessListingSerializer(serializers.ModelSerializer):
    vendor_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BusinessListing
        fields = "__all__"


class BusinessListingReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListingReview
        fields = "__all__"


class YearlyFinancialDetailsSerializer(serializers.Serializer):
    year_2022 = serializers.DecimalField(max_digits=15, decimal_places=2)
    year_2023 = serializers.DecimalField(max_digits=15, decimal_places=2)
    last_12_months = serializers.DecimalField(max_digits=15, decimal_places=2)
    projected_2023 = serializers.DecimalField(max_digits=15, decimal_places=2)
    projected_2024 = serializers.DecimalField(max_digits=15, decimal_places=2)


class FinancialMetricsSerializer(serializers.Serializer):
    revenue = YearlyFinancialDetailsSerializer()
    EBITDA = YearlyFinancialDetailsSerializer()
    gross_profit = YearlyFinancialDetailsSerializer()
    CAPEX = YearlyFinancialDetailsSerializer()


class BusinessLoanRequestSerializer(serializers.ModelSerializer):
    business_financial_details = FinancialMetricsSerializer()

    class Meta:
        model = BusinessLoan
        fields = "__all__"

    def validate_business_financial_details(self, value):
        required_metrics = {"revenue", "EBITDA", "gross_profit", "CAPEX"}
        expected_keys = {
            "year_2022",
            "year_2023",
            "last_12_months",
            "projected_2023",
            "projected_2024",
        }

        for metric, data in value.items():
            if set(data.keys()) != expected_keys:
                raise serializers.ValidationError(f"Invalid structure for {metric}.")

        if set(value.keys()) != required_metrics:
            raise serializers.ValidationError(
                f"Invalid financial details. Please provide data for: {', '.join(required_metrics)}."
            )

        return value
