from django.urls import path
from .views import BusinessListingListCreateView, BusinessListingRequestCreateView, BusinessListingVendorRequestCreateView

urlpatterns = [
    path('listings/request/', BusinessListingRequestCreateView.as_view(), name='business_listing_request'),
    path('listings/vendor/request/', BusinessListingVendorRequestCreateView.as_view(), name='business_listing_vendor_request'),
    path('listings/', BusinessListingListCreateView.as_view(), name='business-listings'),

]
