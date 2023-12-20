from django.contrib import admin
from .models import *


class BusinessListingImageInline(admin.TabularInline):
    model = BusinessListingImage
    extra = 1


class BusinessListingFileInline(admin.TabularInline):
    model = BusinessListingFile
    extra = 1


class BusinessListingSocialInline(admin.TabularInline):
    model = BusinessListingSocial
    extra = 1


class BusinessListingAdmin(admin.ModelAdmin):
    inlines = [
        BusinessListingImageInline,
        BusinessListingFileInline,
        BusinessListingSocialInline,
    ]


admin.site.register(BusinessListing, BusinessListingAdmin)
admin.site.register(BusinessListingCategory)
admin.site.register(BusinessListingVendor)
admin.site.register(BusinessListingRequest)
admin.site.register(BusinessListingImage)
admin.site.register(BusinessListingFile)
admin.site.register(BusinessListingSocial)
admin.site.register(BusinessListingReview)
admin.site.register(BusinessListingRating)
admin.site.register(BusinessLoan)
