from django.urls import path
from .views import BusinessListingRequestCreateView, BusinessListingVendorRequestCreateView

urlpatterns = [
    path('request/', BusinessListingRequestCreateView.as_view(), name='business_listing_request'),
    path('vendor/request/', BusinessListingVendorRequestCreateView.as_view(), name='business_listing_vendor_request'),
]
