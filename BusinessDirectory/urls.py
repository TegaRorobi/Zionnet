from django.urls import path
# # from .views import (
#     TopRatedListingsView, UserListingsView, ListingDetailView
# )

# urlpatterns = [
#     path('api/listings/top_rated/', TopRatedListingsView.as_view(), name='top-rated-listings'),
#     path('api/me/listings/', UserListingsView.as_view(), name='user-listings'),
#     path('api/listings/<int:pk>/', ListingDetailView.as_view(), name='business-listing')
# ]

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
    path(
        'api/listings/top_rated/', 
        BusinessListingRatingViewSet.as_view, 
        name='top-rated-listings'
    ),
    path(
        'api/me/listings/', 
        UserListingsView.as_view(), 
        name='user-listings'
    ),
    path(
        'api/listings/<int:pk>/', 
        ListingDetailView.as_view(), 
        name='business-listing'
    ),
]

