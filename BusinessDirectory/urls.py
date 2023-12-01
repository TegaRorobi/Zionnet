from django.urls import path

from .views import *

urlpatterns = [
    path(
        "listings/", BusinessListingListCreateView.as_view(), name="business-listings"
    ),
    path(
        "listings/request/",
        BusinessListingRequestCreateView.as_view(),
        name="business_listing_request",
    ),
    path(
        "listings/vendor/request/",
        BusinessListingVendorRequestCreateView.as_view(),
        name="business_listing_vendor_request",
    ),
    path(
        "listing-categories/",
        BusinessListingCategoryListView.as_view(),
        name="business-categories",
    ),
    path(
        "listing-categories/popular/",
        PopularBusinessListingCategoryListView.as_view(),
        name="popular-category-list",
    ),
    path(
        "listings/loan/request/",
        BusinessLoanRequestView.as_view(),
        name="business_loan_request",
    ),
]
