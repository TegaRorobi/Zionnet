from django.contrib import admin
from django.forms import inlineformset_factory
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


class BusinessListingImageInline(admin.TabularInline):
    model = BusinessListingImage
    extra = 1


class BusinessListingFileInline(admin.TabularInline):
    model = BusinessListingFile
    extra = 1


class BusinessListingSocialsInline(admin.TabularInline):
    model = BusinessListingSocials
    extra = 1


class BusinessListingAdmin(admin.ModelAdmin):
    inlines = [
        BusinessListingImageInline,
        BusinessListingFileInline,
        BusinessListingSocialsInline,
    ]


admin.site.register(BusinessListing, BusinessListingAdmin)

admin.site.register(BusinessListingCategory)
admin.site.register(BusinessListingRequest)
admin.site.register(BusinessListingImage)
admin.site.register(BusinessListingFile)
admin.site.register(BusinessListingSocials)
admin.site.register(BusinessListingReview)
admin.site.register(BusinessLoan)
