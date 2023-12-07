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
        "categories/",
        BusinessListingCategoryListView.as_view(),
        name="business-categories",
    ),
    path(
        "categories/popular/",
        PopularBusinessListingCategoryListView.as_view(),
        name="popular-category-list",
    ),
    path(
        "listings/loan/request/",
        BusinessLoanRequestView.as_view(),
        name="business_loan_request",
    ),
    path(
        "listings/popular/",
        PopularBusinessListingView.as_view(),
        name="popular-business-listings",
    ),
    path('listings/top_rated/', 
        TopRatedListingsAPIView.as_view(),
        name='top-rated-listings'
    ),
    path('me/listings/', 
         UserListingsView.as_view(), 
         name='user-listings'
    ),
    path('listings/<int:pk>/', 
         ListingDetailView.as_view(), 
         name='business-listing'
    )
]