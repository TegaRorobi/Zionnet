from django.db import models
from helpers.models import TrackingModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
User = get_user_model()



class BusinessListingCategory(TrackingModel, models.Model):
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to="business_listing_category_images")

    def __str__(self):
        return self.name


class BusinessListing(TrackingModel, models.Model):
    vendor_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings"
    )
    category = models.ForeignKey(
        BusinessListingCategory, on_delete=models.CASCADE, related_name="listings"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    country = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    physical_address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BusinessListingRating(TrackingModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listing_ratings')
    listing = models.ForeignKey(BusinessListing, on_delete=models.CASCADE, related_name='ratings')
    value = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])


class BusinessListingRequest(TrackingModel, models.Model):
    vendor_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing_request"
    )
    listing_category = models.ForeignKey(
        BusinessListingCategory,
        on_delete=models.CASCADE,
        related_name="listing_request",
    )
    id_type = models.CharField(
        max_length=20,
        choices=[
            ("type_1", "Type 1"),
            ("type_2", "Type 2"),
        ],
    )
    id_front = models.FileField(upload_to="business_listing_request_id_front", null=True, blank=True)
    id_back = models.FileField(upload_to="business_listing_request_id_back", null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Request by {self.vendor_id.first_name}"


class BusinessListingImage(TrackingModel, models.Model):
    image = models.FileField(upload_to="business_listing_images")
    listing = models.ForeignKey(
        BusinessListing, on_delete=models.CASCADE, related_name="listing_images"
    )

    def __str__(self):
        return f"Image for {self.listing.name}"


class BusinessListingFile(TrackingModel, models.Model):
    file = models.FileField(upload_to="business_listing_files")
    listing = models.ForeignKey(
        BusinessListing, on_delete=models.CASCADE, related_name="listing_files"
    )

    def __str__(self):
        return f"File for {self.listing.name}"


class BusinessListingSocials(TrackingModel, models.Model):
    social_urls = models.CharField(max_length=255)
    listing = models.ForeignKey(
        BusinessListing, on_delete=models.CASCADE, related_name="listing_socials"
    )

    def __str__(self):
        return f"Social for {self.listing.name}"


class BusinessListingReview(TrackingModel, models.Model):
    listing = models.ForeignKey(
        BusinessListing, on_delete=models.CASCADE, related_name="listing_reviews"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing_reviews"
    )
    comment = models.TextField()

    def __str__(self):
        return f"Review for {self.listing.name}"
