from django.db import models
from helpers.models import TimestampsModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class BusinessListingCategory(TimestampsModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="business_listing_category_images")

    def __str__(self):
        return self.name


class BusinessListing(TimestampsModel):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
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


class BusinessListingRating(TimestampsModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing_ratings"
    )
    listing = models.ForeignKey(
        BusinessListing, on_delete=models.CASCADE, related_name="ratings"
    )
    value = models.PositiveSmallIntegerField(
        default=5, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )


class BusinessListingRequest(TimestampsModel):
    vendor = models.ForeignKey(
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
    id_front = models.FileField(
        upload_to="business_listing_request_id_front", null=True, blank=True
    )
    id_back = models.FileField(
        upload_to="business_listing_request_id_back", null=True, blank=True
    )
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Request by {self.vendor.first_name}"


class BusinessListingImage(TimestampsModel):
    image = models.ImageField(upload_to="business_listing_images")
    listing = models.ForeignKey(
        BusinessListing, on_delete=models.CASCADE, related_name="listing_images"
    )

    def __str__(self):
        return f"Image for {self.listing.name}"


class BusinessListingFile(TimestampsModel):
    file = models.FileField(upload_to="business_listing_files")
    listing = models.ForeignKey(
        BusinessListing, on_delete=models.CASCADE, related_name="listing_files"
    )

    def __str__(self):
        return f"File for {self.listing.name}"


class BusinessListingSocials(TimestampsModel):
    social_urls = models.CharField(max_length=255)
    listing = models.ForeignKey(
        BusinessListing, on_delete=models.CASCADE, related_name="listing_socials"
    )

    def __str__(self):
        return f"Social for {self.listing.name}"


class BusinessListingReview(TimestampsModel):
    listing = models.ForeignKey(
        BusinessListing, on_delete=models.CASCADE, related_name="listing_reviews"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing_reviews"
    )
    comment = models.TextField()

    def __str__(self):
        return f"Review for {self.listing.name}"


class BusinessLoan(TimestampsModel):
    LOAN_TYPE_CHOICES = [
        ("loan_type_1", "Loan Type 1"),
        ("loan_type_2", "Loan Type 2"),
    ]

    LOAN_INTERVAL_CHOICES = [
        ("loan_interval_1", "Loan Interval 1"),
        ("loan_interval_2", "Loan Interval 2"),
    ]

    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPE_CHOICES)
    loan_interval = models.CharField(max_length=20, choices=LOAN_INTERVAL_CHOICES)
    business_financial_details = models.JSONField()
    reason = models.TextField()
    amount = models.IntegerField()

    def __str__(self):
        return f"BusinessLoan to {self.vendor.first_name}"
