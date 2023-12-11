from django.db import models
from helpers.models import TimestampsModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from helpers.fields import ValidatedImageField

User = get_user_model()


class BusinessListingCategory(TimestampsModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="business_listing_category_images", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural="Business listing categories"


class BusinessListingVendor(TimestampsModel):

    ID_TYPE_CHOICES = [
        ('NIN', 'NIN'),
        ("Driver's License", "Driver's License"),
        ("Voter's Card", "Voter's Card")
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business_listing_vendor_profile')
    email = models.EmailField(_('vendor email address'))
    id_type = models.CharField(_('id type'), max_length=30, choices=ID_TYPE_CHOICES)
    id_front = models.FileField(_('id front'), upload_to='listings/vendors/id_files', null=True, blank=True)
    id_back = models.FileField(_('id back'), upload_to='listings/vendors/id_files', null=True, blank=True)
    request_info = models.CharField(_('additional request information'), max_length=400, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return 'Business Listing Vendor: ' + self.email.__str__()


class BusinessListingRequest(TimestampsModel):

    ID_TYPE_CHOICES = [
        ("type_1", "Type 1"),
        ("type_2", "Type 2")
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing_requests"
    )
    listing_category = models.ForeignKey(
        BusinessListingCategory, on_delete=models.CASCADE, related_name="listing_requests",
    )
    id_type = models.CharField(
        max_length=20, choices=ID_TYPE_CHOICES,
    )
    id_front = models.FileField(
        upload_to="business_listing_request_id_front", null=True, blank=True
    )
    id_back = models.FileField(
        upload_to="business_listing_request_id_back", null=True, blank=True
    )
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Business listing Request by {self.vendor.user.__str__()}"


class BusinessListing(TimestampsModel):

    vendor = models.ForeignKey(
        BusinessListingVendor, on_delete=models.CASCADE, related_name="listings"
    )
    listing_request = models.OneToOneField(
        BusinessListingRequest, related_name='listing', on_delete=models.PROTECT
    )
    category = models.ForeignKey(
        BusinessListingCategory, on_delete=models.CASCADE, related_name="listings"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = ValidatedImageField(upload_to='listings/cover_images', null=True, blank=True)
    country = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    physical_address = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.listing_request.is_approved is False:
            raise ValidationError('This listing cannot be saved, as it\'s request is not yet approved.')
        if not (
            hasattr(self.listing_request.user, 'business_listing_vendor_profile') and (
                self.listing_request.user.business_listing_vendor_profile != self.vendor
            )
        ):
            raise ValidationError('This listing\'s request was not created by the selected vendor.')
    
        return super().save()

    def __str__(self, *args, **kwargs):
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


class BusinessListingSocial(TimestampsModel):
    social_url = models.CharField(max_length=255)
    listing = models.ForeignKey(
        BusinessListing, on_delete=models.CASCADE, related_name="listing_socials"
    )

    def __str__(self):
        return f"Social for {self.listing.name}"
    
    class Meta:
        verbose_name_plural = "Business listing socials"


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
