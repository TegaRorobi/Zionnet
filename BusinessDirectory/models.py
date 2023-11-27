from django.db import models
from authentication.models import CustomUser as User


class BusinessListingCategory(models.Model):
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to="business_listing_category_images")
    created_at = models.DateTimeField(auto_now_add=True)


class BusinessListing(models.Model):
    vendor_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(BusinessListingCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    country = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    physical_address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class BusinessListingRequest(models.Model):
    listing_category = models.ForeignKey(
        BusinessListingCategory, on_delete=models.CASCADE
    )
    id_type = models.CharField(
        max_length=20,
        choices=[
            ("type_1", "Type 1"),
            ("type_2", "Type 2"),
        ],
    )
    id_front = models.FileField(upload_to="business_listing_request_id_front")
    id_back = models.FileField(upload_to="business_listing_request_id_back")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class BusinessListingImage(models.Model):
    image = models.FileField(upload_to="business_listing_images")
    listing = models.ForeignKey(BusinessListing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class BusinessListingFile(models.Model):
    file = models.FileField(upload_to="business_listing_files")
    listing = models.ForeignKey(BusinessListing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class BusinessListingSocials(models.Model):
    social_urls = models.CharField(max_length=255)
    listing = models.ForeignKey(BusinessListing, on_delete=models.CASCADE)


class BusinessListingReview(models.Model):
    listing = models.ForeignKey(BusinessListing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
