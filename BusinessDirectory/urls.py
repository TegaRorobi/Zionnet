
from django.urls import path
from .views import *

app_name='BusinessDirectory'

urlpatterns = [
    path(
        "listings/", 
        BusinessListingListCreateView.as_view(), 
        name="business-listings"
    ),
    path(
        "listings/request/",
        BusinessListingRequestCreateView.as_view(),
        name="business-listing-request",
    ),
    path(
        "listings/vendor/request/",
        BusinessListingVendorRequestCreateView.as_view(),
        name="business-listing-vendor-request",
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
        name="business-loan-request",
    ),
    path(
        "listings/popular/",
        PopularBusinessListingView.as_view(),
        name="popular-business-listings",
    ),
    path('listings/top-rated/', 
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